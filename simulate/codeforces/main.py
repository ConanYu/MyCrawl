import SimuateAPI
import selenium
import time

def operator_login(kw):
    # url = 'http://codeforces.com/enter'
    try:
        robot.find_element_by_xpath('//*[@id="handleOrEmail"]').send_keys(kw['username'])
        robot.find_element_by_xpath('//*[@id="password"]').send_keys(kw['password'])
        robot.find_element_by_xpath('//*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input').click()
    except selenium.common.exceptions.NoSuchElementException:
        print('登录失败，可能已经登陆。')

def operator_makefriend(kw):
    # url = 'http://codeforces.com/profile/用户名'
    robot.find_element_by_xpath('//*[@id="pageContent"]/div[2]/div[5]/div[2]/div/h1/img[@class="addFriend friendStar" or class="friendStar addFriend"]').click()

if __name__ == '__main__':
    SimuateAPI.chPathToThis()
    data = SimuateAPI.getData()
    robot = SimuateAPI.load(data['command_executor'], data['session_id'])
    SimuateAPI.todo(robot, 'http://codeforces.com/enter', operator_login, username=data['username'], password=data['password'])
    time.sleep(4.0)
    for i in data['friends']:
        try:
            SimuateAPI.todo(robot, 'http://codeforces.com/profile/' + i, operator_makefriend)
        except selenium.common.exceptions.NoSuchElementException:
            print(i + ' 添加失败。')
