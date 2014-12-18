#include <Python.h>

static PyObject* py_hello_world(PyObject* self, PyObject* args)
{
	int str1[5];

	if(!PyArg_ParseTuple(args, "i", str1))
		return NULL;
	printf("%d, %d, %d\n", str1[0], str1[1], str1[2]);
}

static PyMethodDef myModule_methods[] = {
	{"hello_world", py_hello_world, METH_VARARGS, "hello_world"},
	{NULL, NULL, 0, NULL}
};

void initmyModule()
{
	(void) Py_InitModule("myModule", myModule_methods);
}