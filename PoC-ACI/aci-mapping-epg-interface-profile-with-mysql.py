#!/usr/bin/env python
"""
1. get data from ACI and import to mysql database 
2. generate html file epg-port-mappping.html under directory html
Script require apache and mysql server
Written by: Marco Huang
"""

import sys
import re
import json
import warnings
import acitoolkit.acitoolkit as aci


try:
    import mysql.connector as mysql
except ImportError:
    import pymysql as mysql

def connect_mysql(args):
    """
    Connect to the MySQL database
    :param args: command line arguments
    :return: tuple of c, cnx
    """
    # Create the MySQL database
    cnx = mysql.connect(user=args.mysqllogin,
                        password=args.mysqlpassword,
                        host=args.mysqlip)

    c = cnx.cursor()

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        c.execute('CREATE DATABASE IF NOT EXISTS apic;')
        cnx.commit()
    c.execute('USE apic;')

    with warnings.catch_warnings():
	warnings.simplefilter('ignore')
	c.execute('DROP TABLE IF EXISTS epgport')
	cnx.commit()

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        c.execute('''CREATE TABLE IF NOT EXISTS epgport (
                         tenant    CHAR(100) NOT NULL,
                         app       CHAR(100) NOT NULL,
                         epg       CHAR(100) NOT NULL,
                         name      CHAR(100) NOT NULL,
                         intprof   CHAR(100) NOT NULL,
                         interface CHAR(100) NOT NULL);''')
        cnx.commit()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        c.execute('''CREATE TABLE IF NOT EXISTS intfpolgrp (
                         name    CHAR(100) NOT NULL,
                         intprof       CHAR(100) NOT NULL,
                         interface CHAR(100) NOT NULL);''')
        cnx.commit()
    return c, cnx

data = []

def print_port(length, name, leaf_name, path1, path2, path1_1, path2_1, port1, port2, tenant, app, epg, leaf, intgrp_name):
    tenant = "<td>" + tenant + "</td>"
    app = "<td>" + app + "</td>"
    epg = "<td>" + epg + "</td>"
    name = "<td>" + name + "</td>"
    leaf_name = "<td>" + leaf_name + "</td>"
    path1 = "<td>" + path1 + "</td>"
    path1_1 = "<td>" + path1_1 + "</td>"
    path2 = "<td>" + path2 + "</td>"
    path2_1 = "<td>" + path2_1 + "</td>"
    intgrp_name = "<td>" + intgrp_name + "</td>"


    if length == 15 and port1 == port2:
        if path1 == intgrp_name:
            data.append((tenant, app, epg, name, leaf_name, path1, "", ""))
            data.append((tenant, app, epg, name, leaf_name, path2, "", ""))
    elif length == 15 and port1 != port2:
        if path1 == intgrp_name:
            data.append((tenant, app, epg, name, leaf_name, path1, "", ""))
        if path1_1 == intgrp_name:
            data.append((tenant, app, epg, name, leaf_name, path1_1, "", ""))
        if path2 == intgrp_name:
            data.append((tenant, app, epg, name, leaf_name, path2, "", ""))
        if path2_1 == intgrp_name:
            data.append((tenant, app, epg, name, leaf_name, path2_1, "", ""))
    elif length == 11 and port1 != port2:
        if path1 == intgrp_name:
            data.append((tenant, app, epg, name, leaf_name, path1, "", ""))
        if path2 == intgrp_name:
            data.append((tenant, app, epg, name, leaf_name, path2, "", ""))
    elif path1 == intgrp_name:
        data.append((tenant, app, epg, name, leaf_name, path1, "", ""))

