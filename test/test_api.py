import requests
import pytest

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

    delete_car(client_id, car_id) 

def register_client(name, surname, email, birth_date):
    response = requests.put(f'http://{HOST}:{PORT}/clients', json={"name": name, "surname": surname, "email": email, "birth_date": birth_date})
    assert response.status_code == 201
    return response.json()

def get_client(client_id):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{client_id}')
    assert response.status_code == 201
    return response.json()

def register_car(client_id, vin, model, manufacturer, plate, year):
    response = requests.put(f'http://{HOST}:{PORT}/clients/{client_id}/cars', json={"vin": vin, "model": model, "manufacturer": manufacturer, "plate": plate, "year": year})
    assert response.status_code == 201
    return response.json()

def get_car(client_id, car_id):
    response = requests.get(f'http://{HOST}:{PORT}/clients/{client_id}/cars/{car_id}')
    assert response.status_code == 201
    return response.json()

def delete_car(client_id, car_id):
    response = requests.delete(f'http://{HOST}:{PORT}/clients/{client_id}/cars/{car_id}')
    assert response.status_code == 204
    return response

def cleanup():
    response = requests.post(f'http://{HOST}:{PORT}/cleanup')
    assert response.status_code == 204