from sqlalchemy.orm import Session
import math

from . import models, schemas



def get_DataEntries_by_station_id(db: Session, station_id: int):
    compressionFactor = 10
    data = db.query(models.DataEntry).filter(models.DataEntry.owner.has(station_id=station_id)).all()
    

    averageData = []

    for index,dataEntry in enumerate(data):
        try:
            dt = (1/compressionFactor) * int(dataEntry.datetime)
            da = (1/compressionFactor) * dataEntry.data
            if math.floor(index / compressionFactor) == index / compressionFactor:
                averageData.append(schemas.DataEntryLightweightCreate(datetime=dt, data=da))
            else:
                averageData[math.floor(index / compressionFactor)].datetime += dt
                averageData[math.floor(index / compressionFactor)].data += da
        except Exception as e:
            print(e)


    # the last entry may not have had the full compressionFactor number of data entries in it so we should scrap it
    averageData[math.floor(len(data)/10)] = None
    #print(averageData)
    return averageData
    



def get_DataEntry_by_station_id(db: Session, station_id: int):
    return db.query(models.DataEntry).filter(models.DataEntry.owner == station_id).first()



def create_DataEntry(db: Session, dataentry: schemas.DataEntryCreate, station_id: int):
    db_dataentry = models.DataEntry(datetime = dataentry.datetime, data = dataentry.data, owner_id = station_id)
    db.add(db_dataentry)
    db.commit()
    db.refresh(db_dataentry)
    return db_dataentry


def get_StationDatas(db: Session):
    return db.query(models.StationData).all()


def get_StationDataByID(db: Session, station_id : int):
    return db.query(models.StationData).filter(models.StationData.station_id == station_id).first()


def create_StationData(db: Session, stationdata: schemas.StationDataCreate):
    db_stationdata = models.StationData(station_id = stationdata.station_id, title=stationdata.title, description=stationdata.description)
    db.add(db_stationdata)
    db.commit()
    db.refresh(db_stationdata)
    return db_stationdata

