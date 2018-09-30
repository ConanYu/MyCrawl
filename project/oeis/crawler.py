import os
import requests
import random
from time import clock
from pxy import get_proxy as gpxy
from lxml import etree
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
proxy = None
check = clock()

def url_to_str(url):
    global proxy, check
    cur = clock()
    if cur - check > 300 or proxy is None:
        proxy = gpxy()
        check = cur
    html = requests.get(url, headers={'User-agent': user_agent, 'proxies': random.sample(proxy, 1)[0]})
    soup = BeautifulSoup(html.text, 'lxml')
    return soup.prettify()

def str_to_htm(s):
    return etree.HTML(s)

def isNone(htm):
    return len(htm.xpath('//tr[@bgcolor="#EEEEFF"]')) == 0

def write(path, data):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(data)

def main():
    PATH = os.path.abspath(os.path.dirname(__file__)) + '\\web\\'
    for i in range(1, 400000):
        MAJOR = 'A%06d' % i
        ADDRESS = PATH + MAJOR + '.html'
        if os.path.exists(ADDRESS):
            continue
        data = url_to_str('https://oeis.org/' + MAJOR)
        if isNone(str_to_htm(data)):
            print(MAJOR + ' failed.')
            continue
        write(ADDRESS, data)
        print(MAJOR + ' succeed.')

if __name__ == '__main__':
    main()
