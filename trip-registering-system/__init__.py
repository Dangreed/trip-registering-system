from cassandra.cluster import Cluster
import uuid
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
    # session.execute("DROP TABLE IF EXISTS clients")
    # session.execute("DROP TABLE IF EXISTS cars")
    # session.execute("DROP TABLE IF EXISTS client_trips")
    # session.execute("DROP TABLE IF EXISTS car_trips")
    # session.execute("DROP TABLE IF EXISTS points")
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
            distance FLOAT,
            PRIMARY KEY ((client_id, trip_id, finished)))
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS car_trips (
            car TEXT,
            trip_id TEXT,
            finished BOOLEAN,
            client_id TEXT,
            duration BIGINT,
            distance FLOAT,
            PRIMARY KEY ((car, trip_id, finished)))
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS points (
            trip_id TEXT,
            timestamp TIMESTAMP,
            lat DOUBLE,
            long DOUBLE,
            dist_from_prev FLOAT,
            PRIMARY KEY ((trip_id), timestamp))
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
            client = client[0]
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
        pass

    #Delete client and all related info (cars, trips, etc.)
    @app.route('/clients/<clientId>', methods=['DELETE'])
    def delete_client(clientId):
        pass
    
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
        pass   

    #Mark clients trip as finished (in both trip tables)
    @app.route('/clients/<clientId>/cars/<carId>/trips/<tripId>', methods=['POST'])
    def finish_trip(clientId, carId, tripId):
        pass

    #Get clients trip (from CLIENT_TRIPS table), finished = True
    @app.route('/clients/<clientId>/trips/<tripId>', methods=['GET'])
    def get_trip(clientId, carId, tripId):
        pass

    #Delete clients trip (in both trip tables), finished = True
    @app.route('/clients/<clientId>/cars/<carId>/trips/<tripId>', methods=['DELETE'])
    def delete_trip(clientId, carId, tripId):
        pass

    #Get all clients trips (from CLIENT_TRIPS table), finished = True
    @app.route('/clients/<clientId>/trips', methods=['GET'])
    def get_clients_trips(clientId):
        pass

    #Get summarized trips info (distance, duration), 
    #filtered by car (from CAR_TRIPS table), finished = True
    @app.route('/cars/<carId>/trips', methods=['GET'])
    def get_car_trips(carId):
        pass

    #Register a trips point in realtime
    @app.route('/points/<tripId>', methods=['PUT'])
    def add_point(tripId):
        pass

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