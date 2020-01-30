
import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)

result =''
def connScan(tgtHost, tgtPort):
    try:
        global result
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        screenLock.acquire()
        result+='[+] %d/tcp open' % tgtPort+','
        result+='[+] ' + str(results)+','
    except:
        screenLock.acquire()
        result+='[-] %d/tcp closed' % tgtPort+','
    finally:
        screenLock.release()
        connSkt.close()


def portScan(tgtHost, tgtPorts):
    global result
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        result+='\n[+] Scan Results for:' + tgtName[0]+','
    except:
        result+='\n[+] Scan Results for:' + tgtIP+','

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main(tgtHost,tgtPorts):
    int(tgtPorts)

    if (tgtHost == 'None') | (tgtPorts[0] == 'None'):
        result+="you enter nothing"
        return result

    portScan(tgtHost, tgtPorts)
    return result

if __name__ == '__main__':
    main()
