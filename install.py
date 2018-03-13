#!/usr/bin/env python3
import os
import subprocess
from util import *
download_path = "download_dir"

def download_tomcat(install_path):
    apache_tomcat="apache-tomcat"
    tomcat_url="http://mirror.bit.edu.cn/apache/tomcat/tomcat-9/v9.0.6/bin/apache-tomcat-9.0.6.tar.gz"
    tomcat_sha256_url="https://www.apache.org/dist/tomcat/tomcat-9/v9.0.6/bin/apache-tomcat-9.0.6.tar.gz.sha512"

    download(download_path,"apache-tomcat-9.0.6.tar.gz",tomcat_url)
    download(download_path,"apache-tomcat-9.0.6.tar.gz.sha512",tomcat_sha256_url)
    hash_con = open(os.path.join(download_path,"apache-tomcat-9.0.6.tar.gz.sha512")).read()
    if verify_sig(os.path.join(download_path,"apache-tomcat-9.0.6.tar.gz"),hash_con,"sha512"):
        run_cmd(['tar','-xf',"apache-tomcat-9.0.6.tar.gz"],cwd=install_path)



def install_supervisor():
    cmd = ["pip2","install","supervisor"]
    run_cmd(cmd)



def config_tomcat_supervisor(java_home,catalina_home,catalina_base):
    '''

    :param java_home: The JRE_HOME variable is used to specify location of a JRE. The JAVA_HOME
                      variable is used to specify location of a JDK.
    :param catalina_home: tomcat install directory
    :param catalina_base: generally, same as catalina_home
    :return:
    '''
    supervisor_wrapper ='''
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
export JAVA_HOME={java_home}
export CATALINA_HOME={catalina_home}
export CATALINA_BASE={catalina_base}
export CATALINA_PID=/tmp/$$

. $CATALINA_HOME/bin/catalina.sh start

# Allow any signal which would kill a process to stop Tomcat
trap shutdown HUP INT QUIT ABRT KILL ALRM TERM TSTP

echo "Waiting for `cat $CATALINA_PID`"
wait `cat $CATALINA_PID`
    '''.format(java_home=java_home,catalina_home=catalina_home,catalina_base=catalina_base)
    open(os.path.join(catalina_home,'bin','supervisor-wrapper.sh'),'w').write(supervisor_wrapper).close()

download_tomcat('/Users/eig/software')
install_supervisor()
config_tomcat_supervisor("/usr/bin/java","/Users/eig/software/apache-tomcat-9.0.6","/Users/eig/software/apache-tomcat-9.0.6")