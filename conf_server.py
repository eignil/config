import os
import subprocess
from util import *
from config import *

def install_uwsgi():
    pipenv_install("uwsgi")

def gen_uwsgi_conf():
    conf = '''
    [uwsgi]
    chdir={PROJECT_PATH}/{PROJECT_NAME}
    module={PROJECT_NAME}.wsgi:application
    env = LANG=en_US.UTF-8 DJANGO_SETTINGS_MODULE={PROJECT_NAME}.settings 
    master=True
    pidfile=/tmp/project-{PROJECT_NAME}-master.pid
    vacuum=True
    max-requests=5000
    daemonize=/var/log/uwsgi/{PROJECT_NAME}.log
    '''.format(PROJECT_PATH=PROJECT_PATH,PROJECT_NAME=PROJECT_NAME)

