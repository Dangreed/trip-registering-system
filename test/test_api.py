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

def cleanup():
    response = requests.post(f'http://{HOST}:{PORT}/cleanup')
    assert response.status_code == 204