#include <Python.h>

static PyObject* py_int2(PyObject* self, PyObject* args)
{
	const char* str;

	if(!PyArg_ParseTuple(args, "s", &str))
		return NULL;

	return Py_BuildValue("I", strtoul(str+2, NULL, 2));
}

static PyObject* py_sint2(PyObject* self, PyObject* args)
{
	const char* str;

	if(!PyArg_ParseTuple(args, "s", &str))
		return NULL;

	return Py_BuildValue("i", strtol(str+2, NULL, 2));
}

static PyObject* py_eqpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	// printf("str1: %s\n", str1);
	// printf("str2: %s\n", str2);

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) == strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_extractpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2, *str3;
	uint start, end;
	int length;
	char * result;

	if(!PyArg_ParseTuple(args, "sss", &str1, &str2, &str3))
		return NULL;

	start = (int)strtoul(str3+2, NULL, 2);
	end = (int)strtoul(str2+2, NULL, 2);
	length = end - start + 1;
	start = length - start - 1;
	result = malloc(length+1);
	strncpy(result, str1+2+start, length);
	memset(result+length, 0, 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_notpy(PyObject* self, PyObject* args)
{
	const char* str;
	char * result;

	if(!PyArg_ParseTuple(args, "s", &str))
		return NULL;

	result = malloc((int)strlen(str)+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', (int)strlen(str)-2);
	memset(result+(int)strlen(str), 0, 1);
	if(strtoul(str+2, NULL, 2) == 0)
		memset(result+(int)strlen(str)-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_andpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen;
	unsigned int temp;
	int flag, i, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	flag = (len1 > len2)? 1 : 0;
	result = malloc(maxlen+1);
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
		
	return Py_BuildValue("s", result);
}

static PyObject* py_orpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen;
	uint temp;
	int flag, i, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	flag = (len1 > len2)? 1 : 0;
	result = malloc(maxlen+1);
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
		
	return Py_BuildValue("s", result);
}

static PyObject* py_concatpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int len1, len2, i;
	unsigned int temp;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	result = malloc(len1+len2-2+1);
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

	return Py_BuildValue("s", result);
}

static PyObject* py_bvltpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) < strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_bvlepy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) <= strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_bvgtpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) > strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_bvgepy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if(strtoul(str1+2, NULL, 2) >= strtoul(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_sbvltpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;
	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if((int)strtol(str1+2, NULL, 2) < (int)strtol(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_sbvlepy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if((int)strtol(str1+2, NULL, 2) <= (int)strtol(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_sbvgtpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if((int)strtol(str1+2, NULL, 2) > (int)strtol(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

static PyObject* py_sbvgepy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int maxlen, len1, len2;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	len2 = (int)strlen(str2);
	maxlen = (len1 > len2)? len1 : len2;
	result = malloc(maxlen+1);
	memset(result, '0', 1);
	memset(result+1, 'b', 1);
	memset(result+2, '0', maxlen-2);
	memset(result+maxlen, 0, 1);
	if((int)strtol(str1+2, NULL, 2) >= (int)strtol(str2+2, NULL, 2))
		memset(result+maxlen-1, '1', 1);

	return Py_BuildValue("s", result);
}

// not finished yet
static PyObject* py_bvsxpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2;
	char* result;
	int len1, length, i;
	unsigned int temp;

	if(!PyArg_ParseTuple(args, "ss", &str1, &str2))
		return NULL;

	len1 = (int)strlen(str1);
	
	length = strtoul(str2+2, NULL, 2) + 2;
	result = malloc(length+1);
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
	
	return Py_BuildValue("s", result);
}

static PyObject* py_bvpluspy(PyObject* self, PyObject* args)
{
	const char* str1, *str2, *str3;
	char* result;
	unsigned int temp;
	int length, i;

	if(!PyArg_ParseTuple(args, "sss", &str1, &str2, &str3))
		return NULL;

	temp = strtoul(str2+2, NULL, 2) + strtoul(str3+2, NULL, 2);
	length = strtoul(str1+2, NULL, 2) + 2;
	
	result = malloc(length+1);
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

	return Py_BuildValue("s", result);
}

static PyObject* py_bvsubpy(PyObject* self, PyObject* args)
{
	const char* str1, *str2, *str3;
	char* result;
	unsigned int temp;
	int length, i;

	if(!PyArg_ParseTuple(args, "sss", &str1, &str2, &str3))
		return NULL;

	temp = strtoul(str2+2, NULL, 2) - strtoul(str3+2, NULL, 2);
	length = strtoul(str1+2, NULL, 2) + 2;
	
	result = malloc(length+1);
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

	return Py_BuildValue("s", result);
}



static PyMethodDef c_function_module_methods[] = {
	{"int2", py_int2, METH_VARARGS, "int2"},
	{"sint2", py_sint2, METH_VARARGS, "sint2"},
	{"eqpy", py_eqpy, METH_VARARGS, "eqpy"},
	{"extractpy", py_extractpy, METH_VARARGS, "extractpy"},
	{"notpy", py_notpy, METH_VARARGS, "notpy"},
	{"andpy", py_andpy, METH_VARARGS, "andpy"},
	{"orpy", py_orpy, METH_VARARGS, "orpy"},
	{"concatpy", py_concatpy, METH_VARARGS, "concatpy"},
	{"bvltpy", py_bvltpy, METH_VARARGS, "bvltpy"},
	{"bvlepy", py_bvlepy, METH_VARARGS, "bvlepy"},
	{"bvgtpy", py_bvgtpy, METH_VARARGS, "bvgtpy"},
	{"bvgepy", py_bvgepy, METH_VARARGS, "bvgepy"},
	{"sbvltpy", py_sbvltpy, METH_VARARGS, "sbvltpy"},
	{"sbvlepy", py_sbvlepy, METH_VARARGS, "sbvlepy"},
	{"sbvgtpy", py_sbvgtpy, METH_VARARGS, "sbvgtpy"},
	{"sbvgepy", py_sbvgepy, METH_VARARGS, "sbvgepy"},
	{"bvsxpy", py_bvsxpy, METH_VARARGS, "bvsxpy"},
	{"bvpluspy", py_bvpluspy, METH_VARARGS, "bvpluspy"},
	{"bvsubpy", py_bvsubpy, METH_VARARGS, "bvsubpy"},
	{NULL, NULL, 0, NULL}
};

void initc_function_module()
{
	(void) Py_InitModule("c_function_module", c_function_module_methods);
}