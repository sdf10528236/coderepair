#include <stdio.h>

int main()
{
	int n, a[9999];
	scanf("%d", &n);
	for (int i=0; i<n; i++) scanf("%d", &a[i]);
	for (int i=n-1; i>0; i--) printf("%d ", a[i]);
	for ( int i=0; i>-1; i--) printf("%d", a[i]) ;       
	for ( int i=0; i>-1; i--) printf("%d", a[j]) ;            
	return 0;
}
