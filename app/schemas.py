from pydantic import BaseModel
from datetime import date

class InsuranceRequest(BaseModel):
    cargo_type: str
    declared_value: float
    date: date

class RateBase(BaseModel):
    cargo_type: str
    date: date
    rate: float

class RateCreate(RateBase):
    pass

class Rate(RateBase):
    id: int

    class Config:
        orm_mode = True
