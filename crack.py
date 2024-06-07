import requests, os, sys, time
from bs4 import BeautifulSoup
# from selenium import webdriver

if len(sys.argv) - 1 != 1:
    print("Not enough args")
    exit(0)
    
if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1], 'r') as f:
        data = f.read()
        data = data.replace('\n', '%0D%0A')
        f.close()
        
else:
    data = sys.argv[1]


url = "https://crackstation.net/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    # 'referer':'https://www.google.com/'
}


s = requests.Session()


r = s.get(url, headers=headers)

print(r.text)

soup = BeautifulSoup(r.text, 'html.parser')
captcha_sitekey = soup.find("div", {'class', "g-recaptcha"})["data-sitekey"]

# s.post(f"https://www.google.com/recaptcha/api2/userverify?k={captcha_sitekey}")


"""

captcha_url = "https://crackstation.net/recaptcha/api2/reload?k=6LcnNi8UAAAAALJikXrc6jwNWUm00Yjx_rHCJW7u"
cookies = {"_GRECAPTCHA": "09ALyjir-Z0ZIILCI3_ug0EUh-RGVXz8edVzmQZ__KXQGqpin6AxjU9uXPqqiExn68BWc9djA7C8Zx4LfH2s1r2JE"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'referer':'https://www.google.com/recaptcha/api2/bframe?hl=en&v=CDFvp7CXAHw7k3HxO47Gm1O9&k=6LcnNi8UAAAAALJikXrc6jwNWUm00Yjx_rHCJW7u',
    "Te": "trailers",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}
""" 
""" 
site_key = "6LcnNi8UAAAAALJikXrc6jwNWUm00Yjx_rHCJW7u"
api_key = "0fe4facebc443d4478d93eaf444098ab"
pageurl = "https://crackstation.net/recaptcha/api2/reload"
form = {"method": "userrecaptcha",
        "googlekey": site_key,
        "key": api_key, 
        "pageurl": pageurl, 
        "json": 1}
        
while True:
    response = requests.post('http://2captcha.com/in.php', data=form)
    request_id = response.json()['request']
    stat = response.json()['status']
    print(stat)
    time.sleep(3)
    if stat == 1:
        print(stat)
        print(request_id)
        exit(0)
exit(0)
# g-recaptch-response
"""





# dt = {"hashes": data, "crack": "Crack+Hashes"}

# r = requests.post(url, cookies=cookies, headers=headers)

