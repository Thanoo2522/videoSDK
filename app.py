import os
import time
import uuid
import jwt
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VIDEOSDK_API_KEY = os.getenv("VIDEOSDK_API_KEY")
VIDEOSDK_SECRET_KEY = os.getenv("VIDEOSDK_SECRET_KEY")

if not VIDEOSDK_API_KEY or not VIDEOSDK_SECRET_KEY:
    raise ValueError("❌ VIDEOSDK_API_KEY หรือ VIDEOSDK_SECRET_KEY ไม่ถูกตั้งค่าใน .env")


@app.route("/get_token", methods=["POST"])
def get_token():
    try:
        data = request.json
        room_id = data.get("roomId", str(uuid.uuid4()))  # ถ้าไม่มี roomId ให้สร้างอัตโนมัติ
        participant_id = data.get("participantId", str(uuid.uuid4()))

        # เวลาหมดอายุของ Token (วินาที)
        expiration_time_in_seconds = 3600
        current_timestamp = int(time.time())

        payload = {
            "apikey": VIDEOSDK_API_KEY,
            "roomId": room_id,
            "participantId": participant_id,
            "iat": current_timestamp,
            "exp": current_timestamp + expiration_time_in_seconds
        }

        token = jwt.encode(payload, VIDEOSDK_SECRET_KEY, algorithm="HS256")

        return jsonify({
            "apiKey": VIDEOSDK_API_KEY,
            "roomId": room_id,
            "participantId": participant_id,
            "token": token
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
