#!/bin/bash
# opsplatform        Startup script for the opsplatform Server

opsplatform_dir=

base_dir=$(dirname $0)
opsplatform_dir=${opsplatform_dir:-$base_dir}
export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

if [ -f ${opsplatform_dir}/commands/functions ];then
    . ${opsplatform_dir}/commands/functions
elif [ -f /etc/init.d/functions ];then
    . /etc/init.d/functions
else
    echo "No functions script found in [./functions, ./install/functions, /etc/init.d/functions]"
    exit 1
fi

PROC_NAME="opsplatform"
lockfile=/var/lock/subsys/${PROC_NAME}

start() {
        ops_start=$"Starting ${PROC_NAME} service:"
        if [ -f $lockfile ];then
             echo -n "opsplatform is running..."
             success "$ops_start"
             echo
        else
            daemon $opsplatform_dir/venv/bin/python $opsplatform_dir/manage.py crontab add &>> /var/log/opsplatform.log 2>&1
            daemon $opsplatform_dir/venv/bin/python $opsplatform_dir/run_server.py &>> $opsplatform_dir/runtime.log 2>&1 &
            sleep 1
            echo -n "$ops_start"
            ps axu | grep 'run_server' | grep -v 'grep' &> /dev/null
            if [ $? == '0' ];then
                success "$ops_start"
                if [ ! -e $lockfile ]; then
                    lockfile_dir=`dirname $lockfile`
                    mkdir -pv $lockfile_dir
                fi
                touch "$lockfile"
                echo
            else
                failure "$ops_start"
                echo
            fi
        fi
}


stop() {
    echo -n $"Stopping ${PROC_NAME} service:"
    daemon $opsplatform_dir/venv/bin/python $opsplatform_dir/manage.py crontab remove &>> /var/log/opsplatform.log 2>&1
    ps aux | grep -E 'run_server.py' | grep -v grep | awk '{print $2}' | xargs kill -9 &> /dev/null
    ret=$?
    if [ $ret -eq 0 ]; then
        echo_success
        echo
        rm -f "$lockfile"
    else
        echo_failure
        echo
        rm -f "$lockfile"
    fi

}

status(){
    ps axu | grep 'run_server' | grep -v 'grep' &> /dev/null
    if [ $? == '0' ];then
        echo -n "opsplatform is running..."
        success
        touch "$lockfile"
        echo
    else
        echo -n "opsplatform is not running."
        failure
        echo
    fi
}



restart(){
    stop
    start
}

# See how we were called.
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;

  restart)
        restart
        ;;

  status)
        status
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|status}"
        exit 2
esac
