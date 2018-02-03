import json
import sys
import requests

#MISSION: FILL IN THE REQUESTED DETAILS
ACCESS_TOKEN 	= "ZmVjMGY5ZmYtZmVhMi00MTc5LWJmYjgtMTNiOTc1MmFhZjdiMWEyNGViNzQtYmJl" #Replace None with your access token. Shroud with quotes.
ROOM_NAME		= "DevNet_vCC_Team9_Camp1Day3_Mission" #Replace None with the name of the room to be created. Shroud with quotes.
YOUR_MESSAGE 	= "Hello World RestAPI call Spark!" #Replace None with the message that you will post to the room. Shroud with quotes.


#sets the header to be used for authentication and data format to be sent.
def setHeaders():         
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
	return (spark_header)


#check if spark room already exists.  If so return the room id
def findRoom(the_header,room_name):
	roomId=room_name
	uri = 'https://api.ciscospark.com/v1/rooms'
	resp = requests.get(uri, headers=the_header)
	resp = resp.json()
	for room in resp["items"]:
		if room["title"] == room_name:
			print()
			print("findRoom JSON: ", room)	
			print("MISSION: findRoom: REPLACE None WITH CODE THAT PARSES JSON TO ASSIGN ROOM ID VALUE TO VARIABLE roomId")
			roomId=room["id"]
			print()
			print("Room name exist with room ID", roomId)
			break	
	return(roomId)

# checks if room already exists and if true returns that room ID. If not creates a new room and returns the room id.
def createRoom(the_header,room_name):
	roomId=findRoom(the_header,room_name)
	if roomId==room_name:
		roomInfo = {"title":room_name}
		uri = 'https://api.ciscospark.com/v1/rooms'
		resp = requests.post(uri, json=roomInfo, headers=the_header)
		var = resp.json()		
		print()
		print("createRoom JSON: ", var)	
		print("MISSION: createRoom: REPLACE None WITH CODE THAT PARSES JSON TO ASSIGN ROOM ID VALUE TO VARIABLE roomId.")		
		roomId=var["id"]
	return(roomId)
	
# adds a new member to the room.  Member e-mail is test@test.com
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


if __name__ == '__main__':
	if ACCESS_TOKEN==None or ROOM_NAME==None or YOUR_MESSAGE==None:
		sys.exit("Please check that variables ACCESS_TOKEN, ROOM_NAME and YOUR_MESSAGE have values assigned.")
	header=setHeaders()
	#passing the ROOM_NAME for the room to be created
	room_id=createRoom(header,ROOM_NAME) 
	if room_id == None:
		sys.exit("Please check that functions findRoom and createRoom return the room ID value.")
	#passing roomId to members function here to add member to the room.
	addMembers(header,room_id)   
	#passing roomId to message function here to Post Message to a room.
	postMsg(header,room_id,YOUR_MESSAGE)
	print()
	print("MISSION: ADD FUNCTION CALL getRoomInfo(header,room_id)")	
	getRoomInfo(header,room_id)
	print()
