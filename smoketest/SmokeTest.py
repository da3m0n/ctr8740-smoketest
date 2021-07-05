from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from smoketest.mylib.utils import Utils


class SmokeTest:
    def __init__(self, driver, test_log, test_helper):
        self.test_log = test_log
        self.driver = driver
        self.gui_lib = Utils(driver, test_log)
        # self.test_helper = TestHelper(self.test_log, self.driver)
        self.test_helper = test_helper

    def create(self, screen_name):

        try:
            self.gui_lib.navigate_to_screen(screen_name)
            self.gui_lib.is_alert_present(self.driver)

            WebDriverWait(self.driver, 45).until(EC.visibility_of_element_located((By.ID, "contentInner")))

            content_inner = self.driver.find_element(By.ID, "contentInner")
            error_elements = content_inner.find_elements(By.CLASS_NAME, "error")
            name = "/".join(screen_name)

            if not error_elements:
                child_elements = content_inner.find_elements(By.XPATH, "div[starts-with(@class, "
                                                                       "'widget_')]")
                for child in child_elements:

                    try:
                        child.find_element(By.XPATH, "*")
                    except NoSuchElementException as e:
                        self.test_helper.assert_true(True,
                                                     name + ' page not loaded OK',
                                                     name)
            else:
                self.test_helper.assert_true(True,
                                             name + ' page not loaded OK',
                                             name)

        except StaleElementReferenceException as e:
            print('StaleElementException', e)
        except Exception as e:
            name = ""
            count = 1

            for s in screen_name:
                if not count == len(screen_name):
                    name += s + '/'
                    count += 1
                else:
                    name += s

            self.test_helper.assert_true(True, name + ' not displayed', name)
            print('Failure *******', e)

        return True
