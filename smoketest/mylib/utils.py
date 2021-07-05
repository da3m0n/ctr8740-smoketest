import sys, os, time, shutil
import datetime

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
#import urllib, urllib2

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Comment


class GlobalFuncs(object):

    def __init__(self):
        pass

    @staticmethod
    def path():
        global path_to_dir
        return path_to_dir

    @staticmethod
    def rel_path():
        global path_to_dir
        sep = path_to_dir.split(os.sep)
        url_path = urllib.pathname2url(path_to_dir)
        url_path = url_path.partition('ctrguiautotest')

        return url_path[2]

    @staticmethod
    def set_path(p):
        global path_to_dir
        path_to_dir = p

    @staticmethod
    def ensure_path_exists(path):
        import errno
        try:
            print("path to create", path)
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


#
#
# sub_path = requests.get('http://localhost:3000/next').content
path_to_dir = ''


class Utils(object):
    def __init__(self, driver, test_log):
        self.test_log = test_log
        rt = None
        self.driver = driver
        self.pwd = os.getcwd()
        self.local_time = time.localtime()
        self.date = time.strftime('%d_%B_%Y', self.local_time)
        self.ipAddress = Utils.format_ip_address(sys.argv[1])

    @staticmethod
    def win_chrome():
        path_to_chrome_driver = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "drivers", "chromedriver.exe"))
        return webdriver.Chrome(path_to_chrome_driver)
    
    @staticmethod
    def linux_chrome():
        path_to_chrome_driver = '/usr/local/bin/chromedriver'
        return webdriver.Chrome(path_to_chrome_driver)
    
    @staticmethod
    def create_driver(driver_name):
        from selenium import webdriver
        
        if(driver_name == "firefox"):
            from webdriver_manager.firefox import GeckoDriverManager
                     
#            profile = webdriver.FirefoxProfile()
#            profile.accept_untrusted_certs = True

            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install()) 
