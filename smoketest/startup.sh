#!/usr/bin/env bash
EXE=`which $0`
cd `dirname ${EXE}`
cd ..

PYTHONVER=`python --version 2> /dev/null`

if [ $? -eq 0 ]; then
    PYTHON=python
    MAJOR=`echo $PYTHONVER | sed -E 's/^.* ([0-9]+)\..*$/\1/g'`
    MINOR=`echo $PYTHONVER | sed -E 's/^.* ([0-9]+)\.([0-9]+)\..*$/\2/g'`

    if [ $MAJOR -lt 3 ]; then
	PYTHONVER=`python3 --version 2> /dev/null`
	PYTHON=python3
	if [ $? -ne 0 ]; then
	    echo Cannot find correct python version requires 3.6 or above
	    exit 1
	fi
    fi
else
    PYTHONVER=`python3 --version 2> /dev/null`
    PYTHON=python3
fi

MAJOR=`echo $PYTHONVER | sed -E 's/^.* ([0-9]+)\..*$/\1/g'`
MINOR=`echo $PYTHONVER | sed -E 's/^.* ([0-9]+)\.([0-9]+)\..*$/\2/g'`

if [ $MAJOR -lt 3 ]; then
    echo Cannot find correct python version requires 3.6 or above
    exit 1
fi

if [ $MAJOR -eq 3 ]; then
    if [ $MINOR -lt 6 ]; then
	echo Cannot find correct python version requires 3.6 or above
	exit 1
    fi
fi


if command -v lsof ; then

    for i in `lsof -i :3000 -F p | grep ^p | sed s/^p//` ; do
	kill $i
    done    
    
    node smoketest/createrunnumber.js &
	
    for i in `lsof -i :8000 -F p | grep ^p | sed s/^p//` ; do
	kill $i
    done

    #    python -m SimpleHTTPServer 8000&
    $PYTHON -m http.server 8000&
	
else
    for i in `netstat -aon  | gawk ' $2~/:3000/ {gsub("\r","",$5); print $5}'` ; do
	taskkill /F /PID $i	    
    done
    
    
    node smoketest/createrunnumber.js &
    
    for i in `netstat -aon  | gawk ' $2~/:8000/ {gsub("\r","",$5); print $5}'` ; do
	taskkill /F /PID $i
    done
    
    $PYTHON -m http.server 8000& 
    
fi

