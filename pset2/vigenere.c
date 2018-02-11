#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int keyToNum(char keyword);
int checkAlpha(string key);

int main(int argc, string argv[])
{
    if(argc != 2 || !checkAlpha(argv[1]))
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    else
    {
        string s = get_string();
        int n = strlen(argv[1]);
        int sn = strlen(s);
        char cipher[sn+1];
        for(int i = 0 ; i < sn ; i++)
        {
            char ori = s[i];
            if(isupper(ori))
            {
                ori -= 65;
                int ans = (ori + keyToNum(argv[1][i%n])) % 26 ;
                ans += 65;
                cipher[i] = (char)ans;
            }
            else if(islower(ori))
            {
                ori -= 97;
                int ans = (ori + keyToNum(argv[1][i%n])) % 26 ;
                ans += 97;
                cipher[i] = (char)ans;
            }
            else
            {
                cipher[i] = s[i];
            }
        }
    printf("plaintext: %s\n",s);
    printf("ciphertext: %s\n",cipher);
    return 0;
    }
}

int keyToNum(char keyword)
{
    int outp = 0;
    if(isalpha(keyword))
    {
        outp = toupper(keyword) - 65;
    }
    else
    {
        outp = keyword;
    }
    return outp;
}

int checkAlpha(string key)
{
    for(int i = 0, n = strlen(key); i < n; i++)
    {
        if(isalpha(key[i]) == false)
        {
            return false;
        }
    }
    return true;
}