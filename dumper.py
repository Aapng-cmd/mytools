#!/usr/bin/python

import requests
import argparse
import re
import os
import time, random
from fake_useragent import UserAgent
import mimetypes

def is_file(url):
    response = requests.head(url)
    return response.headers.get('Content-Type') != 'text/html'

import re

def extract_links(page):
    """
    Extracts links from a given webpage.

    Args:
        page (object): The webpage object containing the text to search for links.

    Returns:
        list: A list of extracted links.
    """

    # Define a regular expression pattern to match links
    link_pattern = re.compile(r'(?:href|src|video-src)=["\'](.*?)["\']')

    # Split the page text into individual lines
    lines = re.split(r'[\n<>]', page.text)

    # Filter out unwanted links
    links = []
    for line in lines:
        if line.startswith(('#', '/')) or 'android://' in line or 'mailto' in line or 'tel' in line or '+' in line or 'skype' in line or 'twiter' in line or 'javascript:void(0)' in line:
            continue
        if '.ru' in line or '.us' in line or '.en' in line:
            continue

        # Extract links using the regular expression pattern
        matches = link_pattern.findall(line)
        links.extend(matches)

    return links

def filter_links(links):
    exter, inter = set(), set()
    ans = [exter, inter]
    for link in links:
        if "http" in link or "www" in link:
            exter.add(link)
        else:
            print(link)
            try:
                inter.add(link) if len(link) != 0 and link[
                    0] != "#" and link != "/" and link != "." and "data:image" not in link and "javascript:" not in link else None
            except TypeError:
                pass

    return ans


def dump_to_file(url, headers, path):
    if headers != None:
        headers = {k: v for k, v in [headers.split(": ", 1)]}
        r = requests.get(url, headers=headers)
        if r.ok:
            content_type = r.headers.get('Content-Type')
            print(url, content_type)
            if content_type and 'text' in content_type:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(r.text)
            else:
                with open(path, "wb") as f:
                    f.write(r.content)

def dumping(links: list, url, directory="site", file_links=set()):
    os.mkdir(directory) if not os.path.exists(directory) else None

    dump_to_file(url, "User-Agent: Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11", directory + "/index.php")

    if isinstance(links, set): links = list(links)
    if len(links) == 0: return
    print("--------------")
    for link in sorted(links):
        if link[0] != "/": link = "/" + link
        if is_file(url + link):
            if "/" in link:
                if "." not in link.split("/")[-1]:
                    link += "/index.php"
            else:
                link += "/index.php"
        path = (link.split('/')[1:] if "/" in link else [link])
        for el in path:
            if el == "": path.pop(path.index(el))

        d_path = path[:-1] + [re.split("[?#]", path[-1])[0]]
        cur_path = ""
        d_cur_path = ""

        print(link, path, d_path)
        if len(d_path) != 1:

            if mimetypes.guess_type(path[-1])[0] is not None:
                file_links.add("/".join(path))

            for i in range(len(d_path)):
                cur_path += "/" + path[i]
                d_cur_path += "/" + d_path[i]
                if i != len(path) - 1:
                    os.mkdir(directory + cur_path) if not os.path.exists(directory + cur_path) else None
                else:
                    # print(cur_path, path[i])
                    if not os.path.exists(directory + cur_path):
                        dump_to_file(url + cur_path, f"User-Agent: {UserAgent().random}", directory + d_cur_path)
                        time.sleep(_ := random.randint(3, 10))
                        print("Slept for", _, "and path is", cur_path)

        else:
            dump_to_file(url + cur_path, None, directory + cur_path)
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
parser.add_argument('--directory', '-d', help="directory to save where", default="site")
args = parser.parse_args()
url = args.url
directory = args.directory

r = requests.get(url)
links = filter_links(search_links(r))
q_links = list(links)[1]
print(list(links)[1])
dumping(q_links, url, directory)
