from xml.etree import ElementTree
import urllib2
from website.settings import NMAP_XML_URL

class network:
    def __init__(self):
        pass

    def get_online_mac_addesses(self):
        response = urllib2.urlopen(NMAP_XML_URL)
        xml = response.read()
        tree = ElementTree.fromstring(xml)

        mac_addresses = []

        for host in tree.iter('host'):
            state = host.find('status').attrib.get('state')
            if state == 'up':
                for address in host.findall('address'):
                    if address.attrib.get('addrtype') == 'mac':
                        mac = address.attrib.get('addr')
                        mac_addresses.append(mac)

        return mac_addresses
