from selenium.common.exceptions import StaleElementReferenceException
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

            time.sleep(3)
            # self.driver.execute_script("document.getElementById('tableWidget1_3_mapping').innerHTML=\"\";")

            WebDriverWait(self.driver, 45).until(EC.invisibility_of_element_located((By.ID, "loading")))

            warning_elements = self.driver.find_elements_by_class_name('warning')

            for el in warning_elements:
                display_prop = el.value_of_css_property('display')

                page_name = screen_name.split('/').pop().replace(' ', '_')

                if display_prop == u'block':
                    self.test_helper.assert_true(True,
                                                 page_name + ' page not loaded OK',
                                                 page_name)
                else:
                    self.test_helper.assert_true(False,
                                                 'Ensure page is displayed.',
                                                 page_name + ' page loaded OK')

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
            print('Failure', e)

        return True
