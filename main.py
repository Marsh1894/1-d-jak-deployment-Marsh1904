# from typing import Dict, List
# from fastapi import FastAPI, Response, status, Request, HTTPException
# from pydantic import BaseModel, BaseSettings
# from datetime import datetime
# from collections import Counter

# app = FastAPI()

# class Settings(BaseSettings):
#     events_counter: int = 0


# class EventCounterRq(BaseModel):
#     event: str
#     date: str


# class EventCounterResponse(BaseModel):
#     name: str
#     date: str
#     id: int
#     date_added: str


# settings = Settings()

# events: List[EventCounterResponse] = []



# @app.get("/")
# def root():
#     return {"start": "1970-01-01"}

# @app.get('/method',status_code=200)
# def get():
#     return {"method": "GET"}

# @app.put('/method',status_code=200)
# def put():
#     return {"method": "PUT"}

# @app.options('/method',status_code=200)
# def options():
#     return {"method": "OPTIONS"}

# @app.delete('/method',status_code=200)
# def delete():
#     return {"method": "DELETE"}

# @app.post('/method',status_code=201)
# def post():
#     return {"method": "POST"}

# days = {1:"monday", 2:"tuesday", 3:"wednesday", 4:"thursday", 5:"friday", 6:"saturday", 7:"sunday"}

# @app.get('/day', status_code=200)
# def get_day(name: str, number: int, response: Response):
#     if number in days:
#         if days.get(number) == name:
#             response.status_code = status.HTTP_200_OK
#         else:
#             response.status_code = status.HTTP_400_BAD_REQUEST


# events =[]

# class Item(BaseModel):
#     date: str
#     event: str

# # @app.put('/events', status_code=200)
# # def get_event(item: Item):
# #     id = Counter()
# #     date_add = datetime.now()
# #     date_now = date_add.strftime("%Y-%m-%d")

# #     out_json = {
# #         "id" : 0,
# #         "name": item.event,
# #         "date": item.date,
# #         "date_added": date_now
# #     }
# #     return out_json

# @app.put("/events", status_code=200, response_model=EventCounterResponse)
# def put_event(data: EventCounterRq):

#     date_add = datetime.now()
#     date_now = date_add.strftime("%Y-%m-%d")

#     name = data.event
#     date = data.date
#     id = settings.events_counter
#     settings.events_counter += 1
#     date_added = date_now

#     res = EventCounterResponse(
#         name=name, date=date, id=id, date_added=date_added
#     )
#     events.append(res)

#     return res

# @app.get("/events/{date}", status_code=201)
# def get_event(date: str, response: Response):
#     event_date=[]
#     format = "/%Y-%m-%d"
#     try:
#         datetime.datetime.strptime(date, format)
#         for event in events:
#             if event["date"] == date:
#                 event_date.append(event)
#         if len(event_date) == 0:
#             response.status_code = 404
#             return "not found"
#         return event_date

#     except ValueError:
#         response.status_code = 400
#         return "Enter correct date"


# # @app.get("/events/{date}", status_code=200, response_model=List[EventCounterResponse])
# # def get_event(date: str):

# #     try:
# #         _ = (datetime.datetime.strptime(date, "%Y-%m-%d"),)
# #     except:
# #         raise HTTPException(status_code=400, detail="Invalid date format")

# #     final_events: List[EventCounterResponse] = []

# #     for event in events:
# #         if event.date == date:
# #             final_events.append(event)

# #     if len(final_events) > 0:
# #         return final_events
# #     else:
# #         raise HTTPException(status_code=404, detail="Didn't find any data")




import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, BaseSettings


class Settings(BaseSettings):
    events_counter: int = 0


class EventCounterRq(BaseModel):
    event: str
    date: str


class EventCounterResponse(BaseModel):
    name: str
    date: str
    id: int
    date_added: str


app = FastAPI()
settings = Settings()

events: List[EventCounterResponse] = []


