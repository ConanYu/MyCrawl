import requests
from selenium import webdriver
robot = None

def todo(url, operator, **kw):
    global robot
    robot.get(url)
    operator(kw)

def load(command_executor=None, session_id=None):
    if command_executor is None or session_id is None:
        robot = webdriver.Chrome(executable_path=r'D:\Desktop\chromedriver.exe')
    else:
        robot = ReuseChrome(command_executor, session_id)
    with open('last.log', 'w') as dump_file:
        dump_file.write('robot.command_executor: ' + robot.command_executor._url + '\nrobot.session_id: ' + robot.session_id)
