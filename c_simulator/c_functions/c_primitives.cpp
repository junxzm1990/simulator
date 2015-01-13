#include <cmath>
#include "c_functions/c_primitives.h"
#include "c_functions/global.h"
using namespace std;

unsigned int int2(const char* str)
{	
	cout << "inside int2" << endl;
	if(!str)
	{
		cout << "int2: Empty string.\n";
		exit(0);
	}

	return (unsigned int)strtoul(str+2, NULL, 2);
}

int sint2(const char* str)
{
	if(!str)
	{
		cout << "sint2: Empty string.\n";
		exit(0);
	}

	return strtol(str+2, NULL, 2);
}

char* eqpy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) == strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* extractpy(const char* str1, const char* str2, const char* str3)
{
	uint start, end;
	int length;
	char * result;

	if(!str1 || !str2 || !str3)
		return NULL;

	start = (int)strtoul(str3+2, NULL, 2);
	end = (int)strtoul(str2+2, NULL, 2);
	length = end - start + 1;
	start = length - start - 1;
	result = (char*)malloc(length+1);
	strncpy(result, str1+2+start, length);
	memset(result+length, 0, 1);

	return result;
}

char* notpy(const char* str)
{
	char * result;

	if(!str)
		return NULL;

	result = (char*)malloc((int)strlen(str)+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', (int)strlen(str)-2);
	memset(result+(int)strlen(str), 0, 1);
	if(strtoul(str+2, NULL, 2) == 0)
		memset(result+(int)strlen(str)-1, '1', 1);

	return result;
}

char* andpy(const char* str1, const char* str2)
{
	char* result;
	int maxlen;
	unsigned int temp;
	int flag, i, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	flag = (len1 > len2)? 1 : 0;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+maxlen, 0, 1);
	memset(result+2, '0', abs(len1 - len2));
	strcpy(result+2+abs(len1 - len2), (len1 > len2)? str2+2 : str1+2);
	if(len1 > len2)
	{
		for(i = 2; i < maxlen; i ++)
			memset(result+i, (char)(((str1[i]-(int)'0') & (result[i]-(int)'0')) + (int)'0'), 1);
	}
	else
	{
		for(i = 2; i < maxlen; i ++)
		{
			memset(result+i, (char)(((str2[i]-(int)'0') & (result[i]-(int)'0')) + (int)'0'), 1);
		}
	}
		
	return result;
}

char* orpy(const char* str1, const char* str2)
{
	char* result;
	int maxlen;
	uint temp;
	int flag, i, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	flag = (len1 > len2)? 1 : 0;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+maxlen, 0, 1);
	memset(result+2, '0', abs(len1 - len2));
	strcpy(result+2+abs(len1 - len2), (len1 > len2)? str2+2 : str1+2);
	if(len1 > len2)
	{
		for(i = 2; i < maxlen; i ++)
			memset(result+i, (char)(((str1[i]-(int)'0') | (result[i]-(int)'0')) + (int)'0'), 1);
	}
	else
	{
		for(i = 2; i < maxlen; i ++)
		{
			memset(result+i, (char)(((str2[i]-(int)'0') | (result[i]-(int)'0')) + (int)'0'), 1);
		}
	}
		
	return result;
}

char* concatpy(const char* str1, const char* str2)
{
	char* result;
	int len1, len2, i;
	unsigned int temp;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	result = (char*)malloc(len1+len2-2+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+len1+len2-2, 0, 1);
	temp = (strtoul(str1+2, NULL, 2) << (len2-2)) + strtoul(str2+2, NULL, 2);

	unsigned long mask;
	for(i = 2; i < len1 + len2 - 2; i ++)
	{
		mask = 1 << i-2;
		if(((mask & temp) >> i-2) == 1)
			memset(result+len1+len2-i-1, '1', 1);
		else
			memset(result+len1+len2-i-1, '0', 1);
	}

	return result;
}

char* bvltpy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) < strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* bvlepy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) <= strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* bvgtpy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) > strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* bvgepy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) >= strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* sbvltpy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;
	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if((int)strtol(str1+2, NULL, 2) < (int)strtol(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* sbvlepy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if((int)strtol(str1+2, NULL, 2) <= (int)strtol(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* sbvgtpy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if((int)strtol(str1+2, NULL, 2) > (int)strtol(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* sbvgepy(const char* str1, const char* str2)
{
	char* result;
	int maxlen, len1, len2;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = (char*)malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if((int)strtol(str1+2, NULL, 2) >= (int)strtol(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return result;
}

char* bvsxpy(const char* str1, const char* str2)
{
	char* result;
	int len1, length, i;
	unsigned int temp;

	if(!str1 || !str2)
		return NULL;

	len1 = (int)strlen(str1);
	
	length = strtoul(str2+2, NULL, 2) + 2;
	result = (char*)malloc(length+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+length, 0, 1);

	if(strtoul(str1+2, NULL, 2) < pow(2, len1-2-1))
	{
		unsigned long mask;
		temp = strtoul(str1+2, NULL, 2);
		for(i = 2; i < length; i ++)
		{
			mask = 1 << i-2;
			if(((mask & temp) >> i-2) == 1)
				memset(result+length-i+1, '1', 1);
			else
				memset(result+length-i+1, '0', 1);
		}
	}
	else
	{
		unsigned int pad = pow(2, strtoul(str2+2, NULL, 2)) - 1;
		pad = pad - (pow(2, len1-2-1) - 1);

		unsigned long mask;
		temp = pad | strtoul(str1+2, NULL, 2);
		for(i = 2; i < length; i ++)
		{
			mask = 1 << i-2;
			if(((mask & temp) >> i-2) == 1)
				memset(result+length-i+1, '1', 1);
			else
				memset(result+length-i+1, '0', 1);
		}
	}
	
	return result;
}

char* bvpluspy(const char* str1, const char* str2, const char* str3)
{
	char* result;
	unsigned int temp;
	int length, i;

	if(!str1 || !str2 || !str3)
		return NULL;

	temp = strtoul(str2+2, NULL, 2) + strtoul(str3+2, NULL, 2);
	length = strtoul(str1+2, NULL, 2) + 2;
	
	result = (char*)malloc(length+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+length, 0, 1);

	unsigned long mask;
	for(i = 2; i < length; i ++)
	{
		mask = 1 << i-2;
		if(((mask & temp) >> i-2) == 1)
			memset(result+length-i+1, '1', 1);
		else
			memset(result+length-i+1, '0', 1);
	}

	return result;
}

char* bvsubpy(const char* str1, const char* str2, const char* str3)
{
	char* result;
	unsigned int temp;
	int length, i;

	if(!str1 || !str2 || !str3)
		return NULL;

	temp = strtoul(str2+2, NULL, 2) - strtoul(str3+2, NULL, 2);
	length = strtoul(str1+2, NULL, 2) + 2;
	
	result = (char*)malloc(length+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+length, 0, 1);

	unsigned long mask;
	for(i = 2; i < length; i ++)
	{
		mask = 1 << i-2;
		if(((mask & temp) >> i-2) == 1)
			memset(result+length-i+1, '1', 1);
		else
			memset(result+length-i+1, '0', 1);
	}

	return result;
}
