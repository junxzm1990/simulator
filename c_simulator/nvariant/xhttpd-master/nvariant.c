#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <errno.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <math.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
#include <linux/limits.h>

// @guopy start
#include <semaphore.h>
#include <pthread.h>

#define VARIANT_NUM 2
// @guopy end

// Should be defined in a config file or as argv params or similar
#define PORT 8082
#define NUMWORKERS 6
#define GROUPID 1002
#define USERID 1001
#define HTTP_ROOT "/home/spark/public_html/"
#define INDEXFILE "index.html"

#define VERSION "0.1.0"
#define ERROR_TEMPLATE "<!DOCTYPE html><html><head><title>Error %d: %s</title><style type=\"text/css\">body {text-align: center;}</style></head><body><h1>Error %d: %s</h1><hr />xhttpd/0.1.0</body></html>"
#define BUFFER_START_SIZE 512

#define error(desc, ret) do { printf("Error: %s (%s)\n",  desc, strerror(errno)); return ret; } while(0);

int socket_fd = -1;

// @guopy start
sem_t sem_arrives;
sem_t sem_done;
// @guopy end

// @guopy start
void* simulator_0(void *sign)
{
	printf("simulator_0 started.\n");
	while (true)
	{
		sem_wait(&sem_arrives);
		sleep(2);
		printf("In simulator_0: %s.\n", (char *)sign);
		sem_post(&sem_done);
	}
}

void* simulator_1(void *sign)
{
	printf("simulator_1 started.\n");
	while (true)
	{
		sem_wait(&sem_arrives);
		sleep(4);
		printf("In simulator_1: %s.\n", (char *)sign);
		sem_post(&sem_done);
	}
}
// @guopy end

void handle_request(int socket, char* request, int request_length)
{
	// @guopy start
	int i;
	printf("New request arrived.\n");

	for (i = 0; i < VARIANT_NUM; ++i)
	{
		sem_post(&sem_arrives);
	}
	
	for (i = 0; i < VARIANT_NUM; ++i)
	{
		sem_wait(&sem_done);
	}
	// @guopy end
}

void stop()
{
	printf("Closing connection...\n");
	close(socket_fd);
}

void handle_signal(int signal)
{
	printf("Received sigterm, cleaning up.\n");
	exit(EXIT_SUCCESS);
}

int main(int argc, char* argv[])
{

	// @guopy start
	pthread_t simulator_thread[2];

	sem_init(&sem_arrives, 0, 0);
	sem_init(&sem_done, 0, 0);

	char sign_0[] = "xhttpd";
	char sign_1[] = "ghttpd";

	pthread_create(&(simulator_thread[0]), 0, &simulator_0, (void *)sign_0);
	pthread_create(&(simulator_thread[1]), 0, &simulator_1, (void *)sign_1);
	// @guopy end

	socket_fd = socket(AF_INET, SOCK_STREAM, 0);

	if(socket_fd < 0)
		error("Error opening socket", 1);

	// Register stop function that closes the socket
	atexit(stop);

	// Register signal handler
	signal(SIGINT, handle_signal);
	signal(SIGHUP, handle_signal);
	signal(SIGTERM, handle_signal);

	/* Set SO_REUSEADDR to true. Normally, the kernel blocks a TCP port for one
	 * minute after it was closed so that any ingoing packets to the 'old'
	 * server don't confuse the new one. We don't need that.
	 */
	int one = 1;
	if(setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one)) == -1)
		error("Could not setsockopt", EXIT_FAILURE);

	struct sockaddr_in listen_addr;
	memset(&listen_addr, 0, sizeof(struct sockaddr_in));

	listen_addr.sin_family = AF_INET;
	listen_addr.sin_addr.s_addr = INADDR_ANY;
	listen_addr.sin_port = htons(PORT);

	if(bind(socket_fd, (struct sockaddr*)&listen_addr, sizeof(listen_addr)) < 0)
		error("Could not bind", 1);

	// Chroot in the webserver directory
	if(chdir(HTTP_ROOT) != 0)
		error("Could not change to root directory", EXIT_FAILURE);
	if(chroot(HTTP_ROOT) != 0)
		error("Could not chroot", EXIT_FAILURE);

	// Drop root privileges (if any)
	if (getuid() == 0) {
		if (setgid(GROUPID) != 0)
			error("setgid: Unable to drop group privileges", 1);
		if (setuid(USERID) != 0)
			error("setuid: Unable to drop user privileges", 1);
	}

	// Fork worker child processes
	//for(int i = 1; i < NUMWORKERS; i++)
	//	if(fork() == 0) break;

	while(true)
	{
		listen(socket_fd, 5);

		struct sockaddr_in client_addr;
		int client_len = sizeof(client_addr);
		int client_socket_fd = accept(socket_fd, (struct sockaddr*)&client_addr, &client_len);

		if(client_socket_fd < 0)
			error("Error accepting client socket", 1);
		
		int buffer_size = BUFFER_START_SIZE;
		char* request = (char*)malloc(sizeof(char) * buffer_size);
		memset(request, 0, sizeof(char) * buffer_size);

		int line_length = 0;
		int request_length = 0;
		int iteration = 0;

		do {
			if(buffer_size < BUFFER_START_SIZE)
			{
				buffer_size = BUFFER_START_SIZE * pow(2, iteration);

				request = realloc(request, sizeof(char) * buffer_size);
				if(!request)
					error("Reallocating request buffer failed", EXIT_FAILURE);
			}

			line_length = read(client_socket_fd, &request[request_length], buffer_size);
			if(line_length < 0)
				error("Could not read()", EXIT_FAILURE);

			request_length += line_length;
			buffer_size -= line_length;

			if(request_length > 3 && !strcmp(&request[request_length - 3], "\n\r\n"))
				break;

			iteration++;
		} while(line_length > 0);

		if(request_length > 0)
			handle_request(client_socket_fd, request, request_length);

		free(request);
		close(client_socket_fd);
	}

	// @guopy start
	pthread_join(simulator_thread[0], 0);
	pthread_join(simulator_thread[1], 0);

	sem_destroy(&sem_arrives);
	sem_destroy(&sem_done);
	// @guopy end

	exit(EXIT_SUCCESS);
}
