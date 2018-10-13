import os
import time
import requests
from lxml import etree
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
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
    try:
        robot.find_element_by_xpath('//*[@id="pageContent"]/div[2]/div[5]/div[2]/div/h1/img[@class="addFriend friendStar" or class="friendStar addFriend"]').click()
    except selenium.common.exceptions.NoSuchElementException:
        return

if __name__ == '__main__':
    lis = ['Caproner', 'Blogggggg', 'DumplingMew', 'ConanYu', 'Fushicho-XF', 'Canan', 'AII', 'qq897276651', 'SeeeIsAHandsomeBoy', 'Seven0x29a', 'MoogleAndChocobo', 'Se7en0x29a', 'lightyears1998', 'MoogleAndChocobo_', 'xiaokai666666', 'Huang_Shaofeng', 'JonsonBen', 'Gragon_Shao']
    # use getlist_organization
    lis += ['SemonIsAHandsomeBoy', 'Kurisuzzz', 'Archer_x', 'Markfound']

    todo('http://codeforces.com/enter', operator_login, username='Your username', password='Your password')
    time.sleep(4.0)
    for i in lis:
        todo('http://codeforces.com/profile/' + i, operator_makefriend)
