#!/usr/bin/env python3

import requests
import json
import os
import os.path
import pymysql as mysql
import datetime
from config import *
from requests.auth import HTTPBasicAuth 
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) 

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from requests_toolbelt import MultipartEncoder
filetype = 'application/pdf'

CMX_AUTH = HTTPBasicAuth(CMX_USER, CMX_PASSW)

ROOM_NAME       = "DevNet_vCC_Team9" 
URL_ROOM = 'https://api.ciscospark.com/v1/rooms'
URL_MESSAGE = 'https://api.ciscospark.com/v1/messages'

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

def postMsg(room_id,url_message,the_header,room_name,message,file):
    roomId = room_id
    if roomId != "": 
        message_json={'roomId': roomId, 'text': message,'files': (file, open(file,'rb'), filetype)}
        print(message_json)
        mencoder = MultipartEncoder(message_json)
        print(mencoder)
        accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
        the_header = {'Authorization': accessToken_hdr, 'Content-Type': mencoder.content_type} 
        resp = requests.post(url_message, data=mencoder, headers=the_header)
        print(resp.json())

def connect_mysql(mysqluser,mysqlpassword,mysqlip):
    """
    Connect to the MySQL database
    :return: tuple of c, cnx
    """

    cnx = mysql.connect(user=mysqluser,
                        password=mysqlpassword,
                        host=mysqlip)

    c = cnx.cursor()

    c.execute('USE cmx;')
    return c, cnx



def main():
    url = CMX_URL + '/api/location/v1/clients/count/byzone'
    header = {'content-type': 'application/json', 'accept': 'application/json'}
    response = requests.get(url, headers=header, auth=CMX_AUTH, verify=False)
    response_json = response.json()
    today=str(datetime.date.today() - datetime.timedelta(days=1))
    c, cnx = connect_mysql(MYSQLUSER,MYSQLPASSWORD,MYSQLIP)
    zonecount = len(response_json['ZoneCounts']['zoneCountList'])
    file_name = "cmx_report_" + today
    file = file_name+'.pdf'

    doc = SimpleDocTemplate(file, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
    doc.pagesize = landscape(A4)
    elements = []
    style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])

    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'

    msg = [["Date","Campus","Building","Sector","Level","Total Connection"]]

    for count in range(zonecount):
        data = []
        zonelist = response_json['ZoneCounts']['zoneCountList'][count]
        campus = zonelist['hierarchy'].split('/')[0]
        building = zonelist['hierarchy'].split('/')[1]
        zone = zonelist['hierarchy'].split('/')[2]
        sub_zone = zonelist['hierarchy'].split('/')[3]
        result=c.execute("select DISTINCT(client_mac) from cmx_client where sub_zone LIKE %s and current_locate_date LIKE %s", (sub_zone, today))
        print(",".join([today, campus, building, zone, sub_zone, str(result)]))

        data.append(today)
        data.append(campus)
        data.append(building)
        data.append(zone)
        data.append(sub_zone)
        data.append(str(result))
        print(data)
        msg.append(data)

    print(msg)
    data2 = [[Paragraph(cell, s) for cell in row] for row in msg]
    t=Table(data2)
    t.setStyle(style)
    elements.append(t)
    doc.build(elements)

    message='This is auto-generated CMX report daily at 2AM.'
    header=setHeaders()
    roomId = findRoom(URL_ROOM,header,ROOM_NAME)
    postMsg(roomId,URL_MESSAGE,header,ROOM_NAME,message,file)

if __name__ == '__main__':
	main()

