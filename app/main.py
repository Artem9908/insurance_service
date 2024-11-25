from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from datetime import datetime

# Импорт для логирования
import threading
import time
import json
from kafka import KafkaProducer

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Инициализация Kafka producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

log_buffer = []
log_buffer_lock = threading.Lock()
LOG_BATCH_SIZE = 10
LOG_BATCH_INTERVAL = 5  # Интервал в секундах

def log_action(user_id, action, event_time):
    log_entry = {
        'user_id': user_id,
        'action': action,
        'event_time': event_time.isoformat()
    }
    with log_buffer_lock:
        log_buffer.append(log_entry)

def log_worker():
    while True:
        time.sleep(LOG_BATCH_INTERVAL)
        with log_buffer_lock:
            if log_buffer:
                batch = log_buffer.copy()
                log_buffer.clear()
                # Отправляем батч в Kafka
                producer.send('log_topic', batch)
                producer.flush()

log_thread = threading.Thread(target=log_worker, daemon=True)
log_thread.start()

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

@app.delete("/rates/{rate_id}", response_model=schemas.Rate)
def delete_rate(rate_id: int, db: Session = Depends(get_db)):
    rate = crud.delete_rate(db, rate_id=rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    log_action(user_id=None, action=f"Удален тариф с ID {rate_id}", event_time=datetime.now())
    return rate

@app.put("/rates/{rate_id}", response_model=schemas.Rate)
def update_rate(rate_id: int, rate_update: schemas.RateUpdate, db: Session = Depends(get_db)):
    rate = crud.update_rate(db, rate_id=rate_id, rate_update=rate_update)
    if not rate:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    log_action(user_id=None, action=f"Обновлен тариф с ID {rate_id}", event_time=datetime.now())
    return rate
