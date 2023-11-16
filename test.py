import requests, subprocess, re


url = 'https://spys.one/en/'

r = subprocess.getoutput(f"curl {url}")

t = r.split('\n')
o = 1


for i, el in enumerate(t):
    q = re.split("[><]", el)
    for j, l in enumerate(q):
        if 'spy14' in l and q[j - 1] == "&nbsp;":
            print()
            ip = q[j + 1]
            # print(ip)
            method = q[j + 13]
            # print(method)
            
            # print("\n".join([q[j + 1 + p] for p in range(10)]))
            
            print(ip, method)
            
            print()
