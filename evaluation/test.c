#include <stdio.h>

int main()
{
	FILE* fp;
	char buffer[10][100];
	char ch;
	if ((fp = fopen("data/xhttpd", "rb")) != NULL)
	{
		int row = 0;
		while (feof(fp) != EOF)
		{
			fgets(buffer[row++], 100, fp);
			printf("%s##", buffer[row-1]);
			if (row == 10)
				break;
		}
	}
	else
	{
		printf("Cannot open file.\n");
	}
	int i;
	for (i = 0; i < 10; ++i)
	{
		printf("buffer: %s\n", buffer[i]);
	}
	
	return 0;
}
