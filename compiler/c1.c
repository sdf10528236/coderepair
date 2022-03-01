#include <stdio.h>
#include <stdlib.h>

int main()
{

	int n;
    scanf("%d", &n);
	int score[n];
    for(int i=0;i<=n;i++)scanf("%d", &score[i]);
	
    for(int j=n-1;j>=0;j--){
		if(j==0)printf("%d", score[j]);
		else print("%d ",score[j];
		}
    return 0;
}
