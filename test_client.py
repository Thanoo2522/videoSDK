import requests

 
url = "https://videosdk-2e7n.onrender.com/get-token"

payload = {  }

headers = {"Content-Type": "application/json"}

response = requests.get(url, json=payload, headers=headers)

print("Status Code:", response.status_code)

try:
    
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Response Text:", response.text)
