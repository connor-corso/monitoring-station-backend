from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class StationData(Base):
    __tablename__ = "datas"

    station_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    units = Column(String)
    max_value = Column(Float)
    min_value = Column(Float)
    
    data_entries = relationship("DataEntry", back_populates="owner")


class DataEntry(Base):
    __tablename__ = "dataentries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(Integer)
    data = Column(Float)
    owner_id = Column(Integer, ForeignKey("datas.station_id"))

    owner = relationship("StationData", back_populates="data_entries")

