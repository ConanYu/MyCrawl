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
    data = SimuateAPI.getData(os.path.dirname(__file__) + r'\data.json')
    SimuateAPI.load(data['command_executor'], data['session_id'])
    login(username=data['username'], password=data['password'])
    submit(problem=data['problem'], lang=data['lang'], code=data['code'])
