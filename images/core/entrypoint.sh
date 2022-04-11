#!/bin/bash

set -e

platform_path=$(find / -name "1cv8c" | sed 's/1cv8c//g' | sed 's/\.\/opt/\/opt/g')

if [ "$1" = 'srv' ]
then
    chown -R usr1cv8:grp1cv8 ${COREDATA} ${CORELOGS}
    exec gosu usr1cv8 ${platform_path}ragent -debug -http /d ${COREDATA}
elif [ "$1" = 'srv+cli' ]
then
    ulimit -c unlimited
    chown -R usr1cv8:grp1cv8 ${COREDATA} ${CORELOGS}
    exec gosu usr1cv8 ${platform_path}ragent -debug -http /d ${COREDATA} &
    status=$?
    if [ $status -ne 0 ]; then
        echo "Failed to start ragent: $status"
        exit $status
    fi
    rm -rf /tmp/.X99-lock
    exec /usr/bin/Xvfb :99 -screen 0 1680x1050x24 -shmem &
    sleep 5 &&
    exec /usr/bin/x11vnc -display :99 -forever &
    status=$?
    if [ $status -ne 0 ]; then
        echo "Failed to start Xvfb: $status"
        exit $status
    fi
    while sleep 60; do
        ps aux | grep [r]agent
        RAGENT_STATUS=$?
        ps aux | grep [Xvfb]
        XVFB_STATUS=$?
        if [ $RAGENT_STATUS -ne 0 -o $XVFB_STATUS -ne 0 ]; then
            echo "One of the processes has already exited."
            exit 1
        fi
    done    
elif [ "$1" = 'ras' ]
then
    chown -R usr1cv8:grp1cv8 ${CORELOGS}
    exec gosu usr1cv8 ${platform_path}ras cluster
elif [ "$1" = 'cli' ]
then
    chown -R usr1cv8:grp1cv8 ${CORELOGS}
    exec /usr/bin/Xvfb :99 -screen 0 1680x1050x24 -shmem &
    exec /usr/bin/x11vnc -display :99 -forever 
elif [ "$1" = 'web' ]
then
    chown -R usr1cv8:grp1cv8 ${CORELOGS}
    rm -rf /run/httpd/* /tmp/httpd*
    unset HOME
    exec httpd -DFOREGROUND
elif [ "$1" = 'agent' ]
then
    chown -R usr1cv8:grp1cv8 ${COREDATA} ${CORELOGS} ${AGENTBASEDIR}
    exec /usr/bin/Xvfb :99 -screen 0 1680x1050x24 -shmem &
    exec ${platform_path}1cv8 DESIGNER /AgentMode /IBConnectionString "${INFOBASECONNECTIONSTRING}" /AgentBaseDir "${AGENTBASEDIR}" /AgentSSHHostKey "/id_rsa.key" /Visible /AgentListenAddress 0.0.0.0
fi

exec "$@"