import os
import time
from getpass import getpass
import requests
from lxml import etree
import selenium
from selenium import webdriver
robot, session = None, None

def todo(url, operator, **kw):
    global robot, session
    if robot is None or session is None:
        robot = webdriver.Chrome(executable_path=r'D:\Desktop\chromedriver.exe')
        session = requests.Session()
        robot.implicitly_wait(2.0)
    robot.get(url)
    operator(kw)
    cookies = robot.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

def operator_login(kw):
    global robot
    # url = 'http://codeforces.com/enter'
    robot.find_element_by_xpath('//*[@id="handleOrEmail"]').send_keys(kw['username'])
    robot.find_element_by_xpath('//*[@id="password"]').send_keys(kw['password'])
    robot.find_element_by_xpath('//*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input').click()

def operator_makefriend(kw):
    global robot
    # url = 'http://codeforces.com/profile/用户名'
    robot.find_element_by_xpath('//*[@id="pageContent"]/div[2]/div[5]/div[2]/div/h1/img[@class="addFriend friendStar" or class="friendStar addFriend"]').click()
    
def makefriend(username, password, friends):
    if isinstance(friends, str):
        friends = [friends]
    todo('http://codeforces.com/enter', operator_login, username=username, password=password)
    time.sleep(4.0)
    for i in friends:
        try:
            todo('http://codeforces.com/profile/' + i, operator_makefriend)
        except selenium.common.exceptions.NoSuchElementException:
            print(i + ' 添加失败。')

if __name__ == '__main__':
    username = input('输入用户名； ')
    password = getpass('输入密码： ')
    n = int(input('你要添加几个朋友？ '))
    lis = []
    for i in range(1, n + 1):
        lis.append(input('输入第%d个朋友的用户名： ' % i))
    makefriend(username, password, lis)
