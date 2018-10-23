import selenium
import time
import sys
import os
import sys
THIS_PATH = os.path.dirname(__file__)
sys.path.append(THIS_PATH + r'\..')
import SimuateAPI
robot = None

def login(**kw):
    SimuateAPI.toUrl('http://codeforces.com/enter')
    try:
        SimuateAPI.todo('//*[@id="handleOrEmail"]', 'send_keys', kw['username'])
        SimuateAPI.todo('//*[@id="password"]', 'send_keys', kw['password'])
        SimuateAPI.todo('//*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input', 'click')
    except selenium.common.exceptions.NoSuchElementException:
        print('登录失败，可能已经登陆。')

def makefriend(**kw):
    # url = 'http://codeforces.com/profile/用户名'
    SimuateAPI.toUrl(kw['url'])
    SimuateAPI.todo('//*[@id="pageContent"]/div[2]/div[5]/div[2]/div/h1/img[@class="addFriend friendStar" or class="friendStar addFriend"]', 'click')

if __name__ == '__main__':
    SimuateAPI.chPathToThis(__file__)
    data = SimuateAPI.getData(THIS_PATH + r'\data.json')
    SimuateAPI.load(data['command_executor'], data['session_id'])
    login(username=data['username'], password=data['password'])
    time.sleep(4.0)
    for i in data['friends']:
        try:
            makefriend(url=('http://codeforces.com/profile/' + i))
        except selenium.common.exceptions.NoSuchElementException:
            print(i + ' 添加失败。')
