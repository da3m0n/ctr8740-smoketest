import os
from smoketest.mylib.utils import Utils


class TestHelper(object):
    def __init__(self, log, driver, test_type, utils):
        self.test_type = test_type
        self.log_dir = Utils.log_dir()
        self.driver = driver
        self.log = log
        self.error_count = 0
        self.utils = utils

    def assert_true(self, val, msg=None, test_name=None):
        # todo change logic so it makes sense
        if val:
            print('val ****', val, test_name, msg)
            self.error_count += 1
            # utils = Utils(self.driver, None)
            self.utils.save_screenshot(test_name, self.test_type)
            self.log.log_it2(self.error_count, msg, test_name)
        else:
            msg = '-'
            # self.driver.save_screenshot('testypass.png')
            self.log.log_it2(self.error_count, msg, test_name)
        self.error_count = 0

    def assert_false(self, val, msg, test_name):
        if val:
            self.error_count += 1
            # utils = Utils(self.driver, None)
            self.utils.save_screenshot(test_name, self.test_type)
            self.log.log_it2(self.error_count, msg, test_name)
        else:
            msg = '-'
            # self.driver.save_screenshot('testypass.png')
            self.log.log_it2(self.error_count, msg, test_name)
        self.error_count = 0

    def assert_not_equal(self, val1, val2, msg=None):
        if val1 != val2:
            self.error_count += 1
            res = {'expected': val2, 'detected': val1}
            self.log.log_it(res)
