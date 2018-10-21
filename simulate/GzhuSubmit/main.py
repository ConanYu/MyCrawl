import time
import json
from selenium.webdriver.support.ui import Select
import os
import sys
sys.path.append(os.path.dirname(__file__) + r'\..')
import SimuateAPI

def operator_login(kw):
    # url: http://172.22.27.1/
    global robot
    robot.find_element_by_xpath('//*[@id="login"]').click()
    robot.find_element_by_xpath('//*[@id="login_username"]').send_keys(kw['username'])
    robot.find_element_by_xpath('//*[@id="login_password"]').send_keys(kw['password'])
    robot.find_element_by_xpath('//*[@id="login_submit"]').click()

def operator_submit(kw):
    # url: http://172.22.27.1/submit
    global robot
    robot.find_element_by_xpath('//*[@id="pid"]').send_keys(kw['problem'])
    Select(robot.find_element_by_xpath('//*[@id="lang"]')).select_by_value(kw['lang'])
    robot.find_element_by_xpath('//*[@id="code"]').send_keys(kw['code'])
    robot.find_element_by_xpath('//*[@id="submit"]').click()


if __name__ == '__main__':
    SimuateAPI.chPathToThis(__file__)
    data = SimuateAPI.getData(__file__)
    robot = SimuateAPI.load()
    SimuateAPI.todo(robot, 'http://172.22.27.1', operator_login, username=data['username'], password=data['password'])
    time.sleep(0.2)
    SimuateAPI.todo(robot, 'http://172.22.27.1/submit', operator_submit, problem=data['problem'], lang=data['lang'], code=data['code'])
