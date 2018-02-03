import requests
import json
import datetime
import re

requests.packages.urllib3.disable_warnings()

url = "https://198.18.129.100/api/v1/network-device"

def get_token():
	url = "https://198.18.129.100/api/v1/ticket"
	payload = {"username":"admin","password":"C1sco12345"}

	header = {
    	'content-type': "application/json",
    	}

	response = requests.post(url,data=json.dumps(payload), headers=header, verify=False)
	resp = response.json()

	return resp["response"]["serviceTicket"]


def get_device_id(token,url):
	headers = {
    	'content-type': "application/json",
    	'x-auth-token': token
    	}

	response = requests.request("GET", url, headers=headers, verify=False)
	resp = response.json()
#	print(resp)
	for item in resp['response']:
		if item['role'] == 'ACCESS' and not item['family'] == 'Unified AP':
			return item['id']


def get_config(token, url, device_id):
    api_call = "/" + device_id + "/config"

    #Header information
    headers = {"X-AUTH-TOKEN" : token}

    # Combine URL, API call variables
    url += api_call

    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    response = response.json()

	#Find the hostname in the response body and save it to a hostname variable
    hostname = re.findall('hostname\s(.+?)\s', response['response'])[0]

	#Create a date_time variable which will hold current time
    date_time = datetime.datetime.now()

	#Create a variable which will hold the hostname combined with the date and time
    #The format will be hostname_year_month_day_hour.minute.second
    file_name = hostname + '_' + str(date_time.year) + '_' + str(date_time.month) + '_' + \
               str(date_time.day) + '_' + str(date_time.hour) + '.' + str(date_time.minute) + \
                '.' + str(date_time.second)

    file = open(file_name+'.txt', 'w')

	#Write response body to the file
    file.write(response['response'])

	#Close the file when writing is complete
    file.close()


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


if __name__ == '__main__':
	token = get_token()
	device_id = get_device_id(token,url)
	print(device_id)
	get_config(token, url, device_id)
