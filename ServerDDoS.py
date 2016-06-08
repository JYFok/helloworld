#!/usr/bin/env python 
#-*- coding:utf-8 -*- 
import threading
import socket
import struct
import fcntl
import time
import pexpect
import os
import binascii
'''
DDos Detection
c -> s
\x00\x00: exit
\x00\x01: start ddos detection
\x00\x02: stop ddos detection

s -> c
\x00\x10: error
\x00\x11: start ddos detection successfully
\x00\x12: stop ddos detection successfully

'''
def tcplink(sock, addr):
	print "Accept new connection from %s:%s..." % addr
	while True:
		data = sock.recv(1024)
		print "Recv data from client: " + binascii.b2a_hex(data)
		time.sleep(1)
		if data[0] != "\x00" or len(data)<2:	
			sock.send("\x00\x10")
			
			continue
		if data[1] == "\x00":
			break
		elif data[1] == "\x01":
			os.chdir("/home/flavia/blockmon/daemon")
			child = pexpect.spawn("python cli.py")
			child.expect("BM shell:")
			child.sendline("start ../usr/app_HXY/HXY.xml\r")
			print "start ddos detection..."
			sock.send("\x00\x11")
		elif data[1] == "\x02":
			if child:
				child.sendline("stop\t")
				child.sendline("exit\t")
				child.expect(pexpect.EOF)
				sock.send("\x00\x12")
				print "stop ddos detection."
			else:
				sock.send("\x00\x10")		
	sock.close()
	print "Connection from %s:%s closed." % addr

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ethname = "eth0"
	data = "\x00"
	data1 = 0x00
	print data,data1, "  ", data == data1
	ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(),0X8915,struct.pack('256s',ethname[:15]))[20:24])
	#ip = socket.gethostbyname(hostname)
	print "Current ip address: "+ip
	s.bind((ip, 10000))
	s.listen(5)
	print "Waiting for connection..."

	while True:
		# 接受一个新连接:
		sock, addr = s.accept()
		# 创建新线程来处理TCP连接:
		t = threading.Thread(target=tcplink, args=(sock, addr))
		t.start()
