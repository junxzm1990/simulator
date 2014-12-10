#include <Python.h>

static PyObject* py_hello_world(PyObject* self, PyObject* args)
{
	char *s = "Hello World from C!\n";
	printf("%s\n", ()args);
	return Py_BuildValue("s", s);
}

static PyMethodDef myModule_methods[] = {
	{"hello_world", py_hello_world, METH_VARARGS},
	{NULL, NULL}
};

void initmyModule()
{
	(void) Py_InitModule("myModule", myModule_methods);
}