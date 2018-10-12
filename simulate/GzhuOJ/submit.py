import os
import time
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import Select
robot = webdriver.Chrome(executable_path=r'D:\Desktop\CTF\chromedriver.exe')
session = requests.Session()
submit_data = {'Problem': '1000', 'Language': 2, 'Code': ''}
# head

def write(name, data, path=None):
    PATH = os.path.abspath(os.path.dirname(__file__))
    with open(PATH + '\\' + name, 'w', encoding='utf-8', newline='') as f:
        f.write(data)

def operator_login():
    global robot
    robot.find_element_by_xpath('//*[@id="login"]').click()
    robot.find_element_by_xpath('//*[@id="login_username"]').send_keys('Your Username')
    robot.find_element_by_xpath('//*[@id="login_password"]').send_keys('Your Password')
    robot.find_element_by_xpath('//*[@id="login_submit"]').click()

def operator_submit():
    global robot, submit_data
    robot.find_element_by_xpath('//*[@id="pid"]').send_keys(submit_data['Problem'])
    Select(robot.find_element_by_xpath('//*[@id="lang"]')).select_by_value('2')
    robot.find_element_by_xpath('//*[@id="code"]').send_keys(submit_data['Code'])
    robot.find_element_by_xpath('//*[@id="submit"]').click()

def todo(url, operator):
    global robot, session
    robot.get(url)
    operator()
    cookies = robot.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

submit_data['Code'] = r'''
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
    todo('http://172.22.27.1/', operator_login)
    for i in range(5):
        todo('http://172.22.27.1/submit', operator_submit)
        time.sleep(0.5) # 太快了，防卡壳
