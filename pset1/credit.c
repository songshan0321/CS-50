#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int cardNumberLength(double number);

int main(void)
{
    printf("Input a bank card number: ");
    long long inp = get_long_long();
    int length = cardNumberLength(inp);
    int total = 0;
    long long number = inp;

    for(int i=0; i < length; i++)
    {
        int last = number % 10;  /*get the last digit*/
        if(i%2==0)
        {
            total += last;
        }
        else
        {
            if(last*2>=10)
            {
                int digits = 0;
                int last2 = last*2;
                while(last2>0)
                {
                    digits += (last2)%10;
                    last2 /= 10;
                }
                total += digits;
            }
            else
            {
                total += last*2;
            }
        }
        number /= 10;  /*track digit from smaller digit to bigger digit*/
    }
    if(total % 10 == 0)
    {
        int head2 = (int)(inp/pow(10,length-2));
        int head1 = (int)(inp/pow(10,length-1));
        if(length == 15 && (head2 == 34 || head2 == 37))
        {
            printf("AMEX\n");
        }
        else if(length == 16 && (head2 >= 51 && head2 <= 55))
        {
            printf("MASTERCARD\n");
        }
        else if((length == 13 || length == 16) && (head1 == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

int cardNumberLength(double number)
{
    int length = 0;
    while(number > 1)
    {
        number /= 10;
        length ++;
    }
    return length;
}