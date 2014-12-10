import sys
import os

############
# transform a integer into binary with padded zeros
def binary(num, length=8):
	return format(num, '#0{}b'.format(length + 2))

############
#check if a string is in binary format
def check2(val):
	print 'check2() input: ', type(val), val
	try:
		int(val, base=2)
		print 'check2() output: ', type(True), True
		return True
	except ValueError:
		print val + 'is not in the binary format (with 0b as prefix)'
		print 'check2() output: ', type(False), False
		return False

###############
#transform a binary string into integer
def int2(val):
	print 'int2() input: ', type(val), val
	print 'int2() output: ', type(int(val, base=2)), int(val, base=2)
	return int(val, base=2)

def sint2(val):
	print 'sint2() input: ', type(val), val
	length = len(val)-2
	if int2(val) < pow(2, length-1):
		print 'sint2() output: ', type(int2(val)), int2(val)
		return int2(val)
	else:
		print 'sint2() output: ', type(-(pow(2, length)-int2(val))), -(pow(2, length)-int2(val))
		return -(pow(2, length)-int2(val))

#######################################
def eqpy(val1, val2):
	print 'eqpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)

	maxlen = max (len(val1)-2, len(val2)-2)
	if int2(val1) == int2(val2):
	
		# print 'equal: ' + binary(1,maxlen)
		print 'eqpy() output: ', type(binary(1, maxlen)), binary(1, maxlen)
		return binary(1, maxlen)
	else:
		# print 'not equal: ' + binary(0,maxlen) 
		print 'eqpy() output: ', type(binary(0, maxlen)), binary(0, maxlen)
		return binary(0, maxlen)
	

###############################################
def extractpy(val1, val2, val3):
	print 'extractpy() input: ', type(val1), val1, type(val2), val2, type(val3), val3
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	if not check2(val3):
		sys.exit(1)
		print val3 + 'is not in the binary format (with 0b as prefix)'

	start =  int2(val3)
	end = int2(val2)

	if start ==0:
		val=val1[-end-1:]

	else:
		val=val1[-end-1:-start]

	# print '0b'+val

	print 'extractpy() output: ', type(val), '0b'+val
	return '0b'+val
	


#	start = BitArray(p[5]).int
#	end = BitArray(p[3]).int
#	if start ==0:
#		s = s[-end-1:]
#	else:
#		s = s[-end-1:-start]

	

	
####################
#model the not function
def notpy(val):
	print 'notpy() input: ', type(val), val
	if not check2(val):	
		sys.exit(1)

	

#	exp=len(val)-2	
#	maxval = pow(2, exp) - 1

	
	if int2(val)!=0:
		print 'notpy() output: ', type(binary(0, len(val)-2)), binary(0, len(val)-2)
		return binary(0, len(val)-2)
	else:
		print 'notpy() output: ', type(binary(1, len(val)-2)), binary(1, len(val)-2)
		return binary(1, len(val)-2)


#	notval = maxval - int2(val)
#	return binary(notval, len(val)-2)	

##############################
def andpy(val1, val2):
	print 'andpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)

	if not check2(val2):
		sys.exit(1)

	maxlen=max(len(val1), len(val2))
	print 'andpy() output: ', type(binary((int2(val1)&int2(val2)), maxlen-2)), binary((int2(val1)&int2(val2)), maxlen-2)
	return binary((int2(val1)&int2(val2)), maxlen-2)


###############################################
def orpy(val1, val2):
	print 'orpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)

	if not check2(val2):
		sys.exit(1)

	maxlen=max(len(val1)-2, len(val2)-2)
	print 'orpy() output: ', type(binary((int2(val1) | int2(val2)), maxlen)), binary((int2(val1) | int2(val2)), maxlen)
	return binary((int2(val1) | int2(val2)), maxlen)


####################################################
def concatpy(val1, val2):
	print 'concatpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	len1=len(val1)-2
	len2=len(val2)-2	
	val = (int2(val1)<<len2) + int2(val2)
	print 'concatpy() output: ', type(binary(val, len1+len2)), binary(val, len1+len2)
	return binary(val, len1+len2)
		
####################################################
def bvltpy(val1, val2):
	print 'bvltpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	print 'bvltpy() output: ', type(''), binary(1, maxlen) if int2(val1) < int2(val2) else  binary(0, maxlen)
	return binary(1, maxlen) if int2(val1) < int2(val2) else  binary(0, maxlen)


######################################################
def bvlepy(val1, val2):
	print 'bvlepy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	print 'bvlepy() output: ', type(''), binary(1, maxlen) if int2(val1) <= int2(val2) else  binary(0, maxlen)
	return binary(1, maxlen) if int2(val1) <= int2(val2) else  binary(0, maxlen)

