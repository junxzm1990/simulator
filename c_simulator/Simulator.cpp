#include <iostream>
#include <fstream>
#include <cstdlib>
#include <global.h>
using namespace std;

class TNode
{
public:
	TNode* fchild;
	TNode* sibling;
	TNode* father;
	int predicate;
	int index;
	string finalpath;

	TNode(int pre, TNode* fat, int ind)
	{
		fchild		= NULL;
		sibling		= NULL;
		father		= fat;
		predicate	= pre;
		index		= ind;
		finalpath	= "";
	};
	
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


	STree(string sig, string tdf)
	{
		node_count	= 0;
		root		= addnode(-1, NULL);
		signature	= sig;

		search_match_count	= 0;
		search_total_count	= 0;
		search_global_hit	= 0;
		search_local_hit	= 0;
		search_finalpath	= "";

		// initialize function pointers
		if (signature == "openaes")
		{
			// openaes_funcptr(predicate_func);
		}
		else if (signature == "xhttpd")
		{
			xhttpd_funcptr(predicate_func);
		}
		else if (signature == "ghttpd")
		{
			ghttpd_funcptr(predicate_func);
		}
		else if (signature == "wget")
		{
			// wget_funcptr(predicate_func);
		}
		else if (signature == "lzfx")
		{
			// lzfx_funcptr(predicate_func);
		}
		else
		{
			cout << "ERROR: STree::tree_search: Wrong program signature.\n";
			exit(0);
		}

		// initialize search tree
		ifstream handle(tdf.c_str());
		tree_building(handle);
		handle.close();
	};

	TNode* addnode(int pre, TNode* fat)
	{
		return new TNode(pre, fat, node_count++);
	};

	TNode* insertnode(TNode* rt, int pre)
	{
		if (rt == NULL)
		{
			cout << "ERROR: STree:insertnode: root is NULL.\n";
			exit(0);
		}
		else if (rt->fchild == NULL)
		{
			rt->fchild = addnode(pre, rt);
			return rt->fchild;
		}
		else
		{
			TNode* pointer = rt->fchild;
			while (pointer->sibling != NULL)
				pointer = pointer->sibling;
			pointer->sibling = addnode(pre, rt);
			return pointer->sibling;
		}
	};

	void tree_dump()
	{
		rec_tree_dump(root, 0);
	};

	void rec_tree_dump(TNode* rt, int layer)
	{
		if (rt == NULL)
			return;
		cout << "layer: " << layer << "\n";

		TNode* pointer = rt;
		while (pointer != NULL)
		{
			cout << ((pointer->father == NULL) ? -1:pointer->father->index) << "\t\t" << pointer->index << "\t\t" << pointer->predicate << "\t\t" << ((pointer->fchild == NULL) ? -1:pointer->fchild->index) << "\t\t" << pointer->finalpath << "\n";
			pointer = pointer->sibling;
		}

		pointer = rt;
		while (pointer != NULL)
		{
			rec_tree_dump(pointer->fchild, layer+1);
			pointer = pointer->sibling;
		}
	}

	void tree_building(ifstream& handle)
	{
		rec_tree_building(handle, root);
	}

	void rec_tree_building(ifstream& handle, TNode* rt)
	{
		int pre;
		string line;

		getline(handle, line);
		pre = atoi(line.c_str());
		if (pre < 0)
			return;
		else
		{
			TNode* newnode = insertnode(rt, pre);
			getline(handle, line);
			newnode->finalpath = line;
			rec_tree_building(handle, newnode);
			rec_tree_building(handle, rt);
			return;
		}
	}

	void tree_search(int* val)
	{
		int connectip[] = {192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
		int sersymip[] = {192, 168, 1, 244, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
		if (signature == "openaes")
		{

		}
		else if (signature == "xhttpd")
		{
			extern int* CONNECTIP_0x2ec4130;
			extern int* SERSYMIP_0x2e8c640;
			extern int* SymClient_0x2eaacd0;
			CONNECTIP_0x2ec4130 = connectip;
			SERSYMIP_0x2e8c640 = sersymip;
			SymClient_0x2eaacd0 = val;
		}
		else if (signature == "ghttpd")
		{
			extern int* SymClient_0x37fc490;
			SymClient_0x37fc490 = val;
		}
		else if (signature == "wget")
		{

		}
		else if (signature == "lzfx")
		{

		}
		else
		{
			cout << "ERROR: STree::tree_search: Wrong program signature.\n";
			exit(0);
		}
	}
};

class Simulator {

	string signature;
	string mentdatafile;
	string treedatafile;
	STree* search_tree;

	string testdatapath;


public:
	Simulator(string program)
	{
		signature = program;

		if (signature == "openaes")
		{
			mentdatafile = "/home/spark/workspace/github_simulator/simulator_data/openaes/mentiondict";
			treedatafile = "/home/spark/workspace/github_simulator/simulator_data/openaes/c_search_tree";
			testdatapath = "/home/spark/workspace/github_simulator/simulator_data/openaes/stosam/";
		}
		else if (signature == "xhttpd")
		{
			mentdatafile = "/home/spark/workspace/github_simulator/simulator_data/xhttpd/mentiondict";
			treedatafile = "/home/spark/workspace/github_simulator/simulator_data/xhttpd/c_search_tree";
			testdatapath = "/home/spark/workspace/github_simulator/simulator_data/xhttpd/stosam/";
		}
		else if (signature == "ghttpd")
		{
			mentdatafile = "/home/spark/workspace/github_simulator/simulator_data/ghttpd/mentiondict";
			treedatafile = "/home/spark/workspace/github_simulator/simulator_data/ghttpd/c_search_tree";
			testdatapath = "/home/spark/workspace/github_simulator/simulator_data/ghttpd/stosam/";
		}
		else if (signature == "wget")
		{
			mentdatafile = "/home/spark/workspace/github_simulator/simulator_data/wget/mentiondict";
			treedatafile = "/home/spark/workspace/github_simulator/simulator_data/wget/c_search_tree";
			testdatapath = "/home/spark/workspace/github_simulator/simulator_data/wget/stosam/";
		}
		else if (signature == "lzfx")
		{
			mentdatafile = "/home/spark/workspace/github_simulator/simulator_data/lzfx/mentiondict";
			treedatafile = "/home/spark/workspace/github_simulator/simulator_data/lzfx/c_search_tree";
			testdatapath = "/home/spark/workspace/github_simulator/simulator_data/lzfx/stosam/";
		}
		else
		{
			cout << "ERROR: Simulator::Simulator: Wrong program signature.\n";
			exit(0);
		}

		search_tree = new STree(signature, treedatafile);
	}

	// int *value: points to a one-dimentional array that hold all input value
	string simulate(int *value)
	{
		
	}

	void testdata_single(string filename)
	{
		ifstream datafile((testdatapath + filename).c_str());
		string tempdata;
		int data[MAX_VALUE_LENGTH];

		if (datafile.is_open())
		{
			int i = 0;
			while (datafile.good())
			{
				getline(datafile, tempdata, ',');
				data[i++] = atoi(tempdata.c_str());
			}
			datafile.close();
		}
		else
		{
			cout << "ERROR: Simulator:testdata_single: Error opening file.\n";
		}

		search_tree->tree_search(data);
	}
};



// test
int main()
{
	Simulator sim = Simulator("xhttpd");
	sim.testdata_single("test000100.pc");

	return 0;
}
