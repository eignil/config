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

def ubuntu_install(package,para=None):
    cmd = ["apt","install"]
    if para:
        cmd.append(para)
    cmd.append(package)
    return run_command(cmd)

def centos_install(package,para=None):
    cmd = ["yum","install"]
    if para:
        cmd.append(para)
    cmd.append(package)
    return run_command(cmd)

def pipenv_install(package,para=None):
    cmd = ["pipenv","install"]
    if para:
        cmd.append(para)
    cmd.append(package)
    return run_command(cmd)


def run_command(cmd,shell=False,cwd=os.getcwd(),env=None):
    try:
        print(" ".join(cmd))
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=shell,cwd=cwd,env=env)
        out = proc.stdout.read().decode().strip()
        proc.stdout.close()

        err = proc.stderr.read().decode().strip()
        proc.stdout.close()

        if proc.wait() != 0:
            print("out:", out)
            print("err:", err)
            return False
        if err and out:
            return out +err
        if out:
            return out
        elif err:
            return err
        else:
            return True
    except Exception as ex:
        print(ex)
        return ex

def download(url,dir=os.getcwd(),file_name=None):
    if file_name:
        real_path = os.path.join(dir, file_name)
        if os.path.exists(real_path):
            _print("%s exist" % (real_path))
            return file_name
    if not os.path.exists(dir):
        os.makedirs(dir)
    print(dir)
    cmd = ['wget','-c','-nv','-t','3','-T','30']
    if file_name:
        cmd.extend(['-O',file_name,url])
    else:
        cmd.extend([url])

    env = os.environ.copy()
    out = run_command(cmd,shell=False, cwd=dir,env=env)
    print(out)
    if out and isinstance(out, str):
        _file_name = out.split('->')
        #print(file_name)
        _file_name = _file_name[1].split('"')
        print("Dowload:",_file_name)
        return _file_name[1]
        #print(file_name)
    else:
        return out


def verify_sig(file_path,sig,hash_type):
    hash_val = getattr(hashlib,hash_type)(open(file_path,'rb').read()).hexdigest()
    if sig.find(hash_val)>=0:
        print("%s Hash verified pass. %s"%(file_path,hash_val))
        return True
    else:
        print("Wrong hash.File hash %s, should be %s"%(hash_val,sig))
        return False

def download_install(tar_url,tar_name=None,tar_sign_url=None,tar_sign_name=None,download_path=os.getcwd(),install_path=os.getcwd()):

    tar_file_name = download(tar_url,download_path,tar_name)
    print(tar_file_name)
    if not tar_file_name:
        return False
    if tar_file_name == True:
        tar_file_name = os.path.basename(tar_url)
        print(tar_file_name)
        if not os.path.exists(os.path.join(download_path,tar_file_name)):
            return False
    if tar_sign_url:
        tar_sign_file_name = download(tar_sign_url,download_path,tar_sign_name)
        if tar_sign_file_name:
            print(tar_sign_file_name)
            if tar_sign_file_name == True:
                tar_sign_file_name = os.path.basename(tar_sign_url)
                print(tar_sign_file_name)
                if os.path.exists(os.path.join(download_path, tar_sign_file_name)):
                    hash_con = open(os.path.join(download_path,tar_sign_file_name)).read()
                    hash_type = os.path.splitext(tar_sign_file_name)[1].lower()
                    if not verify_sig(os.path.join(download_path,tar_file_name),hash_con,hash_type):
                        return False

    return run_command(['tar','-xf',os.path.join(download_path,tar_file_name),'-C',install_path,"--strip-components=1" ])
