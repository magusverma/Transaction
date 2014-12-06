#include <stdio.h>
#include <map>
#define ll long long

class up{
public:
	ll min_util;
	ll max_support;
	up(ll util,ll support){
		min_util = util;
		max_support = support;
	}
	void show(){
		printf("%d\n",x);
	}
};

class db{
	public:
		transaction <int, int>, eqstr> months;
		db(){
			hash_map<const char*, int, hash<const char*>, eqstr> months;
		}
};
int main(){
	up problem = up(100,20,"mushroomT.dat","mushroomUtility.dat");
	problem.show();
	return 0;
}