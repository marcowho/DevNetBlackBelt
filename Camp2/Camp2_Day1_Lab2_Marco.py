
## Before configuring notificaton
:LM-4901 marco$ ssh learning@128.107.70.29
learning@128.107.70.29's password: 
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-79-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

87 packages can be updated.
8 updates are security updates.


*** System restart required ***
Last login: Fri Oct 27 23:32:46 2017 from 183.82.43.66
learning@ubuntu-coggerin-dev01:~$ node -v
v6.10.3
learning@ubuntu-coggerin-dev01:~$ npm -v
3.10.10


learning@ubuntu-coggerin-dev01:~$ node SampleNotificationListener.js
Server Listening on 8000



# Use the CMX REST API GET notifications by name resource to see how the body was formatted.

## With Status: 201 Created
import requests

url = "https://cmxlocationsandbox.cisco.com/api/config/v1/notifications/mjf_movement"

headers = {
    'authorization': "Basic bGVhcm5pbmc6bGVhcm5pbmc=",
    'cache-control': "no-cache",
    'postman-token': "bc1bb7f1-7040-b09e-a164-dc0758dd1d91"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)


# Use the CMX REST API PUT notification resource request to create the notification.
import requests

url = "https://cmxlocationsandbox.cisco.com/api/config/v1/notification"

payload = "{\n  \"name\": \"mjf_movement\",\n  \"userId\": \"learning\",\n  \"rules\": [\n    {\n      \"conditions\": [\n        {\n          \"condition\": \"movement.distance > 20\"\n        },\n        {\n          \"condition\": \"movement.hierarchy == DevNetCampus>DevNetBuilding>DevNetZone\"\n        },\n        {\n          \"condition\": \"movement.deviceType == client\"\n        }\n      ]\n    }\n  ],\n  \"subscribers\": [\n    {\n      \"receivers\": [\n        {\n          \"uri\": \"http://128.107.70.29:8000\",\n          \"messageFormat\": \"JSON\",\n          \"qos\": \"AT_MOST_ONCE\"\n        }\n      ]\n    }\n  ],\n  \"enabled\": true,\n  \"enableMacScrambling\": true,\n  \"macScramblingSalt\": \"listening\",\n  \"notificationType\": \"Movement\"\n}"
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache",
    'authorization': "Basic bGVhcm5pbmc6bGVhcm5pbmc=",
    'postman-token': "6b08d89f-c4ef-fb24-9df9-1ef2c3cd2054"
    }

response = requests.request("PUT", url, data=payload, headers=headers)

print(response.text)



## After configuring notificaton
learning@ubuntu-coggerin-dev01:~$ node SampleNotificationListener.js 8000
Server Listening on 8000
{"notifications":[{"notificationType":"movement","subscriptionName":"mjf_movement","eventId":50734364,"locationMapHierarchy":"DevNetCampus>DevNetBuilding>DevNetZone>Test1","locationCoordinate":{"x":47.92146,"y":57.322598,"z":0.0,"unit":"FEET"},"geoCoordinate":{"latitude":36.12570344757645,"longitude":-97.06680782582376,"unit":"DEGREES"},"confidenceFactor":56.0,"apMacAddress":"00:2b:01:00:09:00","associated":true,"username":"","ipAddress":["10.10.20.222"],"ssid":"test","band":"IEEE_802_11_B","floorId":723413320329068590,"floorRefId":null,"entity":"WIRELESS_CLIENTS","deviceId":"00:00:a9:3e:a7:3a","lastSeen":"2017-10-30T05:36:37.241+0000","moveDistanceInFt":10000.0,"timestamp":1509341797241}]}
/
{"notifications":[{"notificationType":"inout","subscriptionName":"Locuz","eventId":50734365,"locationMapHierarchy":"CiscoCampus>Building 9>IDEAS!>CakeBread","locationCoordinate":{"x":31.482906,"y":23.09707,"z":0.0,"unit":"FEET"},"geoCoordinate":{"latitude":36.12571089428171,"longitude":-97.06678078853979,"unit":"DEGREES"},"confidenceFactor":72.0,"apMacAddress":"00:2b:01:00:09:00","associated":true,"username":"","ipAddress":["10.10.20.216"],"ssid":"test","band":"IEEE_802_11_B","floorId":723413320329068650,"floorRefId":null,"entity":"WIRELESS_CLIENTS","deviceId":"00:00:aa:14:50:8b","lastSeen":"2017-10-30T05:36:37.241+0000","boundary":"INSIDE","areaType":"FLOOR","deviceDetails":null,"timestamp":1509341797241}]}
/
{"notifications":[{"notificationType":"movement","subscriptionName":"mjf_movement","eventId":50734369,"locationMapHierarchy":"DevNetCampus>DevNetBuilding>DevNetZone","locationCoordinate":{"x":185.89401,"y":41.77008,"z":0.0,"unit":"FEET"},"geoCoordinate":{"latitude":36.12574609946288,"longitude":-97.06633787388053,"unit":"DEGREES"},"confidenceFactor":32.0,"apMacAddress":"00:2b:01:00:03:00","associated":true,"username":"","ipAddress":["10.10.20.175"],"ssid":"test","band":"IEEE_802_11_B","floorId":723413320329068590,"floorRefId":null,"entity":"WIRELESS_CLIENTS","deviceId":"00:00:b9:87:4b:3e","lastSeen":"2017-10-30T05:36:37.241+0000","moveDistanceInFt":24.135397,"timestamp":1509341797241}]}
/
{"notifications":[{"notificationType":"inout","subscriptionName":"Locuz","eventId":50734370,"locationMapHierarchy":"DevNetCampus>DevNetBuilding>DevNetZone>Test1","locationCoordinate":{"x":47.92146,"y":57.322598,"z":0.0,"unit":"FEET"},"geoCoordinate":{"latitude":36.12570344757645,"longitude":-97.06680782582376,"unit":"DEGREES"},"confidenceFactor":56.0,"apMacAddress":"00:2b:01:00:09:00","associated":true,"username":"","ipAddress":["10.10.20.222"],"ssid":"test","band":"IEEE_802_11_B","floorId":723413320329068590,"floorRefId":null,"entity":"WIRELESS_CLIENTS","deviceId":"00:00:69:99:34:80","lastSeen":"2017-10-30T05:36:37.241+0000","boundary":"OUTSIDE","areaType":"FLOOR","deviceDetails":null,"timestamp":1509341797241}]}
/




