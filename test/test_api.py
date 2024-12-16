import requests
import pytest
from datetime import datetime, timedelta
import time
import random
import math
import humanize

HOST = "127.0.0.1"
PORT = 8080

def test_registering_client():
    cleanup()
    client_id = register_client("John", "Johnson", "johnjo@gmail.com", "2000-03-17").get('id')

    client = get_client(client_id)
    assert client["client_id"] == client_id
    assert client["name"] == 'John'
    assert client["surname"] == 'Johnson'
    assert client["email"] == 'johnjo@gmail.com'
    assert client["birth_date"] == '2000-03-17'

    delete_client(client_id)
    response = get_client_raw(client_id)
    assert response.status_code == 404

def test_registering_car():
    client_id = register_client("John", "Johnson", "johnjo@gmail.com", "2000-03-17").get('id')
    car_id = register_car(client_id, "1HGEM21292L047875", "Civic", "Honda", "ABC123", "2002-01-01").get('id')

    car = get_car(client_id, car_id)
    assert car["client_id"] == client_id
    assert car["vin"] == car_id
    assert car["model"] == 'Civic'
    assert car["manufacturer"] == 'Honda'
    assert car["plate"] == 'ABC123'
    assert car["year"] == '2002-01-01'

    delete_client(client_id)
    response = get_car_raw(client_id, car_id)
    assert response.status_code == 404

def test_getting_clients_cars():
    client_id = register_client("John", "Johnson", "johnjo@gmail.com", "2000-03-17").get('id')
    car_id_honda = register_car(client_id, "1HGEM21292L047875", "Civic", "Honda", "ABC123", "2002-01-01").get('id')
    car_id_subaru = register_car(client_id, "3JF1GH6B60BG810286", "Impreza", "Subaru", "DEF456", "2011-01-01").get('id')
    car_id_kia = register_car(client_id, "5XYKT3A17BG157871", "Sorento", "Kia", "HIJ821", "2011-01-01").get('id')

    cars = get_cars(client_id)
    assert cars[0]["client_id"] == client_id
    assert cars[0]["vin"] == car_id_honda
    assert cars[0]["model"] == 'Civic'
    assert cars[0]["manufacturer"] == 'Honda'
    assert cars[0]["plate"] == 'ABC123'
    assert cars[0]["year"] == '2002-01-01'

    assert cars[1]["client_id"] == client_id
    assert cars[1]["vin"] == car_id_subaru
    assert cars[1]["model"] == 'Impreza'
    assert cars[1]["manufacturer"] == 'Subaru'
    assert cars[1]["plate"] == 'DEF456'
    assert cars[1]["year"] == '2011-01-01'

    assert cars[2]["client_id"] == client_id
    assert cars[2]["vin"] == car_id_kia
    assert cars[2]["model"] == 'Sorento'
    assert cars[2]["manufacturer"] == 'Kia'
    assert cars[2]["plate"] == 'HIJ821'
    assert cars[2]["year"] == '2011-01-01'

    delete_client(client_id)
    response_honda = get_car_raw(client_id, car_id_honda)
    response_subaru = get_car_raw(client_id, car_id_subaru)
    response_kia = get_car_raw(client_id, car_id_kia)
    assert response_honda.status_code == 404
    assert response_subaru.status_code == 404
    assert response_kia.status_code == 404

def test_finish_trip ():
    cleanup()
    john = register_client("John", "Johnson", "johnjo@gmail.com", "2000-03-17").get('id')
    honda = register_car(john, "1HGEM21292L047875", "Civic", "Honda", "ABC123", "2002-01-01").get('id')
    subaru = register_car(john, "3JF1GH6B60BG810286", "Impreza", "Subaru", "DEF456", "2011-01-01").get('id')

    john_honda = register_trip(john, honda).get('id')
    duration, distance = generate_points (john_honda)
    finish_trip(john, honda, john_honda)

    trip = get_trip(john, john_honda)
    assert trip["client_id"] == john
    assert trip["trip_id"] == john_honda
    assert trip["car"] == honda
    assert trip["duration"] == int(duration.total_seconds())
    assert int(trip["distance"]) == int(distance)

    _john_honda = register_trip(john, honda).get('id')

    delete_trip(john, honda, john_honda)
    delete_trip(john, honda, _john_honda)

