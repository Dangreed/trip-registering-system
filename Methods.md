## Methods
```
- register_client, '/clients' [PUT],
    201: {"id": string}
    400: Invalid input, missing name, surname, email or birth date.

- get_client, '/clients/<clientId>' [GET],
    201: {
        "client_id": string,
        "name": string,
        "surname": string,
        "email": string,
        "birth_date": string
    }
    404: Client not found

- delete_client, '/clients/<clientId>', [DELETE],
    204: Client deleted 
    404: Client not found

- register_car, '/clients/<clientId>/cars' [PUT],
    201: {"id": string}
    400: Invalid input, missing vin, model, manufacturer, plate or year

- get_car, '/clients/<clientId>/cars/<carId>' [GET],
    201: {
        "client_id": string,
        "vin":  string,
        "model": string,
        "manufacturer": string,
        "plate": string,
        "year": string
    }
    404: Client not found. Car not found

- get_clients_cars, '/clients/<clientId>/cars' [GET],
    201: [{
        "client_id": string,
        "vin":  string,
        "model": string,
        "manufacturer": string,
        "plate": string,
        "year": string
    }]
    404: Client not found

- delete_car, '/clients/<clientId>/cars' [DELETE],
    204: Car deleted
    404: Client not found

- register_trip, '/clients/<clientId>/cars/<carId>/trips' [PUT],
    201: {"id": string}
    404: Client not found. Car not found

- finish_trip, '/clients/<clientId>/cars/<carId>/trips/<tripId>' [POST],
    200: Trip marked as finished
    404: Client not found. Car not found. Trip not found

- get_trip '/clients/<clientId>/trips/<tripId>' [GET],
    201: {
        "client_id": string,
        "trip_id": string,
        "car": string,
        "duration": integer,
        "distance": float
    }
    404: Client not found. Trip not found

- delete_trip, '/clients/<clientId>/cars/<carId>/trips/<tripId>' [DELETE],
    204: Trip deleted
    404: Client not found

- get_clients_trips, '/clients/<clientId>/trips' [GET],
    201: [{
        "client_id": string,
        "trip_id": string,
        "car": string,
        "duration": integer,
        "distance": float
    }]
    404: Client not found

- get_car_trips, '/cars/<carId>/trips' [GET],
    201: {
        "car": string,
        "total_duration": integer,
        "total_distance": float
    }
    404: Car not found

- add_point, '/points/<tripId>' [PUT],
    201: {"timestamp": integer}
    400: Invalid input, timestamp lat or long missing
    404: Trip not found
```