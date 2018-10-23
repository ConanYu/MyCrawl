"""
Author: ConanYu
"""

robot = None

# --------------------------------------------------------------------------------------------
# 作用： 重用webdriver
# 用法： robot = ReuseChrome(command_executor, session_id)
import selenium
from selenium import webdriver
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

import time

# --------------------------------------------------------------------------------------------
# 作用：返回一个webdriver对象，若有command_executor和session_id时重用webdriver
# 需要重用时： robot = load(command_executor, session_id)
# 不需要重用时： robot = load()

def load(command_executor=None, session_id=None):
    global robot
    if command_executor is None or session_id is None:
        robot = webdriver.Chrome(executable_path=r'D:\Desktop\chromedriver.exe') # webdriver's path
    else:
        robot = ReuseChrome(command_executor, session_id)
    with open('last.log', 'a') as dump_file:
        dump_file.write('time: ' + str(time.time()) + '\nrobot.command_executor: ' + robot.command_executor._url + '\nrobot.session_id: ' + robot.session_id + '\n\n')
    return robot

# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# 作用：使webdriver转到某个url中

def toUrl(url):
    global robot
    time.sleep(0.1)
    robot.get(url)

# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# 作用：执行某些操作

from selenium.webdriver.support.ui import Select

def todo(xpath, operator, *args):
    def getElementByXpath(path):
        return 'document.evaluate(\'' + path + '\', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'
    
    global robot
    if 'select_by_value' == operator:
        eval('Select(robot.find_element_by_xpath(\'' + xpath + '\')).select_by_value(' + ', '.join(('args[' + str(e) + ']') for e in range(len(args))) + ')')
    elif 'send_keys' == operator:
        robot.execute_script(getElementByXpath(xpath) + r'.value = `' + args[0] + r'`')
    else:
        eval('robot.find_element_by_xpath(\'' + xpath + '\').' + operator + '(' + ', '.join(('args[' + str(e) + ']') for e in range(len(args))) + ')')

# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# 作用：使工作目录与本文件目录相同
# 用法：chPathToThis(__file__)
import os
def chPathToThis(f=None):
    f = __file__ if f is None else f
    os.chdir(os.path.dirname(f))

# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# 读取data.json
import json
def getData(f):
    with open(f, 'r') as read_file:
        data = json.load(read_file)
    return data

# --------------------------------------------------------------------------------------------
# robot.page_source 获取源码
