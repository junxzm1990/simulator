import os

signature = 'ghttpd'

filelist = os.listdir('/home/spark/workspace/github_simulator/simulator_data/' + signature + '/stosam')

for each in filelist:
	if each.endswith('.pc'):
		with open('/home/spark/workspace/github_simulator/simulator_data/' + signature + '/stosam/' + each, 'r') as handle:
			data = handle.read().split(', ')

		intlist = [int(i) for i in data]
		chrlist = [chr(i) for i in intlist]

		if len(data) < 16:
			continue
		if signature == 'xhttpd':
			chrlist[-2] = '\n'
			chrlist[-3] = '\n'
		elif signature == 'ghttpd':
			chrlist[8] = ' '
			chrlist[14] = '\n'
			chrlist[15] = '\n'
		elif signature == 'lighttpd':
			pass

		with open('/home/spark/workspace/github_simulator/evaluation/data/' + signature, 'ab') as handle:
			handle.write(''.join(chrlist))