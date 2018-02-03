# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems

#!/usr/bin/env python3


import requests
import json
import os
import os.path

from requests.packages.urllib3.exceptions import InsecureRequestWarning

from requests.auth import HTTPBasicAuth  # for Basic Auth
from requests_toolbelt import MultipartEncoder
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

CMX_URL = 'https://cmxlocationsandbox.cisco.com'  # CMX Sandbox
CMX_USER = 'learning'
CMX_PASSW = 'learning'

CMX_AUTH = HTTPBasicAuth(CMX_USER, CMX_PASSW)
auth = "ZmVjMGY5ZmYtZmVhMi00MTc5LWJmYjgtMTNiOTc1MmFhZjdiMWEyNGViNzQtYmJl"
url_room = "https://api.ciscospark.com/v1/rooms"
url_message = "https://api.ciscospark.com/v1/messages"
room_name = "Topic - CMX"
filetype    = 'image/png'

def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """

    pretty_output = (json.dumps(json_data, indent=4, separators=(' , ', ' : ')))
    return(pretty_output)

def all_client_number():
    """
    This function will find out how many wireless clients are visible in the environment
    REST API call to CMX - /api/location/v2/clients/count
    :param
    :return: The total number of clients, associated and not associated with the APs
    """

    url = CMX_URL + '/api/location/v2/clients/count'
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, auth=CMX_AUTH, verify=False)
    response_json = response.json()
    clients_number = response_json['count']
    return clients_number


def get_cmx_map(campus, building, floor, file):
    """
    The function will get the floor map for the floor with the name {floor},
    located in the specified building and campus.
    REST API call to CMX - 'api/config/v1/maps/image/' + campus/building/floor
    :param campus: campus name
    :param building: building name
    :param floor: floor name
    :param file: file name to save the image to
    :return: save the floor map image
    """
    assign2_msg = []
    url = CMX_URL + '/api/config/v1/maps/image/' + campus + '/' + building + '/' + floor

    header = {'content-type': 'application/json'}
    response = requests.get(url, headers=header, auth=CMX_AUTH, verify=False)
#    print('\nThe floor map request url is: ', url)
#    print('Request status code is: ', response.status_code)

    assign2_msg.append('\nThe floor map request url is: ' + url)
    assign2_msg.append('Request status code is: ' + str(response.status_code))

    if response.status_code == 200:  # validate if the request was successful
        assign2_msg.append('Assignment 2 completed')
    else:
        assign2_msg.append('Assignment 2 not completed, please try again')

    # open a file to save the image to

    image_file = open(file, 'wb')
    image_file.write(response.content)  # save the content of the request as it comes back as an image and not JSON
    image_file.close()
    return('\n'.join(assign2_msg))


def get_cmx_ap_info(campus, building, floor, ap_name):
    """
    The function will get the x/y coordinates of the AP with the name {ap_name} located on
    the floor with the name {floor}, located in the specified building and campus
    :param campus: campus name
    :param building: building name
    :param floor: floor name
    :param ap_name: AP name
    :return: x/y coordinates, from the top left corner of the image
    """

    url = CMX_URL + '/api/config/v1/maps/info/' + campus + '/' + building + '/' + floor
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, auth=CMX_AUTH, verify=False)
    aps_list = response.json()['accessPoints']
    for ap in aps_list:
        if ap['name'] == ap_name:
            ap_x = ap['mapCoordinates']['x']
            ap_y = ap['mapCoordinates']['y']
    return ap_x, ap_y

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
            print("Posting message to room:",room_name)
            break   
    return(roomId)


def postMsg(room_id,url_message,the_header,room_name,message,file):
    roomId = room_id

    if roomId != "":
        message_json={'roomId': roomId, 'text': '\n'.join(message),'files': (file, open(file,'rb'), filetype)}
        mencoder = MultipartEncoder(fields=message_json)
        accessToken_hdr = 'Bearer ' + auth
        the_header = {'Authorization': accessToken_hdr, 'Content-Type': mencoder.content_type} 
        resp = requests.post(url_message, data=mencoder, headers=the_header)


"""
 4.
    Write code that will print the MAC addresses for the clients associated with the AP with the name {T1-3}

    Tip: Re-use code provided to you part of the Assignment 1, write another API call,
    and use the pprint() function to print nicely.

    Bonus: can you print the number of associated clients to the AP {T1-3}
    
    # ...... insert your code here
    #print('Assignment 2 completed')
    #print('\nCongratulations! You completed all assignments. Please upload to the CMX Module Spark Room to get credit')
