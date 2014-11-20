import cPickle as pickle
import sys
sys.path.append('/home/spark/workspace/github_simulator/')
import cvc_to_python

########
def load_predicate(sourcefile):
	with open(sourcefile, 'r') as handle:
		return pickle.load(handle)
	
########
def save_predicate(destination_file, predicates):	
	with open(destination_file, 'w') as handle:
		pickle.dump(predicates, handle)	

###########
def generate_python_predicate(sourcefile, destinationfile):
	cvc_predicates=load_predicate(sourcefile)
	pyfunctions = []
	for each in cvc_predicates:
		pyfunctions.append((each[0], cvc_to_python.cvc_translate(each[1])))
	print pyfunctions
	save_predicate(destinationfile, pyfunctions)






#signature = 'openaes'
#
#if signature == 'openaes':
#	var_name = ['A-data_0x2fb50b0']
#	preddata = '/home/spark/workspace/simulator_data/openaes/predicates'
#	funcdata = '/home/spark/workspace/simulator_data/openaes/pyfunctions'
#elif signature == 'xhttpd':
#	var_name = ['SERSYMIP_0x2e8c640', 'CONNECTIP_0x2ec4130', 'SymClient_0x2eaacd0']
#	preddata = '/home/spark/workspace/simulator_data/xhttpd/predicates'
#	funcdata = '/home/spark/workspace/simulator_data/xhttpd/pyfunctions'
#elif signature == 'ghttpd':
#	var_name = ['SymClient_0x37fc490']
#	preddata = '/home/spark/workspace/simulator_data/ghttpd/predicates'
#	funcdata = '/home/spark/workspace/simulator_data/ghttpd/pyfunctions'
#elif signature == 'wget':
#	var_name = ['SYMBOL_CLIENT_0x6ae64b0']
#	preddata = '/home/spark/workspace/simulator_data/wget/predicates'
#	funcdata = '/home/spark/workspace/simulator_data/wget/pyfunctions'
#elif signature == 'lzfx':
#	var_name = ['A-data_0x4326cd0']
#	preddata = '/home/spark/workspace/simulator_data/lzfx/predicates'
#	funcdata = '/home/spark/workspace/simulator_data/lzfx/pyfunctions'
#else:
#	print 'ERROR Simulator __init__: tree signature is wrong.'
#	exit(0)
#
#with open(preddata, 'r') as handle:
#	predicates = pickle.load(handle)
#
#
#
#
#pyfunctions = []
#
#for each in predicates:
#	pyfunctions.append((each[0], cvc_to_python.test_translate(each[1])))
#
#with open(funcdata, 'w') as handle:
#	pickle.dump(pyfunctions)
