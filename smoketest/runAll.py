import sys
import traceback
import os.path, time

from selenium.common.exceptions import NoSuchElementException

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


# to run on multiple radios add the addresses separated by a space
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
    def do_expand(driver, level):
        expanded = False
        list = []
        root = driver.find_element(By.CLASS_NAME,'menu-tree-root');
        menu_items_by_level = root.find_elements_by_xpath(".//div[@aria-level='" + str(level) + "']")
        # menu_items_by_level = driver.find_elements_by_xpath("//a[@href='undefined']")

        for m in menu_items_by_level:
            if Utils.open_folder(m) < 1:
                list.append(m)
            else:
                expanded = True

        if expanded:
            sub_list = RunAll.do_expand(driver, level + 1)
            for i in sub_list:
                list.append(i)
        return list

    @staticmethod
    def make_path(el):
        res = []
        cur = el
        count = 0

# todo fix population of menus. Not all are getting into list
        try:
            while cur:

                if cur.get_attribute('class') == "menu-tree-item":
                    try:
                        res.insert(0, cur.find_element(By.XPATH, "div[@class='menu-tree-row' or @class='menu-tree-row "
                                                                 "selected']").text)
                        count += 1
                    except:
                        print("not found", cur)

                cur = cur.find_element(By.XPATH, "..")
        except NoSuchElementException:
            return res

    @staticmethod
    def get_screens(driver):
        items_list = RunAll.do_expand(driver, 1)
        result = []

        for item in items_list:
            path = RunAll.make_path(item)
            result.append(path)

        return result

    def run_smoke_test(self):
        # driver = Utils.create_driver(sys.argv[2])
        # utils = Utils(driver, self.test_log)
        self.utils.delete_existing_dir()

        # self.test_log.start('login')
        test_helper = TestHelper(self.test_log, self.driver, self.test_type, self.utils)
        login_handler = LoginHandler(self.driver, test_helper, self.test_log)
        login_handler.start()

        # test_log = TestLog(self.dir)

        smoke_test = SmokeTest(self.driver, self.test_log, test_helper)
        try:
            side_menu = WebDriverWait(self.driver, 35).until(
                EC.presence_of_element_located((By.CLASS_NAME, "menu-tree-item")))
        except e:
            test_helper.assert_false(True, "unable to find side menu", "side_menu")
            login_handler.end()
            self.test_log.close()
            raise e

        # if you want to run individual tests follow format below
        # smoke_test.create(["Status", "Alarms"])
        # smoke_test.create(["Status", "System Log"])
        # smoke_test.create(["Status", "Equipment"])
        # smoke_test.create(["System Configuration", "Management IP"])
        # smoke_test.create(["Admin", "Advanced"])
        # smoke_test.create(["System Configuration", "SNMP"])
        # smoke_test.create(["System Configuration", "DNS"])
        # smoke_test.create(["Admin", "User Management", "Local"])
        # smoke_test.create(["Switching and Routing", "Interfaces"])
        # smoke_test.create(["Switching and Routing", "RMON", "Quarter Hour"])
#        smoke_test.create(["Switching and Routing", "Quality of Service", "Policies"])

        # OR
        
        # if you want to run over all the screens, remove the empty array and uncomment rest
        tests = RunAll.get_screens(self.driver)
#        tests = []
        
        for test in tests:
            try:
                if not smoke_test.create(test):
                    return False
            except Exception as ex:
                # error_file.write("Failed running: " + test + ex + '\r\n')
                print("Failed running ", test, ex)

        login_handler.end()
        self.test_log.close()


if __name__ == "__main__":

    count = 0
    # while 1:
    for x in range(1):
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
