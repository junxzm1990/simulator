Use the following command to compile .so module from C source file

'''gcc -fPIC -shared -I/usr/include/python2.7/ -lpython2.7 -o c_function_module.so c_function_module.c'''