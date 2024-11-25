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

def delete_rate(db: Session, rate_id: int):
    db_rate = db.query(models.Rate).filter(models.Rate.id == rate_id).first()
    if db_rate:
        db.delete(db_rate)
        db.commit()
    return db_rate

def update_rate(db: Session, rate_id: int, rate_update: schemas.RateUpdate):
    db_rate = db.query(models.Rate).filter(models.Rate.id == rate_id).first()
    if not db_rate:
        return None
    for key, value in rate_update.dict(exclude_unset=True).items():
        setattr(db_rate, key, value)
    db.commit()
    db.refresh(db_rate)
    return db_rate
