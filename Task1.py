#Web API to store sensor data and retrive the sensor data

#imports
from databases import Database
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import sqlite3

app = FastAPI()
database = Database("sqlite:///DatabaseFolder/sqlitesensordata.db") #replace folder and db file name

class SensorData(BaseModel):
    Temperature_1:int
    Humidity_1: float
    Temperature_2:float
    Humidity_2:float

@app.on_event("startup")
async def open_database():
    await database.connect()

@app.on_event("shutdown")
async def close_database():
    await database.disconnect()

@app.get("/")
def read_root():
    return[{"Hello":"Sensor World"}]

@app.put("/sensor_data")
async def put_data(data:SensorData):
    return await database.execute("INSERT INTO sensortable (Temperature_1,Humidity_1,Temperature_2,Humidity_2) VALUES (:Temperature_1,:Humidity_1,:Temperature_2,:Humidity_2)",
        {"Temperature_1":data.Temperature_1,"Humidity_1":data.Humidity_1,"Temperature_2":data.Temperature_2,"Humidity_2":data.Humidity_2}) 

@app.get("/sensor_data")
async def get_data_flowers():
    return await database.fetch_all("SELECT * FROM sensortable")



