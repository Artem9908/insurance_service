from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/calculate_insurance/")
def calculate_insurance(request: schemas.InsuranceRequest, db: Session = Depends(get_db)):
    rate = crud.get_rate(db, cargo_type=request.cargo_type, date=request.date)
    if not rate:
        raise HTTPException(status_code=404, detail="Тариф не найден для указанного типа груза и даты")
    insurance_cost = request.declared_value * rate.rate
    return {"insurance_cost": insurance_cost}

@app.post("/load_rates/")
def load_rates(db: Session = Depends(get_db)):
    import json
    with open('data/rates.json', encoding='utf-8') as f:
        rates_data = json.load(f)
    for rate_item in rates_data:
        rate = schemas.RateCreate(**rate_item)
        crud.create_rate(db, rate)
    return {"status": "Тарифы успешно загружены"}
