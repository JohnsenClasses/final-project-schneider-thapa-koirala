#Web API to store sensor data and retrive the sensor data

#imports
from datetime import datetime, timedelta
from databases import Database
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(root_path="/wAPI")

database = Database("sqlite:///DatabaseFolder/sqlitesensordata.db" )
 

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

####################################################################################################################
# data storing
@app.put("/sensor_data")
async def put_data(data:SensorData):
    return await database.execute("INSERT INTO sensortable (Latitude,Longitude,Temperature,Humidity) VALUES (:Latitude,:Longitude,:Temperature,:Humidity)",
        {"Latitude":data.Latitude,"Longitude":data.Longitude,"Temperature":data.Temperature,"Humidity":data.Humidity}) 

#######################################################################################################################
#shows all data contained in the database
@app.get("/sensor_data")
async def get_data_sensor():
    return await database.fetch_all("SELECT * FROM sensortable")

#####################################################################################################################
# history of temperature and humidity for a particular location 
@app.get("/sensor_data/{Latitude}/{Longitude}")
async def get_data_bylocation(Latitude:float,Longitude:float):
    return await database.fetch_all("SELECT * FROM sensortable WHERE Latitude=:Latitude AND Longitude=:Longitude",{"Latitude":Latitude,"Longitude":Longitude})

##########################################################################################################################
#temperature and humidity data from a specific time to current time
@app.get("/sensor_data/{Date}")   #user input date to current time, the user input datetime format should be in 2022-05-04 18:11:52
async def get_Sensor_data_fromDate(Date:datetime):
    return await database.fetch_all("SELECT * FROM sensortable WHERE Timestamp>=:Date",{"Date":Date})

##########################################################################################################################
# temperature and humidity data between two points of time
@app.get("/sensor_data/between/{FromDate}/{ToDate}")   #user inputs Form and to  dates in  this format 2022-05-04 18:11:52
async def get_Sensor_data_between_Dates(FromDate:datetime,ToDate:datetime):
    return await database.fetch_all("SELECT * FROM sensortable WHERE Timestamp BETWEEN :FromDate AND :ToDate",{"FromDate":FromDate,"ToDate":ToDate})

#################################################################################################################################
# temperature and humidity data for a particular day
@app.get("/sensor_data/of_a_day/24hours/{Date}")   #date in  this format 2022-05-04
async def get_Sensor_data_of_a_day(Date:str):
    daystart = datetime.strptime(Date, '%Y-%m-%d')
    dayend = daystart + timedelta(hours=23,minutes=59,seconds=59)
    return await database.fetch_all("SELECT * FROM sensortable WHERE Timestamp BETWEEN :daystart AND :dayend",{"daystart":daystart,"dayend":dayend})

#minmum temperature and minmum humidity for a day
@app.get("/sensor_data/of_a_day/24hours/{Date}/temperatureHumidity/Min")   #date in  this format 2022-05-04
async def get_Sensor_data_of_a_day(Date:str):
    daystart = datetime.strptime(Date, '%Y-%m-%d')
    dayend = daystart + timedelta(hours=23,minutes=59,seconds=59)
    return await database.fetch_all("SELECT MIN(Temperature),MIN(Humidity) FROM sensortable WHERE Timestamp BETWEEN :daystart AND :dayend",{"daystart":daystart,"dayend":dayend})

#Maximum temperature and maximum humidity for a day
@app.get("/sensor_data/of_a_day/24hours/{Date}/temperatureHumidity/Max")   #date in  this format 2022-05-04
async def get_Sensor_data_of_a_day(Date:str):
    daystart = datetime.strptime(Date, '%Y-%m-%d')
    dayend = daystart + timedelta(hours=23,minutes=59,seconds=59)
    return await database.fetch_all("SELECT MAX(Temperature),MAX(Humidity) FROM sensortable WHERE Timestamp BETWEEN :daystart AND :dayend",{"daystart":daystart,"dayend":dayend})

# average temperature and average humidity for a day
@app.get("/sensor_data/of_a_day/24hours/{Date}/temperatureHumidity/Avg")   #date in  this format 2022-05-04
async def get_Sensor_data_of_a_day(Date:str):
    daystart = datetime.strptime(Date, '%Y-%m-%d')
    dayend = daystart + timedelta(hours=23,minutes=59,seconds=59)
    return await database.fetch_all("SELECT AVG(Temperature),AVG(Humidity) FROM sensortable WHERE Timestamp BETWEEN :daystart AND :dayend",{"daystart":daystart,"dayend":dayend})
    