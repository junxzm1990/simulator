import sys
import os
from c_function_module import *


def binary(num, length=8):
	return format(num, '#0{}b'.format(length + 2))

###################################################
def pre_process_input(val):
	if type(val) is list:
		varlist=[]

		for i in range(0, len(val)):
			varlist.append(binary(val[i], 8))

		return varlist
	
	else:
		vardata = binary(val, 8)
		return vardata	


def  match_predicate(predicate, args):
	for k, v in args.items():
		# print k
		# print v
		var = pre_process_input(v)
#		print v
		exec(k+"=var")

	result=None
	predicate = 'result = bool(int2(' + predicate +'))'
	# predicate = 'result = ' + predicate


	# predicate = '''result = bool(int2(' + predicate +'))
	# print result
	# with open('/home/spark/workspace/newversion', 'a') as handle:
	# 	handle.write(str(result) + '\n')
	# '''

	exec(predicate)
	return result



# code="print notpy(((eqpy('0b1',extractpy('0b00000001' if int2(((eqpy('0b00001101',SYMBOL_CLIENT_0x6ae64b0[int2('0b00000000000000000000000000001')])))) else '0b00000000','0b00000000','0b00000000')))))"

# match_predicate(code, SYMBOL_CLIENT_0x6ae64b0=[0x01, 0x02, 0x03 ])


#print bvsxpy('0b010', '0b111')
#
#print bvltpy('0b10', '0b00')
#print bvltpy('0b11', '0b111')
#
#print concatpy('0b1110',concatpy('0b1001', '0b0001'))
#
# print match_predicate('''(bvsxpy(SymClient_0x2eaacd0[int2('0b00000000000000000000000000000100')],'0b00100000'),'0b00000000000000000000000000000000')''', {'SERSYMIP_0x2e8c640': [192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'SymClient_0x2eaacd0': [71, 69, 84, 223, 197, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'CONNECTIP_0x2ec4130': [192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})
