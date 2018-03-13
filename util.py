#!/usr/bin/env python3
import os
import sys
import subprocess
import hashlib

def _print(*objects, **kwargs):
  sep = kwargs.get('sep', ' ')
  end = kwargs.get('end', '\n')
  out = kwargs.get('file', sys.stdout)
  out.write(sep.join(objects) + end)

def run_command(cmd,shell=False,cwd=os.getcwd(),env=os.environ.copy()):
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell,cwd=cwd,env=env)
    out = proc.stdout.read().decode()
    proc.stdout.close()

    err = proc.stderr.read().decode()
    proc.stdout.close()

    if proc.wait() != 0 or err.strip()!="":
        _print(out, file=sys.stderr)
        _print(err, file=sys.stderr)
        return False
    if out:
        return out
    else:
        return True

def download(url,dir,file_name=None):
    if file_name:
        real_path = os.path.join(dir, file_name)
        if os.path.exists(real_path):
            _print("%s exist" % (real_path))
            return True
    if not os.path.exists(dir):
        os.makedirs(dir)
    if file_name:
        cmd = 'wget' + ' --no-cookie'+' --no-check-certificate'+' -q'+' -c'+' -nv'+' -t3'+' -T60'+" -O "+file_name+' '+url
    else:
        cmd = 'wget' + ' --no-cookie'+' --no-check-certificate'+' -q' + ' -c' + ' -nv' + ' -t3' + ' -T60' + ' ' + url
    out = run_command(cmd, cwd=dir)
    print(out)
    if out and isinstance(out, str):
        file_name = out.split('->')[1]
        file_name = file_name.split('"')
        print(file_name)
    else:
        return out
    return run_command(cmd,cwd=dir,shell=True)


def verify_sig(file_path,sig,hash_type):
    hash_val = getattr(hashlib,hash_type)(open(file_path,'rb').read()).hexdigest()
    if sig.find(hash_val)>=0:
        print("%s Hash verified pass. %s"%(file_path,hash_val))
        return True
    else:
        print("Wrong hash.File hash %s, should be %s"%(hash_val,sig))
        return False

    