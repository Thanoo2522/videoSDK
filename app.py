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
    raise ValueError("❌ VIDEOSDK_API_KEY หรือ VIDEOSDK_SECRET_KEY ไม่ถูกตั้งค่าใน .env")

@app.route("/get_token", methods=["POST"])
def get_token():
    try:
        data = request.json
        participant_id = data.get("participantId", str(uuid.uuid4()))

        # 1) ขอ meetingId จาก VideoSDK API
        url = "https://api.videosdk.live/v2/rooms"
        headers = {"Authorization": VIDEOSDK_API_KEY}
        res = requests.post(url, headers=headers)

        if res.status_code != 200:
            return jsonify({"error": "❌ Cannot create meeting", "details": res.text}), 500

        meeting_id = res.json().get("roomId")  # VideoSDK return roomId = meetingId

        # 2) สร้าง JWT token
        expiration_time_in_seconds = 3600
        current_timestamp = int(time.time())

        payload = {
            "apikey": VIDEOSDK_API_KEY,
            "roomId": meeting_id,
            "participantId": participant_id,
            "iat": current_timestamp,
            "exp": current_timestamp + expiration_time_in_seconds
        }

        token = jwt.encode(payload, VIDEOSDK_SECRET_KEY, algorithm="HS256")

        return jsonify({
            "apiKey": VIDEOSDK_API_KEY,
            "meetingId": meeting_id,      # ✅ ส่ง meetingId กลับไป
            "participantId": participant_id,
            "token": token
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
