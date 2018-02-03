#!/usr/bin/env python3

import requests
import json
import os
import os.path
import warnings
from config import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from requests.auth import HTTPBasicAuth  # for Basic Auth
from requests_toolbelt import MultipartEncoder
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

CMX_AUTH = HTTPBasicAuth(CMX_USER, CMX_PASSW)

try:
    import mysql.connector as mysql
except ImportError:
    import pymysql as mysql


def get_client_list():
	url = CMX_URL + '/api/location/v2/clients'
	header = {'content-type': 'application/json', 'accept': 'application/json'}
	response = requests.get(url, headers=header, auth=CMX_AUTH, verify=False)
	client_list = response.json()
#    print(json.dumps(client_list, indent=2))

	return(client_list)


def get_ap_list():
	url = CMX_URL + '/api/config/v1/aps'
	header = {'content-type': 'application/json', 'accept': 'application/json'}
	response = requests.get(url, headers=header, auth=CMX_AUTH, verify=False)
	ap_list = response.json()
 #   print(json.dumps(ap_list, indent=2))

	return(ap_list)

def connect_mysql(mysqluser,mysqlpassword,mysqlip):
    """
    Connect to the MySQL database
    :param args: command line arguments
    :return: tuple of c, cnx
    """
    # Create the MySQL database
    cnx = mysql.connect(user=mysqluser,
                        password=mysqlpassword,
                        host=mysqlip)

    c = cnx.cursor()

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        c.execute('CREATE DATABASE IF NOT EXISTS cmx;')
        cnx.commit()
    c.execute('USE cmx;')

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        c.execute('DROP TABLE IF EXISTS cmx_tbl1')
        cnx.commit()

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        c.execute('''CREATE TABLE IF NOT EXISTS cmx_client (
                         client_mac CHAR(100) NOT NULL,
                         campus    CHAR(100) NOT NULL,
                         building  CHAR(100) NOT NULL,
                         zone      CHAR(100) NOT NULL,
                         sub_zone  CHAR(100) NOT NULL,
                         map_x     CHAR(100) NOT NULL,
                         map_y     CHAR(100) NOT NULL,
                         map_z     CHAR(100) NOT NULL,
                         controller    CHAR(100) NOT NULL,
                         current_locate_date  CHAR(100) NOT NULL,
                         current_locate_time  CHAR(100) NOT NULL,
                         first_located_date   CHAR(100) NOT NULL,
                         first_located_time   CHAR(100) NOT NULL,
                         last_located_date    CHAR(100) NOT NULL,
                         last_located_time    CHAR(100) NOT NULL,
                         max_rssi   CHAR(100) NOT NULL,
                         geo_lat    CHAR(100) NOT NULL,
                         geo_long   CHAR(100) NOT NULL,
                         client_ip  CHAR(100) NOT NULL,
                         ssid    CHAR(100) NOT NULL,
                         userName    CHAR(100) NOT NULL,
                         ap_radio_map CHAR(100) NOT NULL,
                         status CHAR(100) NOT NULL,
                         manufacturer CHAR(100) NOT NULL,
                         guest_user CHAR(100) NOT NULL);''')
        cnx.commit()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        c.execute('''CREATE TABLE IF NOT EXISTS cmx_ap (
                         zone    CHAR(100) NOT NULL,
                         client_mac       CHAR(100) NOT NULL,
                         ap_mac CHAR(100) NOT NULL);''')
        cnx.commit()
    return c, cnx

def main():
	"""
	data construction
	"""
	client_list = get_client_list()
	for client in client_list:
		client_mac=client['macAddress']
		campus=client["mapInfo"]["mapHierarchyString"].split(">")[0]
		building=client["mapInfo"]["mapHierarchyString"].split(">")[1]
		zone=client["mapInfo"]["mapHierarchyString"].split(">")[2]
		map_len=len(client["mapInfo"]["mapHierarchyString"].split(">"))
		if map_len == 4:
			sub_zone=client["mapInfo"]["mapHierarchyString"].split(">")[3]
		map_x=client["mapCoordinate"]["x"]
		map_y=client["mapCoordinate"]["y"]
		map_z=client["mapCoordinate"]["z"]
		controller=client["detectingControllers"]
		current_locate_date=client["statistics"]["currentServerTime"].split("T")[0]
		current_locate_time=client["statistics"]["currentServerTime"].split("T")[1]
		first_located_date=client["statistics"]["firstLocatedTime"].split("T")[0]
		first_located_time=client["statistics"]["firstLocatedTime"].split("T")[1]
		last_located_date=client["statistics"]["lastLocatedTime"].split("T")[0]
		last_located_time=client["statistics"]["lastLocatedTime"].split("T")[1]
		max_rssi=client["statistics"]["maxDetectedRssi"]["rssi"]
		geo_lat=client["geoCoordinate"]["latitude"]
		geo_long=client["geoCoordinate"]["longitude"]
		client_ip=client["ipAddress"][0]
		ssid=client["ssId"]
		userName=client["userName"]
		ap_radio_map=client["ssId"]
		status=client["dot11Status"]
		manufacturer=client["manufacturer"]
		guest_user=client["guestUser"]
		print("client_mac:", client_mac)
		print("campus:", campus)
		print("building:", building)
		print("zone:", zone)
		print("sub_zone:", sub_zone)
		print("map_x:", map_x)
		print("map_y:", map_y)
		print("map_z:", map_z)
		print("controller:", controller)
		print("current_locate_time:", current_locate_date)
		print("current_locate_time:", current_locate_time)
		print("first_located_date:", first_located_date)
		print("first_located_time:", first_located_time)
		print("last_located_date:", last_located_date)
		print("last_located_time:", last_located_time)
		print("max_rssi:", max_rssi)
		print("geo_lat:", geo_lat)
		print("geo_long:", geo_long)
		print("client_ip:", client_ip)
		print("ssid:", ssid)
		print("userName:", userName)
		print("ap_radio_map:", ap_radio_map)
		print("status:", status)
		print("manufacturer:", manufacturer)
		print("guest_user:", guest_user)
		print("")
		print("====================")

		c, cnx = connect_mysql(MYSQLUSER,MYSQLPASSWORD,MYSQLIP)

		sql_data = (client_mac, campus, building, zone, sub_zone, map_x, map_y, map_z, controller, current_locate_date, current_locate_time, first_located_date, first_located_time, last_located_date, last_located_time, max_rssi, geo_lat, geo_long, client_ip, ssid, userName, ap_radio_map, status, manufacturer, guest_user)
		c.execute("""INSERT INTO cmx_client (client_mac, campus, building, zone, sub_zone, map_x, map_y, map_z, controller, current_locate_date, current_locate_time, first_located_date, first_located_time, last_located_date, last_located_time, max_rssi, geo_lat, geo_long, client_ip, ssid, userName, ap_radio_map, 
		status, manufacturer, guest_user) VALUES ('%s', '%s', '%s', '%s' , '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % sql_data)
		cnx.commit() 



if __name__ == '__main__':
	main()
