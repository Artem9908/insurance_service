from pydantic import BaseModel
import datetime
from typing import Optional

class InsuranceRequest(BaseModel):
    cargo_type: str
    declared_value: float
    date: datetime.date

class RateBase(BaseModel):
    cargo_type: str
    date: datetime.date
    rate: float

class RateCreate(RateBase):
    pass

class RateUpdate(BaseModel):
    cargo_type: Optional[str] = None
    date: Optional[datetime.date] = None
    rate: Optional[float] = None

class Rate(RateBase):
    id: int

    class Config:
        orm_mode = True
