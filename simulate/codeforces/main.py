import selenium
import time
import sys
import os
import sys
THIS_PATH = os.path.dirname(__file__)
sys.path.append(THIS_PATH + r'\..')
import SimuateAPI
robot = None

@SimuateAPI.todo
def operator_login(**kw):
    try:
        robot.find_element_by_xpath('//*[@id="handleOrEmail"]').send_keys(kw['username'])
        robot.find_element_by_xpath('//*[@id="password"]').send_keys(kw['password'])
        robot.find_element_by_xpath('//*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input').click()
    except selenium.common.exceptions.NoSuchElementException:
        print('登录失败，可能已经登陆。')

@SimuateAPI.todo
def operator_makefriend(**kw):
    # url = 'http://codeforces.com/profile/用户名'
    robot.find_element_by_xpath('//*[@id="pageContent"]/div[2]/div[5]/div[2]/div/h1/img[@class="addFriend friendStar" or class="friendStar addFriend"]').click()

if __name__ == '__main__':
    SimuateAPI.chPathToThis(__file__)
    data = SimuateAPI.getData(__file__)
    robot = SimuateAPI.load(data['command_executor'], data['session_id'])
    print(robot)
    operator_login(robot, url='http://codeforces.com/enter', username=data['username'], password=data['password'])
    time.sleep(4.0)
    for i in data['friends']:
        try:
            operator_makefriend(robot, url=('http://codeforces.com/profile/' + i))
        except selenium.common.exceptions.NoSuchElementException:
            print(i + ' 添加失败。')
