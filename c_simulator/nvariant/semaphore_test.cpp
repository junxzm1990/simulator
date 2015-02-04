#include <iostream>
#include <semaphore.h>
#include <pthread.h>
#include <unistd.h>

using namespace std;

sem_t sem_arrives;
sem_t sem_done;

void* simulator_0(void *sign)
{
	cout << "simulator_0 started." << endl;
	while (true)
	{
		sem_wait(&sem_arrives);
		sleep(2);
		cout << "In simulator_0: " << (char *)sign << endl;
		sem_post(&sem_done);
	}
}

void* simulator_1(void *sign)
{
	cout << "simulator_1 started." << endl;
	while (true)
	{
		sem_wait(&sem_arrives);
		sleep(4);
		cout << "In simulator_1: " << (char *)sign << endl;
		sem_post(&sem_done);
	}
}

int main()
{
	pthread_t simulator_thread[2];

	sem_init(&sem_arrives, 0, 0);
	sem_init(&sem_done, 0, 0);

	char sign_0[] = "xhttpd";
	char sign_1[] = "ghttpd";

	pthread_create(&(simulator_thread[0]), 0, &simulator_0, (void *)sign_0);
	pthread_create(&(simulator_thread[1]), 0, &simulator_1, (void *)sign_1);


	char a;
	int value;
	while (true)
	{
		cout << "New request: " << endl;
		cin >> a;
		sem_post(&sem_arrives);
		sem_post(&sem_arrives);
		sem_wait(&sem_done);
		sem_wait(&sem_done);
	}


	pthread_join(simulator_thread[0], 0);
	pthread_join(simulator_thread[1], 0);

	sem_destroy(&sem_arrives);
	sem_destroy(&sem_done);

	return 0;
}