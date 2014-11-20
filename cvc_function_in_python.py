import sys
import os

############
# transform a integer into binary with padded zeros
def binary(num, length=8):
	return format(num, '#0{}b'.format(length + 2))

############
#check if a string is in binary format
def check2(val):
	try:
		int(val, base=2)
		return True
	except ValueError:
		print val + 'is not in the binary format (with 0b as prefix)'
		return False

###############
#transform a binary string into integer
def int2(val):
	return int(val, base=2)

def sint2(val):
	length = len(val)-2
	if int2(val) < pow(2, length-1):
		return int2(val)
	else:
		return -(pow(2, length)-int2(val))

#######################################
def eqpy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)

	maxlen = max (len(val1)-2, len(val2)-2)
	if int2(val1) == int2(val2):
	
		print 'equal: ' + binary(1,maxlen)
		return binary(1, maxlen)
	else:
		print 'not equal: ' + binary(0,maxlen) 
		return binary(0, maxlen)
	

###############################################
def extractpy(val1, val2, val3):
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

	print '0b'+val

	return '0b'+val
	


#    start = BitArray(p[5]).int
#    end = BitArray(p[3]).int
#    if start ==0:
#        s = s[-end-1:]
#    else:
#        s = s[-end-1:-start]

	

	
####################
#model the not function
def notpy(val):
	if not check2(val):	
		sys.exit(1)

	exp=len(val)-2	
	maxval = pow(2, exp) - 1

	notval = maxval - int2(val)
	return binary(notval, len(val)-2)	

##############################
def andpy(val1, val2):
	if not check2(val1):
		sys.exit(1)

	if not check2(val2):
		sys.exit(1)

	maxlen=max(len(val1), len(val2))
	return binary((int2(val1)&int2(val2)), maxlen-2)


###############################################
def orpy(val1, val2):
    if not check2(val1):
        sys.exit(1)

    if not check2(val2):
        sys.exit(1)

    maxlen=max(len(val1)-2, len(val2)-2)
    return binary((int2(val1) | int2(val2)), maxlen)


####################################################
def concatpy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	len1=len(val1)-2
	len2=len(val2)-2	
	val = (int2(val1)<<len2) + int2(val2)
	return binary(val, len1+len2)
		
####################################################
def bvltpy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	return binary(1, maxlen) if int2(val1) < int2(val2) else  binary(0, maxlen)


######################################################
def bvlepy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	return binary(1, maxlen) if int2(val1) <= int2(val2) else  binary(0, maxlen)

#######################################################
def bvgtpy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	return binary(1, maxlen) if int2(val1) > int2(val2) else  binary(0, maxlen)

#########################################################

def bvgepy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	
	maxlen=max(len(val1)-2, len(val2)-2)
	return binary(1, maxlen) if int2(val1) >= int2(val2) else  binary(0, maxlen)

##########################################################



def sbvltpy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)

	maxlen=max(len(val1)-2, len(val2)-2)
	return binary(1, maxlen) if sint2(val1) < sint2(val2) else  binary(0, maxlen)
##############################################################

def sbvlepy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	return binary(1, maxlen) if sint2(val1) <= sint2(val2) else  binary(0, maxlen)

###############################################################

def sbvgtpy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	maxlen=max(len(val1)-2, len(val2)-2)
	return binary(1, maxlen) if sint2(val1) > sint2(val2) else  binary(0, maxlen)

#########################################################

def sbvgepy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)

	maxlen=max(len(val1)-2, len(val2)-2)
	return binary(1, maxlen) if sint2(val1) >= sint2(val2) else  binary(0, maxlen)



##############################
def bvsxpy(val1, val2):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)

	length = len(val1) - 2
	
	if int2(val1) < pow(2, length-1):
		return binary(int2(val1),int2(val2))
	else:
		pad = pow(2, int2(val2)) - 1
		pad = pad - ( pow(2, length-1) - 1) 
		return binary(pad | int2(val1) , int2(val2))

###############################

def bvpluspy(val1, val2, val3):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(1)
	if not check2(val3):
		sys.exit(1)

	val = int2(val2) + int2(val3)
	return binary(val, int2(val1))

############################################

def bvsub(val1, val2, val3):
	if not check2(val1):
		sys.exit(1)
	if not check2(val2):
		sys.exit(val2)
	if not check2(val3):
		sys.exit(1)

	val = int2(val2) - int2(val3)
	return binary(val, int2(val1))

###################################################
def pre_process_input(val):
	if type(val) is list:
		for i in range(0, len(val)):
			val[i] = binary(val[i], 8)	
	else:
		val = binary(val, 8)	


def  match_predicate(predicate, args):
	for k, v in args.items():
		pre_process_input(v)
		exec(k+"=v")
	exec(predicate)



# code="print notpy(((eqpy('0b1',extractpy('0b00000001' if int2(((eqpy('0b00001101',SYMBOL_CLIENT_0x6ae64b0[int2('0b00000000000000000000000000001')])))) else '0b00000000','0b00000000','0b00000000')))))"

# match_predicate(code, SYMBOL_CLIENT_0x6ae64b0=[0x01, 0x02, 0x03 ])


#print bvsxpy('0b010', '0b111')
#
#print bvltpy('0b10', '0b00')
#print bvltpy('0b11', '0b111')
#
#print concatpy('0b1110',concatpy('0b1001', '0b0001'))
#
