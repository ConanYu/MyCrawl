import os
import sys
import time
import json
sys.path.append(os.path.dirname(__file__) + r'\..')
import SimuateAPI
from selenium.webdriver.common.keys import Keys
from lxml import etree

idxLang = {'C': '1', 'C++': '2', 'Java': '3', 'C++11': '4', 'C#': '5', 'VB.Net': '6'}

def login(**kw):
    SimuateAPI.toUrl('http://172.22.27.1')
    SimuateAPI.todo('//*[@id="login"]', 'click')
    SimuateAPI.todo('//*[@id="login_username"]', 'send_keys', kw['username'])
    SimuateAPI.todo('//*[@id="login_password"]', 'send_keys', kw['password'])
    SimuateAPI.todo('//*[@id="login_submit"]', 'click')

def crawl(html):
    code = html.xpath('//*[@id="xbody"]//div[@class="container"]//textarea/text()')[0]
    return code.replace(u'\xa0', ' ')

def main():
    global idxLang
    SimuateAPI.load()
    data = SimuateAPI.getData(os.path.dirname(__file__) + r'\data\copyFromWhom.json')
    pros = {'1000'}
    code = dict()
    for peo in range(data['nums']):
        # getPro
        SimuateAPI.toUrl('http://172.22.27.1/user/' + data['username'][peo])
        thisPro = list(map(lambda x: x[-4:], etree.HTML(SimuateAPI.robot.page_source).xpath('//*[@id="xbody"]/fieldset/div[2]/div[3]/div[2]/a/@href')))
        # login
        login(username=data['username'][peo], password=data['password'][peo])
        # findCode
        for pro in thisPro:
            if pro in pros or os.path.exists(os.path.dirname(__file__) + '\\data\\' + pro + '.json'):
                continue
            SimuateAPI.toUrl('http://172.22.27.1/status?name=' + data['username'][peo] + '&pid=' + pro + '&result=2')
            lang = idxLang[etree.HTML(SimuateAPI.robot.page_source).xpath('//*[@id="statustable"]/tbody/tr[1]/td[7]/a/text()')[0]]
            # toSourceCode
            SimuateAPI.todo('//*[@id="statustable"]/tbody/tr[1]/td[7]/a', 'click')
            time.sleep(0.1)
            SimuateAPI.todo('//*[@id="xbody"]//div[@class="container"]//div[contains(@class, "line") and contains(@class, "number1")]', 'double_click')
            try:
                code = crawl(etree.HTML(SimuateAPI.robot.page_source))
            except IndexError:
                print('error pro ' + pro)
                continue
            this = {
                "problem": pro,
                "lang": lang,
                "code": code
            }
            with open(os.path.dirname(__file__) + '\\data\\code\\' + pro + '.json', 'w') as dump_f:
                json.dump(this, dump_f)
            pros.add(pro)
        # logout
        SimuateAPI.todo('//*[@id="logout"]', 'click')
        time.sleep(0.1)

# print(SimuateAPI.robot.page_source)

if __name__ == '__main__':
    BEG = time.clock()
    SimuateAPI.chPathToThis(__file__)
    main()
    print(time.clock() - BEG)
