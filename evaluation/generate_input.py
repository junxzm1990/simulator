import os

signature = 'ghttpd'

filelist = os.listdir('/home/spark/workspace/github_simulator/simulator_data/' + signature + '/stosam')

count = 0

for each in filelist:
	if each.endswith('.pc'):
		if count == 3000:
			break
		else:
			count += 1
		with open('/home/spark/workspace/github_simulator/simulator_data/' + signature + '/stosam/' + each, 'r') as handle:
			data = handle.read().split(', ')

		try:
			intlist = [int(i) for i in data]
			chrlist = [chr(i) for i in intlist]
		except:
			continue

		if len(data) < 16:
			continue
		if signature == 'xhttpd':
			chrlist[-1] = '\n'
			chrlist[-2] = '\r'
			chrlist[-3] = '\n'
		elif signature == 'ghttpd':
			chrlist[-1] = '\n'
			chrlist[-2] = '\n'
		# elif signature == 'lighttpd':
		# 	pass

		print each, chrlist
		with open('/home/spark/workspace/github_simulator/evaluation/data/' + signature, 'ab') as handle:
			handle.write(''.join(chrlist))