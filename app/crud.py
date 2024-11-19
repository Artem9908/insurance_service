from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

def get_rate(db: Session, cargo_type: str, date: date):
    return db.query(models.Rate).filter(models.Rate.cargo_type == cargo_type, models.Rate.date <= date).order_by(models.Rate.date.desc()).first()

def create_rate(db: Session, rate: schemas.RateCreate):
    db_rate = models.Rate(cargo_type=rate.cargo_type, date=rate.date, rate=rate.rate)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate
