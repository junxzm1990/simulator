import cPickle as pickle

def func_generate(program, pyfunc, handle):
	handle.write('#include "c_functions/c_primitives.h"\n')
	handle.write('#include "c_functions/global.h"\n\n')
	if program == 'openaes':
		handle.write('char* A_data_0x2fb50b0[VALUE_LENGTH];\n\n')
	elif program == 'xhttpd':
		handle.write('char* CONNECTIP_0x2ec4130[VALUE_LENGTH];\n')
		handle.write('char* SERSYMIP_0x2e8c640[VALUE_LENGTH];\n')
		handle.write('char* SymClient_0x2eaacd0[VALUE_LENGTH];\n\n')
	elif program == 'ghttpd':
		handle.write('char* SymClient_0x37fc490[VALUE_LENGTH];\n\n')
	elif program == 'wget':
		handle.write('char* SYMBOL_CLIENT_0x6ae64b0[VALUE_LENGTH];\n\n')
	elif program == 'lzfx':
		handle.write('char* A_data_0x4326cd0[VALUE_LENGTH];\n\n')
	for each in pyfunc:
		handle.write('bool ' + program + '_pre_' + str(each[0]) + '()\n{\n')
		handle.write('\t' + 'return (bool)(int2(' + each[1].replace('"', '').replace('\'', '"') + '));\n')
		handle.write('}\n\n')

	# modify global.h on modification!
	handle.write('void ' + program + '_funcptr(funcptr* ptrarray)\n{\n')
	for each in pyfunc:
		handle.write('\tptrarray[' + str(each[0]) + '] = &'  + program + '_pre_' + str(each[0]) + ';\n')
	handle.write('}\n\n')


openaes_funcpath = '/home/spark/workspace/github_simulator/simulator_data/openaes/pyfunctions'
xhttpd_funcpath = '/home/spark/workspace/github_simulator/simulator_data/xhttpd/pyfunctions'
ghttpd_funcpath = '/home/spark/workspace/github_simulator/simulator_data/ghttpd/pyfunctions'
openaes_c_funcpath = '/home/spark/workspace/github_simulator/c_simulator/c_functions/openaes_c_predicates.cpp'
xhttpd_c_funcpath = '/home/spark/workspace/github_simulator/c_simulator/c_functions/xhttpd_c_predicates.cpp'
ghttpd_c_funcpath = '/home/spark/workspace/github_simulator/c_simulator/c_functions/ghttpd_c_predicates.cpp'


with open(openaes_funcpath, 'r') as handle:
	openaes_pyfunctions = pickle.load(handle)

with open(xhttpd_funcpath, 'r') as handle:
	xhttpd_pyfunctions = pickle.load(handle)

with open(ghttpd_funcpath, 'r') as handle:
	ghttpd_pyfunctions = pickle.load(handle)

openaes_handle = open(openaes_c_funcpath, 'a')
xhttpd_handle = open(xhttpd_c_funcpath, 'a')
ghttpd_handle = open(ghttpd_c_funcpath, 'a')

func_generate('openaes', openaes_pyfunctions, openaes_handle)
func_generate('xhttpd', xhttpd_pyfunctions, xhttpd_handle)
func_generate('ghttpd', ghttpd_pyfunctions, ghttpd_handle)