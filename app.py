import os
import time
import uuid
import jwt
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VIDEOSDK_API_KEY = os.getenv("VIDEOSDK_API_KEY")
VIDEOSDK_SECRET_KEY = os.getenv("VIDEOSDK_SECRET_KEY")

if not VIDEOSDK_API_KEY or not VIDEOSDK_SECRET_KEY:
    raise ValueError("VIDEOSDK_API_KEY หรือ VIDEOSDK_SECRET_KEY ไม่ถูกตั้งค่าใน .env")

# สร้าง meeting ผ่าน VideoSDK REST API
def create_meeting():
    url = "https://api.videosdk.live/v2/rooms"
    headers = {
        "Authorization": VIDEOSDK_API_KEY,
        "Content-Type": "application/json"
    }
    # ถ้า API ต้องการ body อาจส่ง {} หรือ config ต่าง ๆ
    resp = requests.post(url, headers=headers, json={})
    resp.raise_for_status()
    data = resp.json()
    # บาง API ใช้ key ชื่อ "roomId" บางอัน "id" หรือ "room_id"
    room_id = data.get("roomId") or data.get("id")
    return room_id

@app.route("/get_token", methods=["POST"])
def get_token():
    try:
        data = request.json or {}

        # ถ้า client ส่ง roomId มา ให้ใช้, ถ้าไม่ให้สร้างใหม่
        room_id = data.get("roomId")
        if not room_id:
            room_id = create_meeting()

        participant_id = data.get("participantId", str(uuid.uuid4()))

        current_timestamp = int(time.time())
        expiration_time_in_seconds = 3600

        payload = {
            "apikey": VIDEOSDK_API_KEY,
            "meetingId": room_id,  # ใช้ meetingId
            "participantId": participant_id,
            "iat": current_timestamp,
            "exp": current_timestamp + expiration_time_in_seconds
        }

        token = jwt.encode(payload, VIDEOSDK_SECRET_KEY, algorithm="HS256")

        return jsonify({
            "apiKey": VIDEOSDK_API_KEY,
            "meetingId": room_id,
            "participantId": participant_id,
            "token": token
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
