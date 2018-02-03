"""
Create a spark room named “Cisco Spark API Lab1-Q1” through the rooms api in python.
Add any one of your teammembers into the room(created in assign1) through the membership API. For those who do not have a teammate - you can add "joeljos@cisco.com" into the room.
Post the message “I completed my Spark API Assignments!!” to the above room.
"""

import json
import sys
import requests

ACCESS_TOKEN = "ZmVjMGY5ZmYtZmVhMi00MTc5LWJmYjgtMTNiOTc1MmFhZjdiMWEyNGViNzQtYmJl" 
URL_ROOM = 'https://api.ciscospark.com/v1/rooms'
URL_MEMBER = 'https://api.ciscospark.com/v1/memberships'
URL_MESSAGE = 'https://api.ciscospark.com/v1/messages'
ROOM_NAME = "Cisco Spark API Lab1-Q1" 
MESSAGE = ""


def setHeaders():         
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
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

def createRoom(url_room,the_header,room_name):
	roomId = findRoom(url_room,header,room_name)
	if roomId == "":
		roomInfo = {"title":room_name}
		resp = requests.post(url_room, json=roomInfo, headers=the_header)
		resp_json = resp.json()
		print()
		print("Room " + room_name + " has been created successfully!")
		roomId=resp_json["id"]
	return(roomId)


def addMembers(room_id,url_member,the_header,room_name):
	roomId = room_id
	if roomId != "":
		member = {"roomId":roomId,"personEmail":MEMBEREMAIL, "isModerator": False}
		resp = requests.post(url_member, json=member, headers=the_header)
		print("Member " + MEMBEREMAIL + " has been added successfully!")
	else:
		print("Room " + room_name + " is not exist ....")


def postMsg(room_id,url_message,the_header,room_name,message):
	roomId = room_id
	if roomId != "":
		message_json = {"roomId":roomId,"text":message}
		resp = requests.post(url_message, json=message_json, headers=the_header)
		print()
		print("Message\"", message, "\"has been sent successfullly!")
	else:
		print("Room " + room_name + " is not exist ....")


if __name__ == '__main__':
	header=setHeaders()
	roomId = createRoom(URL_ROOM,header,ROOM_NAME) 
	addMembers(roomId,URL_MEMBER,header,ROOM_NAME)
	postMsg(roomId,URL_MESSAGE,header,ROOM_NAME,MESSAGE)

