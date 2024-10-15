#!/usr/bin/env python3

import subprocess
import argparse

parser = argparse.ArgumentParser(description='Work with sites, which were got from scanner.py')
parser.add_argument('-f', '--file', type=str, help='log file from read', required=True)
args = parser.parse_args()



def run_joomscan(url, options=None):
    command = ["/root/joomlavs/joomlavs.rb", "-u", url]
    if options:
        command.extend(options)

    output = subprocess.check_output(command).decode()
    return output


def wtf(fn, string):
    with open(fn, "a") as f:
        f.write(string + "\n")


with open(args.file, "r") as f:
    hosts = []
    for el in f.read().split("\n")[:-1]:
        if "Check this out" in el:
            hosts.append(el.split()[1])

for host in hosts:
    # print(host, "host")
    output = run_joomscan(host, ["-q", "--hide-banner", '--no-colour', '--follow-redirection'])
    if "Joomla" not in output:
        continue
    else:
        output = output.split("\n")
        for el in output:
            if "Joomla" in el:
                version = el.split()[3]
                print(version,el)
                wtf("vuln.hosts", host + "\t" + version + "\t" + "(" + el[:-1] + ")")
                #output = subprocess.check_output(["searchsploit", "joomla", version]).decode()


# let's go further

with open ('vuln.hosts', "r") as f:
    data = f.read().split("\n")[:-1]

d = []
_ = {}

for el in data:
    ip, ver, info = el.split("\t")
    if not _.get(ip):
        if ver[0] == "v": ver = ver[1:]
        _[ip] = ver
        d.append([ip, ver])


d = sorted(d, key=lambda x: x[1])

for i in range(len(d)):
    d[i] = "\t".join(d[i])

with open("vuln.hosts", "w") as f:
    f.write("\n".join(d))
