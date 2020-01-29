#!/usr/bin/env bash
EXE=`which $0`
cd `dirname ${EXE}`
cd ..


if command -v lsof ; then

    for i in `lsof -i :3000 -F p | grep ^p | sed s/^p//` ; do
	kill $i
    done    
    
    node smoketest/createrunnumber.js &
	
    for i in `lsof -i :8000 -F p | grep ^p | sed s/^p//` ; do
	kill $i
    done
    
    python -m SimpleHTTPServer 8000&
	
else
    for i in `netstat -aon  | gawk ' $2~/:3000/ {gsub("\r","",$5); print $5}'` ; do
	taskkill /F /PID $i	    
    done
    
    
    node smoketest/createrunnumber.js &
    
    for i in `netstat -aon  | gawk ' $2~/:8000/ {gsub("\r","",$5); print $5}'` ; do
	taskkill /F /PID $i
    done
    
    python -m SimpleHTTPServer 8000& 
    
fi

