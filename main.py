from typing import Dict
from fastapi import FastAPI, Response, status, Request
from pydantic import BaseModel
from datetime import datetime
from collections import Counter

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


events =[]

class Item(BaseModel):
    date: str
    event: str

@app.put('/events', status_code=200)
def get_event(item: Item):
    id = Counter()
    date_add = datetime.now()
    date_now = date_add.strftime("%Y-%m-%d")

    out_json = {
        "id" : 0,
        "name": item.event,
        "date": item.date,
        "date_added": date_now
    }
    events.append(out_json)
    return out_json
    
app.get("/events/{date}",status_code=200)
def event_on_date(date: str, response: Response):
    if type(date) != str:
        response.status_code = status.HTTP_400_BAD_REQUEST
    else:
        if date in events['date']:
            response.status_code = status.HTTP_200_OK
            return events
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
    return response.status_code

