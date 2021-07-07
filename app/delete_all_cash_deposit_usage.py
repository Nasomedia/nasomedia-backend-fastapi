from app.db.session import SessionLocal
from app import crud

db = SessionLocal()

crud.cash_deposit.remove_all(db)
crud.cash_usage.remove_all(db)
