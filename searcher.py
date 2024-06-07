import requests, subprocess
import nmap

f = open("log.log", "w")

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



url = "https://www.mmnt.ru/ftp-sites"

nmScan = nmap.PortScanner()

r = requests.get(url)

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




for ip in ips:
	s = ""
	s += ("-------===================-----------" + "\n")
	s += (ip + "\n")
	"""
	s = subprocess.getoutput(f"docker run -it --rm --name rustscan rustscan/rustscan:2.1.1 -a {ip}")
	
	print(s)
	if f"Open {ip}:21" in s:
		print("ftp port is opened")
	if f"Open {ip}:80" in s:
		print("http port is opened")
	"""
	
	sc = nmScan.scan(ip, ports="21,80", arguments="-sS -A")
	ftp = sc['scan'][ip]['tcp'][21]
	http = sc['scan'][ip]['tcp'][80]
	
	vuln_info_http = ""
	vuln_info_ftp = ""
	
	if http['state'] == "open":
		s += ("try this http" + "\n")
		
		if http['product'] != "":
			vuln_info_http = http['product'] + " " + http['version']
		else:
			vuln_info_http = ""
			
	if ftp['state'] == "open":
		s += ("try to find some files" + "\n")
		
		if ftp['product'] != "":
			vuln_info_ftp = ftp['product'] + " " + ftp['version']
		else:
			vuln_info_ftp = ""
	
	# -- CHECK VULN
	s += ("===========" + "\n")
	
	s += ("http vulns" + "\n")
	if vuln_info_http != "":
		s += (subprocess.getoutput("searchsploit " + vuln_info_http) + "\n")
	else:
		s += ("Nothing" + "\n")
	
	s += ("===========" + "\n")
	
	s += ("===========" + "\n")
	
	s += ("ftp vulns" + "\n")
	if vuln_info_ftp != "":
		s += (subprocess.getoutput("searchsploit " + vuln_info_ftp) + "\n")
	else:
		s += ("Nothing" + "\n")
	
	s += ("===========" + "\n")
	# -- ECND CHECK VULN
	
	s += ("full scan" + "\n")
	
	s += print_scan(ip, nmScan[ip])
	
	s += ("\n\n" + "\n")
	s += ("-------===================-----------" + "\n")
	print(s)
	
	f.write(s)

f.close()
