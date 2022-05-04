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
    Latitude:   float
    Longitude:  float
    Temperature:float
    Humidity:   float
    

@app.on_event("startup")
async def open_database():
    await database.connect()

@app.on_event("shutdown")
async def close_database():
    await database.disconnect()

@app.get("/")
def read_root():
    return[{"Hello":"Sensor World"}]

""" @app.put("/sensor_data")
async def put_data(data:SensorData):
    return await database.execute("INSERT INTO sensortable (Temperature_1,Humidity_1,Temperature_2,Humidity_2) VALUES (:Temperature_1,:Humidity_1,:Temperature_2,:Humidity_2)",
        {"Temperature_1":data.Temperature_1,"Humidity_1":data.Humidity_1,"Temperature_2":data.Temperature_2,"Humidity_2":data.Humidity_2})  """

@app.put("/sensor_data")
async def put_data(data:SensorData):
    return await database.execute("INSERT INTO sensortable (Latitude,Longitude,Temperature,Humidity) VALUES (:Latitude,:Longitude,:Temperature,:Humidity)",
        {"Latitude":data.Latitude,"Longitude":data.Longitude,"Temperature":data.Temperature,"Humidity":data.Humidity}) 

@app.get("/sensor_data")
async def get_data_flowers():
    return await database.fetch_all("SELECT * FROM sensortable")


@app.get("/sensor_data/{}")
async def get_data_genus(a_genus:str):
    return await database.fetch_all("SELECT * FROM flower WHERE genus=:g_name",{"g_name":a_genus})

@app.get("/flowers/{a_genus}/{a_species}")
async def get_data_genus_species(a_genus:str,a_species:str):
    return await database.fetch_all("SELECT * FROM flower WHERE genus=:g_name AND species=:s_name",{"g_name":a_genus,"s_name":a_species})

@app.get("/flowers/{a_genus}/{a_species}/petals/avg")
async def get_data_genus_species_petal_avg(a_genus:str,a_species:str):
        return await database.fetch_all(f"SELECT AVG(petal_count) as avg FROM flower WHERE genus='{a_genus}' AND species='{a_species}'")

@app.get("/flowers/{a_genus}/{a_species}/petals/min")
async def get_data_genus_species_petal_avg(a_genus:str,a_species:str):
        return await database.fetch_all(f"SELECT MIN(petal_count) as min FROM flower WHERE genus='{a_genus}' AND species='{a_species}'")
     
@app.get("/flowers/{a_genus}/{a_species}/petals/max")
async def get_data_genus_species_petal_avg(a_genus:str,a_species:str):
        return await database.fetch_all(f"SELECT MAX(petal_count) as max FROM flower WHERE genus='{a_genus}' AND species='{a_species}'")
