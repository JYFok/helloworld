#!/usr/bin/env python 
#-*- coding:utf-8 -*- 
import pexpect
import os
import time

os.chdir("/home/flavia/blockmon/daemon")
child = pexpect.spawn("python cli.py")
child.expect("BM shell:")
child.sendline("start ../usr/app_HXY/HXY.xml\r")
print "start ddos detection..."

time.sleep(10)

child.sendline("stop\t")
child.sendline("exit\t")
#child.expect(pexpect.EOF)