#            driver = webdriver.Firefox(firefox_profile=profile)
            
        elif (driver_name == "chrome"):
            from webdriver_manager.chrome import ChromeDriverManager
            options = webdriver.ChromeOptions()
            options.add_argument('ignore-certificate-errors')
            driver = webdriver.Chrome(chrome_options=options)
            
        elif (driver_name == "chromium"):
            from webdriver_manager.chrome import ChromeDriverManager
            from webdriver_manager.utils import ChromeType
            from subprocess import Popen, PIPE

            p = Popen(['bash', 'which', 'chromium-browser'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate(b"")
            
            options = webdriver.ChromeOptions()
            options.add_argument('ignore-certificate-errors')
            options.binary_location = output.decode("utf-8").strip()
            
            driver = webdriver.Chrome(chrome_options=options)
   
        return driver
       #raise Exception("Unable to create Driver " + driver_name)
        
    def start_browser(self, driver):
        self.get_address(driver)
        self.window_init(driver)

    @classmethod
    def login(self, driver, username, password, test_helper, test_log):

        try:
            inputElement = driver.find_element_by_id("username")
            inputElement.send_keys(username)
            inputElement = driver.find_element_by_id("password")
            inputElement.send_keys(password)
            inputElement.submit()
        except Exception as e:
            print('login failed')
            print("Login page not as expected. Exiting...")

            test_helper.assert_false(True, "unexpected login page", "login")
            test_log.close()
            driver.close()
            raise e

        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "layout_device_name")))
            print('Login Successful')
            time.sleep(5)
        except Exception as e:
            print("Page not loaded correctly")
            test_helper.assert_false(True, "unexpected login page", "login")

            test_helper.close()
            driver.close()
            raise e

    def logout(self, driver):
        # find the logout button
        try:
            time.sleep(1)
            self.click_element("profileHeader")
            time.sleep(3)
            profile_popup = self.driver.find_element(By.ID, 'profilePopupMenu')

            sign_out = profile_popup.find_element(By.XPATH, "a/div/span[text()='SIGN OUT']")
            sign_out.click()

            # self.click_element(logoutTag)
            # self.click_element("top_menu_logout")
        except Exception as e:
            print("Logout unsuccessful. This may cause errors with max number of sessions", e)
        else:
            print("Successfully logged out")
        finally:
            time.sleep(2)
            driver.quit()

    @classmethod
    def window_init(self, driver):
        driver.set_window_size(1200, 1150)
        # handle = driver.window_handles

    @classmethod
    def get_addressORIG(self, driver):
        if len(sys.argv) < 2:
            print("Address argument missing")
            sys.exit()
        address = "http://" + sys.argv[1]
        try:
            response = urllib2.urlopen(address)
            response.close()
        except:
            address = "https://" + sys.argv[1]

        # get page
        driver.get(address)

    @classmethod
    def get_address(self, driver):
        if len(sys.argv) < 2:
            print("Address argument missing")
            sys.exit()
        print('arg', sys.argv[1])
        driver.get("https://" + sys.argv[1])

    def click_element(self, element):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, element)))
        self.driver.find_element(By.ID, element).click()

    @staticmethod
    def log_dir():
        return os.path.dirname(os.path.dirname(__file__))

    def find_element(self, element):
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, element)))
            return self.driver.find_element(By.ID, element)
        except NoSuchElementException:
            return 'not found'

    RETRIES = 3
    TIMEOUT_SECONDS = 30

    @staticmethod
    def get_dirs(file_path):
        logs_in_dir = []
        for log_file in os.listdir(file_path):
            if os.path.isdir(os.path.join(file_path, log_file)):
                logs_in_dir.append(log_file)

        return logs_in_dir

    @classmethod
    def print_tree(cls, results_dir):
        # Utils.delete_existing_dir()

        root = ET.Element("results")
        # doc = ET.SubElement(root, 'logs')
        root.append(Comment('Auto Generated by print_tree() in mylib/utils.py'))
        # ipAddress = sys.argv[1]

        # logs_directory = os.path.join(Utils.log_dir(), 'logs')

        # total_errors_count = 0
        # path_dir = Utils.get_dirs(results_dir)
        run_number = os.path.basename(results_dir)

        test_run_tag = ET.SubElement(root, 'testRun')
        test_run_tag.set('testRun', run_number)
        test_run_tag.set('outputDir', results_dir)

        for ip_address in Utils.get_dirs(results_dir):
            # num_times_run = os.listdir(os.path.join('logs', ip_address))
            # print('run times', num_times_run)
            # print('log_date', log_date, addresses_in_dir, test_dir, os.getcwd())

            # ip_addresses_root_tag = ET.Element('ipAddresses')
            # output_file = ET.ElementTree(root)

            screenshot_dir = Utils.get_dirs((os.path.join(results_dir, ip_address)))

            if screenshot_dir:
                screen_shots_tag = ET.SubElement(root, 'screenShots')
                screenshot_path = os.path.join(results_dir, ip_address, 'screenshots')

                for ss in os.listdir(screenshot_path):
                    screen_shot_tag = ET.SubElement(screen_shots_tag, 'screenShot')
                    screen_shot_tag.set('imageurl', os.path.join(screenshot_path, ss))
                    # screem_shot_tag.set('screenshotDir', os.path.join())

            else:
                print('no screenshots', ip_address)

            # output_file.write(os.path.join(results_dir, ip_address, 'results.xml'))

    @classmethod
    def extract_error_count(cls, xmlfile):

        xmlfile = os.path.join('logs', xmlfile)
        try:
            file = open(xmlfile, 'r')

            tree = ET.parse(file)
            for child in tree.findall('.//errorCount'):
                return int(child.attrib['errorCount'])
        except:
            print('Error opening the file ', xmlfile)

        return 0

    @classmethod
    def reformat_date(cls, date):
        return datetime.datetime.strptime(date, "%d_%B_%Y").strftime("%Y%m%d")

    @staticmethod
    def is_alert_present(driver):
        present_flag = False

        try:
            from selenium.webdriver.common.alert import Alert
            alert = driver.switch_to.alert
            present_flag = True
            alert.accept()

        except NoAlertPresentException:
            pass

        return present_flag

    @classmethod
    def __insert_underscores(cls, str):
        val = str.replace(' ', '_')
        return val

    def open_all(self):
        side_menus = self.driver.find_elements_by_class('side_menu_folder')
        print('side folders', len(side_menus))

    @staticmethod
    def format_ip_address(ip_address):
        import re
        return re.sub(r'\*|\<|\>|\%|:|\?|\||\\', "_", ip_address)
        # return ip_address.replace(":", "_port_")

    def save_screenshot(self, test_name, test_type):
        # test_name = test_name.rstrip('.')
        test_name = test_name.replace('/', '-')

        # screenshots_dir = self.pwd + '\\logs\\' + self.date + '\\' + test_type + '\\screenshots'
        # screenshots_dir = os.path.join(GlobalFuncs.path(), self.ipAddress, 'screenshots')
        screenshots_dir = os.path.join(GlobalFuncs.path(), Utils.format_ip_address(self.ipAddress), 'screenshots')
        GlobalFuncs.ensure_path_exists(screenshots_dir)
        self.test_log.store_screenshot_info(test_name, screenshots_dir)
        self.driver.save_screenshot(os.path.join(screenshots_dir, test_name + '.png'))
        print('image saving complete')

    @classmethod
    def __make_sure_path_exists(cls, path):
        import errno
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    @staticmethod
    def delete_existing_dir():
        import sys
        ipAddress = Utils.format_ip_address(sys.argv[1])

        date = time.strftime('%d_%B_%Y', time.localtime())

        screenshots_dir = os.getcwd() + '\\logs\\' + date + '\\smoketest\\' + ipAddress + '\\screenshots'
        if os.path.exists(screenshots_dir):
            shutil.rmtree(screenshots_dir)
        else:
            print(screenshots_dir + ' does not exist.')

    def navigate_to_screen(self, screen_name):
        time.sleep(1)
        # breadcrumbs = screen_name.split('/')
        res = self.__navigate_to_location(screen_name)
        # self.driver.switch_to_frame('frame_content')

        # self.test_log.start(screen_name[-1])
        self.test_log.start('/'.join(screen_name))
        return res

    def __navigate_to_location(self, breadcrumbs):
        self.driver.switch_to_default_content()
        return self.__navigate_to_location_rec(self.driver.find_element(By.CLASS_NAME,'menu-tree-root'), breadcrumbs, 0)

    def __navigate_to_location_rec(self, root, breadcrumbs, pos):
        breadcrumb = breadcrumbs[pos]
        if len(breadcrumbs) == pos + 1:
            WebDriverWait(root, 20).until(EC.visibility_of_element_located((By.LINK_TEXT, breadcrumbs[pos])))
            last_el = root.find_element_by_link_text(breadcrumbs[pos])

            # there is a problem here since the search input box is sticky it floats above the
            # menu item, that means that selenium does not scroll the menu to the right spot, sometimes
            # leaving it under the search input, but that means it cannot click on it.

            # in order to get around this on the first menu (the one with no link)
            # we find the top level otem and alwaysnscroll up to it
            from selenium.webdriver.common.action_chains import ActionChains
            base = root.find_element_by_xpath("//div[@aria-level='0']")
            first = base.find_element_by_xpath(".//span[@class='menu-tree-item-label']//a[@class='menu-entity']")
            ActionChains(self.driver).move_to_element(first).perform()

            if not last_el.get_attribute('href') is None:
                last_el.click()
                return True
            else:
                return False
        else:

            menus = root.find_elements_by_xpath("//div[@aria-level='" + str(pos + 1) + "']")
            for m in menus:
                try:
                    if m.find_element(By.CLASS_NAME, "menu-entity").text == breadcrumb:
                        Utils.open_folder(m)
                        return self.__navigate_to_location_rec(m, breadcrumbs, pos + 1)
                except NoSuchElementException:
                    pass
            return False

            # print "folder", folder

            # expanded = len(folder.find_elements_by_class_name('expanded')) > 0
            # if not expanded:
            #     folder.click()


    @staticmethod
    def open_folder(menu_item):
        expanded = 0
        try:
            tree_row = menu_item.find_element(By.CLASS_NAME, "menu-tree-row")
            if Utils.element_exists(tree_row, "menu-tree-collapsed-folder-icon"):
                menu_item.click()
                time.sleep(1)
                expanded += 1

            elif Utils.element_exists(tree_row, "menu-tree-expanded-folder-icon"):
                expanded += 1
        except NoSuchElementException:
            pass

        return expanded

    @staticmethod
    def element_exists(web_element, class_name):
        try:
            if web_element.find_element(By.CLASS_NAME, class_name):
                return True
        except NoSuchElementException as e:
            return False


from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.expected_conditions import _find_elements


class my_visibility_of_elements(object):
    def __init__(self, locator, name):
        self.locator = locator
        self.name = name

    def __call__(self, driver):
        try:
            folders = _find_elements(driver, self.locator)
            for folder in folders:
                # time.sleep(0.25)
                if folder.is_displayed():
                    if folder.text == self.name:
                        return folder

            return False
        except StaleElementReferenceException:
            return False


from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(self, *self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


# if __name__ == "__main__":
    # main()
