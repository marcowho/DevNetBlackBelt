"""
Enter the room "Leaderboard" that is created in the Coding Camp Spark Team space. 
Read the latest position of your team from the Leaderboard messages posted
In your team space - "DevNet_vCC_TeamX" - mention the position of your team and total points.
"""

import json
import sys
import requests

ACCESS_TOKEN = "ZmVjMGY5ZmYtZmVhMi00MTc5LWJmYjgtMTNiOTc1MmFhZjdiMWEyNGViNzQtYmJl" 
URL_ROOM = 'https://api.ciscospark.com/v1/rooms'
URL_MESSAGE = 'https://api.ciscospark.com/v1/messages'
ROOM_NAME = "Leaderboard" 
TEAM_NAME = "DevNet_vCC_Team9"
SEARCH_FOR = "APJ Leaderboard Rank"
HOSTER_EMAIL = "leaderboard@sparkbot.io"

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
			print("Group:",room_name)
#			print(roomId)
			break	
	return(roomId)

def getListMsg(url_room,url_message,the_header,room_name):
	roomId = findRoom(url_room,the_header,room_name)
	msg = ""
	if roomId != "":
		roomId_json = {"roomId":roomId}
#		print(roomId_json)
		url_message = "https://api.ciscospark.com/v1/messages?" + "roomId=" + roomId
#		print(url_message)
		resp = requests.get(url_message, headers=the_header)
		resp = resp.json()
		for messages in resp["items"]:
			if messages["personEmail"] == HOSTER_EMAIL and SEARCH_FOR in messages["text"]:
#				print(messages["html"])
				msg = messages["html"]
				break
	else:
		print("Room " + room_name + " is not exist ....")
	return(msg)


if __name__ == '__main__':
	header=setHeaders()
	msg=getListMsg(URL_ROOM,URL_MESSAGE,header,ROOM_NAME)
	count = 0
	while True:
		if TEAM_NAME in msg.split('<br><br>')[count]:
			last_msg=(msg.split('<br><br>')[count])
			rank = last_msg.split('<code>')[0].split('#')[1]
			total = last_msg.split('</code>')[5].split('-')[1].strip()
			break
		count = count + 1
	print("Team Name:", TEAM_NAME)
	print("Rank:", rank)
	print("Total:", total)

