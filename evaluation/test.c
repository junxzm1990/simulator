#include <stdio.h>

int main()
{
	FILE* fp;
	char buffer[10][129];
	char ch;
	if ((fp = fopen("data/ghttpd", "rb")) != NULL)
	{
		int row = 0;
		int col = 0;
		do {
			ch = fgetc(fp);
			if (feof(fp))
				break;
			// printf("|'%c, %d'|", ch, (int)ch);
			buffer[row][col++] = ch;
			if (col == 128)
			{
				buffer[row][col] = '\0';
				row += 1;
				col = 0;
				if (row == 10)
					break;
			}
		}while (1);
	}
	else
	{
		printf("Cannot open file.\n");
	}
	int i;
	for (i = 0; i < 10; ++i)
	{
		printf("%s\n", buffer[i]);
	}
	
	return 0;
}
