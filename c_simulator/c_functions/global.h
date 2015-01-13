#include <iostream>
#include <fstream>
#include <cstdlib>
#include <bitset>
#include <cstring>
#include <sys/time.h>

#define MAX_PREDICATE_NUMBER 1000000
#define MAX_VALUE_LENGTH 512
#define VALUE_LENGTH 11

typedef bool (*funcptr)();

void xhttpd_funcptr(funcptr* ptrarray);
void ghttpd_funcptr(funcptr* ptrarray);