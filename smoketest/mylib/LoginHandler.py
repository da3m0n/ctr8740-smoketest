import sys, os
from smoketest.mylib.utils import Utils


class LoginHandler(object):
    def __init__(self, driver, test_helper, test_log):
        self.utils = Utils(driver, None)
        self.driver = driver
        self.login_info = {}
        self.test_helper = test_helper
        self.test_log = test_log

        try:
            with open("login.config") as f:
                content = f.readlines()
                for line in content:
                    parts = line.strip().split(',', 2)
                    print("parts", parts)
                    self.login_info[parts[0]] = (parts[1], parts[2])
        except:
            pass

    def login(self):
        print('doing nothing, already logged from start()')

    def logout(self):
        print('normal logout')

    def start(self):

        self.utils.start_browser(self.driver)
        override = self.login_info.get(sys.argv[1])
        print("get override", override, sys.argv[1])
        if override is None:
            self.utils.login(self.driver, 'root', 'admin123', self.test_helper, self.test_log)
        else:
            self.utils.login(self.driver, override[0], override[1], self.test_helper, self.test_log)

    def end(self):
        # self.driver.switch_to_default_content()
        self.utils.logout(self.driver)