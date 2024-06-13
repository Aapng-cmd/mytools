#!/usr/bin/python

import requests
import argparse
import re
import os, subprocess
import time, random
from fake_useragent import UserAgent


def search_links(page):
    links = list(filter((lambda x: ("href=\"" in x or "src=\"" in x) and x[0] != "#" and x != "/" and "android://" not in x and "mailto" not in x and "tel" not in x and "+" not in x and "skype" not in x and "twiter" not in x and not (".ru" in x or ".us" in x or ".en" in x) and "javascript:void(0)" not in x), re.split("[\n<>]", page.text)))
    
    for i, el in enumerate(links):
        el = re.split("['\" ]", el)
        try:
            if "src=" in el:
                el = el[(el.index("src=") + 1)]
            elif "video-src=" in el:
                el = el[el.index("video-src=") + 1]
            else:
                el = el[(el.index("href=") + 1)]
        except ValueError:
            pass
        finally:
            links[i] = el
    return links
    

def filter_links(links):
    exter, inter = set(), set()
    ans = [exter, inter]
    for link in links:
        if "http" in link or "www" in link:
            exter.add(link)
        else:
            print(link)
            inter.add(link) if len(link) != 0 and link[0] != "#" and link != "/" and link != "." else None
    
    return ans


def dumping(links: list, url, directory="/home/kali/tmp/site", file_links=set()):
    os.mkdir(directory) if not os.path.exists(directory) else None
    subprocess.getoutput(f"wget --header='User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11' {url} -O {directory}/index.php")
    
    if isinstance(links, set): links = list(links)
    if len(links) == 0: return
    print("--------------")
    for link in sorted(links):
        if link[0] != "/": link = "/" + link
        path = (link.split('/')[1:] if "/" in link else [link])
        for el in path:
            if el == "": path.pop(path.index(el))
        
        d_path = path[:-1] + [re.split("[?#]", path[-1])[0]]
        cur_path = ""
        d_cur_path = ""
        
        
        
        print(link, path, d_path)
        if len(d_path) != 1:
        
            if ".js" in path[-1] or ".css" in path[-1] or re.findall(".*h*", path[-1])[1:]:
                file_links.add("/".join(path))
        
            for i in range(len(d_path)):
                cur_path += "/" + path[i]
                d_cur_path += "/" + d_path[i]
                if i != len(path) - 1:
                    os.mkdir(directory + cur_path) if not os.path.exists(directory + cur_path) else None
                else:
                    # print(cur_path, path[i])
                    if not os.path.exists(directory + cur_path):
                        # print(f"wget --header='User-Agent: {UserAgent().random}' {url + cur_path} -O {directory}{d_cur_path}")
                        subprocess.getoutput(f"wget --header='User-Agent: {UserAgent().random}' {url + cur_path} -O {directory}{d_cur_path}")
                        time.sleep(_ := random.randint(3, 10))
                        print("Slept for", _, "and path is", cur_path)
                    
        else:
            subprocess.getoutput(f"wget {url + cur_path} -O {directory}{cur_path}")
            time.sleep(_ := random.randint(3, 10))
            print("Slept for", _, "and path is", cur_path)
    
    for i in range(len(file_links)):
        print("starting copying new file!!!")
        # print(file_links)
        if list(file_links)[i] == list(links)[0]:
            pass
        else:
            q = filter_links(search_links(requests.get(url + list(file_links)[i])))
            print(q[1])
            dumping(q[1], url, directory, file_links)
        

parser = argparse.ArgumentParser()
parser.add_argument('--url', '-u', help="url to work with")
parser.add_argument('--directory', '-d', help="directory to save where", default="/home/kali/tmp/site")
args = parser.parse_args()
url = args.url
directory = args.directory

r = requests.get(url)
links = filter_links(search_links(r))
q_links = list(links)[1]
print(list(links)[1])
dumping(q_links, url, directory)

