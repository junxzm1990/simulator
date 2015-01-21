import test
import re
from bitstring import BitArray
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()


names = {}
# names['a'] = ['0x00000001','0x00000001', '0x00000001', '0x00000000']
# TODO 'WITH' : 'with' not dealed yet
reserved = {
'LET' : 'let',
'IN' : 'in',
'WITH' : 'with',   
"NOT" : 'not',
'ASSERT' : 'assert',
'BVLT' : 'bvlt',
'BVLE' : 'bvle',
'BVGT' : 'bvgt',
'BVGE' : 'bvge',
'SBVLT': 'sbvlt',
'SBVGT': 'sbvgt',
'SBVLE': 'sbvle',
'SBVGE': 'sbvge',
'BVSX' : 'bvsx',
'BVPLUS' : 'bvplus',
'BVSUB' : 'bvsub',
'IF'    : 'if',
'THEN'  : 'then',
'ELSE'  : 'else',
'ENDIF' : 'endif'
}

tokens = [ 'COLONEQ', 'ASS','NAME','NUMBER','HEX', 'BIN', 'CONCAT', 'EQ', 'COLON', 'COMMA', 'AND', 'OR'
] + list(reserved.values())


literals = ['[',']', '(',')']

t_CONCAT  = r'@'
t_EQ = r'='
t_COLONEQ = ':='
t_COLON = r':'
t_COMMA = r','
t_AND = '&'
t_OR = '\|'
t_ASS = '=='

t_ignore = " \t"


def t_HEX(t):
    r'0x[0-9a-fA-F]+'
    s=BitArray(t.value)
    t.value='\'0b' + s.bin +'\''
    return t

def t_BIN(t):
    r'0b[01]+'
    s=BitArray(t.value)
    t.value='\'0b' + s.bin + '\''
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_-]*'
    t.type = reserved.get(t.value,'NAME')
    return t

def t_NUMBER(t):
    r'\d+'
    # TODO: all integers are extended to 8 bits
    s=BitArray(int = int(t.value),length=8)
    t.value='\'0b'+s.bin + '\''
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

import lex as lex
lexer = lex.lex(errorlog=log)

precedence = (
    ('left','CONCAT','EQ','AND','OR'),
    ('left', 'COLON','['),
    ('nonassoc','NAME'),
    ('right', 'not', 'let','ASS', 'COLONEQ'),
    )


local = {}

def p_statement_expr(p):
    'statement : assert expression'
    p[0]=p[2]
    return p[0]


def p_expression_name(p):
    # function already modified
    "expression : NAME"
    global names
    if p[1] in names:
        p[0]=names[p[1]]
    else:
        p[0]=p[1]   

#     try:
#         if type(names[p[1]]) is list: 
#             p[0]=p[1]
#         else:
#             p[0] = names[p[1]]
#         local[p[0]]=p[1]
#     except LookupError:
#         # NEWREVISE
#         if p[1].startswith('const_arr'):
#             names[p[1]] = []
#             p[0] = p[1]
#             local[p[0]]=p[1]
#         else:
#             print "Undefined name '%s'" % p[1]
#             p[0]=0
# 


# def p_expression_with_var(p):
#     'expression : expression in expression'
#     p[0] = p[3]

# def p_expression_assign(p):
#     'expression : let NAME ASS expression'
#     names[p[2]] = p[4]

def p_expression_assign(p):
    'letexpression : let NAME ASS expression'
    global names
    names[p[2]] = p[4]

def p_expression_moreassign(p):
    'letexpression : letexpression COMMA NAME ASS expression'
    global names
    names[p[3]] = p[5]

def p_expression_with_var(p):
    'expression : letexpression in expression'
    p[0] = p[3]


def p_expression_eq(p):
	#this function already modified
    "expression : expression EQ expression"
    p[0] =	'eqpy(' + p[1] + ',' + p[3] + ')'  

#		  p[1] +  '=='  + p[3]

    # print 'in p_expression_eq s1 before BitArray: ', p[1]
    # print 'in p_expression_eq s2 before BitArray: ', p[3]

