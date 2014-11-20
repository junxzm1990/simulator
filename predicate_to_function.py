import cPickle as pickle


# build python function for each predicate
def function_building():

	with open('test_data/openaes_predicates', r) as handle:
		predicates = pickle.load(handle)

	predicates[0]
