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

@app.get("/list-records/{station_id}/", response_model=list[schemas.DataEntry])
def read_dataEntries(station_id: int, db: Session = Depends(get_db)):
    data_entries = crud.get_DataEntries_by_station_id(db, station_id=station_id)
    return data_entries


if __name__ == "__main__":
    uvicorn.run("MPextract:app", port=8000, log_level="debug")