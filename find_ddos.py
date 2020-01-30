#!/usr/bin/python
# -*- coding: utf-8 -*-
import dpkt
import optparse
import socket
THRESH = 1000

result =''
def findDownload(pcap):
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            tcp = ip.data
            http = dpkt.http.Request(tcp.data)
            if http.method == 'GET':
                uri = http.uri.lower()
                if '.zip' in uri and 'loic' in uri:
                    result+='[!] ' + src + ' Downloaded LOIC,'
        except:
            pass


def findHivemind(pcap):
    global result
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            dport = tcp.dport
            sport = tcp.sport
            if dport == 6667:
                if '!lazor' in tcp.data.lower():
                    result+='[!] DDoS Hivemind issued by: '+src+','
                    result+='[+] Target CMD: ' + tcp.data+','
            if sport == 6667:
                if '!lazor' in tcp.data.lower():
                    result+='[!] DDoS Hivemind issued to: '+src
                    result+=',[+] Target CMD: ' + tcp.data
        except:
            pass


def findAttack(pcap):
    pktCount = {}
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            tcp = ip.data
            if dport == 80:
                stream = src + ':' + dst
                if pktCount.has_key(stream):
                    pktCount[stream] = pktCount[stream] + 1
                else:
                    pktCount[stream] = 1
        except:
            pass

    for stream in pktCount:
        pktsSent = pktCount[stream]
        if pktsSent > THRESH:
            src = stream.split(':')[0]
            dst = stream.split(':')[1]
            result+=',[+] '+src+' attacked '+dst+' with ' \
                + str(pktsSent) + ' pkts.'


def main(pcapFile):
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    findDownload(pcap)
    findHivemind(pcap)
    findAttack(pcap)
    return result


if __name__ == '__main__':
    main()