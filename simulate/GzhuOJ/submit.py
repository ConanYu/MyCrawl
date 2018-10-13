import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
robot, session = None, None

def todo(url, operator, **kw):
    global robot, session
    if robot is None or session is None:
        robot = webdriver.Chrome(executable_path=r'D:\Desktop\chromedriver.exe')
        session = requests.Session()
    robot.get(url)
    operator(kw)
    cookies = robot.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

# ************************************************** HEAD ************************************************** #

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

CODE = r'''
#include<iostream>
using namespace std;
int main()
{
    int a, b;
    while(cin >> a >> b)
    {
        cout << (a + b) << endl;
    }
}
'''

if __name__ == '__main__':
    todo('http://172.22.27.1', operator_login, username='1706300092', password='12345679')
    for i in range(2):
        todo('http://172.22.27.1/submit', operator_submit, problem='1000', lang='2', code=CODE)
        time.sleep(0.5)
