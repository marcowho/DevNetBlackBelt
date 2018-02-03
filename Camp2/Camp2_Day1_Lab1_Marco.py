import requests

# Active clients count
# Use the following URL to query the total number of connected wireless clients known to CMX.
url = "https://cmxlocationsandbox.cisco.com/api/location/v2/clients/count"

headers = {
    'authorization': "Basic bGVhcm5pbmc6bGVhcm5pbmc=",
    'cache-control': "no-cache",
    'postman-token': "14f0fa8c-5000-97d1-d9fc-a9269f1ee70b"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)

# Access Map information
# Many applications will require that you filter the total number of connected clients by certain variables 
# such as clients in a building or on a floor. Run the following query the API to determine the following values for the DevNetZone.

url = "https://cmxlocationsandbox.cisco.com/api/config/v1/maps"

headers = {
    'authorization': "Basic bGVhcm5pbmc6bGVhcm5pbmc=",
    'cache-control': "no-cache",
    'postman-token': "4aa51586-0ce9-cec4-0446-cbb9241fa186"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)

# Try the following API call to get all of the clients in DevNetZone yesterday.
url = "https://cmxlocationsandbox.cisco.com/api/location/v1/history/uniqueclientsbyhierarchy"

querystring = {"date":"2016/07/10","floorid":"723413320329068590"}

headers = {
    'authorization': "Basic bGVhcm5pbmc6bGVhcm5pbmc=",
    'cache-control': "no-cache",
    'postman-token': "73ad1640-9c62-decc-2dd5-ec498b51bfb6"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

# Track client location history
# Query the path of a specific client through the environment. 
url = "https://cmxlocationsandbox.cisco.com/api/location/v1/historylite/clients/00%3A00%3A2a%3A01%3A00%3A08"

headers = {
    'authorization': "Basic bGVhcm5pbmc6bGVhcm5pbmc=",
    'cache-control': "no-cache",
    'postman-token': "43d2531e-0253-fc06-97cc-a95095014162"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)

# Acitve clients
# Run the following query to determine the number of connected clients that are in the DevNetZone.
url = "https://cmxlocationsandbox.cisco.com/api/location/v1/history/uniqueclientsbyhierarchy"

querystring = {"hierarchy":"DevNetCampus/DevNetBuilding/DevNetZone","date":"2017/04/16"}

headers = {
    'authorization': "Basic bGVhcm5pbmc6bGVhcm5pbmc=",
    'cache-control': "no-cache",
    'postman-token': "27f88d68-c7ea-b548-94da-9c0defd2d4a7"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
