from xml.etree import ElementTree
import urllib
from website.settings import NMAP_XML_URL

#todo cache 1-5 minuts
def get_online_mac_addesses():
    try:
        response = urllib.urlopen(NMAP_XML_URL)


        xml = response.read()
        tree = ElementTree.fromstring(xml)

        mac_addresses = []

        for host in tree.findall('host'):
            state = host.find('status').attrib.get('state')
            if state == 'up':
                for address in host.findall('address'):
                    if address.attrib.get('addrtype') == 'mac':
                        mac = address.attrib.get('addr')
                        mac_addresses.append(mac)
    except :
        mac_addresses = []
    return mac_addresses
