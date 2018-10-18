import SimuateAPI
import json
SimuateAPI.chPathToThis(__file__)
data = {
    "username": "username",
    "password": "password",
    "problem": "1000",
    "lang": "1",
    "code": r"""#include<stdio.h>
int main()
{
    int a, b;
    while(~scanf("%d %d", &a, &b))
    {
        printf("%d\n", a + b);
    }
    return 0;
}
""",
    "command_executor": None,
    "session_id": None
}

with open('data.json', 'w') as dump_f:
    json.dump(data, dump_f)
