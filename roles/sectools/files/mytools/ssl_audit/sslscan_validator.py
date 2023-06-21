''' 
INPUT:
    sslscan_out2.xml > output from sslcan tool
    weak_ciphers.lst > list of weak ciphers

OUTPUT:
    weak_ssl_version.csv > CSV file of the hosts with Weak SSL version
    weak_ssl_ciphers.csv > CSV file of the hosts with Weak Ciphers Enabled
    weak_list_discovered.lst > List of weak ciphers discovered

To generate the sslcan xml file:
sslscan --tls --no-check-certificate \
    --no-fallback --no-heartbleed  --no-heartbleed \
    --no-compression --no-groups --no-renegotiation \
    --xml="sslscan_out.xml"  --targets=targets.lst
'''
from bs4 import BeautifulSoup
import argparse
from pathlib import Path

# SSLSCANXML = "sslscan_out2.xml"
# WEAKCIPHERS = "weak_ciphers.lst"
OUTPUTFILE1 = "weak_ssl_version.csv"
OUTPUTFILE2 = "weak_ssl_ciphers.csv"
OUTPUTFILE3 = "weak_list_discovered.lst"

def loadWeakCiphers(filename):
    with open(filename) as file:
        content = file.read().splitlines()
    
    return content

def toCSV(ipdict, filename):
    header = "IP,fqdn,tls10,tls11,ssl3\n"
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        f.write(header)
        for ip,v in ipdict.items() :
            if v['tls10'] or  v['tls11'] or  v['ssl3']:
                f.write('{},{},"{}","{}","{}"\n'.format(ip, v['fqdn'], v['tls10'], v['tls11'], v['ssl3']))

def weakCipherToCSV(ipdict, filename):
    header = "IP,Port\n"
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        f.write(header)
        for ip,v in ipdict.items():
            if v['port']:
                f.write('{},"{}"\n'.format(ip, v['port']))

def getWeakSSLVersion(soup, ipdict):

    all_ssltests = soup.find_all("ssltest")
    print (f"[+] Checking if weak SSL/TLS versions are enabled")
    print(f"[+] Entries found: {len(all_ssltests)}")
    # Checking SSL/TLS Versions enabled
    for ssltest in all_ssltests:
        host = ssltest['host']
        port = ssltest['port']
        print(f"\t[+] {host}:{port}")
        all_protocols = ssltest.find_all('protocol')
        for protocol in all_protocols:
            #checking SSL version enabled
            if protocol['type'] == "ssl" and protocol['enabled'] == "1":            
                print(f"\t\t[-] {protocol['type']} {protocol['version']}")
                ipdict[host]["ssl3"].append(port)
            #checking TLS 1.0 version enabled
            elif protocol['type'] == "tls" and protocol['version'] =="1.0" and protocol['enabled'] == "1":
                    print(f"\t\t[-] {protocol['type']} {protocol['version']}")
                    ipdict[host]["tls10"].append(port)
            #checking TLS 1.1 version enabled
            elif protocol['type'] == "tls" and protocol['version'] =="1.1" and protocol['enabled'] == "1":
                    print(f"\t\t[-] {protocol['type']} {protocol['version']}")
                    ipdict[host]["tls11"].append(port)  
    
    return (ipdict)

def getWeakCiphers(soup, weak_ciphers, ipdict):
    all_ssltests = soup.find_all("ssltest")
    print (f"[+] Checking weak ciphers")
    print(f"[+] Entries found: {len(all_ssltests)}")

    weak_list = []
    for ssltest in all_ssltests:
        host = ssltest['host']
        port = ssltest['port']
        print(f"\t[+] {host}:{port}")
        # Checking Weak Ciphers
        all_ciphers = ssltest.find_all('cipher')
        for cipher in all_ciphers:            
            if cipher['cipher'] in weak_ciphers:
                print(f"\t\t[-] {cipher['sslversion']}: {cipher['cipher']}")
                if not port in ipdict[host]["port"]:
                    ipdict[host]["port"].append(port)  
                weak_list.append(cipher['cipher'])

    return (ipdict, weak_list)
    
def toFIle(filename, list):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        f.write('\n'.join(list))

if __name__ == '__main__':
    ipdict_ver = {}
    ipdict_cipher = {}
    weak_list = []



    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Positional arguments
    parser.add_argument("xml", type=str, help="XML sslscan output")
    parser.add_argument("cipherlist", type=str, help="Weak cipher list")

    # Read arguments from command line
    args = parser.parse_args()
 
    SSLSCANXML = Path(args.xml)
    WEAKCIPHERS = Path(args.cipherlist)

    # Reading sslscan xml file 
    with open(SSLSCANXML) as file:
        soup = BeautifulSoup(file, features="lxml-xml")
    
    # Creating dictionary f IPs
    for el in soup.select("[host]"):
        ipdict_ver[el['host']] = {"fqdn": "", "tls10":[], "tls11":[], "ssl3":[]}
        ipdict_cipher[el['host']] = {"port": []}

    # Parse sslscan xml data for Weak SSL Version
    result = getWeakSSLVersion(soup, ipdict_ver)
    # print(result)
    toCSV(result, OUTPUTFILE1)

    print()

    # Load weak cipher list
    weak_ciphers = loadWeakCiphers(WEAKCIPHERS)
    # Parse sslscan xml data for Weak Ciphers enabled
    result, weak_list = getWeakCiphers(soup, weak_ciphers, ipdict_cipher)
    # print(result)
    weakCipherToCSV(result,OUTPUTFILE2)
    # print(weak_list)
    toFIle(OUTPUTFILE3, weak_list)