#    s1=BitArray(p[1])
#    s2=BitArray(p[3])
#
#    # print 'in p_expression_eq s1: ', s1
#    # print 'in p_expression_eq s2: ', s2
#
#    if s1.bin == s2.bin:
#        s = BitArray(uintbe=1, length=max(len(p[1]), 10)-2)
#        p[0] = '0b' + s.bin
#    else:
#        # print 'p[1]: ' + str(p[1])
#        s = BitArray(uintbe=0, length=max(len(p[1]), 10)-2)
#        p[0] = '0b' + s.bin



def p_expression_group(p):
	# this function already modified
    "expression : '(' expression ')'"
    p[0] = p[2]




def p_expression_number(p):
    '''expression : NUMBER 
            | HEX 
            | BIN'''
    p[0] = p[1]


def p_expression_ext(p):
    #this function has been modified
    "expression : expression '[' expression COLON expression ']'"

    p[0] = 'extractpy(' + p[1] + ',' + p[3] + ',' + p[5] + ')'
#    s=BitArray(p[1])
#    start = BitArray(p[5]).int
#    end = BitArray(p[3]).int
#    if start ==0:
#        s = s[-end-1:]
#    else:
#        s = s[-end-1:-start]
#    
#    p[0] = '0b' + s.bin
#

# NEWREVISE
def p_expression_withassign(p):
	#function clready modified
    "expression : expression with '[' expression ']' COLONEQ expression"
    global names

    try:
        # names[p[1]][BitArray(p[4]).int] = p[7]
        names[p[1]].append(p[7])
        p[0] = p[1]
    except:
        names[p[1]] = [p[7]]
        # print "Undefined name in p_expression_withassign '%s'" % p[1]
        p[0] = p[1]


mentiondict = dict()

def p_expression_array(p):
    "expression : expression '[' expression ']'"
    global mentiondict
    global names

    if p[1] in names:
        try:
            p[0]=names[p[1]][BitArray(p[3]).int]
        except:
            p[0] = '###' + p[1] + '= {'
            for index, each in enumerate(names[p[1]]):
                if index != len(names[p[1]]) - 1:
                    p[0] += each + ', '
            p[0] += names[p[1]][len(names[p[1]]) - 1] + '}###' + p[1] + '[int2(' + p[3] + ')]'
        # print 'new variable: ', p[1]
    else:
        p[0]=p[1] + '[int2(' + p[3] +')]'

        # global cache
        # print p[3]
        if mentiondict.get(p[1]) is None:
            mentiondict[p[1]] = []
        
        try:
            temp = BitArray(p[3].replace('\'','')).int
            mentiondict[p[1]].append(temp)
        except:
            matcher = re.compile('A_data_0x4326cd0\[int2\([^\)]*\)')
            matchlist = matcher.findall(p[3])
            templist = [each.split('\'')[1] for each in matchlist]
            for each in templist:
                temp = BitArray(each.replace('\'','')).int
                if temp not in mentiondict[p[1]]:
                    mentiondict[p[1]].append(temp)
#
#    try:
#        p[0] = names[p[1]][BitArray(p[3]).int]
#    except LookupError:
#        print "Undefined name and position '%s'" % p[1]
#        p[0] = 0


def p_expression_not(p):
    "expression : not expression"
    p[0] = 'notpy(' + p[2] +')'
  

	  # print 'in p_expression_not: ' + str(p[2])
#    s = BitArray (p[2])
#    if s.int:
#        s = BitArray(uintbe=0, length=len(p[2])-2)
#        p[0] = '0b' + s.bin
#
#    else:
#        s = BitArray(uintbe=1, length=len(p[2])-2)
#        p[0] = '0b' + s.bin


def p_expression_and(p):
    "expression : expression AND expression"
    # print 'in p_expression_and p1: ' + str(p[1])
    # print 'in p_expression_and p3: ' + str(p[3])
    p[0]='andpy(' + p[1] + ',' + p[3] + ')'
    
