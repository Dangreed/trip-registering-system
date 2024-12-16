from cassandra.cluster import Cluster
from datetime import timedelta
import uuid
import math
import humanize
from flask import (Flask, request, jsonify)

def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect()

    session.execute('''
        CREATE KEYSPACE IF NOT EXISTS nav
        WITH REPLICATION = {
            'class' : 'SimpleStrategy',
            'replication_factor': 1}
    ''')
    session.set_keyspace('nav')
    
    session.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id TEXT PRIMARY KEY,
            name TEXT,
            surname TEXT,
            email TEXT,
            birth_date DATE)
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            client_id TEXT,
            vin TEXT,
            model TEXT,
            manufacturer TEXT,
            plate TEXT,
            year DATE,
            PRIMARY KEY ((client_id), vin))       
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS client_trips (
            client_id TEXT,
            trip_id TEXT,
            finished BOOLEAN,
            car TEXT,
            duration BIGINT,
            distance DOUBLE,
            PRIMARY KEY ((client_id, finished), trip_id))
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS car_trips (
            car TEXT,
            trip_id TEXT,
            finished BOOLEAN,
            client_id TEXT,
            duration BIGINT,
            distance DOUBLE,
            PRIMARY KEY ((car, finished), trip_id))
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS points (
            trip_id TEXT,
            timestamp TIMESTAMP,
            lat DOUBLE,
            long DOUBLE,
            dist_from_prev DOUBLE,
            PRIMARY KEY ((trip_id), timestamp)
        ) WITH CLUSTERING ORDER BY (timestamp DESC);
    ''')

    #Register a client
    @app.route('/clients', methods=['PUT'])
    def register_cient():
        req_body = request.json
        name = req_body.get('name')
        surname = req_body.get('surname')
        email = req_body.get('email')
        birth_date = req_body.get('birth_date')

        if not name or not surname or not email or not birth_date:
            return {"message": 'Some values are missing'}, 400 
        
        client_id = 'Cl-' + uuid.uuid4().hex
        session.execute(f"INSERT INTO clients (client_id, name, surname, email, birth_date) VALUES ('{client_id}', '{name}', '{surname}', '{email}', '{birth_date}') IF NOT EXISTS")
        return {"id": client_id}, 201

    #Register clients car
    @app.route('/clients/<clientId>/cars', methods=['PUT'])
    def register_car(clientId):
        req_body = request.json
        vin = req_body.get('vin')
        model = req_body.get('model')
        manufacturer = req_body.get('manufacturer')
        plate = req_body.get('plate')
        year = req_body.get('year')
        
        if not vin or not model or not manufacturer or not plate or not year:
            return {"message": 'Some values are missing'}, 400
    
        client = session.execute(f"SELECT * FROM clients WHERE client_id='{clientId}'")
        if client:
            session.execute(f"INSERT INTO cars (client_id, vin, model, manufacturer, plate, year) VALUES ('{clientId}', '{vin}', '{model}', '{manufacturer}', '{plate}', '{year}') IF NOT EXISTS")
            return {"id": vin}, 201 

        return {"message": "Client not found"}, 404
    
    #Get client info
    @app.route('/clients/<clientId>', methods=['GET'])
    def get_client(clientId):
        client = session.execute(f"SELECT * FROM clients WHERE client_id='{clientId}'")
        if client:
            client = client[0]
            client_info = {
                "client_id": client.client_id,
                "name": client.name,
                "surname": client.surname,
                "email": client.email,
                "birth_date": str(client.birth_date)
            }
            return client_info, 201
        return {"message": 'Client not found'}, 404
        
    #Get clients car info
    @app.route('/clients/<clientId>/cars/<carId>', methods=['GET'])
    def get_car(clientId, carId):
        client = session.execute(f"SELECT * FROM clients WHERE client_id='{clientId}'")
        if client:
            car = session.execute(f"SELECT * FROM cars WHERE client_id='{clientId}' AND vin='{carId}'")
            if car:
                car = car[0]
                car_info = {
                    "client_id": car.client_id,
                    "vin": car.vin,
                    "model": car.model,
                    "manufacturer": car.manufacturer,
                    "plate": car.plate,
                    "year": str(car.year)
                }
                return car_info, 201
            return {"message": 'Car not found'}, 404 
        return {"message": 'Client not found'}, 404 
    
    #Get all clients cars
    @app.route('/clients/<clientId>/cars', methods=['GET'])
    def get_clients_cars(clientId):
        client = session.execute(f"SELECT * FROM clients WHERE client_id='{clientId}'")
        if client:
            car_array = []
            cars = session.execute(f"SELECT * FROM cars WHERE client_id='{clientId}'")
            if cars:
                for car in cars:
                    car_info = {
                        "client_id": car.client_id,
                        "vin": car.vin,
                        "model": car.model,
                        "manufacturer": car.manufacturer,
                        "plate": car.plate,
                        "year": str(car.year)
                    }
                    car_array.append(car_info)
                return car_array, 201
        return {"message": 'Client not found'}, 404 

    #Delete client and all related info (cars, trips, etc.)
    @app.route('/clients/<clientId>', methods=['DELETE'])
    def delete_client(clientId):
        client = session.execute(f"SELECT * FROM clients WHERE client_id='{clientId}'")
        if client:
            cars = session.execute(f"SELECT vin FROM cars WHERE client_id='{clientId}'")
            trips = session.execute(f"SELECT trip_id FROM client_trips WHERE client_id='{clientId}' AND finished=true")

            for car in cars:
                for trip in trips:
                    session.execute(f"DELETE FROM car_trips WHERE car='{car.vin}' AND trip_id='{trip.trip_id}' AND finished=true IF EXISTS")

            for trip in trips:
                session.execute(f"DELETE FROM client_trips WHERE client_id='{clientId}' AND trip_id='{trip.trip_id}' AND finished=true IF EXISTS")
            
            for car in cars:
                session.execute(f"DELETE FROM cars WHERE client_id='{clientId}' AND vin='{car.vin}' IF EXISTS")

            session.execute(f"DELETE FROM clients WHERE client_id='{clientId}'")
            return {"message": "Client deleted"}, 204
        
        return {"message": 'Client not found'}, 404 
    
    #Delete clients car
    @app.route('/clients/<clientId>/cars/<carId>', methods=['DELETE'])
    def delete_car(clientId, carId):
        client = session.execute(f"SELECT * FROM clients WHERE client_id='{clientId}'")
        if client:
            session.execute(f"DELETE FROM cars WHERE client_id='{clientId}' AND vin='{carId}' IF EXISTS")
            return {"message": "Car deleted"}, 204
        return {"message": 'Client not found'}, 404
    
    #Register clients trip (in both trip tables), finished = False
    @app.route('/clients/<clientId>/cars/<carId>/trips', methods=['PUT'])
    def register_trip(clientId, carId):
        tripId = 'Tr-' + uuid.uuid4().hex
        session.execute(f"INSERT INTO client_trips (client_id, trip_id, finished, car, duration, distance) VALUES ('{clientId}', '{tripId}', false, '{carId}', 0, 0) IF NOT EXISTS")
        session.execute(f"INSERT INTO car_trips (car, trip_id, finished, client_id, duration, distance) VALUES ('{carId}', '{tripId}', false, '{clientId}', 0, 0) IF NOT EXISTS")
        return {"id": tripId}, 201 

    #Mark clients trip as finished (in both trip tables)
    @app.route('/clients/<clientId>/cars/<carId>/trips/<tripId>', methods=['POST'])
    def finish_trip(clientId, carId, tripId):
        result = session.execute('''
            SELECT 
                SUM(dist_from_prev) AS distance,
                MAX(timestamp) AS last,
                MIN(timestamp) AS first
            FROM points
            WHERE trip_id = %s
        ''', (tripId,))

        if result:
            row = result[0]
            duration = int((row.first - row.last).total_seconds())
            session.execute('''
                DELETE FROM client_trips
                WHERE client_id = %s AND finished = %s AND trip_id = %s
                IF EXISTS
            ''', (clientId, False, tripId))

            session.execute('''
                DELETE FROM car_trips
                WHERE car = %s AND finished = %s AND trip_id = %s
                IF EXISTS
            ''', (carId, False, tripId))

            session.execute('''
                INSERT INTO client_trips (client_id, trip_id, finished, car, duration, distance)
                VALUES (%s, %s, %s, %s, %s, %s)
                IF NOT EXISTS
            ''', (clientId, tripId, True, carId, duration, row.distance))

            session.execute('''
                INSERT INTO car_trips (car, trip_id, finished, client_id, duration, distance)
                VALUES (%s, %s, %s, %s, %s, %s)
                IF NOT EXISTS
            ''', (carId, tripId, True, clientId, duration, row.distance))
            return  {"message": "Trip marked as finished"}, 200
        return {"message": "No points found for the specified trip"}, 404

    #Get clients trip (from CLIENT_TRIPS table), finished = True
    @app.route('/clients/<clientId>/trips/<tripId>', methods=['GET'])
    def get_trip(clientId, tripId):
        trip = session.execute(f"SELECT * FROM client_trips WHERE client_id='{clientId}' AND finished=true")
        if trip:
            trip = trip[0]
            trip_info = {
                "client_id": trip.client_id,
                "trip_id": trip.trip_id,
                "car": trip.car,
                "duration": trip.duration,
                "distance": trip.distance
            }
            return trip_info, 200
        return {"message": 'Trip not found'}, 404

    #Delete clients trip (in both trip tables), finished = True/False
    @app.route('/clients/<clientId>/cars/<carId>/trips/<tripId>', methods=['DELETE'])
    def delete_trip(clientId, carId, tripId):
        results = []
        results.append(session.execute(f"DELETE FROM client_trips WHERE client_id='{clientId}' AND finished=true AND trip_id='{tripId}' IF EXISTS"))
        results.append(session.execute(f"DELETE FROM client_trips WHERE client_id='{clientId}' AND finished=false AND trip_id='{tripId}' IF EXISTS"))
        results.append(session.execute(f"DELETE FROM car_trips WHERE car='{carId}' AND finished=true AND trip_id='{tripId}' IF EXISTS"))
        results.append(session.execute(f"DELETE FROM car_trips WHERE car='{carId}' AND finished=false AND trip_id='{tripId}' IF EXISTS"))

        delete_count = sum(1 for result in results if result.was_applied)

        if delete_count >= 2:
            return {"message": "Trip deleted"}, 204
        else:
            return {"message": "Trip not found"}, 404

    #Get all clients trips (from CLIENT_TRIPS table), finished = True
    @app.route('/clients/<clientId>/trips', methods=['GET'])
    def get_clients_trips(clientId):
        client_trips = session.execute(f"SELECT * FROM client_trips WHERE client_id='{clientId}' AND finished=true")
        if client_trips:
            trip_list = []
            for trip in client_trips:
                trip_info = {
                    "client_id": trip.client_id,
                    "trip_id": trip.trip_id,
                    "car": trip.car,
                    "duration": trip.duration,
                    "distance": trip.distance
                }
                trip_list.append(trip_info)
            return trip_list, 200
        return {"message": 'No trips associated with the client found'}, 404 

    #Get summarized trips info (distance, duration), 
    #filtered by car (from CAR_TRIPS table), finished = True
    @app.route('/cars/<carId>/trips', methods=['GET'])
    def get_car_trips(carId):
        result = session.execute('''
            SELECT COUNT(*) AS trip_count, SUM(duration) AS total_duration, SUM(distance) AS total_distance
            FROM car_trips 
            WHERE car = %s AND finished = true
        ''', (carId,))
        
        if result:
            row = result[0]
            if row.trip_count > 0:
                return {
                    "car": carId,
                    "duration": row.total_duration,
                    # humanize.naturaldelta(timedelta(seconds=row.total_duration)),
                    "distance": row.total_distance
                }, 200
            else:
                return {"message": "No trips found for the specified car"}, 404
        return {"message": "Error processing request"}, 500

    #Register a trips point in realtime
    @app.route('/points/<tripId>', methods=['PUT'])
    def add_point(tripId):
        req_body = request.json
        timestamp = req_body.get('timestamp')
        lat = req_body.get('lat')
        long = req_body.get('long')

        if not timestamp or not lat or not long:
            return {"message": 'Some values are missing'}, 400 

        last = session.execute(f"SELECT * FROM points WHERE trip_id='{tripId}' LIMIT 1")
        if last:
            last = last[0]
            dist_from_prev = math.sqrt((lat - last.lat)**2 + (long - last.long)**2)
        else:
            dist_from_prev = 0

        session.execute(f"INSERT INTO points (trip_id, timestamp, lat, long, dist_from_prev) VALUES ('{tripId}', '{timestamp}', {lat}, {long}, {dist_from_prev}) IF NOT EXISTS")
        return {"timestamp": timestamp}, 201

    #Delete all data
    @app.route('/cleanup', methods=['POST'])
    def cleanup():
        session.execute("TRUNCATE TABLE clients")
        session.execute("TRUNCATE TABLE cars")
        session.execute("TRUNCATE TABLE client_trips")
        session.execute("TRUNCATE TABLE car_trips")
        session.execute("TRUNCATE TABLE points")
        return "", 204

    return app