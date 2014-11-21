import cPickle as pickle

def load_predicates(predfile):
	with open(predfile, 'r') as handle:
		predicates = pickle.load(handle)
	return [each[1] for each in predicates]

	# with open(file_to_write, 'w') as handle:
	# 	pickle.dump(data_to_write, handle)