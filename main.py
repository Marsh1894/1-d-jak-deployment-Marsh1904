from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



@app.get("/")
def root():
    return {"start": "1970-01-01"}

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
