import os
import collections
import re
import cPickle as pickle

# get .cvc file in path
def get_files(dir):
	files = [(dir+f) for f in os.listdir(dir) if f.endswith('.cvc')]
	return files

# build index based on path constrants
def build_index(f):
	global pathsindex
	global constraints
	global varindex
	global var_name

	pathindex = [f.split('/')[-1]]

	handle = open(f, 'r')
	data = handle.read()
	handle.close()

	constrs = data.split(';')

	index = 0

	for constr in constrs:
		if not 'ASSERT' in constr:
			continue
		# TODO only this kind of variable is included
		temp = False
		for each in var_name:
			if each in constr:
				temp = True
				break
		if temp == False:
			continue
		if constraints.has_key(constr):
			constraints[constr] += 1
		else:
			constraints.update({constr: 1})

			# get the variables inside the constant
			var = re.findall(r'[a-zA-Z][_a-zA-Z0-9-]*\[0x[a-fA-F0-9]+\]', constr)

			if var != []:
				varindex_appending(tuple(var), index)
			index += 1

		pathindex.append(constraints.keys().index(constr))

	#stat_index(varindex, constraints)

	pathsindex.append(sort_path(pathindex, 1))



# calculate the number of variable index
def stat_index(varindex, constrants):
	for each in varindex:
		temp = 0
		for i in varindex[each]:
			temp += constraints.items()[i][1]
		varindex[each].append(temp)

	# print varindex


# append new variable index if it is newly meet
def varindex_appending(var, index):
	global varindex

	if not varindex.get(var):
		varindex[var] = []

	varindex[var].append(index)



# sort path constraints index, so that we have an ordered list for future matching
def sort_path(pathindex, bpoint):

	for i in range(bpoint, len(pathindex)):
		for j in range(i+1, len(pathindex)):
			if pathindex[i] > pathindex[j]:
				temp = pathindex[i]
				pathindex[i] = pathindex[j]
				pathindex[j] = temp

	return pathindex

# generate path constraint ranking by their count order
def constr_ranking():
	global constraints
	global pathsindex

	# rank constraints based on their counts
	order = range(len(constraints))
	for i in range(0, len(constraints)):
		for j in range(i+1, len(constraints)):
			if constraints.items()[order[i]][1] > constraints.items()[order[j]][1]:
				temp = order[i]
				order[i] = order[j]
				order[j] = temp

	#print order
	return order


# =============================================================

def tree_building(path_remain, constrs_dic, var_dic):
	global pathsindex



# =============================================================


# =============================================================

settings = 'lzfx'

if settings == 'openaes':
	var_name = ['A-data_0x2fb50b0']
	filedir = '/home/spark/workspace/github_simulator/simulator_data/openaes/'
	cvcfiledir = '/home/spark/workspace/github_simulator/simulator_data/openaes/klee-out-11/'
elif settings == 'xhttpd':
	var_name = ['SERSYMIP_0x2e8c640', 'CONNECTIP_0x2ec4130', 'SymClient_0x2eaacd0']
	filedir = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/'
	cvcfiledir = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/klee-out-22/'
elif settings == 'ghttpd':
	var_name = ['SymClient_0x37fc490']
	filedir = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/'
	cvcfiledir = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/klee-out-4/'
elif settings == 'lzfx':
	var_name = ['A-data_0x4326cd0']
	filedir = '/home/spark/workspace/github_simulator/simulator_data/lzfx/'
	cvcfiledir = '/home/spark/workspace/github_simulator/simulator_data/lzfx/klee-out-33/'
elif settings == 'wget':
	var_name = ['SYMBOL_CLIENT_0x6ae64b0']
	filedir = '/home/spark/workspace/github_simulator/simulator_data/wget/'
	cvcfiledir = '/home/spark/workspace/github_simulator/simulator_data/wget/klee-out-28/'
else:
	print 'ERROR: tree signature is wrong.'

# =============================================================


files = get_files(cvcfiledir)

# list of paths: each element represents for the index for each path
pathsindex = []

# ordered dictionary of index: each element represents for a path constraint and its count
constraints = collections.OrderedDict()

# dictionary of path constraint variable and corrsponding index in constraints
varindex = {}

# statistics
for f in files:
	build_index(f)

# generate order
order = constr_ranking()

#print constraints
# print pathsindex
#print constraints.items()


predicates = constraints.keys()

indexed_predicates = []

index = 0
for each in predicates:
	indexed_predicates.append((index, each))
	index += 1

# write to files

handle = open(filedir+'predicates', 'w')
pickle.dump(indexed_predicates, handle)
handle.close()

with open(filedir+'raw_pathsindex', 'w') as handle:
	handle.write(str(pathsindex))

handle = open(filedir+'pathsindex', 'w')
pickle.dump(pathsindex, handle)
handle.close()
