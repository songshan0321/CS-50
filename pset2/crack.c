#define _XOPEN_SOURCE
#include <unistd.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[])
{
    if(argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }

    const char* hashed_given = argv[1];
    char word[5];
    const char* salt = "50";
    char* hashed_word = NULL;
    char* alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    //check a-Z
    for(int x = 0 ; x < 52 ; x++ )
    {
        word[0] = alphabet[x];
        hashed_word = crypt(word,salt);
        printf("word: %s     hashed word: %s\n",word,hashed_word);
        if(strcmp(hashed_word,hashed_given) == 1)
        {
            goto PRINT;
        }
    }

    //check aa-ZZ
    for(int x = 0 ; x < 52 ; x++ )
    {
        word[0] = alphabet[x];
        for(int y = 0 ; y < 52 ; y++ )
        {
            word[1] = alphabet[y];
            hashed_word = crypt(word,salt);
            printf("word: %s     hashed word: %s\n",word,hashed_word);
            if(strcmp(hashed_word,hashed_given) == 0)
            {
                goto PRINT;
            }
        }
    }

    //check aaa-ZZZ
    for(int x = 0 ; x < 52 ; x++ )
    {
        word[0] = alphabet[x];
        for(int y = 0 ; y < 52 ; y++ )
        {
            word[1] = alphabet[y];
            for(int z = 0 ; z < 52 ; z++ )
            {
                word[2] = alphabet[z];
                hashed_word = crypt(word,salt);
                printf("word: %s     hashed word: %s\n",word,hashed_word);
                if(strcmp(hashed_word,hashed_given) == 0)
                {
                    goto PRINT;
                }
            }
        }
    }

    //check aaaa-ZZZZ
    for(int x = 0 ; x < 52 ; x++ )
    {
        word[0] = alphabet[x];
        for(int y = 0 ; y < 52 ; y++ )
        {
            word[1] = alphabet[y];
            for(int z = 0 ; z < 52 ; z++ )
            {
                word[2] = alphabet[z];
                for(int t = 0 ; t < 52 ; t++ )
                {
                    word[3] = alphabet[t];
                    hashed_word = crypt(word,salt);
                    printf("word: %s     hashed word: %s\n",word,hashed_word);
                    if(strcmp(hashed_word,hashed_given) == 0)
                    {
                        goto PRINT;
                    }
                }
            }
        }
    }


    PRINT: printf("%s\n",word);

    return 0;
}