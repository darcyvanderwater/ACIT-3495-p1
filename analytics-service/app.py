from flask import Flask, jsonify
from sqlalchemy import Column, Integer, Float, String, DateTime, select, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from pymongo import MongoClient
import time
import sqlalchemy
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:rootpassword@mysql-db/metrics"
engine = None

# Fix services starting before MySQL is ready (retry loop)
for attempt in range(10):
    try:
        engine = create_engine(DATABASE_URL, echo=False)
        c = engine.connect()
        c.close()
        print("Connected to MySQL!")
        break
    except Exception as e:
        print("MySQL not ready", e)
        time.sleep(5)

if engine is None:
    raise RuntimeError("MySQL unavailable")

Base = declarative_base()

# Define table
class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    label = Column(String(50))
    value = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create table if not exists
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

MONGO_URL = "mongodb://mongo-db:27017/"
DB = "analyticsdb"
COLL = "metrics"

app = Flask(__name__)

@app.post("/run-once")
def run_once():
    # Read all measurements from MySQL
    db = SessionLocal()
    row = db.execute(
        select(
            func.count(Measurement.id),
            func.min(Measurement.value),
            func.max(Measurement.value),
            func.avg(Measurement.value)
        )
    ).one()
    db.close()

    # Prepare summary
    summary = {
        "count": int(row[0] or 0),
        "min": row[1],
        "max": row[2],
        "avg": row[3],
        "computed_at": datetime.utcnow().isoformat() + "Z"
    }

    # Fix the problem I had with objectid
    c = MongoClient(MONGO_URL)
    c[DB][COLL].insert_one(summary.copy())   # insert a COPY to avoid modifying summary
    c.close()

    return jsonify(summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
