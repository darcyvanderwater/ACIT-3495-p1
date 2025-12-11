from flask import Flask, request, jsonify

app = Flask(__name__)
AUTH_TOKEN = "secret-token"
USERS = {"darcy":"weakpass","darcy2":"weakpass"}

@app.post("/login")
def login():
    data = request.get_json() or {}
    u=data.get("username"); p=data.get("password")
    if USERS.get(u)!=p:
        return jsonify({"error":"invalid credentials"}),401
    return jsonify({"token":AUTH_TOKEN})

@app.get("/validate")
def validate():
    h=request.headers.get("Authorization","")
    if not h.startswith("Bearer "):
        return jsonify({"error":"missing"}),401
    if h.split()[1]!=AUTH_TOKEN:
        return jsonify({"error":"invalid"}),401
    return jsonify({"status":"ok"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)
