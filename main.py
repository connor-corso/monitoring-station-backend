#/usr/bin/python3

##############################
# 
# Written by Connor Corso
# 
##############################


import datetime

import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine


# fast api stuff
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_file_data(inputfile):
    pass

# this has no checking to see if the data already exists but I feel like that is okay
@app.post("/create-record/{station_id}/", response_model=schemas.DataEntry)
def create_record(station_id: int, record: schemas.DataEntryCreate, db: Session = Depends(get_db)):
    station = crud.get_StationDataByID(db, station_id=station_id)
    if not station:
        crud.create_StationData(db, schemas.StationDataCreate(station_id=station_id))
    return crud.create_DataEntry(db, dataentry=record, station_id=station_id)

@app.get("/list-records/{station_id}/", response_model=list[schemas.DataEntryLightweight])
def read_dataEntries(station_id: int, db: Session = Depends(get_db), compression_factor: int = 10):
    data_entries = crud.get_DataEntries_by_station_id(db, station_id=station_id, compression_factor = compression_factor)
    return data_entries

@app.get("/list-records/{station_id}/{start_time}/{end_time}/")
def read_dataEntries(station_id: int, start_time: int, end_time: int, db: Session = Depends(get_db), compression_factor: int = 10):
    data_entries = crud.get_DataEntries_by_station_id_and_time(db, station_id=station_id, start_time = start_time, end_time = end_time, compression_factor = compression_factor)
    return data_entries

@app.get("/list-latest-record/{station_id}/", response_model=schemas.DataEntry)
def get_latest_record(station_id: int, db: Session = Depends(get_db)):
    latest_record = crud.get_DataEntry_by_station_id(db, station_id)
    return latest_record

@app.get("/list-stations/", response_model=list[schemas.StationData])
def read_station_datas(db: Session = Depends(get_db)):
    station_datas = crud.get_StationDatas(db)
    return station_datas

@app.get("/get-station-info/{station_id}/", response_model=schemas.StationData)
def get_station_info(station_id: int, db: Session = Depends(get_db)):
    station_information = crud.get_StationDataByID(db, station_id)
    return station_information
