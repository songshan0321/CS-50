#include <stdio.h>
#include <cs50.h>

int main(void)
{
    printf("How long do you shower everyday? ");
    int minutes = get_int();
    printf("Minutes: %i\n", minutes);
    printf("Bottles: %i\n", minutes * 12);
}