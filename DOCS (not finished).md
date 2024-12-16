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
### Client
**⟶ Užregistruoti klientą**
```python
@app.route('/', methods=[PUT])
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
- 201: Client registered

**⟶ Gauti kliento informaciją**
```python
@app.route('/', methods=[GET])
```
***Responses***
```json
- 200: Client details
{
    "client_id": "string",
    "name": "string",
    "surname": "string",
    "email": "string",
    "birth_date": "string"
}
- 404: Client not found
```

---
### Vehicle
**⟶ Užregistruoti automobilį**
```python
@app.route('/', methods=[PUT])
```
***Payload***
```json
{
    "model": "Prius",
    "manufacturer": "Toyota",
    "state_number": "ABC123",
    "VIN": "JM1NB3538Y0153757",
    "manufacturing_date": "2007-06"
}
```
***Responses***
- ...


**⟶ Gauti automobilio informaciją**
```python
@app.route('/', methods=[PUT])
```
***Responses***
- ...


**⟶ Gauti kliento auotmobilius**
```python
@app.route('/', methods=[GET])
```
***Responses***
- ...

---
### Trip
**⟶ Užregistruoti kelionę**
```python
@app.route('/', methods=[PUT])
```
***Responses***
- ...


**⟶ Užbaigti kelionę**
```python
@app.route('/', methods=[POST])
```
***Responses***
- ...


**⟶ Gauti kelionės informaciją**
```python
@app.route('/', methods=[GET])
```
***Responses***
- ...


**⟶ Gauti kliento keliones**
```python
@app.route('/', methods=[GET])
```
***Responses***
- ...


**⟶ Gauti automobilio keliones**
```python
@app.route('/', methods=[GET])
```
***Responses***
- ...

---
### Other
**⟶ Pridėti naują tašką**
```python
@app.route('/points/<tripId>', methods=[PUT])
```
***Payload***
```json
{
    "lat": 0.0000000,
    "long": 0.0000000
}
```
***Responses***
- ...


**⟶ Išvalyti duomenų bazę**
```python
@app.route('/cleanup', methods=[POST])
```
***Responses***
- 200: Cleanup successful  



