import requests

 
url = "https://videosdk-2e7n.onrender.com/get_token"

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
