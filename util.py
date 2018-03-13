#!/usr/bin/env python3
import os
import sys
import subprocess
import hashlib

def run_cmd(cmd,shell=False,env=os.environ.copy(),cwd=os.getcwd()):
    proc = subprocess.Popen(cmd,
                            env=env,
                            cwd=cwd,
                            shell=shell,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    cur = proc.stdout.read().strip()
    proc.stdout.close()
    err = proc.stderr.read()
    proc.stderr.close()

    if proc.wait() != 0 or err:
        print(proc.wait())
        print(cur)
        print(err)
        return False
    else:
        print(cur)
    return True

def download(dir,file_name,url):
    real_path = os.path.join(dir,file_name)
    if os.path.exists(real_path):
        print("%s is exist"%(real_path))
        return True
    if not os.path.exists(dir):
        os.mkdir(dir)
    cmd = 'wget' + ' --no-cookie'+' --no-check-certificate'+' -q'+' -c'+' -t3'+' -T60'+" -O "+file_name+' '+url
    return run_cmd(cmd,cwd=dir,shell=True)


def verify_sig(file_path,sig,hash_type):
    hash_val = getattr(hashlib,hash_type)(open(file_path,'rb').read()).hexdigest()
    if sig.find(hash_val)>=0:
        print("%s Hash verified pass. %s"%(file_path,hash_val))
        return True
    else:
        print("Wrong hash.File hash %s, should be %s"%(hash_val,sig))
        return False

    