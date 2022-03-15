import json, base64, os
import urllib.parse

code = '''
#include <stdio.h>
int main()
{
    printf("Hello")
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
