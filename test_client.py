import requests

# URL ของ Flask API ที่ deploy บน Render
url = "https://acs-e9lu.onrender.com/get_token"

# ข้อมูลที่จะส่งไปหา Flask API
payload = {
    "roomId": "TA",          # ห้อง (VideoSDK ใช้ roomId)
    "participantId": "123"   # ผู้เข้าร่วม (แทน uid ของ Agora)
}

headers = {"Content-Type": "application/json"}

# ส่ง request
response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)

try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Response Text:", response.text)  # ถ้า response ไม่ใช่ JSON
