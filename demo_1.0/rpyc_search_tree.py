import cPickle as pickle
from build_tree import TNode
from build_tree import STree
import os
from datetime import datetime
import time

def rpyc_search_tree(tree_sig, input_val):

# =============================================================

	settings = tree_sig

	if settings == 'openaes':
		var_name = ['A-data_0x2fb50b0']
		predpath = '/home/spark/workspace/spark/code_1024/openaes/predicates'
		treepath = '/home/spark/workspace/spark/code_1024/openaes/search_tree'
		testpath = '/home/spark/workspace/spark/code_1024/openaes/stosam'
	elif settings == 'xhttpd':
		var_name = ['SERSYMIP_0x2e8c640', 'CONNECTIP_0x2ec4130', 'SymClient_0x2eaacd0']
		predpath = '/home/spark/workspace/spark/code_1024/xhttpd/predicates'
		treepath = '/home/spark/workspace/spark/code_1024/xhttpd/search_tree'
		testpath = '/home/spark/workspace/spark/code_1024/xhttpd/stosam'
	elif settings == 'ghttpd':
		var_name = ['SymClient_0x37fc490']
		predpath = '/home/spark/workspace/spark/code_1024/ghttpd/predicates'
		treepath = '/home/spark/workspace/spark/code_1024/ghttpd/search_tree'
		testpath = '/home/spark/workspace/spark/code_1024/ghttpd/stosam'
	else:
		print 'ERROR: tree signature is wrong.'

# =============================================================

	stime = datetime.now()
	with open(treepath, 'r') as handle:
		search_tree = pickle.load(handle)
	with open(predpath, 'r') as handle:
		predicates = pickle.load(handle)
	etime = datetime.now()
	# print 'TREE LOADING: ', (etime-stime).total_seconds()
	print 'TREE LOADED.'

	time.sleep(2)

	stime = datetime.now()
	search_tree.tree_search(predicates, input_val, var_name)

	etime = datetime.now()
	print 'SEARCHING TIME: ', (etime-stime).total_seconds()

	print (search_tree.search_finalpath, search_tree.searchcount)
	return (search_tree.search_finalpath, search_tree.searchcount)