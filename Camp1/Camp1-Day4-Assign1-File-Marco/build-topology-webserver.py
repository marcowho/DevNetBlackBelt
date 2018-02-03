# Example of render a topology via a web server. This include :
# - building a web server via Flask (http://flask.pocoo.org/)
# - render topology graphic via NeXt UI toolkit (https://wiki.opendaylight.org/view/NeXt:Main)
# - get topology data from APIC-EM via REST API calls from Python

# Before start please install flask by `pip install flask`
# Then use python run this script via: python build-topology-webserver.py
# Use Chrome or Safari browser. In the url field enter this link: `http://127.0.0.1:5000/`

# * THIS SAMPLE APPLICATION AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY
# * OF ANY KIND BY CISCO, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED
# * TO THE IMPLIED WARRANTIES OF MERCHANTABILITY FITNESS FOR A PARTICULAR
# * PURPOSE, NONINFRINGEMENT, SATISFACTORY QUALITY OR ARISING FROM A COURSE OF
# * DEALING, LAW, USAGE, OR TRADE PRACTICE. CISCO TAKES NO RESPONSIBILITY
# * REGARDING ITS USAGE IN AN APPLICATION, AND IT IS PRESENTED ONLY AS AN
# * EXAMPLE. THE SAMPLE CODE HAS NOT BEEN THOROUGHLY TESTED AND IS PROVIDED AS AN
# * EXAMPLE ONLY, THEREFORE CISCO DOES NOT GUARANTEE OR MAKE ANY REPRESENTATIONS
# * REGARDING ITS RELIABILITY, SERVICEABILITY, OR FUNCTION. IN NO EVENT DOES
# * CISCO WARRANT THAT THE SOFTWARE IS ERROR FREE OR THAT CUSTOMER WILL BE ABLE
# * TO OPERATE THE SOFTWARE WITHOUT PROBLEMS OR INTERRUPTIONS. NOR DOES CISCO
# * WARRANT THAT THE SOFTWARE OR ANY EQUIPMENT ON WHICH THE SOFTWARE IS USED WILL
# * BE FREE OF VULNERABILITY TO INTRUSION OR ATTACK. THIS SAMPLE APPLICATION IS
# * NOT SUPPORTED BY CISCO IN ANY MANNER. CISCO DOES NOT ASSUME ANY LIABILITY
# * ARISING FROM THE USE OF THE APPLICATION. FURTHERMORE, IN NO EVENT SHALL CISCO
# * OR ITS SUPPLIERS BE LIABLE FOR ANY INCIDENTAL OR CONSEQUENTIAL DAMAGES, LOST
# * PROFITS, OR LOST DATA, OR ANY OTHER INDIRECT DAMAGES EVEN IF CISCO OR ITS
# * SUPPLIERS HAVE BEEN INFORMED OF THE POSSIBILITY THEREOF.-->

"""
Camp1 - Day 4 - Assign1

Assignment 1
Please use the file as given in https://github.com/Devanampriya/DevNet_vCC_Team0/blob/master/Camp1-Day4-Assign1-Files.zip.

Task1 - Complete and Run the python file to get to see your APIC-EM topo diagram in the ubuntu workstation.
Paste the url you get after successful execution of this python file - into the "Topic - APIC-EM" spark room.

Task2 - please get the values for the keys below for each of the devices in the apic-em network and paste it in same spark room as above.
1. "deviceType"
2. "softwareVersion"
3. "platformId"

Please note that there should be only a single python file for both the tasks combined.
Hint: the flask part is already completed for you - you just need to do the APIC-EM part(take help of swagger to find the right api) and use your spark api skills. 
As a further reference you can take a look here to understand in detail about how the UI element works : https://abdvl.github.io/
"""

# import requests library
import requests

# import json library
import json

#import datetime
#import re

# import flask web framewoork
from flask import Flask

# from flask import render_template function
from flask import render_template, jsonify

requests.packages.urllib3.disable_warnings()

# controller
url = "https://198.18.129.100/api/v1/"
auth = "ZmVjMGY5ZmYtZmVhMi00MTc5LWJmYjgtMTNiOTc1MmFhZjdiMWEyNGViNzQtYmJl"
url_room = "https://api.ciscospark.com/v1/rooms"
url_message = "https://api.ciscospark.com/v1/messages"
room_name = "Topic - APIC-EM"
#room_name = "Cisco Spark API Lab1-Q1"

def getTicket(url):
    api_call = "ticket"
    url = url + api_call

    payload = {"username":"admin","password":"C1sco12345"}

    header = {
        'content-type': "application/json",
        }

    response = requests.post(url,data=json.dumps(payload), headers=header, verify=False)
    resp = response.json()
    ticket = resp["response"]["serviceTicket"]
    return ticket  


def getTopology(token,url):
    api_call = "topology/physical-topology"

    url = url + api_call

    header = {"content-type": "application/json", "X-Auth-Token": token}

    response = requests.get(url, headers=header, verify=False)

    r_json = response.json()

    return r_json["response"]


def get_device_info(token,url):
    result = []
    api_call = "network-device"
    url = url + api_call

    headers = {
        'content-type': "application/json",
        'x-auth-token': token
        }

    response = requests.request("GET", url, headers=headers, verify=False)
    resp = response.json()
#   print(resp)
    for item in resp['response']:
        result.append("deviceType:" + item["type"])
        result.append("softwareVersion:" + item["softwareVersion"]) 
        result.append("platformId: " + item["platformId"] + "\n")
    return(result)


def setHeaders():         
    accessToken_hdr = 'Bearer ' + auth
    spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
    return (spark_header)


def findRoom(url_room,the_header,room_name):
    roomId=""
    resp = requests.get(url_room, headers=the_header)
    resp = resp.json()
    for room in resp["items"]:
        if room["title"] == room_name:
            roomId = room["id"] 
            print("Found group:",room_name)
            break   
    return(roomId)


def postMsg(room_id,url_message,the_header,room_name,message):
    roomId = room_id
    if roomId != "":
        message_json = {"roomId":roomId,"text":'\n'.join(message)}
        resp = requests.post(url_message, json=message_json, headers=the_header)
        print()
        print("Message\"", message, "\"has been sent successfullly!")
    else:
        print("Room " + room_name + " is not exist ....")



# intialize a web app
app = Flask(__name__)
	
# define index route to return topology.html
@app.route("/")
def index():
    # when called '/' which is the default index page, render the template 'topology.html'
    return render_template("topology.html")


# define an reset api to get topology data
@app.route("/api/topology")
def topology():
    # get ticket
    theTicket = getTicket(url)

    # get topology data and return `jsonify` string to request
    return jsonify(getTopology(theTicket,url))

	

if __name__ == "__main__":
    theTicket = getTicket(url)
    message = get_device_info(theTicket,url)
    header = setHeaders()
    roomId = findRoom(url_room,header,room_name)
    postMsg(roomId,url_message,header,room_name,message)
    app.run()