#    s1 = BitArray(p[1])
#    s2 = BitArray(p[3])
#
#    # print 'in p_expression_and s1: ' + str(s1)
#    # print 'in p_expression_and s2: ' + str(s2)
#    s1.__iand__(s2)
#    p[0] = '0b' + s1.bin
#

def p_expression_or(p):
    "expression : expression OR expression"
    p[0] = 'orpy(' + p[1] + ',' +p[3] +')'
#    s1 = BitArray(p[1])
#    s2 = BitArray(p[3])
#    s1.__ior__(s2)
#    p[0] = '0b' + s1.bin
#


def p_expression_concat(p):
    "expression : expression CONCAT expression"
    p[0] = 'concatpy (' + p[1] + ',' + p[3] + ')' 
#
#    s1=BitArray(p[1])
#    s2=BitArray(p[3])
#    # print str(s2)
#    s1.append('0b' + s2.bin)
#    p[0] = '0b' + s1.bin



def p_expression_bvlt(p):
    "expression : bvlt '(' expression COMMA expression ')' "
    p[0] = 'bvltpy(' + p[3] + ',' + p[5] + ')'

#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    if int(s1.uint < s2.uint):
#        s = BitArray(uintbe=1, length=len(p[3])-2)
#    else:
#        s = BitArray(uintbe=0, length=len(p[3])-2)
#    p[0] = '0b' + s.bin
#    
def p_expression_bvle(p):
    "expression : bvle '(' expression COMMA expression ')' "
    p[0] = 'bvlepy(' + p[3] + ',' + p[5] + ')'
#
#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    if int(s1.uint <= s2.uint):
#        s = BitArray(uintbe=1, length=len(p[3])-2)
#    else:
#        s = BitArray(uintbe=0, length=len(p[3])-2)
#    p[0] = '0b' + s.bin
#
def p_expression_bvgt(p):
    "expression : bvgt '(' expression COMMA expression ')' "  
    p[0] = 'bvgtpy(' + p[3] + ',' + p[5] + ')'
#
#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    if int(s1.uint > s2.uint):
#        s = BitArray(uintbe=0, length=len(p[3])-2)
#    else:
#        s = BitArray(uintbe=1, length=len(p[3])-2)
#    p[0] = '0b' + s.bin

def p_expression_bvge(p):
    "expression : bvge '(' expression COMMA expression ')' "

    p[0] = 'bvgepy(' + p[3] + ',' + p[5] + ')'

#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    if int(s1.uint >= s2.uint):
#        s = BitArray(uintbe=0, length=len(p[3])-2)
#    else:
#        s = BitArray(uintbe=1, length=len(p[3])-2)
#    p[0] = '0b' + s.bin
#


def p_expression_sbvlt(p):
    "expression : sbvlt '(' expression COMMA expression ')' "
    p[0] = 'sbvltpy(' + p[3] + ',' + p[5] + ')'
#
#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    if int(s1.int < s2.int):
#        s = BitArray(uintbe=1, length=len(p[3])-2)
#    else:
#        s = BitArray(uintbe=0, length=len(p[3])-2)
#    p[0] = '0b' + s.bin
#    
def p_expression_sbvle(p):
    "expression : sbvle '(' expression COMMA expression ')' "
    p[0] = 'sbvlepy(' + p[3] + ',' + p[5] + ')'
#
#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    if int(s1.int <= s2.int):
#        s = BitArray(uintbe=1, length=len(p[3])-2)
#    else:
#        s = BitArray(uintbe=0, length=len(p[3])-2)
#    p[0] = '0b' + s.bin
#
def p_expression_sbvgt(p):
    "expression : sbvgt '(' expression COMMA expression ')' "
    p[0] = 'sbvgtpy(' + p[3] + ',' + p[5] + ')'

#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    if int(s1.int > s2.int):
#        s = BitArray(uintbe=0, length=len(p[3])-2)
#    else:
#        s = BitArray(uintbe=1, length=len(p[3])-2)
#    p[0] = '0b' + s.bin
#
def p_expression_sbvge(p):
    "expression : sbvge '(' expression COMMA expression ')' "
    p[0] = 'sbvgepy(' + p[3] + ',' + p[5] + ')'

