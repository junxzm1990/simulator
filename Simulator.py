import os


class Simulator:
	# set up simulator configurations and start the simulator
	def __init__(self, signature):

		if signature == 'openaes':
			var_name = ['A-data_0x2fb50b0']
			preddata = '/home/spark/workspace/simulator_data/openaes/predicates'
			funcdata = '/home/spark/workspace/simulator_data/openaes/pyfunctions'
			treedata = '/home/spark/workspace/simulator_data/openaes/search_tree'
			testpath = '/home/spark/workspace/simulator_data/openaes/stosam'
			effcpath = '/home/spark/workspace/simulator_data/openaes/cleaneffects'
		elif signature == 'xhttpd':
			var_name = ['SERSYMIP_0x2e8c640', 'CONNECTIP_0x2ec4130', 'SymClient_0x2eaacd0']
			preddata = '/home/spark/workspace/simulator_data/xhttpd/predicates'
			funcdata = '/home/spark/workspace/simulator_data/xhttpd/pyfunctions'
			treedata = '/home/spark/workspace/simulator_data/xhttpd/search_tree'
			testpath = '/home/spark/workspace/simulator_data/xhttpd/stosam'
			effcpath = '/home/spark/workspace/simulator_data/xhttpd/cleaneffects'
		elif signature == 'ghttpd':
			var_name = ['SymClient_0x37fc490']
			preddata = '/home/spark/workspace/simulator_data/ghttpd/predicates'
			funcdata = '/home/spark/workspace/simulator_data/ghttpd/pyfunctions'
			treedata = '/home/spark/workspace/simulator_data/ghttpd/search_tree'
			testpath = '/home/spark/workspace/simulator_data/ghttpd/stosam'
			effcpath = '/home/spark/workspace/simulator_data/ghttpd/cleaneffects'
		elif signature == 'wget':
			var_name = ['SYMBOL_CLIENT_0x6ae64b0']
			preddata = '/home/spark/workspace/simulator_data/wget/predicates'
			funcdata = '/home/spark/workspace/simulator_data/wget/pyfunctions'
			treedata = '/home/spark/workspace/simulator_data/wget/search_tree'
			testpath = '/home/spark/workspace/simulator_data/wget/stosam'
			effcpath = '/home/spark/workspace/simulator_data/wget/cleaneffects'
		elif signature == 'lzfx':
			var_name = ['A-data_0x4326cd0']
			preddata = '/home/spark/workspace/simulator_data/lzfx/predicates'
			funcdata = '/home/spark/workspace/simulator_data/lzfx/pyfunctions'
			treedata = '/home/spark/workspace/simulator_data/lzfx/search_tree'
			testpath = '/home/spark/workspace/simulator_data/lzfx/stosam'
			effcpath = '/home/spark/workspace/simulator_data/lzfx/cleaneffects'
		else:
			print 'ERROR Simulator __init__: tree signature is wrong.'
			exit(0)

		# load configurations
		with open(funcdata, 'r') as handle:
			pyfunctions = pickle.load(handle)
			print 'Simulator __init__: python functions loaded.'

		with open(treedata, 'r') as handle:
			search_tree = pickle.load(handle)
			print 'Simulator __init__: search tree loaded.'

		effects = dict()
		filelist = os.listdir(effcpath)
		for each in filelist:
			with open(effcpath + '/' + each, 'r') as handle:
				effects[each.split('.')[0]] = handle.read()



	def simulate(value):
		