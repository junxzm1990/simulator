#include "c_functions/global.h"
using namespace std;

// a stupid design
char (*def_connectip)[VALUE_LENGTH];
char (*def_sersymip)[VALUE_LENGTH];

char connectip[32][VALUE_LENGTH];
char sersymip[32][VALUE_LENGTH];


TNode::TNode(int pre, TNode* fat, int ind)
{
	fchild		= NULL;
	sibling		= NULL;
	father		= fat;
	predicate	= pre;
	index		= ind;
	finalpath	= "";
};

STree::STree(string sig, string tdf)
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
		openaes_funcptr(predicate_func);
	}
	else if (signature == "xhttpd")
	{
		xhttpd_funcptr(predicate_func);
	}
	else if (signature == "ghttpd")
	{
		ghttpd_funcptr(predicate_func);
	}
	else if (signature == "lighttpd")
	{
		lighttpd_funcptr(predicate_func);
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

TNode* STree::addnode(int pre, TNode* fat)
{
	return new TNode(pre, fat, node_count++);
};

TNode* STree::insertnode(TNode* rt, int pre)
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

void STree::tree_dump()
{
	rec_tree_dump(root, 0);
};

void STree::rec_tree_dump(TNode* rt, int layer)
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
};

void STree::tree_building(ifstream& handle)
{
	rec_tree_building(handle, root);
};

void STree::rec_tree_building(ifstream& handle, TNode* rt)
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
};

void STree::tree_search(char val[][VALUE_LENGTH])
{
	if (signature == "openaes")
	{
		extern char (*A_data_0x2fb50b0)[VALUE_LENGTH];
		A_data_0x2fb50b0 = val;
	}
	else if (signature == "xhttpd")
	{
		extern char (*CONNECTIP_0x2ec4130)[VALUE_LENGTH];
		extern char (*SERSYMIP_0x2e8c640)[VALUE_LENGTH];
		extern char (*SymClient_0x2eaacd0)[VALUE_LENGTH];
		CONNECTIP_0x2ec4130 = def_connectip;
		SERSYMIP_0x2e8c640 = def_sersymip;
		SymClient_0x2eaacd0 = val;
	}
	else if (signature == "ghttpd")
	{
		extern char (*SymClient_0x37fc490)[VALUE_LENGTH];
		SymClient_0x37fc490 = val;
	}
	else if (signature == "lighttpd")
	{
		extern char (*readsym_1_0xabc7b20)[VALUE_LENGTH];
		readsym_1_0xabc7b20 = val;
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

	// local caching table
	short localcachingtable[MAX_PREDICATE_NUMBER] = {0}; // initialize all into 0

	// tree traverse
	search_match_count	= 0;
	search_total_count	= 0;
	search_global_hit	= 0;
	search_local_hit	= 0;
	search_finalpath	= "";

	TNode* pointer = root->fchild;

	while (true)
	{
		search_total_count ++;

		bool result;

		// do a predicate match attempt
		if (localcachingtable[pointer->predicate] != 0)
		{
			result = (localcachingtable[pointer->predicate] > 0)? true : false;
			search_local_hit ++;
		}
		else
		{
			result = predicate_func[pointer->predicate]();
			search_match_count ++;
			localcachingtable[pointer->predicate] = result? 1 : -1;
		}

		if (result == true)
		{
			if (pointer->fchild == NULL)
			{
				search_finalpath = pointer->finalpath;
				return;
			}
			else
			{
				pointer = pointer->fchild;
			}
		}
		else
		{
			while (pointer->sibling == NULL)
			{
				if (pointer != root)
					pointer = pointer->father;
				else
					return;
			}
			pointer = pointer->sibling;
		}
	}
};


Simulator::Simulator(string program)
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
		// prepare two IPs for xhttpd
		strcpy(connectip[0], "0b11000000");
		strcpy(sersymip[0], "0b11000000");
		strcpy(connectip[1], "0b10101000");
		strcpy(sersymip[1], "0b10101000");
		strcpy(connectip[2], "0b00000001");
		strcpy(sersymip[2], "0b00000001");
		strcpy(connectip[3], "0b11110100");
		strcpy(sersymip[3], "0b11110100");
		for (int i = 4; i <32; i ++)
		{
			strcpy(connectip[i], "0b00000000");
			strcpy(sersymip[i], "0b00000000");
		}
		def_sersymip = sersymip;
		def_connectip = connectip;
	}
	else if (signature == "ghttpd")
	{
		mentdatafile = "/home/spark/workspace/github_simulator/simulator_data/ghttpd/mentiondict";
		treedatafile = "/home/spark/workspace/github_simulator/simulator_data/ghttpd/c_search_tree";
		testdatapath = "/home/spark/workspace/github_simulator/simulator_data/ghttpd/stosam/";
	}
	else if (signature == "lighttpd")
	{
		mentdatafile = "/home/spark/workspace/github_simulator/simulator_data/lighttpd/mentiondict";
		treedatafile = "/home/spark/workspace/github_simulator/simulator_data/lighttpd/c_search_tree";
		testdatapath = "/home/spark/workspace/github_simulator/simulator_data/lighttpd/stosam/";
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
};

