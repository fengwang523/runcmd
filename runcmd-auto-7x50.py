#!/usr/local/bin/python2.7
from os.path import expanduser
import sys

#import user defined module readpass.py
home = expanduser("~")
sys.path.append(home + "/python/lib")
import readpass 
import read_args
from runcmd import runcmd

if __name__ == '__main__':
    passwords = readpass.get_user_pass()
    username = passwords['default_user']
    password = passwords['default_pass']

    (devices, cmds, enable_mode, log, prnt) = read_args.read()
    if enable_mode:
        enable =  passwords[enable_mode]
    else:
        enable = False
   
    for device in devices:
        device = device.upper() 
        try:
            session = runcmd(device, username, password)
        except:
            print "!!!!skipping ", device, " due to error encountered!!!!\n"
            continue
        if log:
            sessionlog = home + "/log/" + device + ".log"
            logfile = open(sessionlog, 'wb')
            session.logfile=logfile
        else:
            logfile = None
        if prnt:
            session.prnt=prnt
        else:
            session.prnt=False
        if enable:
            session.enable_cmd(enable)
        for cmd in cmds:
            cmd = cmd.replace ("<HOSTNAME>", device)
            output=session.run_cmd (cmd, 600)

        if log:
            logfile.close()
        session.close()

