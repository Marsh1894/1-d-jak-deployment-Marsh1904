from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"start": "1970-01-01"}

@app.get("/method")
def root():
    return {"method": "1970-01-01"}