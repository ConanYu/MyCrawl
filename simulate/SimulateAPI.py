"""
Author: ConanYu
"""

# --------------------------------------------------------------------------------------------
# 作用： 重用webdriver
# 用法： robot = ReuseChrome(command_executor, session_id)
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



# --------------------------------------------------------------------------------------------
# 作用：返回一个webdriver对象，若有command_executor和session_id时重用webdriver
# 需要重用时： robot = load(command_executor, session_id)
# 不需要重用时： robot = load()

def load(command_executor=None, session_id=None):
    robot = None
    if command_executor is None or session_id is None:
        robot = webdriver.Chrome(executable_path=r'D:\Desktop\chromedriver.exe') # webdriver's path
    else:
        robot = ReuseChrome(command_executor, session_id)
    with open('last.log', 'w') as dump_file:
        dump_file.write('robot.command_executor: ' + robot.command_executor._url + '\nrobot.session_id: ' + robot.session_id)
    return robot

# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# 作用：使webdriver转到某个url并执行某些操作
# 用法：operator指的是某个操作函数，kw里面是操作所需要的数据
def todo(robot, url, operator, **kw):
    robot.get(url)
    operator(kw)

"""
operator函数示例：
无论有无数据输入输出都要有一个参数
def operator_makefriend(kw):
    global robot
    # url = 'http://codeforces.com/profile/用户名'
    robot.find_element_by_xpath('//*[@id="pageContent"]/div[2]/div[5]/div[2]/div/h1/img[@class="addFriend friendStar" or class="friendStar addFriend"]').click()
"""

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
def getData():
    chPathToThis(__file__)
    with open('data.json', 'r') as read_file:
        data = json.load(read_file)
    return data

# --------------------------------------------------------------------------------------------
