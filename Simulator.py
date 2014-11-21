import os
import cPickle as pickle
import datetime as datetime
import sys
sys.path.append('/home/spark/workspace/github_simulator/preprocessing')
from build_tree import TNode
from build_tree import STree

class Simulator:
	# set up simulator configurations and start the simulator
	def __init__(self, signature):

		self.signature = signature

		if signature == 'openaes':
			self.var_name = ['A_data_0x2fb50b0']
			self.preddata = '/home/spark/workspace/github_simulator/simulator_data/openaes/predicates'
			self.funcdata = '/home/spark/workspace/github_simulator/simulator_data/openaes/pyfunctions'
			self.treedata = '/home/spark/workspace/github_simulator/simulator_data/openaes/search_tree'
			self.testpath = '/home/spark/workspace/github_simulator/simulator_data/openaes/stosam'
			# self.effcpath = '/home/spark/workspace/github_simulator/simulator_data/openaes/cleaneffects'
		elif signature == 'xhttpd':
			self.var_name = ['SERSYMIP_0x2e8c640', 'CONNECTIP_0x2ec4130', 'SymClient_0x2eaacd0']
			self.preddata = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/predicates'
			self.funcdata = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/pyfunctions'
			self.treedata = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/search_tree'
			self.testpath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/stosam'
			self.effcpath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/cleaneffects'
		elif signature == 'ghttpd':
			self.var_name = ['SymClient_0x37fc490']
			self.preddata = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/predicates'
			self.funcdata = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/pyfunctions'
			self.treedata = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/search_tree'
			self.testpath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/stosam'
			self.effcpath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/cleaneffects'
		elif signature == 'wget':
			self.var_name = ['SYMBOL_CLIENT_0x6ae64b0']
			self.preddata = '/home/spark/workspace/github_simulator/simulator_data/wget/predicates'
			self.funcdata = '/home/spark/workspace/github_simulator/simulator_data/wget/pyfunctions'
			self.treedata = '/home/spark/workspace/github_simulator/simulator_data/wget/search_tree'
			self.testpath = '/home/spark/workspace/github_simulator/simulator_data/wget/stosam'
			self.effcpath = '/home/spark/workspace/github_simulator/simulator_data/wget/cleaneffects'
		elif signature == 'lzfx':
			self.var_name = ['A_data_0x4326cd0']
			self.preddata = '/home/spark/workspace/github_simulator/simulator_data/lzfx/predicates'
			self.funcdata = '/home/spark/workspace/github_simulator/simulator_data/lzfx/pyfunctions'
			self.treedata = '/home/spark/workspace/github_simulator/simulator_data/lzfx/search_tree'
			self.testpath = '/home/spark/workspace/github_simulator/simulator_data/lzfx/stosam'
			self.effcpath = '/home/spark/workspace/github_simulator/simulator_data/lzfx/cleaneffects'
		else:
			print 'ERROR Simulator __init__: tree signature is wrong.'
			exit(0)

		# load configurations
		with open(self.funcdata, 'r') as handle:
			self.pyfunctions = pickle.load(handle)
			print 'Simulator __init__: python functions loaded.'

		with open(self.treedata, 'r') as handle:
			self.search_tree = pickle.load(handle)
			print 'Simulator __init__: search tree loaded.'

		# self.effects = dict()
		# filelist = os.listdir(self.effcpath)
		# for each in filelist:
		# 	with open(self.effcpath + '/' + each, 'r') as handle:
		# 		self.effects[each.split('.')[0]] = handle.read()
		# print 'Simulator __init__: effects loaded.'



	# find path to a concrete value and its effects
	def simulate(self, value):
		self.search_tree.tree_search(self.pyfunctions, value, self.var_name)
		print self.search_tree.search_finalpath
		try:
			return [self.search_tree.search_finalpath[0], effects[self.search_tree.search_finalpath[0].split('.')[0]]]
		except Exception, e:
			return []
		

	# format test data
	def format_test_data(self, handle):
		templist = handle.read().split(', ')
		return [int(each) for each in templist]

	# test on a single testfile in stosam dir. example: test000010.pc
	def testdata_single(self, filename):
		with open(self.testpath + '/' + filename, 'r') as handle:
			if self.signature == 'xhttpd':
				self.search_tree.tree_search(self.pyfunctions, [[192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], self.format_test_data(handle)], self.var_name)
			else:
				self.search_tree.tree_search(self.pyfunctions, [self.format_test_data(handle)], self.var_name)
				print self.search_tree.search_finalpath
		try:
			return [self.search_tree.search_finalpath[0], effects[self.search_tree.search_finalpath[0].split('.')[0]]]
		except Exception, e:
			return []

	# conduct test on all testfiles in stosam diir, and collect statistics. (ramdomly select 2000 if files are too many)
	def testdata_all(self):
		testfilelist = os.listdir(self.testpath)
		stime = datetime.now()
		for each in testfilelist:
			with open(testfilelist + '/' + each, 'r') as handle:
				if self.signature == 'xhttpd':
					self.search_tree.tree_search(self.pyfunctions, [[192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], self.format_test_data(handle)], self.var_name)
				else:
					self.search_tree.tree_search(self.pyfunctions, [self.format_test_data(handle)], self.var_name)
		etime = datetime.now()

		print (etime - stime).total_seconds() / len(testfilelist)


sim = Simulator('openaes')
print sim.testdata_single('test000003.pc')
