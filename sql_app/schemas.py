from pydantic import BaseModel

class DataEntryBase(BaseModel):
    datetime: int
    data: float
    owner_id: int


class DataEntryCreate(DataEntryBase):
    pass


class DataEntry(DataEntryBase):
    id: int | None = None


    class Config:
        from_attributes = True


####################

class StationDataBase(BaseModel):
    title: str | None = None
    description: str | None = None
    units: str | None = None
    data: list[DataEntry] = []
    station_id: int


class StationDataCreate(StationDataBase):
    pass


class StationData(StationDataBase):

    class Config:
        from_attributes = True
