#include <bitset>
#include <iostream>
using namespace std;

int main()
{
	bitset<8> x(24);
	cout << "0b" + x.to_string() << endl;
}