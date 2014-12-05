import cPickle as pickle
from cvc_parsing import constr_testing
from bitstring import BitArray
import sys
sys.path.append('/home/spark/workspace/github_simulator')
import cvc_function_in_python

class TNode:

	def __init__(self, pre, fat, ind):
		self.fchild		= None
		self.sibling	= None
		self.predicate	= pre
		self.father		= fat
		self.finalpath	= []
		self.index		= ind

class STree:

	def __init__(self, sig):
		self.node_index	= 0
		self.root		= self.addnode(None, None)
		self.signature	= sig
		self.search_finalpath = []
		self.searchcount= 0
		self.totalcount	= 0
		self.pretable	= dict()
		self.donesearch = False

	def addnode(self, pre, fat):
		self.node_index += 1
		return TNode(pre, fat, self.node_index-1)

	def insertnode(self, root, pre):
		if root is None:
			print 'insertnode: root is None'
			return
		elif root.fchild is None:
			root.fchild = self.addnode(pre, root)
			return root.fchild
		else:
			pointer = root.fchild
			while pointer.sibling is not None:
				pointer = pointer.sibling
			pointer.sibling = self.addnode(pre, root)
			return pointer.sibling

	def judge(self, pointer):
		if pointer is None:
			return None
		else:
			return pointer.index

	def dump_tree(self):
		self.rec_dump_tree(self.root.fchild, 1)

	def rec_dump_tree(self, root, layer):
		if root is not None:
			print 'layer: ', layer
		pointer = root
		while pointer is not None:
			print self.judge(pointer.father), pointer.index, pointer.predicate, self.judge(pointer.fchild)
			pointer = pointer.sibling

		pointer = root
		while pointer is not None:
			self.rec_dump_tree(pointer.fchild, layer+1)
			pointer = pointer.sibling

	def translate_constr_testing(self, result):
		if BitArray(result[1]).int == 1:
			return True
		else:
			return False

	# dummy function use to confirm code caching in CPU
	def dummy_function(self):
		a = 'string'
		for i in xrange(10000):
			a += 'string'
			a = 'string'

	def tree_search(self, predicates, value, var):
		# print predicates[0:10]
		self.searchcount = 0
		self.totalcount = 0
		self.search_finalpath = []
		self.donesearch = False
		self.pretable = dict()
		self.rec_tree_search(predicates, value, var, self.root.fchild)

	def rec_tree_search(self, predicates, value, var, root):
		# print 'inside rec_tree_search'
		# print 'root predicate: ', predicates[root.predicate]
		results = []
		pointer = root
		if pointer is None:
			return False
		while pointer is not None:
			# print 'tested predicate: ', pointer.predicate
			# print pointer.predicate[1]
			self.totalcount += 1
			temp = self.pretable.get(pointer.predicate)
			if temp is not None:
				results.append(temp)
			else:
				value_dict = dict()
				for ind, each in enumerate(var):
					value_dict[each] = value[ind]
				results.append(cvc_function_in_python.match_predicate(predicates[pointer.predicate][1], value_dict))

				# results.append(self.translate_constr_testing(constr_testing(value, ('pad', predicates[pointer.predicate][1]), var)))
				self.pretable[pointer.predicate] = results[-1]
				self.searchcount += 1
			##############################################
			if results[-1] == True:
				if self.rec_tree_search(predicates, value, var, pointer.fchild) == False:
					self.search_finalpath.extend(pointer.finalpath)
					self.donesearch = True
			if self.donesearch == True:
				return True
			else:
				pointer = pointer.sibling
			##############################################
		# 	pointer = pointer.sibling
		
		# pointer = root
		# for res_each in results:
		# 	if res_each == True:
		# 		if self.rec_tree_search(predicates, value, var, pointer.fchild) == False:
		# 			self.search_finalpath.extend(pointer.finalpath)
		# 	pointer = pointer.sibling
		##############################################
		return True


	def build_tree(self, paths):
		self.rec_build_tree(paths, self.root, 1)

	def rec_build_tree(self, paths, root, index):
		global predicates
		newpaths	= []
		newnodes	= []
		newpreds	= []

		# if index >= 3:
		# 	return

		if len(paths) != 0:
			# print len(paths)
			for paths_each in paths:
				# print paths_each
				# if paths_each[0] == '/home/spark/workspace/github_simulator/simulator_data/xhttpd/klee-out-22/test000001.cvc':
				# 	print '++++++++++'
				if len(paths_each) < index+1:
					return
				else:
					if paths_each[index] not in newpreds:
						newnode = self.insertnode(root, paths_each[index])
						newnodes.append(newnode)
						newpreds.append(paths_each[index])
						if len(paths_each) == index+1:
							newnode.finalpath.append(paths_each[0])
							newpaths.append([])
						else:
							newpaths.append([paths_each])
					else:
						if len(paths_each) == index+1:
							newnodes[newpreds.index(paths_each[index])].finalpath.append(paths_each[0])
						else:
							newpaths[newpreds.index(paths_each[index])].append(paths_each)
			
			# print newpaths
			# print len(newpaths)
			# print len(newnodes)
			# print len(newpreds), '\n'

			for newpaths_index, newpaths_each in enumerate(newpaths):
				self.rec_build_tree(newpaths[newpaths_index], newnodes[newpaths_index], index+1)
		


if __name__ == '__main__':

# =============================================================
	settings = 'lzfx'

	if settings == 'openaes':
		treesign = 'openaes_tree_1'
		predpath = '/home/spark/workspace/github_simulator/simulator_data/openaes/predicates'
		pathpath = '/home/spark/workspace/github_simulator/simulator_data/openaes/pathsindex'
		treepath = '/home/spark/workspace/github_simulator/simulator_data/openaes/search_tree'
	elif settings == 'xhttpd':
		treesign = 'xhttpd_tree_1'
		predpath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/predicates'
		pathpath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/pathsindex'
		treepath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/search_tree'
	elif settings == 'ghttpd':
		treesign = 'ghttpd_tree_1'
		predpath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/predicates'
		pathpath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/pathsindex'
		treepath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/search_tree'
	elif settings == 'lzfx':
		treesign = 'lzfx_tree_1'
		predpath = '/home/spark/workspace/github_simulator/simulator_data/lzfx/predicates'
		pathpath = '/home/spark/workspace/github_simulator/simulator_data/lzfx/pathsindex'
		treepath = '/home/spark/workspace/github_simulator/simulator_data/lzfx/search_tree'
	elif settings == 'wget':
		treesign = 'wget_tree_1'
		predpath = '/home/spark/workspace/github_simulator/simulator_data/wget/predicates'
		pathpath = '/home/spark/workspace/github_simulator/simulator_data/wget/pathsindex'
		treepath = '/home/spark/workspace/github_simulator/simulator_data/wget/search_tree'
	else:
		print 'ERROR: tree signature is wrong.'

# =============================================================

	with open(predpath, 'r') as handle:
		predicates = pickle.load(handle)

	with open(pathpath, 'r') as handle:
		pathsindex = pickle.load(handle)

	# print predicates
	# print pathsindex

	search_tree = STree(treesign)

	# xhttpd
	# search_tree.build_tree(pathsindex[:83903]+pathsindex[83905:])

	# ghttpd
	# search_tree.build_tree(pathsindex[:6023]+pathsindex[6025:])

	# lzfx
	search_tree.build_tree(pathsindex)

	# search_tree.build_tree(pathsindex)
	# print pathsindex[0]
	search_tree.dump_tree()

	with open(treepath, 'w') as handle:
	 	pickle.dump(search_tree, handle)
