import os

filelist = os.listdir('/home/spark/workspace/github_simulator/simulator_data/xhttpd/stosam')

for each in filelist:
	if each.endswith('.pc'):
		with open('/home/spark/workspace/github_simulator/simulator_data/xhttpd/stosam/'+each, 'r') as handle:
			data = handle.read().split(', ')

		if len(data) < 16:
			continue

		intlist = [int(i) for i in data]
		chrlist = [chr(i) for i in intlist]
		chrlist[-2] = '\n'
		chrlist[-3] = '\n'

		with open('/home/spark/workspace/github_simulator/evaluation/data/xhttpd', 'ab') as handle:
			handle.write(''.join(chrlist))