#include <iostream>
#include <fstream>
#include <cstdlib>
#include <bitset>
#include <cstring>
#include <vector>
#include <dirent.h>
#include <sys/time.h>
#include <sys/types.h>

#define MAX_PREDICATE_NUMBER 1000000
#define MAX_VALUE_LENGTH 512
#define VALUE_LENGTH 11

typedef bool (*funcptr)();

void openaes_funcptr(funcptr* ptrarray);
void xhttpd_funcptr(funcptr* ptrarray);
void ghttpd_funcptr(funcptr* ptrarray);


