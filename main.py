from typing import Dict
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()



@app.get("/")
def root():
    return {"start": "1970-01-01"}

@app.get('/method',status_code=200)
def get():
    return {"method": "GET"}

@app.put('/method',status_code=200)
def put():
    return {"method": "PUT"}

@app.options('/method',status_code=200)
def options():
    return {"method": "OPTIONS"}

@app.delete('/method',status_code=200)
def delete():
    return {"method": "DELETE"}

@app.post('/method',status_code=201)
def post():
    return {"method": "POST"}

days = {1:"monday", 2:"tuesday", 3:"wednesday", 4:"thursday", 5:"friday", 6:"saturday", 7:"sunday"}

@app.get('/day', status_code=200)
def get_day(name: str, number: int, response: Response):
    if number in days:
        if days.get(number) == name:
            response.status_code = status.HTTP_200_OK
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST



@app.put('/events', status_code=200)
def get_date(in_json, response: Response):
    date_added = datetime.date(datetime.now())
    out_json = {
        "id" : 0,
        "name": in_json['event'],
        "date": in_json['date'],
        "date_added": date_added
    }
    response.status_code = status.HTTP_200_OK
    return{out_json}

