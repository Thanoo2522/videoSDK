import requests
import json

# URL Flask Server ของคุณ (แก้ให้ตรงกับของคุณ)
FLASK_SERVER_URL = "https://videosdk-2e7n.onrender.com/get_token"

# ส่ง request ไปที่ Flask Server
def test_flask_server():
    try:
        headers = {
            "Content-Type": "application/json"
        }
        # คุณสามารถส่ง participantId หรือไม่ก็ได้
        payload = {
            "participantId": "user-1234"
        }

        response = requests.post(FLASK_SERVER_URL, headers=headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            print("✅ Response จาก Flask Server:")
            print(json.dumps(data, indent=4))
        else:
            print(f"❌ Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")


if __name__ == "__main__":
    test_flask_server()
