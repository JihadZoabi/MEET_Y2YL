from bs4 import BeautifulSoup
import requests
import string

def cleaner(s):
    txt = string.ascii_letters + string.digits + string.whitespace + "#"
    ans = ""
    s = str(s)
    delete = False
    for x in s:
        if x == "<":
            delete = True
        if x == ">":
            delete = False
        if not delete and x != ">" and x in txt:
            ans += str(x)
    return ans


def get_info(hex):
    url = "https://encycolorpedia.com/" + hex
    url2 = "https://www.colorhexa.com/" + hex

    html_text = requests.get(url).text
    html_text2 = requests.get(url2).text

    soup = BeautifulSoup(html_text, "lxml")
    soup2 = BeautifulSoup(html_text2, "lxml")

    prgs = soup.find_all('p')
    divs = soup2.find_all("div", {"class": "color-description"})
    c_info = []

    for x in prgs:
        if "shade" in str(x):
            #return cleaner(x).split('.')[0] + '\n' + cleaner(divs).split('.')[0]
            c_info.append(cleaner(divs).split('.')[0])
            c_info.append((cleaner(x).split('.')[0]).split('In')[0])
            return c_info