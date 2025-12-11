from flask import Flask, request
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import requests
import time, sqlalchemy
from sqlalchemy import create_engine
DATABASE_URL="mysql+pymysql://root:rootpassword@mysql-db/metrics"
engine=None
for attempt in range(10):
    try:
        engine=create_engine(DATABASE_URL,echo=False)
        c=engine.connect(); c.close()
        print("Connected to MySQL!")
        break
    except Exception as e:
        print("MySQL not ready", e)
        time.sleep(5)
if engine is None:
    raise RuntimeError("MySQL unavailable")

Base=declarative_base()
class Measurement(Base):
    __tablename__="measurements"
    id=Column(Integer,primary_key=True)
    label=Column(String(50))
    value=Column(Float)
    created_at=Column(DateTime,default=datetime.utcnow)
Base.metadata.create_all(engine)
SessionLocal=sessionmaker(bind=engine)
AUTH_URL="http://auth-service:5000"
app=Flask(__name__)
FORM = """<!doctype html>
<html>
<head>
    <title>Darcy's Data Entry</title>
</head>
<body>
<h1>Darcy's Data Entry Page</h1>

<form method='post'>
    User:<input name='username'><br>
    Pass:<input name='password' type='password'><br>
    Label:<input name='label'><br>
    Value:<input name='value'><br>
    <button>Save</button>
</form>

<hr>
<a href="http://localhost:5001/">Go to Results Page</a>

<p style='color:red;'>%s</p>
</body>
</html>"""


@app.route("/",methods=["GET","POST"])
def idx():
    err=""
    if request.method=="POST":
        u=request.form.get("username"); p=request.form.get("password")
        lab=request.form.get("label"); v=request.form.get("value")
        try:
            r=requests.post(AUTH_URL+"/login",json={"username":u,"password":p})
            if r.status_code!=200: return FORM%"Invalid credentials"
        except Exception as e:
            return FORM%("Auth error %s"%e)
        try: val=float(v)
        except: return FORM%"Value must be numeric"
        db=SessionLocal(); db.add(Measurement(label=lab,value=val)); db.commit(); db.close()
        return "<h1>Saved</h1><a href='/'>Back</a><br><a href='http://localhost:5001/'>Go to Results Page</a>"

    return FORM%err

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
