#!/usr/bin/env python3
import os
import subprocess
from util import *
download_path = "download"
tomcat_url="http://mirror.bit.edu.cn/apache/tomcat/tomcat-9/v9.0.6/bin/apache-tomcat-9.0.6.tar.gz"
tomcat_sha256_url="https://www.apache.org/dist/tomcat/tomcat-9/v9.0.6/bin/apache-tomcat-9.0.6.tar.gz.sha1"





def install_supervisor():
    cmd = ["pip2","install","supervisor"]
    run_command(cmd)



def config_tomcat_supervisor(user,java_home,catalina_home,catalina_base):
    '''

    :param java_home: The JRE_HOME variable is used to specify location of a JRE. The JAVA_HOME
                      variable is used to specify location of a JDK.
    :param catalina_home: tomcat install directory
    :param catalina_base: generally, same as catalina_home
    :return:
    '''
    supervisor_wrapper =\
"""#!/bin/bash
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
    supervisor_conf =\
"""[program:tomcat]
command={cmd_path}
process_name=%(program_name)s
directory={run_dir}
user={user}
redirect_stderr=true
stdout_logfile=/var/log/tomcat.log
""".format(cmd_path=os.path.join(catalina_home,'bin','supervisor-wrapper.sh'),run_dir=os.path.join(catalina_home),user=user)
    open(os.path.join(catalina_home,'bin','supervisor-wrapper.sh'),'w').write(supervisor_wrapper)
    open(os.path.join(catalina_home,'tomcat.conf'),'w').write(supervisor_conf)

#https://www.vultr.com/docs/how-to-install-apache-tomcat-8-on-centos-7
def create_tomcat_env(install_dir):
    run_command(["groupadd","tomcat"])
    run_command(["mkdir",install_dir])
    run_command(["useradd","-s","/bin/nologin","-g","tomcat","-d",install_dir,"tomcat"])

def setup_tomcat_dir(install_dir):
    run_command(["chgrp","-R","tomcat",os.path.join(install_dir,"conf")])
    run_command(["chmod","g+rwx",os.path.join(install_dir,"conf")])
    run_command(["chmod","g+r",os.path.join(install_dir,"conf/*")])
    run_command(["chown","-R","tomcat",os.path.join(install_dir,"logs"),os.path.join(install_dir,"temp"),os.path.join(install_dir,"webapps"),os.path.join(install_dir,"work")])
    run_command(["chgrp","-R","tomcat",os.path.join(install_dir,"bin")])
    run_command(["chgrp","-R","tomcat",os.path.join(install_dir,"lib")])
    run_command(["chmod","g+rwx",os.path.join(install_dir,"bin")])
    run_command(["chmod","g+r",os.path.join(install_dir,"bin/*")])

create_tomcat_env()
download_install(tar_url=tomcat_url,tar_sign_url=tomcat_sha256_url,download_path=os.path.join(os.getcwd(),download_path),install_path="/opt/tomcat")

create_tomcat_env("/opt/tomcat")
setup_tomcat_dir("/opt/tomcat")

install_supervisor()
config_tomcat_supervisor("tomcat","/usr/bin/java","/opt/tomcat","/opt/tomcat")