@app.get("/")
def root():
    return {"start": "1970-01-01"}


@app.post(path="/method", status_code=201)
def get_post():
    return {"method": "POST"}


@app.api_route(
    path="/method",
    methods=["GET", "PUT", "OPTIONS", "DELETE"],
    status_code=200,
)
async def get_methods(request: Request):
    return {"method": request.method}


days = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday",
}


@app.get("/day/", status_code=200)
def get_day(name: str, number: int):
    if number in days:
        if days.get(number, False) == name:
            return days[number]
        else:
            raise HTTPException(status_code=400, detail="Invalid day!")
    else:
        raise HTTPException(status_code=400, detail="Number higher than 7!")


@app.put("/events", status_code=200, response_model=EventCounterResponse)
def put_event(data: EventCounterRq):

    name = data.event
    date = data.date
    id = settings.events_counter
    settings.events_counter += 1
    date_added = str(datetime.date.today())

    res = EventCounterResponse(
        name=name, date=date, id=id, date_added=date_added
    )
    events.append(res)

    return res


@app.get(
    "/events/{date}",
    status_code=200,
    response_model=List[EventCounterResponse],
)
def get_event(date: str):

    try:
        _ = (datetime.datetime.strptime(date, "%Y-%m-%d"),)
    except:
        raise HTTPException(status_code=400, detail="Invalid date format")

    final_events: List[EventCounterResponse] = []

    for event in events:
        if event.date == date:
            final_events.append(event)

    if len(final_events) > 0:
        return final_events
    else:
        raise HTTPException(status_code=404, detail="Didn't find any data")




import datetime

from dateutil.relativedelta import relativedelta
from fastapi import Depends, FastAPI, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()


@app.get("/start", response_class=HTMLResponse)
def start():
    return """
    <h1>The unix epoch started at 1970-01-01</h1>
    """


@app.post("/check", response_class=HTMLResponse)
def check(credentials: HTTPBasicCredentials = Depends(security)):
    date_str = credentials.password
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return Response(status_code=401)

    # Taken from https://stackoverflow.com/questions/4436957/pythonic-difference-between-two-dates-in-years.
    age = relativedelta(datetime.datetime.now(), date).years
    if age < 16:
        return Response(status_code=401)

    return f"""
    <h1>Welcome {credentials.username}! You are {age}</h1>
    """


@app.get("/info")
def info(request: Request, format: str = ""):
    if format == "json":
        return {
            "user_agent": f"{request.headers['User-Agent']}"
        }
    elif format == "html":
        return HTMLResponse(f"""
        <input type="text" id=user-agent name=agent value="{request.headers['User-Agent']}">
        """)
    else:
        return Response(status_code=400)


paths_used = set()


@app.put("/save/{string}")
def save(string: str):
    paths_used.add(string)
    return Response(status_code=200)


@app.get("/save/{string}")
def save(string: str):
    if string in paths_used:
        return RedirectResponse("/info", status_code=301)
    else:
        return Response(status_code=404)


@app.delete("/save/{string}")
def save(string: str):
    paths_used.remove(string)
    return Response(status_code=200)


@app.post("/save/{string}")
@app.options("/save/{string}")
@app.head("/save/{string}")
@app.trace("/save/{string}")
@app.patch("/save/{string}")
def save(string: str):
    return Response(status_code=400)






# @app.get("/hello/{name}", response_model=HelloResp)
# def read_item(name: str):
#     return HelloResp(msg=f"Hello {name}")


# class GiveMeSomethingRq(BaseModel):
#     first_key: str


# class GiveMeSomethingResp(BaseModel):
#     received: Dict
#     constant_data: str = "python jest super"


# @app.post("/dej/mi/co??", response_model=GiveMeSomethingResp)
# def receive_something(rq: GiveMeSomethingRq):
#     return GiveMeSomethingResp(received=rq.dict())

# class HelloResp(BaseModel):
#     msg: str
