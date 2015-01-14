#ifndef GLOBAL
#define GLOBAL


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

using namespace std;

typedef bool (*funcptr)();

void openaes_funcptr(funcptr* ptrarray);
void xhttpd_funcptr(funcptr* ptrarray);
void ghttpd_funcptr(funcptr* ptrarray);

class TNode
{
public:
	TNode* fchild;
	TNode* sibling;
	TNode* father;
	int predicate;
	int index;
	string finalpath;

	TNode(int pre, TNode* fat, int ind);
	
};

class STree
{
public:
	int node_count;
	TNode* root;
	string signature;

	// local cache table
	bool localcache[MAX_PREDICATE_NUMBER];

	// predicate function array
	funcptr predicate_func[MAX_PREDICATE_NUMBER];

	int search_match_count;
	int search_total_count;
	int search_global_hit;
	int search_local_hit;
	string search_finalpath;


	STree(string sig, string tdf);

	TNode* addnode(int pre, TNode* fat);

	TNode* insertnode(TNode* rt, int pre);

	void tree_dump();

	void rec_tree_dump(TNode* rt, int layer);

	void tree_building(ifstream& handle);

	void rec_tree_building(ifstream& handle, TNode* rt);

	void tree_search(char val[][VALUE_LENGTH]);
};

class Simulator {

	string signature;
	string mentdatafile;
	string treedatafile;
	STree* search_tree;

	string testdatapath;
public:
	Simulator(string program);

	string simulate(char allval[][VALUE_LENGTH]);

	void inttobinary(int* data, char str_data[][VALUE_LENGTH], int count);

	void testdata_single(string filename);

	void getdir(string dir, vector<string> &files);

	void testdata_all();
};


#endif