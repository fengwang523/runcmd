#!/usr/local/bin/python2.7
import paramiko
import time
import re
import sys
import getopt
import os
import socket
from os.path import expanduser

#import user defined module readpass.py
home = expanduser("~")
sys.path.append(home + "/python/lib")
import readpass
import read_args

class runcmd:

    def __init__(self, device, username, password, logfile=None, prnt=True):
        self.device=device
        self.username=username
        self.password=password
        self.logfile=logfile
        self.prnt=prnt
        self.promptregex = "^\S*" + device.upper() + "\S*$"
        self.regex = ""
        self.max_buffer = 65535

        # Create instance of SSHClient object
        client = paramiko.SSHClient()
        # Automatically add untrusted hosts
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # initiate SSH connection
        try:
            client.connect(device, username=self.username, password=self.password, look_for_keys=False)
        except paramiko.AuthenticationException:
            print "\n!!!! ", device, " login failed !"
            print e
            sys.exit(2)
        except socket.error, e:
            print "\n!!!! ", device, " ssh socket failed !"
            print e
            sys.exit(2)
        except:
            print "\n!!!! ", device, " ssh failed !"
            sys.exit(2)
        # Use invoke_shell to establish an 'interactive session'
        try:
            self.shell = client.invoke_shell()
        except:
            print "\n!!!! ", device, " ssh invoke_shell failed!"
            sys.exit(2)
        self.shell.keep_this = client

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.shell.close()
        except:
            print "\n!!!! ", self.device, " can not close ssh session !"

    def enable_cmd (self, enable, enable_cmd='enable'):
        self.shell.send(enable_cmd)
        self.shell.send("\n")
        time.sleep (0.5)
        output = self.shell.recv(self.max_buffer)
        if self.logfile:
            self.logfile.write(output)
        if self.prnt:
            print output,
        self.shell.send(enable)
        self.shell.send("\n")
        time.sleep (0.5)
        output = self.shell.recv(self.max_buffer)
        if self.logfile:
            self.logfile.write(output)
        if self.prnt:
            print output,
        outputs = output.splitlines()
        lastline = outputs[-1].strip()
        if re.search(self.promptregex, lastline, re.I|re.M):
            self.prompt = lastline
        else:
            print "\n!!!! ", self.device, " enable failed, can not find cli prompt"
            sys.exit(2)
        for line in outputs:
            if re.search("(failed|sorry|denied|password|error|invalid)", line, re.I):
                print "\n!!!! ", self.device,  " enable failed: " , line
                sys.exit(2)

    def run_cmd (self, cmd, timeout=120):
        max_loop = 30000
        sleep = 0.1
        total_output = ''
        waited = 0
        waitfor = True
        output = ""
        i = 1
        self.shell.send(cmd)
        self.shell.send("\n")
        # Wait for the command to complete
        while (waitfor and i<=max_loop):
            if self.shell.recv_ready():
                output =  self.shell.recv(self.max_buffer)
                total_output += output
                if self.logfile:
                    self.logfile.write(output)
                if self.prnt:
                    print output,
                outputs = output.splitlines()
                lastline = outputs[-1].strip()
                if re.search(self.promptregex, lastline, re.M|re.I):
                    waitfor = False
                    self.prompt = lastline
                    break
                output = ''
            elif waited >= timeout:
                waitfor = False
                print "\n!!!! ", device, " ", cmd, " timed out!!"
                sys.exit(2)
            else:
                time.sleep(sleep)
                waited += sleep
                i += 1
        return (total_output)


if __name__ == '__main__':

    passwords = readpass.get_user_pass()
    username = passwords['default_user']
    password = passwords['default_pass']

    (devices, cmds, enable_mode, log, prnt) = read_args.read()
    enable =  passwords[enable_mode]

    for device in devices:
        session = runcmd(device, username, password)

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
        session.enable_cmd(enable)
        for cmd in cmds:
            cmd = cmd.replace ("<HOSTNAME>", device)
            output=session.run_cmd (cmd)

        if log:
            logfile.close()
        session.close()

    print "\n\n******************** Script Complete !*******************"

