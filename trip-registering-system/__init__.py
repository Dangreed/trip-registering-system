from cassandra.cluster import Cluster
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
            client_id UUID PRIMARY KEY,
            name TEXT,
            surname TEXT,
            email TEXT,
            birth DATE)
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            client_id UUID,
            VIN TEXT,
            model TEXT,
            manufacturer TEXT,
            plate TEXT,
            year DATE,
            PRIMARY KEY ((client_id), VIN))       
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS client_trips (
            client_id UUID,
            trip_id UUID,
            finished BOOLEAN,
            car TEXT,
            duration BIGINT,
            distance FLOAT,
            PRIMARY KEY ((client_id, trip_id, finished)))
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS car_trips (
            car TEXT,
            trip_id UUID,
            finished BOOLEAN,
            client_id UUID,
            duration BIGINT,
            distance FLOAT,
            PRIMARY KEY ((car, trip_id, finished)))
    ''')

    session.execute('''
        CREATE TABLE IF NOT EXISTS points (
            trip_id UUID,
            timestamp TIMESTAMP,
            lat DOUBLE,
            long DOUBLE,
            dist_from_prev FLOAT,
            PRIMARY KEY ((trip_id), timestamp))
    ''')

    #Register a client
    @app.route('/clients', methods=['PUT'])
    def register_cient():
        pass

    #Register clients car
    @app.route('/clients/<clientId>/cars', methods=['PUT'])
    def register_car(clientId):
        pass
    
    #Get client info
    @app.route('/clients/<clietnId>', methods=['GET'])
    def get_client(clientId):
        pass
        
    #Get clients car info
    @app.route('/clients/<clientId>/cars/<carId>', methods=['GET'])
    def get_car(clientId, carId):
        pass
    
    #Get all clients cars
    @app.route('/clients/<clientId>/cars', methods=['GET'])
    def get_clients_cars(clientId):
        pass

    #Delete client and all related info (cars, trips, etc.)
    @app.route('/clients/<clientId>', methods=['DEL'])
    def delete_client(clientId):
        pass
    
    #Delete clients car
    @app.route('/clients/<clientId>/cars/<carId>', methods=['DEL'])
    def delete_car(clientId, carId):
        pass
    
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
    @app.route('/clients/<clientId>/cars/<carId>/trips/<tripId>', methods=['DEL'])
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