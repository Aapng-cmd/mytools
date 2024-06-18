#! env python3


"""
tool for search exploits with searchsploit from nrich json report
"""

import json, subprocess, sys
import argparse



def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\033[F%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')



# Create the argument parser
parser = argparse.ArgumentParser(description='Dump the contents of a JSON file.')

# Add the filename argument
parser.add_argument('--filename', '-f', help='The name of the JSON file from dump', required=True)
parser.add_argument('--output', '-o', help='The name of the JSON file to dump', default="/tmp/output.json")

# Parse the arguments
args = parser.parse_args()

# Open the filename and load the JSON data
with open(args.filename, 'r') as f:
    data = json.load(f)

js = {}


for __, target in enumerate(data):
    print_progress_bar(__ / len(data) * 100, 100, prefix="Processing...", suffix="Complete")
    for cve in target.get("vulns"):
        
        rep = subprocess.getoutput(f"searchsploit --cve {cve}")
        if "Exploit Title" in rep:
            # print(f"{cve}")
            q = rep.split("\n")[3:]
            _ = next((i for i, x in enumerate(q) if "----------------------------------------------------------------------------------" in x), None)
            q = q[:_]
            # print(target.get("hostnames"), target.get("ip"), cve, "\n".join(q))
            js[target.get("ip")] = [target.get("hostnames"), cve, q]
            # print("================")
            
print(js)

with open(args.output, 'w') as f:
    json.dump(js, f, indent=4)
