import requests

url = "https://198.18.129.100//api/v1/ticket"

payload = "{\n  \"username\": \"admin\",\n  \"password\": \"C1sco12345\"\n}"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "71292ddf-6833-87fa-d9af-236f1b11f2f0"
    }

response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.text)