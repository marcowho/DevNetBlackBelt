#!/usr/bin/env python
# edit config of device

from ncclient import manager
import sys
import xml.dom.minidom
import os, sys
# the variables below assume the user is leveraging the
# network programmability lab and accessing csr1000v
# use the IP address or hostname of your CSR1000V device
#HOST = 'adam-csr'
HOST="198.18.133.218"
# use the NETCONF port for your CSR1000V device
#PORT = 830
PORT=2022
# use the user credentials for your CSR1000V device
USER = 'admin'
PASS = 'C1sco12345'

# create a main() method
def get_config(xml_filter):
    """
    Main method that retrieves the interfaces from config via NETCONF.
    """
    ### ASSIGNMENT 1:  This code comes from one of the ealier labs
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        with open(xml_filter) as f:
            return(m.get_config('running', f.read()))

    ### ASSIGMENT 2
def edit_config(xml_config):
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        with open(xml_config) as f:
            return(m.edit_config(config=f.read(), target='running'))

def update_xml_config(int_name):
    stext = "<name></name>"
    rtext = "<name>" + int_name + "</name>"
    input = open("ip_filter.xml")
    output = open("ip_filter_int_name.xml","w")

    for s in input.readlines(  ):
        output.write(s.replace(stext, rtext))
    output.close(  )
    input.close(  )


def main(argv):
    """
    Simple main method calling our function.
    """
    """
    try:
        config_file = argv[1]
    except IndexError as k:
        print ("ERROR - No file provided - Usage: %s filename" % argv[0] )
        sys.exit(1)
    """
    resp = str(input("Get or Edit config. Please enter [get/edit]: "))
    while resp == "get" or resp == "edit":
        if resp == "edit":
            config_file = str(input("Please enter XML config file name: "))
            response = edit_config(config_file)
            break
        else:
            int_name = str(input("Please enter interface name [Gi1/Gi2/all]: "))
            if int_name == "Gi1" or int_name == "Gi2":
                if int_name == "Gi1":
                    int_name = "GigabitEthernet1"
                    update_xml_config(int_name)
                    config_file = "ip_filter_int_name.xml"
                elif int_name == "Gi2":
                    int_name = "GigabitEthernet2"
                    update_xml_config(int_name)
                    config_file = "ip_filter_int_name.xml"
 #               config_file = str(input("Please enter XML config file name: "))
                response = get_config(config_file)
                break
            else:
                config_file = "ip_filter.xml"
                response = get_config(config_file)
                break

    xml_response = xml.dom.minidom.parseString(response.xml)

    print(xml_response.toprettyxml())


if __name__ == '__main__':
    sys.exit(main(sys.argv))