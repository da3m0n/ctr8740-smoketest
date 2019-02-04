import sys
import traceback
import os.path, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from smoketest.TestHelper import TestHelper
from smoketest.TestLog import TestLog
from smoketest.mylib.LoginHandler import LoginHandler
from smoketest.mylib.utils import Utils, GlobalFuncs
from smoketest.SmokeTest import SmokeTest
from optparse import OptionParser


def main():
    parser = OptionParser(usage="usage: %prog ipAddress browser logFileLocation")
    # parser.add_option("-c", "--chelp", help="Add arguments for IP Address for radio and target browser")
    (options, args) = parser.parse_args()
    # print('args', args)
    if len(args) != 3:
        parser.error("wrong number of arguments")

    GlobalFuncs.set_path(args[2])
    TEST_TYPE = 'smoketest'

    run_all = RunAll(TEST_TYPE)
    run_all.run_all()

    # try:
    #     run_all.run_all()
    # finally:
    #     Utils.print_tree(Utils.log_dir())

    # Utils.generate_overall_result(Utils.log_dir(), TEST_TYPE)


class RunAll:
    def __init__(self, test_type):
        self.test_type = test_type
        self.dir = Utils.log_dir()
        self.test_log = TestLog(self.dir)
        self.driver = Utils.create_driver(sys.argv[2])
        self.utils = Utils(self.driver, self.test_log)
        print('init')

    def run_all(self):

        self.run_smoke_test()

    @staticmethod
    def expand_folders(driver):
        has_unopened = True

        while has_unopened:
            folders = driver.find_elements_by_xpath("//div[@class='side_menu_folder']")
            has_unopened = False
            for folder in folders:

                collapsed = len(folder.find_elements_by_xpath("div[@class='side_menu_toggle collapsed']")) > 0
                if folder.is_displayed() and collapsed:
                    name = folder.text
                    driver.execute_script("arguments[0].scrollIntoView(true);", folder)
                    time.sleep(2)
                    search = "//div[normalize-space(.)='" + name + "']/div[@class='side_menu_toggle collapsed']"
                    folder = folder.find_elements_by_xpath(search)[0]
                    folder.click()
                    search = "//div[normalize-space(.)='" + name + "']/div[@class='side_menu_toggle expanded']"
                    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.XPATH, search)))

                    has_unopened = True
                    break

    @staticmethod
    def get_screens(driver):
        RunAll.expand_folders(driver)
        items = driver.find_elements_by_xpath("//a[@class='side_menu_entry']")

        result = []
        for item in items:
            path = [item.text]
            container = item.find_element(By.XPATH, "..")
            folders = container.find_elements_by_xpath("preceding-sibling::div[1]")

            while len(folders) > 0:
                path.insert(0, folders[0].text)
                container = container.find_element(By.XPATH, "..")
                folders = container.find_elements_by_xpath("preceding-sibling::div[@class='side_menu_folder'][1]")
            result.append("/".join(path))

        return result

    def run_smoke_test(self):
        # driver = Utils.create_driver(sys.argv[2])
        # utils = Utils(driver, self.test_log)
        self.utils.delete_existing_dir()

        self.test_log.start('login')
        test_helper = TestHelper(self.test_log, self.driver, self.test_type, self.utils)
        login_handler = LoginHandler(self.driver, test_helper, self.test_log)
        login_handler.start()

        # test_log = TestLog(self.dir)

        smoke_test = SmokeTest(self.driver, self.test_log, test_helper)
        try:
            side_menu = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CLASS_NAME, "side_menu_folder")))
        except e:
            test_helper.assert_false(True, "unable to find side menu", "side_menu")
            login_handler.end()
            self.test_log.close()
            raise e

        # if you want to run individual tests
        smoke_test.create("Status/Alarms")
        # smoke_test.create("System Configuration/Admin/Users")
        # smoke_test.create("Status/Manufacture Details")
        smoke_test.create("Radio Configuration/Radio Links")
        # smoke_test.create("Switching & Routing Configuration/Port Manager")
        # smoke_test.create("Switching & Routing Configuration/Interfaces")

        # OR
        
        # if you want to run over all the screens, uncomment below
        # tests = RunAll.get_screens(self.driver)
        #
        # for test in tests:
        #     try:
        #         if not smoke_test.create(test):
        #             return False
        #     except Exception as ex:
        #         # error_file.write("Failed running: " + test + ex + '\r\n')
        #         print("Failed running ", test, ex)

        login_handler.end()
        self.test_log.close()


if __name__ == "__main__":

    count = 0
    # while 1:
    for x in xrange(1):
        # time.sleep(5)
        # main()
        try:
            time.sleep(5)
            main()
            count += 1
            print("Run " + str(count) + " times.")
        except Exception as e:
            import signal

            print("Main loop exception")

            traceback.print_exc()
            print("About to kill process: ", os.getpid())
            # os.kill(os.getpid(), signal.SIGBREAK)

    # main()
