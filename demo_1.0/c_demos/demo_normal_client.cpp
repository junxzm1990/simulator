#include "../../c_simulator/c_functions/global.h"
using namespace std;

int main()
{
	Simulator sim = Simulator("xhttpd");

	// struct timeval stime, etime;
	// gettimeofday(&stime, NULL);
	// sim.testdata_single("test000401.pc");
	// gettimeofday(&etime, NULL);
	// cout << (etime.tv_sec - stime.tv_sec) + (double)(etime.tv_usec - stime.tv_usec) / 1000000 << endl;

	sim.testdata_all();

	return 0;
}
