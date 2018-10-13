import requests
from selenium import webdriver
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
