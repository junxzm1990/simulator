#include <cstring>
#include <cstdlib>
#include <sys/time.h>
#include <sys/types.h>
#include <iostream>
using namespace std;

int main()
{
	struct timeval stime, etime;

	gettimeofday(&stime, NULL);
	for (int j = 0; j < 10; j ++)
	{
		int * ptr = (int*)malloc(100000000*sizeof(int));
		for (int i = 0; i < 100000000; i ++)
		{
			if (ptr[i] != 0)
				cout << ptr[i] << endl;
			ptr[i] = i % 10000;
		}
		free(ptr);
	}
	gettimeofday(&etime, NULL);
	cout << (etime.tv_sec - stime.tv_sec) + (double)(etime.tv_usec - stime.tv_usec) / 1000000 << endl;
}