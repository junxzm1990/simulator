import socket
import sys
sys.path.append('/home/spark/workspace/github_simulator')
sys.path.append('/home/spark/workspace/github_simulator/preprocessing')
import Simulator
from build_tree import TNode
from build_tree import STree
import os
import time
from datetime import datetime
import errno

symclient = ''

def type_convert_ip(value):
	temp = value.split('.')
	for index, each in enumerate(temp):
		temp[index] = int(each)
	for i in range(0, 128-4):
		temp.append(0)
	print 'IP: ', value
	print temp
	return temp

def type_convert_string(value):
	return [int(each) for each in value]

def child(connectip, data):
	global symclient
	print '\n\n'

	print 'SIMULATION BEGIN'
	with open('/home/spark/workspace/spark/code_1024/currentIP', 'r') as handle:
		sersymip = handle.readline()


	converted_sersymip = type_convert_ip(sersymip)
	converted_connectip = type_convert_ip(connectip)
	conveted_data = type_convert_string(data)

	stime = datetime.now()

	paths = sim_xhttpd.simulate([converted_sersymip, converted_connectip, conveted_data])
	etime = datetime.now()
	print 'Time for simulator execution: ', (etime-stime).total_seconds()

	pathdir = '/home/spark/workspace/spark/code_1024/cleaneffects/'
	for each in paths:
		lines = []
		with open(pathdir+each.split('.')[0]+'.pc', 'r') as handle:
			lines = handle.readlines()
		print '++++++++++++++++++++++++'
		print 'type action effect: '
		for eachline in lines:
			print eachline
		print '++++++++++++++++++++++++'
		for line in lines:
			if 'unlink' in line:
				print '============================='
				print 'instantiation effect for unlink: '
				print 'sersymip: ', sersymip
				print 'connectip: ', connectip
				print 'symclient: ', symclient
				print 'file to be deleted: ', symclient.split(':) ')[1]
				print '============================='
				break
 



print 'in demo_delete_socket_client'
connectip = '192.168.1.161'

sim_xhttpd = Simulator.Simulator('xhttpd')

data = []

filelist = os.listdir('/home/spark/workspace/spark/code_1024/xhttpd/stosam')
for filelist_each in filelist:
	# time.sleep(2)
	with open('/home/spark/workspace/spark/code_1024/xhttpd/stosam/'+'test096941.pc', 'r') as handle:
		data = handle.read().split(', ')

	if len(data) < 16:
		continue

	intlist=[int(i) for i in data]
	chrlist=[chr(i) for i in intlist]
	chrlist[-2] = '\n'
	chrlist[-3] = '\n'
	chrlist[16] = ' '
	chrlist[17] = 'a'
	chrlist[18] = 'b'
	chrlist[19] = 'c'		

	print ''.join(chrlist)
	symclient = ''.join(chrlist)

	newpid = os.fork()

	if newpid != 0:
		data[16] = str(ord(' '))
		data[17] = str(ord('a'))
		data[18] = str(ord('b'))
		data[19] = str(ord('c'))
		child(connectip, data)
		break
	else:
		

		clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# newsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# newsock.connect(('localhost', 10000))

		try:
			clientsocket.connect((connectip, 8082))
		except socket.error, v:
			errorcode=v[0]
			if errorcode==errno.ECONNREFUSED:
				newsock.sendall("Connection Refused: no route to host")
			break

		

		stime = datetime.now()
		clientsocket.sendall(symclient)
		while 1:
			a=clientsocket.recv(4096)
			if a:
				print a
				# newsock.sendall(a)
			else:
				break
		etime = datetime.now()
		# newsock.sendall('Time for real system execution: ' + str((etime-stime).total_seconds()))

		# newsock.close()
		clientsocket.close()
		break

	



