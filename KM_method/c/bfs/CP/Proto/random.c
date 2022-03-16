#include<stdio.h>
#include<stdlib.h>
 
int main()
{
	int a,b;
	srand(100);   //我參數輸入１００做例子
	for(a=1;a<5;a++)
	{
		b = rand();
		printf("%d\n",b);
	}
	return 0;
}
