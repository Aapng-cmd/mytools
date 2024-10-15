#!/usr/bin/env python3
import requests, time
import argparse


parser = argparse.ArgumentParser(description='Search ips from specific pattern')
parser.add_argument('-f', '--file', type=str, help='log file to save', required=True)
args = parser.parse_args()

PREFIX = "gymn"


with open(args.file, "w") as f:
	s = ""


	for i in range(1, 1000):
		try:
			print(f"Trying http://{PREFIX}" + str(i) + ".ru", end="\t")
			f.write(f"Trying http://{PREFIX}" + str(i) + ".ru\t")
			r = requests.get(f"http://{PREFIX}" + str(i) + ".ru", timeout=2)
			if r.ok:
				if "gos" in r.url:
					print(f"GOS. RUN! http://{PREFIX}" + str(i) + ".ru")
					f.write(f"GOS. RUN! http://{PREFIX}" + str(i) + ".ru\n")
				if (f'https://{PREFIX}' + str(i) + ".ru") in r.url:
					print(f"Check this out: ", f"https://{PREFIX}" + str(i) + ".ru\tssl")
					f.write(f"Check this out: https://{PREFIX}" + str(i) + ".ru\tssl\n")
				elif "http://domains.domainname.ru/" not in r.text and 'Find out the price!' not in r.text and "aviasales" not in r.text:
					print(f"Check this out: ", f"http://{PREFIX}" + str(i) + ".ru")
					f.write(f"Check this out: http://{PREFIX}" + str(i) + ".ru\n")
				else:
					print("For sale")
					f.write("For sale\n")
				
			else:
				print("Nah")
				f.write("Nah\n")
			time.sleep(0.2)
		except requests.exceptions.ConnectionError:
			print("No route to host")
			f.write("No route to host\n")
		except requests.exceptions.ReadTimeout:
			print("Cannot read")
			f.write("Cannot read\n")
			