#######################################################
def bvgtpy(val1, val2):
	print 'bvgtpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	print 'bvgtpy() output: ', type(''), binary(1, maxlen) if int2(val1) > int2(val2) else  binary(0, maxlen)
	return binary(1, maxlen) if int2(val1) > int2(val2) else  binary(0, maxlen)

#########################################################

def bvgepy(val1, val2):
	print 'bvgepy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	
	maxlen=max(len(val1)-2, len(val2)-2)
	print 'bvgepy() output: ', type(''), binary(1, maxlen) if int2(val1) >= int2(val2) else  binary(0, maxlen)
	return binary(1, maxlen) if int2(val1) >= int2(val2) else  binary(0, maxlen)

##########################################################



def sbvltpy(val1, val2):
	print 'sbvltpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)

	maxlen=max(len(val1)-2, len(val2)-2)
	print 'sbvltpy() output: ', type(''), binary(1, maxlen) if sint2(val1) < sint2(val2) else  binary(0, maxlen)
	return binary(1, maxlen) if sint2(val1) < sint2(val2) else  binary(0, maxlen)
##############################################################

def sbvlepy(val1, val2):
	print 'sbvlepy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	print 'sbvlepy() output: ', type(''), binary(1, maxlen) if sint2(val1) <= sint2(val2) else  binary(0, maxlen)
	return binary(1, maxlen) if sint2(val1) <= sint2(val2) else  binary(0, maxlen)

###############################################################

def sbvgtpy(val1, val2):
	print 'sbvgtpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	print 'sbvgtpy() output: ', type(''), binary(1, maxlen) if sint2(val1) > sint2(val2) else  binary(0, maxlen)
	return binary(1, maxlen) if sint2(val1) > sint2(val2) else  binary(0, maxlen)

#########################################################

def sbvgepy(val1, val2):
	print 'sbvgepy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)

	maxlen=max(len(val1)-2, len(val2)-2)
	print 'sbvgepy() output: ', type(''), binary(1, maxlen) if sint2(val1) >= sint2(val2) else  binary(0, maxlen)
	return binary(1, maxlen) if sint2(val1) >= sint2(val2) else  binary(0, maxlen)



##############################
def bvsxpy(val1, val2):
	print 'bvsxpy() input: ', type(val1), val1, type(val2), val2
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)

	length = len(val1) - 2
	
	if int2(val1) < pow(2, length-1):
		print 'bvsxpy() output: ', type(''), binary(int2(val1),int2(val2))
		return binary(int2(val1),int2(val2))
	else:
		pad = pow(2, int2(val2)) - 1
		pad = pad - ( pow(2, length-1) - 1) 
		print 'bvsxpy() output: ', type(''), binary(pad | int2(val1) , int2(val2))
		return binary(pad | int2(val1) , int2(val2))

###############################

def bvpluspy(val1, val2, val3):
	print 'bvpluspy() input: ', type(val1), val1, type(val2), val2, type(val3), val3
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	if not check2(val3):
		sys.exit(1)

	val = int2(val2) + int2(val3)
	print 'bvpluspy() output: ', type(''), binary(val, int2(val1))
	return binary(val, int2(val1))

############################################

def bvsubpy(val1, val2, val3):
	print 'bvsubpy() input: ', type(val1), val1, type(val2), val2, type(val3), val3
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(val2)
	if not check2(val3):
		sys.exit(1)

	val = int2(val2) - int2(val3)
	print 'bvsubpy() output: ', type(''), binary(val, int2(val1))
	return binary(val, int2(val1))

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
	print predicate
	print args
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
# print sint2("0b11111111111111111111111111111100")
# print andpy('0b11111111111111111111111111111100', '0b00000000000000001111111111111100')
# print bvsxpy('0b00101111', '0b00100000')
# print bvsubpy('0b01000000', '0b0000000000000000000000000000000000000000000000000000000000110110', '0b0000000000000000000000000000000000000000000000000000000000100100')
# print bvpluspy('0b01000000', '0b0000000000000000000000000000000000000000000000000000000000001100', '0b0000000000000000000000000000000000000000000000000000000000000010')
# print sbvltpy('0b11111111111111111111111111000101', '0b00000000000000000000000000000000')
# print int2('0b00000000000000000000000000000001')

# print match_predicate('''(bvsxpy(SymClient_0x2eaacd0[int2('0b00000000000000000000000000000100')],'0b00100000'),'0b00000000000000000000000000000000')''', {'SERSYMIP_0x2e8c640': [192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'SymClient_0x2eaacd0': [71, 69, 84, 223, 197, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'CONNECTIP_0x2ec4130': [192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})