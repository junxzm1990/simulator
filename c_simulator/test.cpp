#include <cstring>
#include <iostream>
using namespace std;

int main()
{
	string a = "string";
	char b[2];
	char c[] = "xxxxx";
	strcpy(b, a.c_str());
	cout << b << endl;
	cout << c << endl;
}