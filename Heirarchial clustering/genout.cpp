#include<bits/stdc++.h>
using namespace std;
int rand_gen()
{
	
	int x = rand() % 100000 + 1;
	return x;
}
int main()
{
	int n;
	cin>>n;
	cout<<n;
	srand ( time(NULL) );	
	for(int i=0;i<n;i++)
	{
		cout<<((double)rand_gen())/63<<" "<<((double)rand_gen())/63<<endl;
	}
	return 0;
}
