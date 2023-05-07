import os
import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.gzip import GZipMiddleware
from supabase import create_client, Client
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from operator import itemgetter
# from starlette.middleware import Middleware
# from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

class RegisteredUser(BaseModel):
    id: int
    text: str
    day: str
    reminder: bool

origins = [
    # "*"
    "http://localhost",
    "http://localhost:3000"
]
# app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def connect_to_db() -> Client:
    URL: str = os.environ.get('SUPABASE_URL')
    KEY: str = os.environ.get('SUPABASE_KEY')
    supabase: Client = create_client(URL, KEY)
    return supabase

# @app.middleware("http")
# async def add_cors_headers(request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "http://localhost, http://localhost:3000"
#     response.headers["Access-Control-Allow-Credentials"] = "true"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     return response

@app.get("")
async def root():
    return {"message": "Hello World"}

@app.get('/get-event/{id}')
async def get_event(id: int):
    supabase = connect_to_db()
    data = supabase.table('events').select('*').eq('id', id).execute().data
    # players = supabase.table('event_players').select('users(name)').eq('event_id', id).execute().data
    json_compatible_item_data = jsonable_encoder(data)
    return JSONResponse(content=json_compatible_item_data)

@app.get('/get-players')
async def get_players():
    supabase = connect_to_db()
    data = supabase.table('users').select('name, point').execute()
    data.data = sorted(data.data, key=itemgetter('point'), reverse=True)
    json_compatible_item_data = jsonable_encoder(data)
    return JSONResponse(content=json_compatible_item_data)

@app.get("/get-events")
async def get_events():
    supabase = connect_to_db()
    data = supabase.table('events').select('*').execute()
    json_compatible_item_data = jsonable_encoder(data)
    # payload = []
    # for x in json_compatible_item_data['data']:
    #     result = {}
    #     result['key'] = x['id']
    #     result['text'] = result['value'] = x['event_name']
    #     payload.append(result)
            
    return JSONResponse(content=json_compatible_item_data)

# @app.get("/get-tasks/")
# async def get_tasks():
#     supabase = connect_to_db()
#     data = supabase.table('events').select('*').execute()

#     json_compatible_item_data = jsonable_encoder(data)

#     # print(data)
#     # print(type(data))
#     # print(json_compatible_item_data)
#     # print(type(json_compatible_item_data))
#     return JSONResponse(content=json_compatible_item_data)

@app.post("/add-event")
async def add_event(data: Request):
    data = await data.json()
    data['event_name'] = data.pop('name')
    data['event_date'] = data.pop('date')
    data['event_start_time'] = data.pop('time')
    data['event_address'] = data.pop('address')
    supabase = connect_to_db()
    supabase.table('events').insert(data).execute()
    return data

# @app.get("/get-task/{id}")
# async def add_task(id: int):
#     supabase = connect_to_db()
#     data = supabase.table('mock').select('*').eq('id', id).execute()
#     json_compatible_item_data = jsonable_encoder(data)
#     return JSONResponse(content=json_compatible_item_data)

@app.delete("/delete-event/{id}")
async def delete_task(id: int):
    supabase = connect_to_db()
    supabase.table('events').delete().eq('id', id).execute()
    # return data

# @app.put("/update-task/{id}")
# async def update_task(id):
#     supabase = connect_to_db()
#     data = supabase.table('mock').select('reminder').eq('id', id).execute()
#     json_compatible_item_data = jsonable_encoder(data)
#     print(json_compatible_item_data['data'][0])
#     # print(not json_compatible_item_data['data'][0]['reminder'])
#     # print(data[0]['reminder'])
#     data = supabase.table('mock').update({'reminder': not json_compatible_item_data['data'][0]['reminder']}).eq('id', id).execute()
#     # data = supabase.table('mock').select('*').execute()

#     json_compatible_item_data = jsonable_encoder(data)
#     print(json_compatible_item_data['data'][0])
#     val = JSONResponse(content=json_compatible_item_data)
#     return val


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG)
#     uvicorn.run(
#         'main:app',
#         port=8000,
#         host='127.0.0.1',
#         reload=True
#     )
