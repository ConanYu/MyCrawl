# copy from 'http://www.spiderpy.cn/blog/detail/36'

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

if __name__ == '__main__':
    #  第一次使用Chrome() 新建浏览器会话
    driver = webdriver.Chrome(executable_path=r'D:\Desktop\chromedriver.exe')

    # 记录 executor_url 和 session_id 以便复用session
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    # 访问百度
    driver.get("http://www.spiderpy.cn/")

    print(session_id)
    print(executor_url)

    # 假如driver对象不存在，但浏览器未关闭
    del driver

    # 使用ReuseChrome()复用上次的session
    driver2 = ReuseChrome(command_executor=executor_url, session_id=session_id)

    # 打印current_url为百度的地址，说明复用成功
    print(driver2.current_url)
    driver2.get("https://www.baidu.com")

# copy from 'http://www.spiderpy.cn/blog/detail/36'
