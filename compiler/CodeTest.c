#include <stdio.h>

int main()
{
	int n, a[9999];
	scan("%d", &n);
	for (int i=0; i<n; i++) canf("%d", &a[i]);
	for (int i=n-1; i>0; i--) pintf("%d ", a[i]);
	for (int i=0; i>-1; i--) print("%d", a[i]);
	return 0;
}