import sys
import os
import os.path
sys.path.append('/home/spark/workspace/github_simulator/')
sys.path.append('/home/spark/workspace/github_simulator/preprocessing/')

import cvc_function_in_python
import pre_processing_func

from datetime import datetime


def getallfiles(curdir):
	files = [f for f in os.listdir(curdir) if os.path.isfile(curdir+f)]
	return files



def modifylast(MYFILE):
	lines = open(MYFILE, 'r').read()
	intlist=lines.split(',')
	results = [int(i) for i in intlist]
	return results







def test_predicates(pypredicatepath,testcasepath):
	var1='SymClient_0x37fc490'
	pyfunctions = pre_processing_func.load_predicate(pypredicatepath)
	testcasefiles = getallfiles(testcasepath)
	
	cnt=0

	start = datetime.now()

	for eachcase in testcasefiles:
		case_array = modifylast(testcasepath+ eachcase)	
		for pyfunc in pyfunctions:
			variables = dict()
			variables[var1] = list(case_array)	
			pypredicate = pyfunc[1]
#			print pypredicate
			pypredicate = pypredicate.replace('A-data', 'A_data')
			print pypredicate


			cvc_function_in_python.match_predicate(pypredicate, variables)	
			cnt+=1

	end = datetime.now()
	
	c=end - start	
	print 'test ' + str(cnt) + ' matching uses ' + str((c.days * 24 * 60 * 60 + c.seconds) * 1000 + c.microseconds / 1000.0) +' microsecond'
	
	

test_predicates('/home/spark/workspace/simulator_data/ghttpd/pyfunctions', '/home/spark/workspace/simulator_data/ghttpd/stosam/' )

#test_predicates('/home/spark/workspace/simulator_data/openaes/pyfunctions', '/home/spark/workspace/simulator_data/openaes/stosam/' )















