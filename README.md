# ctr8740-smoketest

The purpose of this is to go to all, or specific, ATR pages and if any page fails to load an error and screenshot will be captured.

Prerequisites

1) Install Python 3.6 or later. (multi-run.py assumes it is installed in default c:\PythonXX)
2) pip install the following modules
	a) selenium
	b) requests
	c) urllib3
	d) webdriver-manager

To run

1) If wanting to override the default login credentails in LoginHandler.py, add new credentials to login.config file
2) Start webserver by running startup.sh
3) Start test by running: python3.6 multi-run.py -browser <IPADDRESS/S> space separated

![Example application](/smoketest/example.png)
