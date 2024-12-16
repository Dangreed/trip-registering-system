# Trip registering system docs

## Tables
***Client***
```SQL
client_id text PRIMARY KEY,
name text,
surname text,
email text,
birth date  
```

***Car***
```SQL
client_id text,
VIN text,
model text,
manufacturer text,    
plate text,
year date(?),
PRIMARY KEY ((client_id), VIN)
```

***CLient trips***
```SQL
client_id text,
trip_id text,
finished boolean,
car text,
duration bigint,
distance float,
PRIMARY KEY ((client_id, trip_id) ,finished)
```

***Car trips***
```SQL
car text,
trip_id uuid,
finished boolean,
client_id text,
duration bigint,
distance float,
PRIMARY KEY ((car, trip_id), finished)
``` 

***Points***
```SQL
trip_id text,
timestamp timestamp,
lat double,
long double,
dist_from_prev float,
```

## Codes
> [!TIP]
400 - mising data,\
404 - not found,\
200 - get/post,\
201 - put,\
204 - delete success.

## Methods

**- Užregistruoti klientą**
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
```json
- 201: {"id": string}
- 400: Invalid input, missing name, surname, email or birth date.
```
---
**- Gauti kliento informaciją**
```
Request: GET 
URL: '/clients/<clientId>' 
```
***Responses***
```json
- 200: {
    "client_id": string,
    "name": string,
    "surname": string,
    "email": string,
    "birth_date": string
}   
- 404: Client not found.
```
---
**- Ištrinti klientą**
```js
Request: PUT  
URL: '/clients/<clientId>'
```
***Responses***
```json
- 204: Client deleted. 
- 404: Client not found.
```

---
**- Užregistruoti automobilį**
```js
Request: PUT  
URL: '/clients/<clientId>/cars' 
```
***Payload***
```json
{   
    "vin": string,
    "model": string,
    "manufacturer": string,
    "plate": string,
    "manufacturing_date": string
}
```
***Responses***
```json
- 201: {"id": string}. 
- 404: Client not found.
```

---
**- Gauti automobilio informaciją**
```js
Request: GET  
URL: '/clients/<clientId>/cars/<carId>' 
```
***Responses***
```json
- 201: {
        "client_id": string,
        "vin":  string,
        "model": string,
        "manufacturer": string,
        "plate": string,
        "year": string
}
- 404: Client not found. Car not found
```

---
**- Gauti kliento auotmobilius**
```js
Request: GET  
URL: '/clients/<clientId>/cars' 
```
***Responses***
```json
- 201: [{
        "client_id": string,
        "vin":  string,
        "model": string,
        "manufacturer": string,
        "plate": string,
        "year": string
}]
- 404: Client not found. Car not found
```

---
**- Ištrinti kliento automobilį**
```js
Request: DELETE  
URL: '/clients/<clientId>/cars/<carId>' 
```
***Responses***
```json
- 204: Car deleted.
- 404: Client not found. Car not found
```

---
**- Užregistruoti kelionę**
```js
Request: PUT  
URL: '/clients/<clientId>/cars/<carId>/trips' 
```
***Responses***
```json
- 201: {"id": string}
- 404: Client not found. Car not found.
```

---
**- Užbaigti kelionę**
```js
Request: POST  
URL: '/clients/<clientId>/cars/<carId>/trips/<tripId>' 
```
***Responses***
```json
- 200: Trip marked as finihed.
- 404: Trip not found.
```

---
**- Gauti kelionės informaciją**
```js
Request: GET
URL: '/clients/<clientId>/cars/<carId>/trips/<tripId>' 
```
***Responses***
```json
- 201: {
        "client_id": string,
        "trip_id": string,
        "car": string,
        "duration": integer,
        "distance": float
}
- 404: Client not found. Trip not found
```

---
**- Ištrinti kelionę**
```js
Request: DELETE 
URL: '/clients/<clientId>/cars/<carId>/trips/<tripId>' 
```
***Responses***
```json
- 204: Trip deleted.
- 404: Client not found.
```

---
**- Gauti kliento keliones**
```js
Request: GET 
URL: '/clients/<clientId>/trips' 
```
***Responses***
```json
- 201: [{
        "client_id": string,
        "trip_id": string,
        "car": string,
        "duration": integer,
        "distance": float
}]
- 404: Client not found
```

---
**- Gauti automobilio keliones**
```js
Request: GET  
URL: '/cars/<carId>/trips' 
```
***Responses***
```json
- 201: {
        "car": string,
        "total_duration": integer,
        "total_distance": float
    }
- 404: Car not found
```

---
**- Pridėti naują tašką**
```js
Request: PUT 
URL: '/points/<tripId>' 
```
***Payload***
```json
{   
    "timestamp": integer,
    "lat": float,
    "long": float
}
```
***Responses***
```json
- 201: {"timestamp": integer}
- 400: Invalid input, timestamp lat or long missing
- 404: Trip not found
```  

---
**- Išvalyti duomenų bazę**
```js
Request: POST 
URL: '/cleanup' 
```
***Responses***
```json
- 204: Cleanup successful.
```  