#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    if int(s1.int >= s2.int):
#        s = BitArray(uintbe=0, length=len(p[3])-2)
#    else:
#        s = BitArray(uintbe=1, length=len(p[3])-2)
#    p[0] = '0b' + s.bin

def p_expression_bvsx(p):
    "expression : bvsx '(' expression COMMA expression ')' "
    p[0] = 'bvsxpy(' + p[3] + ',' + p[5] + ')'
#
#    s1=BitArray(p[3])
#    s2=BitArray(p[5])
#    s = BitArray(intbe=s1.int, length=s2.int)
#    p[0] = '0b' + s.bin
#
def p_expression_bvplus(p):
    "expression : bvplus '(' expression COMMA expression COMMA expression ')'"
    p[0] = 'bvpluspy(' + p[3]+',' + p[5] + ',' + p[7] + ')'
#
#    s0 = BitArray(p[3])
#    s1 = BitArray(p[5])
#    s2 = BitArray(p[7])
#    temp = s1.int + s2.int
#    # temp = s1.uint + s2.uint
#    s = BitArray(uintbe=temp, length = s0.int)
#    p[0] = '0b' + s.bin

def p_expression_bvsub(p):
    "expression : bvsub '(' expression COMMA expression COMMA expression ')'"
    p[0] = 'bvsubpy(' + p[3]+',' + p[5] + ',' + p[7] + ')'
#
#    s0 = BitArray(p[3])
#    s1 = BitArray(p[5])
#    s2 = BitArray(p[7])
#    temp = s1.int - s2.int
#    # temp = s1.uint + s2.uint
#    s = BitArray(uintbe=temp, length = s0.int)
#    p[0] = '0b' + s.bin

def p_expression_if_then_else_endif(p):
    "expression : if expression then expression else expression endif"
    p[0] = p[4] + ' if int2(' + p[2] + ') else ' + p[6]
#
#    s1 = BitArray(p[2])
#    if int(s1.int > 0):
#        p[0] = p[4]
#    else:
#        p[0] = p[6]

def p_error(p):
    print "Syntax error at '%s'" % p.value


import yacc as yacc
yacc.yacc(errorlog=log)



# test concrete value against a path constraint

def constr_testing(value, constr, var_name):
    global names

    lexer = lex.lex()
    parser = yacc.yacc()
    # print parser.parse('ASSERT(NOT(123 = 123))')

    # print constr

    for index, eachvar in enumerate(var_name):
        str_value = []
        for val in value[index]:
            if val != '':
                # TODO: input concrete value must be integer
                str_val = BitArray(uint = int(val), length = 8)
                str_value.append('0x' + str_val.hex)

        names[eachvar] = str_value
    #print names


    return ([constr[0]], yacc.parse(constr[1]))

# This dictionary is for building global cache table. We get the mentioned variables and indexes inside a predicate, and compare the value with what is inside the cache table, and see if it matches.

def cvc_translate(test_str):
    global names
    names = {}
    return yacc.parse(test_str)


# cvc_translate('''
#     ASSERT( (LET let_k_0 == BVPLUS(32,
# 0xFFFFFFD0,
# BVSX(SYMBOL_CLIENT_0x6ae64b0[0x00000004],32)
# )
# ,
# let_k_1 == BVPLUS(32,
# 0xFFFFFFD0,
# BVSX(SYMBOL_CLIENT_0x6ae64b0[0x00000005],32)
# )

#     ''')

# data = test.load_predicates('/home/spark/workspace/github_simulator/simulator_data/openaes/predicates')

# i=0
# translated_predicate=[]

# for eachdata in data:
# 	translated_predicate.append(cvc_translate(eachdata))
# 	print '\n'+str(i)+'\n'
# 	i+=1
# print translated_predicate



#test_translate('''ASSERT( ( NOT( (0b1 = IF((0x0D = SYMBOL_CLIENT_0x6ae64b0[0x00000008])) THEN 0x01 ELSE 0x00 ENDIF[0:0] ))) )''')
