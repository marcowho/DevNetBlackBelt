import requests
import json

requests.packages.urllib3.disable_warnings()

url = "https://198.18.129.100/api/v1/ticket"

payload = {"username":"admin","password":"C1sco12345"}

header = {
    'content-type': "application/json",
    }

response = requests.post(url,data=json.dumps(payload), headers=header, verify=False)

response = response.json()
print("Token:", response["response"]["serviceTicket"])
