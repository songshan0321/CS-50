#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do{
        printf("Input a height: ");
        height = get_int();
    } while(height < 0 || height > 23);

    for(int i = 1; i<=height; i++)
        {
            for(int j = 0; j<height-i; j++) /*spaces*/
            {
                printf(" ");
            }
            for(int k = 0; k<i; k++) /*hashes*/
            {
                printf("#");
            }


            printf("  ");

            for(int k = 0; k<i; k++) /*hashes*/
            {
                printf("#");
            }

            printf("\n");
        }
}