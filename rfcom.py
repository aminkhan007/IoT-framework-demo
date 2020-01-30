
from bluetooth import *

result =''
def rfcommcon(addr, port):
    global result
    sock = BluetoothSocket(RFCOMM)
    try:
        sock.connect((addr, port))
        result+='[+] RFCOMM Port ' + str(port) + ' open,'
        sock.close()
    except Exception as e:
        result+='[-] RFCOMM Port ' + str(port) + ' closed,'
    return result
def main():
    for port in range(1, 30):
        result += rfcommcon('8C:85:90:A7:86:FE', port)
    return result