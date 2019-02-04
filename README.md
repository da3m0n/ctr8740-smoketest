# ctr-smoketest

Prerequisites

1) Install Python2.7 (multi-run.py assumes it is installed in default c:\Python27)
2) pip install the following modules
	a) selenium
	b) requests
	c) urllib3

To run

1) Add login details to login.config file if wanting to override default credentials in LoginHandler.py
2) Start webserver by running startup.sh
3) Start test (from Windows command prompt): python multi-run.py 10.16.15.113 11.19.4.214 ... (one or many radios)

![Example application](/smoketest/example.png)
