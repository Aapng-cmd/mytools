import requests, re
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
from webdriver_manager.chrome import ChromeDriverManager

import time


def is_ip_port(string):
    pattern = r"(([0-9]{1,3}\.){3}[0-9]{1,3}):[0-9]{1,4}"
    match = re.search(pattern, string)
    if match:
        return True
    else:
        return False




def get_proxies():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=selenium.webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)
    s = ""
    driver.get("https://spys.one/free-proxy-list/")

    page_text = driver.page_source
    flag_1 = False
    flag_2 = False
    # print(page_text)
    soup = BeautifulSoup(page_text, 'html.parser')
    for tr in soup.find_all("tr"):
        if "HTTP" in tr.text:
            ac = tr.text[1:tr.text.index("HTTP")]
            if is_ip_port(ac):
                s += "http\t" + ac.replace(":", " ") + "\n"
    # Close the webdriver
    driver.quit()
    return s


while True:
    print("New proxy incoming")
    proxies = get_proxies()
    # with open("/etc/proxychains4.conf.bak", "r", encoding="utf-8") as file:
    #     backup = file.read()
    # with open("/etc/proxychains4.conf", "w") as file:
    #     file.write(backup)
    # with open("/etc/proxychains4.conf", "a") as file:
    #     file.write(proxies)
    print(proxies)
    time.sleep(60 * 2)
