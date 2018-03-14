#!/usr/bin/env python3
import os
import subprocess
from util import *
download_path = "download_dir"
tomcat_url="http://mirror.bit.edu.cn/apache/tomcat/tomcat-9/v9.0.6/bin/apache-tomcat-9.0.6.tar.gz"
tomcat_sha256_url="https://www.apache.org/dist/tomcat/tomcat-9/v9.0.6/bin/apache-tomcat-9.0.6.tar.gz.sha1"





def install_supervisor():
    cmd = ["pip2","install","supervisor"]
    run_command(cmd)



def config_tomcat_supervisor(java_home,catalina_home,catalina_base):
    '''

    :param java_home: The JRE_HOME variable is used to specify location of a JRE. The JAVA_HOME
                      variable is used to specify location of a JDK.
    :param catalina_home: tomcat install directory
    :param catalina_base: generally, same as catalina_home
    :return:
    '''
    supervisor_wrapper ="""
#!/bin/bash
# Source: http://serverfault.com/questions/425132/controlling-tomcat-with-supervisor
function shutdown()
{
    date
    echo "Shutting down Tomcat"
    unset CATALINA_PID # Necessary in some cases
    $CATALINA_HOME/bin/catalina.sh stop
}

date
echo "Starting Tomcat"
export JAVA_HOME=%s
export CATALINA_HOME=%s
export CATALINA_BASE=%s
export CATALINA_PID=/tmp/$$

. $CATALINA_HOME/bin/catalina.sh start

# Allow any signal which would kill a process to stop Tomcat
trap shutdown HUP INT QUIT ABRT KILL ALRM TERM TSTP

echo "Waiting for `cat $CATALINA_PID`"
wait `cat $CATALINA_PID`
    """%(java_home,catalina_home,catalina_base)
    open(os.path.join(catalina_home,'bin','supervisor-wrapper.sh'),'w').write(supervisor_wrapper)

download_install(tomcat_url,tomcat_sha256_url,download_path,"/home/eig/tmp")
install_supervisor()
config_tomcat_supervisor("/usr/bin/java","/home/eig/tmp/apache-tomcat-9.0.6","/home/eig/tmp/apache-tomcat-9.0.6")