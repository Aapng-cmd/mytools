import requests, time
import argparse


parser = argparse.ArgumentParser(description='Search ips from specific pattern')
parser.add_argument('-f', '--file', type=str, help='log file to save', required=True)
args = parser.parse_args()


with open(args.file, "w") as f:
	s = ""


	for i in range(1, 1000):
		try:
			print("Trying http://school" + str(i) + ".ru", end="\t")
			f.write("Trying http://school" + str(i) + ".ru\t")
			r = requests.get("http://school" + str(i) + ".ru", timeout=2)
			if r.ok:
				
				if ('https://school' + str(i) + ".ru") in r.url:
					print("Check this out: ", "http://school" + str(i) + ".ru\tssl")
					f.write("Check this out: http://school" + str(i) + ".ru\tssl\n")
				elif "http://domains.domainname.ru/" not in r.text and 'Find out the price!' not in r.text and "aviasales" not in r.text:
					print("Check this out: ", "http://school" + str(i) + ".ru")
					f.write("Check this out: http://school" + str(i) + ".ru\n")
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
			
