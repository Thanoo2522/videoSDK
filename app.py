import os
import time
import uuid
import jwt
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# โหลด ENV
load_dotenv()
app = Flask(__name__)

VIDEOSDK_API_KEY = os.getenv("VIDEOSDK_API_KEY")
VIDEOSDK_SECRET_KEY = os.getenv("VIDEOSDK_SECRET_KEY")

if not VIDEOSDK_API_KEY or not VIDEOSDK_SECRET_KEY:
    raise Exception("❌ VIDEOSDK_API_KEY or VIDEOSDK_SECRET_KEY not found in .env file")

# -------------------------------
# ฟังก์ชันสร้าง JWT token
# -------------------------------
def generate_token():
    payload = {
        "apikey": VIDEOSDK_API_KEY,
        "iat": int(time.time()),
        "exp": int(time.time()) + 60 * 60 * 24,  # อายุ token 24 ชั่วโมง
        "jti": str(uuid.uuid4()),
    }
    token = jwt.encode(payload, VIDEOSDK_SECRET_KEY, algorithm="HS256")
    return token

# -------------------------------
# API: GET token
# -------------------------------
@app.route("/get-token", methods=["GET"])
def get_token():
    token = generate_token()
    return jsonify({"token": token})

# -------------------------------
# API: Create room
# -------------------------------
@app.route("/create-room", methods=["POST"])
def create_room():
    token = generate_token()
    url = "https://api.videosdk.live/v2/rooms"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    data = {"region": "sg001"}  # เลือก region ตามใกล้ที่สุด
    response = requests.post(url, headers=headers, json=data)

    return jsonify(response.json()), response.status_code

# -------------------------------
# API: Validate token
# -------------------------------
@app.route("/validate", methods=["POST"])
def validate():
    token = request.json.get("token")
    try:
        decoded = jwt.decode(token, VIDEOSDK_SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "decoded": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
