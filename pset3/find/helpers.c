/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    if(n <= 0)
    {
        return false;
    }
    int left = 0;
    int right = n-1;
    int mid;
    while(left <= right)
    {
        mid = left + (right - left)/2;

        if(values[mid] == value)
        {
            return true;
        }
        // value at left half
        else if(values[mid] > value)
        {
            right = mid - 1;
        }
        // value at right half
        else
        {
            left = mid + 1;
        }
    }
    return false;

}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    if(n < 2)
    {
        return;
    }
    int temp;
    int min;
    for(int i = 0; i < n; i++)
    {
        min = i;
        for(int j = i; j < n; j++)
        {
            if(values[j] < values[min])
            {
                min = j;
            }
        }
        temp = values[i];
        values[i] = values[min];
        values[min] = temp;
    }
    return;
}
