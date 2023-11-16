import nmap, argparse

ip = '127.0.0.1'
ports = ''
Scan = nmap.PortScanner()

res = Scan.scan(ip)

print(res)
