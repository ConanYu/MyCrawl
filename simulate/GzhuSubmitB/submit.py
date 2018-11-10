import time
import os
import sys
sys.path.append(os.path.dirname(__file__) + r'\..')
import SimuateAPI

def login(**kw):
    SimuateAPI.toUrl('http://172.22.27.1')
    SimuateAPI.todo('//*[@id="login"]', 'click')
    SimuateAPI.todo('//*[@id="login_username"]', 'send_keys', kw['username'])
    SimuateAPI.todo('//*[@id="login_password"]', 'send_keys', kw['password'])
    SimuateAPI.todo('//*[@id="login_submit"]', 'click')

def submit(**kw):
    SimuateAPI.toUrl('http://172.22.27.1/submit')
    SimuateAPI.todo('//*[@id="pid"]', 'send_keys', kw['problem'])
    SimuateAPI.todo('//*[@id="lang"]', 'select_by_value', kw['lang'])
    SimuateAPI.todo('//*[@id="code"]', 'send_keys', kw['code'])
    SimuateAPI.todo('//*[@id="submit"]', 'click')

if __name__ == '__main__':
    SimuateAPI.chPathToThis(__file__)
    user = SimuateAPI.getData(os.path.dirname(__file__) + r'\data\userOfRobot.json')
    SimuateAPI.load()
    login(username=user['username'], password=user['password'])
    list_dirs = os.walk(os.path.dirname(__file__) + r'\data\code')
    for root, dirs, files in list_dirs:
        for f in files:
            data = SimuateAPI.getData(os.path.join(root, f))
            code = data['code'].replace('\\', '\\\\')
            submit(problem=data['problem'], lang=data['lang'], code=code)
            time.sleep(0.1)
