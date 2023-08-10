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

###########
class DataEntryLightweight(BaseModel):
    datetime: int
    data: float

class DataEntryLightweightCreate(DataEntryLightweight):
    pass


####################

class StationDataBase(BaseModel):
    title: str | None = None
    description: str | None = None
    units: str | None = None
    data: list[DataEntry] = []
    station_id: int = 0 # this is an autoincrementing field, set to 0 to allow it to pick


class StationDataCreate(StationDataBase):
    pass


class StationData(StationDataBase):

    class Config:
        from_attributes = True
