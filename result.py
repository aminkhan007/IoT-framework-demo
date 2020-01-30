import flask as f
from flask import Flask, request, redirect, url_for     
from flask import render_template 
from flask import jsonify,request
import Syn_flood
import sql
import sniffingicmp
import rfcom
import port_scan
import mail
import geoip
import find_ddos
import brute
import arp_poison

app = f.Flask(__name__,static_folder='static')
app.config["DEBUG"] = True

@app.route('/upload/',methods =['POST'])
@app.route('/arp_poision/',methods =['GET','POST'])
def arp_poision():
    jsonData = request.get_json()
    tip = jsonData['tip']
    gip = jsonData['gip']
    result=arp_poison.main()
    return result

@app.route('/brute_force/',methods =['GET','POST'])
def brute_force():
    jsonData = request.get_json()
    print(jsonData)
    tip = jsonData['turl']
    gip = jsonData['purl']
    return ('I am here, this is a dummy text, just to see wheter what I am trying to do works or not')



@app.route('/find_ddos/',methods =['GET','POST'])
def find_ddos():
    try:
        jsonData = request.get_json()
        fname = jsonData['file_name']
        pcap_file = open('../pcap_files/'+fname+'.pcap')
        result = find_ddos.main(fname+'.pcap')
        return result
    except Exception as e:
        return('Sorry File Not Found Please Try Again')

@app.route('/geo_ip/',methods =['GET','POST'])
def geo_ip():
    try:
        jsonData = request.get_json()
        fname = jsonData['file_name']
        pcap_file = open('../pcap_files/'+fname+'.pcap')
        result = geoip.main(pcap_file)

        return result
    except Exception as e:
        print(e)
        return('Sorry File was not found')

@app.route('/port_scan/',methods =['GET','POST'])
def port_scan():
    try:
        jsonData = request.get_json()
        host = jsonData['host']
        port = jsonData['port']
        return ('I am in port Scan')
    except Exception as e:
        print(e)
        return('Sorry File was not found')

@app.route('/rfcom/',methods =['GET','POST'])
def rfcom():
    try:

        result = rfcom.main('','')
        return result
    except Exception as e:
        print(e)
        return('Sorry File was not found')

@app.route('/mail/',methods =['GET','POST'])
def mail():
    try:
        result = mail.main_runner()
        return result
    except Exception as e:
        print(e)
        return('Sorry File was not found')

@app.route('/sniffing_icmp/',methods =['GET','POST'])
def sniffing_icmp():
    try:
        obj = sniffingicmp()
        jsonData = request.get_json()
        print(jsonData)
        host = jsonData['host']
        result = obj.main()
        return result
    except Exception as e:
        print(e)
        return('Sorry File was not found')

@app.route('/sql/',methods =['GET','POST'])
def sql():
    try:
        jsonData = request.get_json()
        url = jsonData['url']
        result = sql.start(url)
        return result
    except Exception as e:
        print(e)
        return('Sorry File was not found')

@app.route('/sin_flood/',methods =['GET','POST'])
def sin_flood():
    try:
        jsonData = request.get_json()
        src_sin = jsonData['src_sin']
        spoof = jsonData['spoof']
        tgt = jsonData['tgt']
        result = Syn_flood.main(spoof,src_sin,tgt)
        return result
    except Exception as e:
        print(e)
        return('Sorry File was not found')

@app.route('/xss1/',methods =['GET','POST'])
def xss1():
    try:
        jsonData = request.get_json()
        mthd = jsonData['mthd']
        url = jsonData['url']
        wlist = jsonData['wlist']
        print(jsonData)
        return ('I am in XSS')
    except Exception as e:
        print(e)
        return('Sorry File was not found')


if __name__ == "__main__":

    app.run()