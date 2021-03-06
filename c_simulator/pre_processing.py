import cPickle as pickle
import sys
sys.path.append('/home/spark/workspace/github_simulator/preprocessing')
from build_tree import TNode
from build_tree import STree

def serialize(node, handle):
	if node != None:
		serialize_node(node, handle)
		serialize(node.fchild, handle)
		serialize(node.sibling, handle)
	else:
		handle.write("-1\n")

def serialize_node(node, handle):
	handle.write("%d\n" % node.predicate)
	handle.write("%s\n" % ' '.join(node.finalpath))

openaes_treepath = '/home/spark/workspace/github_simulator/simulator_data/openaes/search_tree'
xhttpd_treepath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/search_tree'
ghttpd_treepath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/search_tree'
lighttpd_treepath = '/home/spark/workspace/github_simulator/simulator_data/lighttpd/search_tree'
openaes_c_treepath = '/home/spark/workspace/github_simulator/simulator_data/openaes/c_search_tree'
xhttpd_c_treepath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/c_search_tree'
ghttpd_c_treepath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/c_search_tree'
lighttpd_c_treepath = '/home/spark/workspace/github_simulator/simulator_data/lighttpd/c_search_tree'


# with open(openaes_treepath, 'r') as handle:
# 	openaes_search_tree = pickle.load(handle)

# with open(xhttpd_treepath, 'r') as handle:
# 	xhttpd_search_tree = pickle.load(handle)

# with open(ghttpd_treepath, 'r') as handle:
# 	ghttpd_search_tree = pickle.load(handle)

with open(lighttpd_treepath, 'r') as handle:
	lighttpd_search_tree = pickle.load(handle)

# openaes_handle = open(openaes_c_treepath, 'a')
# xhttpd_handle = open(xhttpd_c_treepath, 'a')
# ghttpd_handle = open(ghttpd_c_treepath, 'a')
lighttpd_handle = open(lighttpd_c_treepath, 'a')


# serialize(openaes_search_tree.root.fchild, openaes_handle)
# serialize(xhttpd_search_tree.root.fchild, xhttpd_handle)
# serialize(ghttpd_search_tree.root.fchild, ghttpd_handle)
serialize(lighttpd_search_tree.root.fchild, lighttpd_handle)


# openaes_handle.close()
# xhttpd_handle.close()
# ghttpd_handle.close()
lighttpd_handle.close()
