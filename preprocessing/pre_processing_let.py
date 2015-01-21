import os
import re

def get_files(dir):
	files = [(dir+f) for f in os.listdir(dir) if f.endswith('.cvc')]
	return files

# =============================================================

settings = 'lighttpd'

if settings == 'lzfx':
	var_name = ['A-data_0x4326cd0']
	cvcfiledir = '/home/spark/workspace/github_simulator/simulator_data/lzfx/klee-out-33/'
elif settings == 'wget':
	var_name = ['SYMBOL_CLIENT_0x6ae64b0']
	cvcfiledir = '/home/spark/workspace/github_simulator/simulator_data/wget/klee-out-28/'
elif settings == 'lighttpd':
	var_name = ['readsym_1_0xabc7b20']
	cvcfiledir = '/home/spark/workspace/github_simulator/simulator_data/lighttpd/klee-out-5/'	
else:
	print 'ERROR: tree signature is wrong.'

# =============================================================

cvcfiles = get_files(cvcfiledir)

for cvcfile in cvcfiles:
	data = ''
	with open(cvcfile, 'r') as handle:
		data = handle.read()
	constrs = data.split(';')
	temp = []

	# # old version
	# for constr in constrs:
	# 	index = []
	# 	for m in re.finditer('LET let_k_[0-9]+', constr):
	# 		index.append(m.end())
	# 	for each in reversed(index):
	# 		constr = constr[:each+2] + '=' + constr[each+2:]
	# 	temp.append(constr)
	# #print temp
	# data = ';'.join(temp)
	# with open(cvcfile, 'w') as handle:
	# 	handle.write(data)

	# new version
	for constr in constrs:
		# print constr, '\n\n\n\n'
		index = []
		for m in re.finditer('LET (.*) IN', constr, re.DOTALL):
			print 'm', m.start()
			for mm in re.finditer('let_k_[0-9]+ =', m.group(1), re.DOTALL):
				print 'mm', mm.end()
				index.append(m.start()+mm.end())
		for each in reversed(index):
			constr = constr[:each+4] + '=' + constr[each+4:]
		temp.append(constr)
	#print temp
	data = ';'.join(temp)
	with open(cvcfile, 'w') as handle:
		handle.write(data)