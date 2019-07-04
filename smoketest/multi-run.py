import subprocess
import sys
import signal
import sys
import os, shutil
import xml.etree.ElementTree as ET

import time
import requests
from xml.etree.ElementTree import Comment

from requests import ConnectionError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smoketest.mylib.utils import Utils


def ensure_path_exists(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


logs_dir = os.path.join(Utils.log_dir(), 'logs')
try:
    sub_path = requests.get('http://localhost:3000/next').content
    path_to_dir = os.path.join(os.getcwd(), 'logs', *sub_path.split('/'))
    ensure_path_exists(path_to_dir)
except ConnectionError:
    print "Need to start webserver. Run ./startup.sh from ", os.getcwd()


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    [p.kill() for p in opens]
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

opens = []
root = ET.Element("ipAddresses")
root.append(Comment('Auto Generated in multi-run.py'))

run_dates_path = os.path.join(Utils.log_dir(), 'logs', "runInfo.txt")


def run_some(start, end):
    from sys import platform as platform

    if platform == "win32":
        path_to_python = "c:\\Python27\\python.exe"
    else:
        path_to_python = "/cygdrive/c/cygwin64/bin/python"
    for i in range(start, end):
        time.sleep(2)
        opens.append(subprocess.Popen([path_to_python, "./runAll.py", sys.argv[i], "chrome", path_to_dir]))

    [p.wait() for p in opens]


if not os.path.exists(run_dates_path):

    run_dates_file = open(run_dates_path, "a+")

    for date in Utils.get_dirs(logs_dir):
        for run in Utils.get_dirs(os.path.join(Utils.log_dir(), 'logs', date)):
            print 'date', date, 'list', os.listdir(os.path.join(Utils.log_dir(), 'logs', date))
            run_dates_file.write(date + '/' + run + '\n')

else:
    run_dates_file = open(run_dates_path, "a+")
    run_dates_file.write(sub_path + '\n')

run_dates_file.close()

for i in range(1, len(sys.argv)):
    field = ET.SubElement(root, "ipAddress").text = sys.argv[i]

tree = ET.ElementTree(root)
tree.write(os.path.join(path_to_dir, 'ip-addresses.xml'))

step = 3
for i in range(1, len(sys.argv), step):
    run_some(i, min(i + step, len(sys.argv)))

Utils.print_tree(path_to_dir)

res = {}


def get_test_run_info(date):

    total_error_count = 0
    total_test_count = 0

    for run in Utils.get_dirs(os.path.join(logs_dir, date)):
        for ip_in_runs in Utils.get_dirs(os.path.join(logs_dir, date, run)):
            for xml in os.listdir(os.path.join(logs_dir, date, run, ip_in_runs)):
                if xml.startswith('testresult'):
                    fname = os.path.join(logs_dir, date, run, ip_in_runs, xml)
                    tree = ET.parse(fname)

                    test_count = tree.find('totalTestCount').get('totalTestCount')
                    error_count = tree.find('errorCount').get('errorCount')

                    total_test_count += int(test_count)
                    total_error_count += int(error_count)

    return {'date': date, 'total_test_count': total_test_count, 'total_error_count': total_error_count}


def make_test_summary_xml(date):

    summary_data = get_test_run_info(date)

    root_ele = ET.Element('results')

    summary_ele = ET.SubElement(root_ele, 'summary')
    summary_ele.set('date', summary_data['date'])
    summary_ele.set('totalTestCount', str(summary_data['total_test_count']))
    summary_ele.set('totalErrorCount', str(summary_data['total_error_count']))

    tree = ET.ElementTree(root_ele)

    path = os.path.join(logs_dir, date, 'testsummary.xml')
    tree.write(path)


for log_date in Utils.get_dirs(logs_dir):
    make_test_summary_xml(log_date)