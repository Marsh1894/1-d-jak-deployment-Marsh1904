from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"start": "1970-01-01"}