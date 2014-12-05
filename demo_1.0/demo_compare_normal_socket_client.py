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

###################################################
def type_convert_ip(value):
	temp = value.split('.')
	for index, each in enumerate(temp):
		temp[index] = int(each)
	for i in range(0, 128-4):
		temp.append(0)
	print 'IP: ', value
	print temp
	return temp
#########################################################

def type_convert_string(value):
	return [int(each) for each in value]

##############################################################

def child_xhttpd(xhttpd_pipeout, connectip, data):
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
	pathdir = '/home/spark/workspace/spark/code_1024/cleaneffects/'
	for each in paths:
		lines = []
		with open(pathdir+each.split('.')[0]+'.pc', 'r') as handle:
			lines = handle.readlines()
		print '++++++++++++++++++++++++'
		print 'type action effect: '
		
		writepipe = []

		for eachline in lines:
			print eachline
			writepipe.append(eachline)
		print '++++++++++++++++++++++++'
		for line in lines:
			if 'unlink' in line:
				print '============================='
				print 'instantiation effect for unlink: '
				print 'sersymip: ', sersymip
				print 'connectip: ', connectip
				print 'symclient: ', symclient_xhttpd
				writepipe.append('file to be deleted: ' + str(symclient_xhttpd.split(':) ')[1]))
				print 'file to be deleted: ', symclient_xhttpd.split(':) ')[1]
				print '============================='
				break
		os.write(xhttpd_pipeout, "====\n".join(writepipe))		
	print 'Time for xhttpd simulator execution: ', (etime-stime).total_seconds()


############################################################################################################

def child_ghttpd(ghttpd_pipeout , data):
	print '\n\n'
	print 'SIMULATION BEGIN'
	writepipe = []

	conveted_data = type_convert_string(data)

	stime = datetime.now()

	paths = sim_ghttpd.simulate([conveted_data])
	etime = datetime.now()
	pathdir = '/home/spark/workspace/spark/code_1024/ghttpd/cleaneffects/'
	for each in paths:
		lines = []
		with open(pathdir+each.split('.')[0]+'.pc', 'r') as handle:
			lines = handle.readlines()
		print '++++++++++++++++++++++++'
		print 'type action effect: '
		for eachline in lines:
			writepipe.append(eachline)
			print eachline
		print '++++++++++++++++++++++++'
		os.write(ghttpd_pipeout, "====\n".join(writepipe))
	print 'Time for ghttpd simulator execution: ', (etime-stime).total_seconds()

###############################################################################################################

def send_request(ser_name, connectip, port, symclient):
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsocket.connect((connectip, port))

	# newsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# newsock.connect(('localhost', 10000))

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
	clientsocket.close()
	# newsock.close()



connectip = '192.168.1.160'
symclient_xhttpd = ''
symclient_ghttpd = ''

sim_xhttpd = Simulator.Simulator('xhttpd')
sim_ghttpd = Simulator.Simulator('ghttpd')

data = []

filelist = os.listdir('/home/spark/workspace/spark/code_1024/xhttpd/stosam')
for filelist_each in filelist:
	# time.sleep(2)
	with open('/home/spark/workspace/spark/code_1024/xhttpd/stosam/'+'test000289.pc', 'r') as handle:
		data = handle.read().split(', ')

	if len(data) < 16:
		continue

	intlist=[int(i) for i in data]
	chrlist=[chr(i) for i in intlist]

	
	
###################################################
	chrlist_xhttpd = list(chrlist)
	chrlist_xhttpd[-2] = '\n'
	chrlist_xhttpd[-3] = '\n'	

	print 'symclient_xhttpd', ''.join(chrlist_xhttpd)
	symclient_xhttpd = ''.join(chrlist_xhttpd)
###############################################################

	chrlist_ghttpd = list(chrlist)

	chrlist_ghttpd[8] = ' '
	chrlist_ghttpd[14] = '\n'
	chrlist_ghttpd[15] = '\n'
	print 'symclient_ghttpd', ''.join(chrlist_ghttpd)
	symclient_ghttpd = ''.join(chrlist_ghttpd)
##########################################################
	

	xhttpd_pipein, xhttpd_pipeout = os.pipe()	

	newpid = os.fork()

	# xhttpd ###################################################
	if newpid != 0:
		data_xhttpd = list(data)
		data_xhttpd[16] = str(ord(' '))
		data_xhttpd[17] = str(ord('a'))
		data_xhttpd[18] = str(ord('b'))
		data_xhttpd[19] = str(ord('c'))
		child_xhttpd(xhttpd_pipeout, connectip, data_xhttpd)
		break
	else:
		send_request('xhttpd', connectip, 8082, symclient_xhttpd)

		ghttpd_pipein, ghttpd_pipeout = os.pipe()	


		newpid = os.fork()




		# ghttpd ################################################\
		if newpid != 0:
			data_ghttpd = list(data)
			data_ghttpd[8] = '32'
			data_ghttpd[14] = '10'
			data_ghttpd[15] = '10'

			child_ghttpd(ghttpd_pipeout, data_ghttpd)
			break

		else:
			send_request('ghttpd', connectip, 8081, symclient_ghttpd)
			
			xhttpd_message=''
			ghttpd_message=''
			while True:
				if not xhttpd_message:
					xhttpd_message=os.read(xhttpd_pipein,4096)
				if not ghttpd_message:
					ghttpd_message=os.read(ghttpd_pipein,4096)

				if xhttpd_message and ghttpd_message:
					print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Message from simulation on xhttpd"
					print xhttpd_message
					print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Message from simulation on ghttpd"
					print ghttpd_message
					break	
			
			xhttpd_effects=xhttpd_message.split("====\n")
			ghttpd_effects=ghttpd_message.split("====\n")

			xhttpd_set=set(xhttpd_effects)
			ghttpd_set=set(ghttpd_effects)
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Same effects in ghttpd and xhttpd are:"
			print xhttpd_set.intersection(ghttpd_set)
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Different effects in ghttpd and xhttpd are:"
			print xhttpd_set.symmetric_difference(ghttpd_set)

			break
	