"""
# insert your functions for Assignment 4 here
def get_clients(radioMAC):
    data = []
    total = 0
    url = CMX_URL + '/api/location/v2/clients'
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, auth=CMX_AUTH, verify=False)
    client_list = response.json()
    count = len(client_list)
    num = 0
    while num < count: 
 #       apMAC = client_list[num]["statistics"]["maxDetectedRssi"]["apMacAddress"]
        apMAC = client_list[num]["apMacAddress"]
        if apMAC == radioMAC:
            clientMAC = client_list[num]["macAddress"]
            data.append({"AP_MAC_ADDRESS": apMAC, "CLIENT_MAC_ADDRESS": clientMAC})
            total = total + 1
        num = num + 1

 #   client_ap_list = pprint(data)
    return(data, total)


def find_ap_radioMAC(ap_name):
    radioMAC = ""
    url = CMX_URL + '/api/config/v1/aps'
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, auth=CMX_AUTH, verify=False)
    ap_list = response.json()
    count = len(ap_list)
    num = 0
    while num < count: 
        ap = ap_list[num]["name"]
        if ap == ap_name:
            radioMAC = ap_list[num]["radioMacAddress"]
 #           print(radioMAC)
        num = num + 1
    return(radioMAC)


def main():
    """
    This is your assignment for the CMX module. Please complete steps in sequence.

    1. The function all_client_number() will return the number of all active clients.
    Please check the function and correct the errors (tip - two errors).


    2. The function get_cmx_map(campus, building, floor, file) will save with the name {file} the CMX floor map for
    campus = 'DevNetCampus'
    building = 'DevNetBuilding'
    floor = 'DevNetZone'
    The function has one error. Please correct it to run correctly.

    Tip: The correct answer will print the Request Status Code: 200 and it will save the file image with this name
    {DevNetZoneFloorMap.png} in the same folder where you have the script.


    3. The final assignment for this module includes one error. Please correct to run correctly.

    Upload the output to the Module Spark Room and the file with the image from the previous step.

    """
    message = []
    # 1.

    clients_number = all_client_number()
 #   print('\nNumber of all active clients: ', clients_number)
 #   print('Assignment 1 completed')
    message.append('\nNumber of all active clients: ' + str(clients_number))
    message.append('Assignment 1 completed')

    # 2.

    campus = 'DevNetCampus'
    building = 'DevNetBuilding'
    floor = 'DevNetZone'
    file = 'DevNetZoneFloorMap_Marco.png'

    cmx_map = get_cmx_map(campus, building, floor, file)
    message.append(str(cmx_map))

    # 3.

    ap_name = 'T1-3'

    ap_x_coordinate = get_cmx_ap_info(campus, building, floor, ap_name)[0]
    ap_y_coordinate = get_cmx_ap_info(campus, building, floor, ap_name)[1]


#    print('\nThe AP with the name ', ap_name, ' coordinates are x/y: ', ap_x_coordinate, ap_y_coordinate)
#    print('Assignment 3 completed')
    message.append('\nThe AP with the name ' + ap_name + ' coordinates are x/y: ' + str(ap_x_coordinate) + ' ' + str(ap_y_coordinate))
    message.append('Assignment 3 completed')

    radioMAC = find_ap_radioMAC(ap_name)
    data_output = get_clients(radioMAC)[0]
    total = get_clients(radioMAC)[1]
    message.append('\n' + pprint(data_output))
    message.append('\nTotal ' + str(total) + ' clients associated to the AP')
    message.append('\nAssignment 4 completed')

 # Post to Spark room    
    header = setHeaders()
    roomId = findRoom(url_room,header,room_name)
    postMsg(roomId,url_message,header,room_name,message,file)




if __name__ == '__main__':
        main()