def main():
    # Take login credentials from the command line if provided
    # Otherwise, take them from your environment variables file ~/.profile
    description = 'EPG mapping with port.'
    creds = aci.Credentials('apic', description)
    creds = aci.Credentials(qualifier=('apic', 'mysql'), description=description)
    args = creds.get()

    # Login to APIC
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        sys.exit(0)

    c, cnx = connect_mysql(args)

    resp_blk = session.get('/api/node/class/infraAccPortP.json?query-target=subtree&target-subtree-class=infraPortBlk')
    resp_epg_static_port = session.get('/api/mo/uni/tn-Corporate.json?query-target=subtree&target-subtree-class=fvRsPathAtt')
    
    intpolgrp_blk = json.loads(resp_blk.text)['imdata']
    epg_stat = json.loads(resp_epg_static_port.text)['imdata']

    for epg_po in epg_stat:
        dn_epg = epg_po['fvRsPathAtt']['attributes']['dn']
        tenant = dn_epg.split('/')[1].split('tn-')[1]
        app = dn_epg.split('/')[2]
        epg = dn_epg.split('/')[3]
        intf = re.split(r'\[|\]', dn_epg)[2]
        leaf = dn_epg.split('/')[6].split('paths-')[1]
        intgrp_name = leaf + "/" + intf
        for polgrp in intpolgrp_blk:
            dn = polgrp['infraPortBlk']['attributes']['dn']
            leaf_name = dn.split('/')[2].split('accportprof-')[1]
            name = dn.split('/')[3].split('-typ-range')[0].split('hports-')[1]
            fromCard = polgrp['infraPortBlk']['attributes']['fromCard']
            fromPort = polgrp['infraPortBlk']['attributes']['fromPort']
            toCard = polgrp['infraPortBlk']['attributes']['toCard']
            toPort = polgrp['infraPortBlk']['attributes']['toPort']
            port1 = " eth" + fromCard + "/" + fromPort
            port2 = " eth" + toCard + "/" + toPort
            length = len(leaf_name)



            if length == 15:
                fex1 = leaf_name.split('-')[0]
                fex2 = leaf_name.split('-')[1]
                path1 = fex1 + "/eth" + fromCard + "/" + fromPort
                path2 = fex2 + "/eth" + toCard + "/" + toPort
                path1_1 = fex1 + "/eth" + toCard + "/" + toPort
                path2_1 = fex2 + "/eth" + fromCard + "/" + fromPort
                if path1 == intgrp_name:
                    int_name = port1 + " " + port2 
                    sql_data = (tenant, app, epg, name, leaf_name, int_name)
                    c.execute("""INSERT INTO epgport (tenant,
                                app, epg, name, intprof, interface) VALUES ('%s', '%s', '%s', '%s' , '%s', '%s')""" % sql_data)
                    cnx.commit() 
               
                print_port(length, name, leaf_name, path1, path2, path1_1, path2_1, port1, port2, tenant, app, epg, leaf, intgrp_name)
            elif length == 11:
                fex1 = leaf_name.split('-')[0]
                path1 = fex1 + "/eth" + fromCard + "/" + fromPort
                if path1 == intgrp_name:
                    int_name = port1 + " " + port2 
                    sql_data = (tenant, app, epg, name, leaf_name, int_name)
                    c.execute("""INSERT INTO epgport (tenant,
                                app, epg, name, intprof, interface) VALUES ('%s', '%s', '%s', '%s' , '%s', '%s')""" % sql_data)
                    cnx.commit() 

                print_port(length, name, leaf_name, path1, path2, path1_1, path2_1, port1, port2, tenant, app, epg, leaf, intgrp_name)
            else:
                if path1 == intgrp_name:
                    int_name = port1 + " " + port2 
                    sql_data = (tenant, app, epg, name, leaf_name, int_name)
                    c.execute("""INSERT INTO epgport (tenant,
                                app, epg, name, intprof, interface) VALUES ('%s', '%s', '%s', '%s' , '%s', '%s')""" % sql_data)
                    cnx.commit() 
               
                print_port(length, name, leaf_name, path1, path2, path1_1, path2_1, port1, port2, tenant, app, epg, leaf, intgrp_name)


    template = "{0:15} {1:20} {2:33} {3:25} {4:20} {5:15}"
    print("<html><head><style>")
    print("table {border-collapse: collapse;width: 100%;}")
    print("th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;}")
    print("tr:hover{background-color:#f5f5f5}")
    print("</style></head>")
    print("<h2>APIC EPG to Physical port mapping table</h2>")
    print("<p>Table is generated 5AM daily.</p>")
    print("<table><tr>")
    print(template.format("<th>Tenant         </th>", "<th>AppProfile          </th>", "<th>EPG                              </th>", "<th>Interface Group          </th>", "<th>Interface Profile   </th>", "<th>Port           </th>"))
    print("</tr>")
    print("<tr>")
    print(template.format("<th>---------------</th>", "<th>--------------------</th>", "<th>---------------------------------</th>", "<th>-------------------------</th>", "<th>--------------------</th>", "<th>---------------</th>"))
    print("</tr>")
    for rec in data:
        print("<tr>")
        print(template.format(*rec))
        print("</tr>")
    print("</table></html>")


if __name__ == '__main__':
    main()
