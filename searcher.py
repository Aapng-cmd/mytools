#!/usr/bin/python3
import requests, subprocess
import nmap
import argparse
import socket


parser = argparse.ArgumentParser(description='Search ips from specific dump site for testing')
parser.add_argument('-f', '--file', type=str, help='log file to save', required=True)
args = parser.parse_args()


f = open(args.file, "w")

def rec_pr_dict(dic, level=0):
	s = ""
	for el in dic:
		if str(type(dic[el])) == "<class 'dict'>":
			s += ("\t" * level + str(el) + ":" + "\n")
			s += rec_pr_dict(dic[el], level + 1)
		else:
			s += ("\t" * level + el + ":" + dic[el].replace('\n', '\n' + '\t' * level) + "\n")
	return s

def print_scan(ip, sc):
	s = ""
	s += ('Host : %s (%s)' % (ip, sc.hostname()) + "\n")
	s += ('State : %s' % sc.state() + "\n")
	for proto in sc.all_protocols():
	    s += ('----------' + "\n")
	    s += ('Protocol : %s' % proto + "\n")
	    s += rec_pr_dict(sc[proto])
	return s  



# url = "https://www.mmnt.ru/ftp-sites"

nmScan = nmap.PortScanner()

# r = requests.get(url)
"""
ips = []

for el in r.text.split("\n"):
	try:
		el = el.split('title="')
		el = el[1].split('"')[0]
		# print(el[0])
		q = el.split(".")
		if list(map(int, q)):
			ips.append(el)
	except:
		pass

"""

with open("/home/kali/tmp/hosts", "r") as fa:
	ips = fa.read().split("\n")[:-1]
	for i in range(len(ips)):
		ips[i] = ips[i][7:]


ports = ["80", "3306"]

for ip in ips:
	s = ""
	s += ("-------===================-----------" + "\n")
	s += (socket.gethostbyname(ip) + " " + ip + "\n")
	ip = socket.gethostbyname(ip)
	
	"""
	s = subprocess.getoutput(f"docker run -it --rm --name rustscan rustscan/rustscan:2.1.1 -a {ip}")
	
	print(s)
	if f"Open {ip}:21" in s:
		print("ftp port is opened")
	if f"Open {ip}:80" in s:
		print("http port is opened")
	"""
	sc = nmScan.scan(ip, ports=",".join(ports), arguments="-sS -A")
	
	vuln_info_http = ""
	vuln_info_ftp = ""
	
	for port in ports:
		h = sc['scan'][ip]['tcp'][int(port)]
		if h['state'] == 'open':
			s += ("try this " + port + "\n")
			if h['product'] != "":
				vih = h['product'] + " " + h['version']
			else:
				vih = ""
			
	
		# -- CHECK VULN
			s += ("===========" + "\n")
			s += vih + " reason: " + h['extrainfo'] + "\n"
			s += (port + " vulns" + "\n")
			if vuln_info_http != "":
				s += (subprocess.getoutput("searchsploit " + vih) + "\n")
			else:
				s += ("Nothing" + "\n")
			
			s += ("===========" + "\n")
			
			# -- ECND CHECK VULN
		
		# s += ("full scan" + "\n")
		
		# s += print_scan(ip, nmScan[ip])
		


	s += ("\n\n" + "\n")
	s += ("-------===================-----------" + "\n")
	print(s)
	
	f.write(s)

f.close()
