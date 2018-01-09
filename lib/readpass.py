#!/usr/local/bin/python2.7
import re
import os
from os.path import expanduser

def get_user_pass():
    home = expanduser("~")
    passwords = {}
    myfile = open(home + '/.runcmd.passwd', 'r')
    for line in myfile.readlines():
        s = re.search (r'default_user *= *(\w+)', line)
        if s:
            passwords["default_user"] = s.group(1)
        s = re.search ("default_pass *= *(\S+)", line)
        if s:
            passwords["default_pass"] = s.group(1)
        s = re.search ("edge_enable *= *(\S+)", line)
        if s:
            passwords["edge_enable"] = s.group(1)
        s = re.search ("core_enable *= *(\S+)", line)
        if s:
            passwords["core_enable"] = s.group(1)
    myfile.close()
    return passwords;

if __name__ == '__main__':
    passwords = get_user_pass()
    for item in passwords:
        print item, " is ", passwords[item]

