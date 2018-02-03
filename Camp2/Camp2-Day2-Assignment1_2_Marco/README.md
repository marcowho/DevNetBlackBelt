# Assignment 1:
The first assignment is to create a python script that takes a filter file as an argument and returns the required configuration.

You will need to modify the script `Camp2-Day2-Assign1.py` to add a code to the function get_config(xml_filter).  
You should be able to reuse some code from an earlier Lab you did.

This script takes a filter as an argument, in my example the filter file is `ip_filter.xml`.

You will also need to write the filter to include only the name and IP address.

A sample is shown below:

```buildoutcfg
$ ./Camp2-Day2-Assign1.py ip_filter.xml 
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:15f4aa2a-7ece-4688-b763-f38bb561871d" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <data>
                <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                                <name>GigabitEthernet1</name>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                <ip>198.18.133.212</ip>
                                                <netmask>255.255.192.0</netmask>
                                        </address>
                                </ipv4>
                        </interface>
                        <interface>
                                <name>GigabitEthernet2</name>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                </interfaces>
        </data>
</rpc-reply>

```
## HINTS
- Start with the interface filter you had in the lab and add the `name` and `ipv4` attributes.
- You will need the namespace for the ipv4 container.


# Assignment 2:
This assignment will edit a configuration file to add an IP address to interface GigabitEthernet2.

The file `add_ip_gig2.xml` is an example YANG snippet to add an IP address to the interface GigabitEthernet2.  You do not need to change this file.

You need to copy the file `Camp2-Day2-Assign1.py` to  `Camp2-Day2-Assign2.py`.

Modify the script `Camp2-Day2-Assign2.py` to read and edit the configuration using a filter.  Instead of doing a "get_config" as in the previous assigment, it will need to edit the configuration.

You should only need to change one line in the file.  

It would be better to change the name of the name of the function `get_config`, to something more appropriate such as `edit_config`.

Example output shown below:
```buildoutcfg
$ ./Camp2-Day2-Assign2.py add_ip_gig2.xml 
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:04b4f285-9dd7-42ee-993c-cafe6dfd769e" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <ok/>
</rpc-reply>

```

## HINTS
- You will need to change the m.get_config call
- You will need to change the arguments to m.XXXX_config.  `target='running'` is the main difference

Run your filter program from Assignment 1 to verify the IP has changed. 

```buildoutcfg
$ ./Camp2-Day2-Assign1.py ip_filter.xml 
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:5deceaec-ea10-4f1a-a013-1a271d134dda" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <data>
                <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                                <name>GigabitEthernet1</name>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                <ip>198.18.133.212</ip>
                                                <netmask>255.255.192.0</netmask>
                                        </address>
                                </ipv4>
                        </interface>
                        <interface>
                                <name>GigabitEthernet2</name>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                <ip>10.10.10.1</ip>
                                                <netmask>255.255.192.0</netmask>
                                        </address>
                                </ipv4>
                        </interface>
                </interfaces>
        </data>
</rpc-reply>
```

## Optional

Here are some ideas to extend these examples:
- You can modify the filter to just return the interface GigabitEthernet2
- You could make the interface filter a command line option
- Ideally, you could have a single script, and have a commandline argument to indicate if an get or edit config was required.