import time
from smoketest.mylib.utils import Utils
import xml.etree.ElementTree as ET
import os
import sys
from smoketest.mylib.utils import GlobalFuncs
import urllib

from xml.etree.ElementTree import Comment


class TestLog(object):
    overall_errors = 0
    num_tests_run = 0
    name = ''
    test_errors = 0
    num_screens = 0

    def __init__(self, dir, test_type="smoketest"):
        """Class to log errors"""
        self.test_type = test_type
        self.log = None
        self.doc = None
        self.root = ET.Element("tests")
        self.root.append(Comment('Auto Generated in TestLog.py'))

        self.time = time.localtime()
        self.all_tests_start = time.strftime('%d %B %Y %H:%M:%S', self.time)
        self.url_friendly_start = time.strftime('%d_%B_%Y', self.time)
        self.dir = dir
        self.ipAddress = sys.argv[1]

        path = os.path.join(GlobalFuncs.path())

        el = ET.SubElement(self.root, 'allTestsStart')
        el.set('allTestsStart', self.all_tests_start)
        el.set("runNumber", path.split(os.sep)[-1])
        el.set('ipAddress', self.ipAddress)

        self.screenshots = []

    def start(self, name):
        self.doc = ET.SubElement(self.root, "testScreen", testScreen=name)
        self.num_tests_run += 1

        # test_start = time.strftime('%d %B %Y %H:%M:%S ', self.time)
        #
        # el = ET.SubElement(self.doc, "testStart")
        # el.set("testStart", test_start)
        # test_start_time = time.strftime('%H:%M:%S', self.time)
        # test_start_date = time.strftime('%d %B %Y', self.time)
        #
        # el = ET.SubElement(self.doc, "testStart")
        # el.set("startTime", test_start_time)
        # el.set("startDate", test_start_date)

    def log_it2(self, count, msg=None, test_name=None):
        self.test_errors += count
        if self.doc == None:
            self.start(test_name)
        el = ET.SubElement(self.doc, 'error')
        el.set('msg', msg)

    def log_info(self, msg=None):
        el = ET.SubElement(self.doc, 'info')
        el.set('msg', msg)

    def store_screenshot_info(self, screenshot_info, dir):
        rel_path = os.path.relpath(dir, self.dir)
        url_path = '/smoketest/' + urllib.pathname2url(rel_path)

        self.screenshots.append(screenshot_info)
        el = ET.SubElement(self.doc, 'screenshot')
        el.set('path', url_path + '/' + screenshot_info + '.png')

        # print 'storing info', self.screenshots

    def close(self):
        local_time = time.localtime()
        date = time.strftime('%d_%B_%Y', local_time)

        errors = ET.SubElement(self.root, 'errorCount')
        errors.set('errorCount', str(self.test_errors))

        total_tests = ET.SubElement(self.root, 'totalTestCount')
        total_tests.set('totalTestCount', str(self.num_tests_run))
        time.sleep(2)  # cause would sometimes return zero screens for whatever reason

        if self.num_screens > 0:
            coverage_percentage = float(self.num_tests_run / float(self.num_screens) * 100)
            coverage = ET.SubElement(self.root, 'coveragePercentage')
            coverage.set('coveragePercentage', ('%.f' % coverage_percentage) + '%')

        tree = ET.ElementTree(self.root)

        tests = os.path.join(GlobalFuncs.path(), self.ipAddress)

        if not os.path.exists(tests):
            os.mkdir(tests)

        # path = os.path.join(tests, date + '.xml')
        path = os.path.join(tests, 'testresult.xml')

        # path = os.path.join(os.path.abspath(tests + '\\' + date + '.xml'))

        tree.write(path)

    def add_num_screens(self, num_screens):
        self.num_screens = num_screens
        screens = ET.SubElement(self.root, 'totalScreens')
        screens.set('totalScreens', str(num_screens))
