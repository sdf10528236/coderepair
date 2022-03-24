import json, base64, os
import urllib.parse

code = '''
#include <stdio.h>

int main()
{   
    int x[5][5], y[5][5];
   int a, b;
   for(a=0;a<5;a++)
   {
       for(b=0;b<5;b++)
       {
           scanf("%d", &x[a][b]);
       }
   }
   for(a=0;a<5;a++)
   {
       for(b=0;b<5;b++)
       {
           y[b][a]=x[a][b];
       }
   }
   for(a=0;a<5;a++)
   {
       for(b=0;b<5;b++)
       {
           printf(" %2d", y[b][a]);
       }
	   printf("\n")
   }
    return 0;
}


'''

data = {
    "probid": 'test001', # this.problem.id,
    "info": "INFO",
    "subid": "Subid",
    "code": code,
}

datastr = json.dumps(data) #.replace("'", "\\'")
msg = base64.b64encode(datastr.encode())
umsg = urllib.parse.quote(msg)
command = f"curl http://140.135.13.120:3000/test3388/pred3388?q={umsg}"
ans = os.popen(command).read()
with open('result.html', 'w') as f:
    f.write(ans)
