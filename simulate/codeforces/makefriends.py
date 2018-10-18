import os
import time
import json
from getpass import getpass
import requests
import selenium
from selenium import webdriver
robot = None

# --------------------------------------------------------------------------------------------
# reuseChrome.py
from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException

class ReuseChrome(Remote):

    def __init__(self, command_executor, session_id):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={})

    def start_session(self, capabilities, browser_profile=None):
        # 重写start_session方法
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = False
# --------------------------------------------------------------------------------------------

def chPathToThis(f=None):
    f = __file__ if f is None else f
    os.chdir(os.path.dirname(f))

def todo(url, operator, **kw):
    global robot
    robot.get(url)
    operator(kw)

def operator_login(kw):
    global robot
    # url = 'http://codeforces.com/enter'
    try:
        robot.find_element_by_xpath('//*[@id="handleOrEmail"]').send_keys(kw['username'])
        robot.find_element_by_xpath('//*[@id="password"]').send_keys(kw['password'])
        robot.find_element_by_xpath('//*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input').click()
    except selenium.common.exceptions.NoSuchElementException:
        print('登录失败，可能已经登陆。')

def operator_makefriend(kw):
    global robot
    # url = 'http://codeforces.com/profile/用户名'
    robot.find_element_by_xpath('//*[@id="pageContent"]/div[2]/div[5]/div[2]/div/h1/img[@class="addFriend friendStar" or class="friendStar addFriend"]').click()
    
def makefriend(username, password, friends):
    todo('http://codeforces.com/enter', operator_login, username=username, password=password)
    time.sleep(4.0)
    for i in friends:
        try:
            todo('http://codeforces.com/profile/' + i, operator_makefriend)
        except selenium.common.exceptions.NoSuchElementException:
            print(i + ' 添加失败。')


if __name__ == '__main__':
    data = None
    chPathToThis()
    with open('data.json', 'r') as read_file:
        data = json.load(read_file)
    command_executor, session_id = data.get('command_executor', None), data.get('session_id', None)
    if command_executor is None or session_id is None:
        robot = webdriver.Chrome(executable_path=r'D:\Desktop\chromedriver.exe')
    else:
        robot = ReuseChrome(command_executor, session_id)
    with open('last.log', 'w') as dump_file:
        dump_file.write('robot.command_executor: ' + robot.command_executor._url + '\nrobot.session_id: ' + robot.session_id)
    makefriend(data['username'], data['password'], data['friends'])
