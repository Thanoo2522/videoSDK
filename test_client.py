import requests

# URL ของ Flask API (ถ้า local ให้ใช้ http://127.0.0.1:5000/get_token)
url = "http://127.0.0.1:5000/get_token"

payload = {
    "roomId": "TA",          # กำหนดห้อง
    "participantId": "123"   # กำหนดผู้เข้าร่วม
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)

try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Response Text:", response.text)