string Simulator::simulate(char allval[][VALUE_LENGTH])
{
	if (signature == "xhttpd")
	{
		def_sersymip = allval;
		def_connectip = allval + 32;
		allval += 64;
	}
	search_tree->tree_search(allval);
	cout << search_tree->search_finalpath << endl;
};

void Simulator::inttobinary(int* data, char str_data[][VALUE_LENGTH], int count)
{
	for (int i = 0; i < count; i ++)
	{
		bitset<8> bits(data[i]);
		strcpy(str_data[i], ("0b" + bits.to_string()).c_str());
	}
};

void Simulator::testdata_single(string filename)
{
	ifstream datafile((testdatapath + filename).c_str());
	string tempdata;
	int data[MAX_VALUE_LENGTH];
	char str_data[MAX_VALUE_LENGTH][VALUE_LENGTH];

	int i = 0;
	if (datafile.is_open())
	{
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

	inttobinary(data, str_data, i);

	search_tree->tree_search(str_data);
	cout << search_tree->search_finalpath << endl;
};

void Simulator::getdir(string dir, vector<string> &files)
{
	DIR *dp;
	struct dirent *dirp;
	if ((dp = opendir(dir.c_str())) == NULL)
	{
		cout << "Simulator::getdir: Error opening diretory." << endl;
		exit(0);
	}
	else
	{
		while((dirp = readdir(dp)) != NULL)
		{
			if ((!string(dirp->d_name).compare(".")) || (!string(dirp->d_name).compare("..")))
				continue;
			// cout << dirp->d_name << endl;
			files.push_back(string(dirp->d_name));
		}
		closedir(dp);
	}
};

void Simulator::testdata_all()
{
	struct timeval stime, etime;

	vector<string> files = vector<string>();

	getdir(testdatapath, files);

	int i = 0;
	long total_count = 0;
	long match_count = 0;
	gettimeofday(&stime, NULL);
	for (i = 0; i < files.size(); i++)
	{
		if (i == 3000)
			break;
		ifstream datafile((testdatapath + files[i]).c_str());
		string tempdata;
		int data[MAX_VALUE_LENGTH];
		char str_data[MAX_VALUE_LENGTH][VALUE_LENGTH];

		int j = 0;
		if (datafile.is_open())
		{
			while (datafile.good())
			{
				getline(datafile, tempdata, ',');
				data[j++] = atoi(tempdata.c_str());
			}
			datafile.close();
		}
		else
		{
			cout << "ERROR: Simulator:testdata_all: Error opening file.\n";
		}

		inttobinary(data, str_data, j);

		cout << files[i] << endl;
		search_tree->tree_search(str_data);
		cout << search_tree->search_finalpath << endl;
		total_count += search_tree->search_total_count;
		match_count += search_tree->search_match_count;
	}
	gettimeofday(&etime, NULL);
	cout << "avg search total count: " << total_count / i << endl;
	cout << "avg search match count: " << match_count / i << endl;
	cout << "avg search time: " << ((etime.tv_sec - stime.tv_sec) + (double)(etime.tv_usec - stime.tv_usec) / 1000000) / i << endl;
};



// test function
// int main()
// {
// 	Simulator sim = Simulator("xhttpd");

// 	struct timeval stime, etime;

// 	gettimeofday(&stime, NULL);
// 	sim.testdata_single("test096941.pc");
// 	gettimeofday(&etime, NULL);
// 	cout << (etime.tv_sec - stime.tv_sec) + (double)(etime.tv_usec - stime.tv_usec) / 1000000 << endl;

// 	// sim.testdata_all();

// 	return 0;
// }
