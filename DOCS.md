# Trip registering system docs

## Tables
***Client***
```SQL
client_id TEXT PRIMARY KEY,
name TEXT,
surname TEXT,
email TEXT,
birth_date DATE
```

***Car***
```SQL
client_id TEXT,
vin TEXT,
model TEXT,
manufacturer TEXT,
plate TEXT,
year DATE,
PRIMARY KEY ((client_id), vin)) 
```

***Client trips***
```SQL
client_id TEXT,
trip_id TEXT,
finished BOOLEAN,
car TEXT,
duration BIGINT,
distance DOUBLE,
PRIMARY KEY ((client_id, finished), trip_id))
```

***Car trips***
```SQL
car TEXT,
trip_id TEXT,
finished BOOLEAN,
client_id TEXT,
duration BIGINT,
distance DOUBLE,
PRIMARY KEY ((car, finished), trip_id))
``` 

***Points***
```SQL
(
    trip_id TEXT,
    timestamp TIMESTAMP,
    lat DOUBLE,
    long DOUBLE,
    dist_from_prev DOUBLE,
    PRIMARY KEY ((trip_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);
```

## Codes
> [!TIP]
400 - mising data,\
404 - not found,\
200 - get/post,\
201 - put,\
204 - delete success.

## Methods

### Register a client
```
Request: PUT  
URL: '/clients' 
```
***Payload***
```json 
{
    "name": "John",
    "surname": "Johnatan",
    "email": "johnjohn@gmai.com",
    "birth_date": "1999-05-17"
}
```
***Responses***
- 201:
```json
 {"id": "string"}
```
- 400: `Invalid input, missing name, surname, email or birth date.`
---
### Get client's info
```
Request: GET 
URL: '/clients/<clientId>' 
```
***Responses***
- 200:
```json
{
    "client_id": "string",
    "name": "string",
    "surname": "string",
    "email": "string",
    "birth_date": "string"
}
```
- 404: `Client not found.`
---
### Delete a client
```js
Request: PUT  
URL: '/clients/<clientId>'
```
***Responses***
- 204: `Client deleted.`
- 404: `Client not found.`

---
### Register a car
```js
Request: PUT  
URL: '/clients/<clientId>/cars' 
```
***Payload***
```json
{   
    "vin": "string",
    "model": "string",
    "manufacturer": "string",
    "plate": "string",
    "manufacturing_date": "string"
}
```
***Responses***
- 201:
```json
{"id": "string"}
```
- 404: `Client not found.`

---
### Get car's info
```js
Request: GET  
URL: '/clients/<clientId>/cars/<carId>' 
```
***Responses***
- 201:
```json
{
        "client_id": "string",
        "vin":  "string",
        "model": "string",
        "manufacturer": "string",
        "plate": "string",
        "year": "string"
}
```
- 404: `Client not found. Car not found`

---
### Get client's cars
```js
Request: GET  
URL: '/clients/<clientId>/cars' 
```
***Responses***
- 201:
```json
[{
        "client_id": "string",
        "vin":  "string",
        "model": "string",
        "manufacturer": "string",
        "plate": "string",
        "year": "string"
}]
```
- 404: `Client not found. Car not found`

---
### Delete a car
```js
Request: DELETE  
URL: '/clients/<clientId>/cars/<carId>' 
```
***Responses***
- 204: `Car deleted.`
- 404: `Client not found. Car not found`

---
### Register a trip
```js
Request: PUT  
URL: '/clients/<clientId>/cars/<carId>/trips' 
```
***Responses***
- 201:
```json
{"id": "string"}
```
- 404: `Client not found. Car not found.`


---
### End a trip
```js
Request: POST  
URL: '/clients/<clientId>/cars/<carId>/trips/<tripId>' 
```
***Responses***
- 200: `Trip marked as finihed.`
- 404: `Trip not found.`

---
### Get trip's info
```js
Request: GET
URL: '/clients/<clientId>/cars/<carId>/trips/<tripId>' 
```
***Responses***
- 201:
```json
{
        "client_id": "string",
        "trip_id": "string",
        "car": "string",
        "duration": "integer",
        "distance": "float"
}
```
- 404: `Client not found. Trip not found`

---
### Delete a trip
```js
Request: DELETE 
URL: '/clients/<clientId>/cars/<carId>/trips/<tripId>' 
```
***Responses***
- 204: `Trip deleted.`
- 404: `Client not found.`

---
### Get client's trips
```js
Request: GET 
URL: '/clients/<clientId>/trips' 
```
***Responses***
- 201:
```json
[{
        "client_id": "string",
        "trip_id": "string",
        "car": "string",
        "duration": "integer",
        "distance": "float"
}]
```
- 404: `Client not found`

---
### Get trips by car
```js
Request: GET  
URL: '/cars/<carId>/trips' 
```
***Responses***
- 201:
```json
{
        "car": "string",
        "total_duration": "integer",
        "total_distance": "float"
    }
```
- 404: `Car not found`

---
### Add a new point
```js
Request: PUT 
URL: '/points/<tripId>' 
```
***Payload***
```json
{   
    "timestamp": "integer",
    "lat": "float",
    "long": "float"
}
```
***Responses***
- 201: 
```json
{"timestamp": "integer"}
```
- 400: `Invalid input, timestamp lat or long missing`
- 404: `Trip not found`

---
### Cleanup
```js
Request: POST 
URL: '/cleanup' 
```
***Responses***
- 204: `Cleanup successful.`
