#!/usr/bin/env python
# edit config of device

from ncclient import manager
import sys
import xml.dom.minidom

# the variables below assume the user is leveraging the
# network programmability lab and accessing csr1000v
# use the IP address or hostname of your CSR1000V device
#HOST = 'adam-csr'
HOST="198.18.133.218"
# use the NETCONF port for your CSR1000V device
PORT = 830
PORT=2022
# use the user credentials for your CSR1000V device
USER = 'admin'
PASS = 'C1sco12345'

# create a main() method
def get_config(xml_filter):
    """
    Main method that retrieves the interfaces from config via NETCONF.
    """
    ### ASSIGNMENT:  This code comes from one of the ealier labs
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        with open(xml_filter) as f:
            return(m.get_config('running', f.read()))
 #           return(m.get(f.read()))


def main(argv):
    """
    Simple main method calling our function.
    """
    try:
        config_file = argv[1]
    except IndexError as k:
        print ("ERROR - No file provided - Usage: %s filename" % argv[0] )
        sys.exit(1)
    response = get_config(config_file)
    xml_response = xml.dom.minidom.parseString(response.xml)

    print(xml_response.toprettyxml())


if __name__ == '__main__':
    sys.exit(main(sys.argv))