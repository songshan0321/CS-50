// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

unsigned int word_count = 0;
bool loaded = false;
#define TABLE_SIZE 16

// create node struct
typedef struct node
    {
        char word[LENGTH + 1];
        struct node *next;
    }
    node;

// create hash table
node *hashtable[TABLE_SIZE];

/**
 * Hash function via reddit user delipity:
 * https://www.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9nlkn
 */
int getHash(const char* word)
{
    unsigned int hash = 0;
    for (int i=0, n=strlen(word); i<n; i++)
        hash = (hash << 2) ^ word[i];
    return hash % TABLE_SIZE;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *cursor = hashtable[getHash(word)];
    int len = strlen(word);
    char copy_word[len + 1];
    // convert word to lowercase and store it in word_copy
    for (int i = 0; i < len; i++)
    {
       copy_word[i] = tolower(word[i]);
    }

    copy_word[len] = '\0';

    while(cursor != NULL)
    {
        if (strcmp(cursor->word,copy_word) == 0)

        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // open input file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open dictionary.\n");
        return false;
    }

    // import words into new node, then link new node with hash table
    while(true)
    {
        node *new_node = malloc(sizeof(node));
        fscanf(file, "%s", new_node->word);
        new_node->next = NULL;

        if (feof(file))
        {
            // hit end of file
            free(new_node);
            break;
        }

        int index = getHash(new_node->word);

        node* head = hashtable[index];
        if (head == NULL)
        {
        hashtable[index] = new_node;
        }
        else
        {
            new_node->next = hashtable[index];
            hashtable[index] = new_node;
        }
        word_count++;
    }

    fclose(file);
    loaded = true;
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (loaded)
    {
    return word_count;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < TABLE_SIZE; i++)
    {
        node *cursor = hashtable[i];
        while(cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
            if (temp == NULL)
            {
                return false;
            }
        }
    }
    return true;
}
