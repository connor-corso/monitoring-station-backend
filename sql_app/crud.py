from sqlalchemy.orm import Session
import math

from . import models, schemas



def get_DataEntries_by_station_id(db: Session, station_id: int, compression_factor: int):
    data = db.query(models.DataEntry).filter(models.DataEntry.owner.has(station_id=station_id)).all()
    
    averageData = []

    for index,dataEntry in enumerate(data):
        try:
            dt = int((1/compression_factor) * int(dataEntry.datetime))
            da = (1/compression_factor) * dataEntry.data,2
            if math.floor(index / compression_factor) == index / compression_factor:
                averageData[averageData.count -1].data = round(averageData[averageData.count -1].data,2)
                averageData.append(schemas.DataEntryLightweightCreate(datetime=dt, data=da))
            else:
                averageData[math.floor(index / compression_factor)].datetime += dt
                averageData[math.floor(index / compression_factor)].data += da
        except Exception as e:
            print(e)


    # the last entry may not have had the full compression_factor number of data entries in it so we should scrap it so that we don't have some entry that is at 1/compression_factor * actual time, resulting in it being way earlier
    averageData.pop()
    print(data)
    print(averageData)
    return averageData
    

def get_DataEntries_by_station_id_and_time(db: Session, station_id: int, start_time: int, end_time: int, compression_factor: int):
    data = db.query(models.DataEntry).filter(models.DataEntry.owner.has(station_id=station_id)).all()
    
    averageData = []

    for index,dataEntry in enumerate(data):
        try:
            if(int(dataEntry.datetime) > start_time and int(dataEntry.datetime) < end_time):
                
                dt = int((1/compression_factor) * int(dataEntry.datetime))
                da = (1/compression_factor) * dataEntry.data,2
                if math.floor(index / compression_factor) == index / compression_factor:
                    averageData[averageData.count -1].data = round(averageData[averageData.count -1].data,2)
                    averageData.append(schemas.DataEntryLightweightCreate(datetime=dt, data=da))
                else:
                    averageData[math.floor(index / compression_factor)].datetime += dt
                    averageData[math.floor(index / compression_factor)].data += da
        except Exception as e:
            print(e)


    # the last entry may not have had the full compression_factor number of data entries in it so we should scrap it so that we don't have some entry that is at 1/compression_factor * actual time, resulting in it being way earlier
    averageData.pop()
    print(data)
    print(averageData)
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