def test_filter ():
    cleanup() # this one will be removed eventually
    john = register_client("John", "Johnson", "johnjo@gmail.com", "2000-03-17").get('id')
    honda = register_car(john, "1HGEM21292L047875", "Civic", "Honda", "ABC123", "2002-01-01").get('id')
    subaru = register_car(john, "3JF1GH6B60BG810286", "Impreza", "Subaru", "DEF456", "2011-01-01").get('id')

    # alisa = register_client("Alisa", "Cater", "alica@gmail.com", "2003-03-17").get('id')
    # kia = register_car(alisa, "5XYKT3A17BG157871", "Sorento", "Kia", "HIJ821", "2011-01-01").get('id')

    john_subaru = register_trip(john, subaru).get('id') # this one won't be finished
    
    john_honda = register_trip(john, honda).get('id')
    duration, distance = generate_points (john_honda)
    finish_trip(john, honda, john_honda)

    _john_honda = register_trip(john, honda).get('id')
    _duration, _distance = generate_points (_john_honda)
    finish_trip(john, honda, _john_honda)

    trips = get_clients_trips(john)
    if (john_honda < _john_honda):
        first = 0
        second = 1
    else:
        first = 1
        second = 0
    assert     trips[first]["client_id"] == john
    assert     trips[first]["trip_id"] == john_honda
    assert     trips[first]["car"] == honda
    assert     trips[first]["duration"] == int(duration.total_seconds())
    assert int(trips[first]["distance"]) == int(distance)

    assert     trips[second]["client_id"] == john
    assert     trips[second]["trip_id"] == _john_honda
    assert     trips[second]["car"] == honda
    assert     trips[second]["duration"] == int(_duration.total_seconds())
    assert int(trips[second]["distance"]) == int(_distance)

    honda_trips = get_car_trips(honda)
    assert     honda_trips["car"] == honda
    assert     honda_trips["duration"] == int((duration + _duration).total_seconds())
    # humanize.naturaldelta(timedelta(seconds=int((duration + _duration).timestamp())))
    assert int(honda_trips["distance"]) == int(distance + _distance)

def generate_points (trip_id):
    random.seed(int(datetime.now().timestamp()))
    amount = random.randint (2, 10)
    lat = random.uniform (-90, 90)
    long = random.uniform (-180, 180)

    timestamps = []
    last_lat  = 0
    last_long = 0
    distance = 0
    for i in range (amount):
        # timestamp = int(datetime.now().timestamp())
        timestamp = datetime.now()
        timestamps.append (timestamp)

        add_point(trip_id, timestamp.isoformat(), lat, long)
        if i > 0:
            distance += math.sqrt((lat - last_lat)**2 + (long - last_long)**2)
        last_lat = lat
        last_long = long

        lat += random.uniform (-5, 5)
        long += random.uniform (-10, 10)
        time.sleep(5)

    first = timestamps[0]
    last = timestamps[-1]
    duration = last - first

    return duration, distance

def register_client(name, surname, email, birth_date):
    response = requests.put(f'http://{HOST}:{PORT}/clients', json={"name": name, "surname": surname, "email": email, "birth_date": birth_date})
    assert response.status_code == 201
    return response.json()

def get_client_raw(client_id):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{client_id}')
    return response

def get_client(client_id):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{client_id}')
    assert response.status_code == 201
    return response.json()

def delete_client(client_id):
    response = requests.delete(f'http://{HOST}:{PORT}/clients/{client_id}')
    assert response.status_code == 204
    return response

def register_car(client_id, vin, model, manufacturer, plate, year):
    response = requests.put(f'http://{HOST}:{PORT}/clients/{client_id}/cars', json={"vin": vin, "model": model, "manufacturer": manufacturer, "plate": plate, "year": year})
    assert response.status_code == 201
    return response.json()

def get_car_raw(client_id, car_id):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{client_id}/cars/{car_id}')
    return response

def get_car(client_id, car_id):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{client_id}/cars/{car_id}')
    assert response.status_code == 201
    return response.json()

def get_cars(client_id):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{client_id}/cars')
    assert response.status_code == 201
    return response.json()

def delete_car(client_id, car_id):
    response = requests.delete(f'http://{HOST}:{PORT}/clients/{client_id}/cars/{car_id}')
    assert response.status_code == 204
    return response

def register_trip(clientId, carId):
    response = requests.put(f'http://{HOST}:{PORT}/clients/{clientId}/cars/{carId}/trips')
    assert response.status_code == 201
    return response.json()

def finish_trip(clientId, carId, tripId):
    response = requests.post(f'http://{HOST}:{PORT}/clients/{clientId}/cars/{carId}/trips/{tripId}')
    assert response.status_code == 200
    return response.json()

def get_trip(clientId, tripId):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{clientId}/trips/{tripId}')
    assert response.status_code == 200
    return response.json()

def delete_trip(clientId, carId, tripId):
    response = requests.delete(f'http://{HOST}:{PORT}/clients/{clientId}/cars/{carId}/trips/{tripId}')
    assert response.status_code == 204
    return response

def get_clients_trips(clientId):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{clientId}/trips')
    assert response.status_code == 200
    return response.json()

def get_car_trips(carId):
    response = requests.get(f'http://{HOST}:{PORT}/cars/{carId}/trips')
    assert response.status_code == 200
    return response.json()

def add_point(tripId, timestamp, lat, long):
    response = requests.put(f'http://{HOST}:{PORT}/points/{tripId}', json={"timestamp": timestamp, "lat": lat, "long": long})
    assert response.status_code == 201
    return response.json()

def cleanup():
    response = requests.post(f'http://{HOST}:{PORT}/cleanup')
    assert response.status_code == 204