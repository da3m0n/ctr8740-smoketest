#!/usr/bin/env bash
EXE=`which $0`
cd `dirname ${EXE}`
cd ..

for i in `netstat -aon  | gawk ' $2~/:3000/ {gsub("\r","",$5); print $5}'` ; do
    taskkill /F /PID $i
done

node smoketest/createrunnumber.js &

for i in `netstat -aon  | gawk ' $2~/:8000/ {gsub("\r","",$5); print $5}'` ; do
    taskkill /F /PID $i
done

python -m SimpleHTTPServer 8000&
