#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    string s = get_string();
    if(isspace(s[0]) == 0)
        {
            printf("%c",toupper(s[0]));
        }
    for(int i = 0, n = strlen(s); i < n; i++)
    {
        if(isspace(s[i]) && isspace(s[i+1]) == 0)
        {
            if(i < n-1)
            {
               printf("%c",toupper(s[i+1]));
            }
        }
    }
    printf("\n");
}