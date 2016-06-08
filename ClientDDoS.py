#!/usr/bin/env python 
#-*- coding:utf-8 -*- 
import binascii
import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('10.128.128.11', 10000))

#start
s.send('\x00\x01')
d = s.recv(1024)
print "Recv data from server: " + binascii.b2a_hex(d)
time.sleep(20)
#stop
s.send('\x00\x02')
d = s.recv(1024)
print "Recv data from server: " + binascii.b2a_hex(d)
#exit
s.send('\x00\x00')
s.close()
