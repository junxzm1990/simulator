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

def save_mentiondict(destination_file, mentiondict):	
	with open(destination_file, 'w') as handle:
		pickle.dump(mentiondict, handle)	

###########
def generate_python_predicate(sourcefile, destinationfile):
	cvc_predicates=load_predicate(sourcefile)
	pyfunctions = []
	mentiondict = []

	if sourcefile.find('xhttpd') > 0:
		multiflag = True
	else:
		multiflag = False

	for each in cvc_predicates:
		cvc_to_python.mentiondict = dict()
		pyfunctions.append((each[0], cvc_to_python.cvc_translate(each[1].replace('A-data', 'A_data'))))
		if multiflag:
			temp = [[], [], []]
			temp[0] = cvc_to_python.mentiondict.get('SERSYMIP_0x2e8c640') if cvc_to_python.mentiondict.get('SERSYMIP_0x2e8c640') is not None else []
			temp[1] = cvc_to_python.mentiondict.get('CONNECTIP_0x2ec4130')if cvc_to_python.mentiondict.get('CONNECTIP_0x2ec4130') is not None else []
			if cvc_to_python.mentiondict.get('SymClient_0x2eaacd0') is not None:
				temp[2] = cvc_to_python.mentiondict.get('SymClient_0x2eaacd0')
			mentiondict.append((each[0], temp, dict()))
		else:
			mentiondict.append((each[0], cvc_to_python.mentiondict.values(), dict()))



	# print pyfunctions
	save_predicate(destinationfile, pyfunctions)

	mentiondictfile = destinationfile.split('/')
	mentiondictfile[-1] = 'mentiondict'
	mentiondictfile = '/'.join(mentiondictfile)
	print mentiondict

	save_mentiondict(mentiondictfile, mentiondict)





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
