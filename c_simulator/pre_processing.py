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

xhttpd_treepath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/search_tree'
ghttpd_treepath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/search_tree'
xhttpd_c_treepath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/c_search_tree'
ghttpd_c_treepath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/c_search_tree'

with open(xhttpd_treepath, 'r') as handle:
	xhttpd_search_tree = pickle.load(handle)

with open(ghttpd_treepath, 'r') as handle:
	ghttpd_search_tree = pickle.load(handle)

xhttpd_handle = open(xhttpd_c_treepath, 'a')
ghttpd_handle = open(ghttpd_c_treepath, 'a')


serialize(xhttpd_search_tree.root.fchild, xhttpd_handle)
serialize(ghttpd_search_tree.root.fchild, ghttpd_handle)

xhttpd_handle.close()
ghttpd_handle.close()
