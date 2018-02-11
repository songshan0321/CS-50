# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

pneumonoultramicroscopicsilicovolcanoconiosis is the longest word in this problem set's dictionary.

## According to its man page, what does `getrusage` do?

Returns resource usage measures for its parameter 'who'

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Because C requires passing structs by reference in functions, because by value, the size would be too big

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

Speller.c reads words from the file, character by character, using a for loop to begin reading the first character of
the file, incrementing by one character until it reaches the end of the file. If the character is a letter or apostrophe,
it is added to a word. If the word becomes larger than what we have defined as the largest word possible, the word is
ignored. If the word has a digit, it is ignored as well.

If a word still exists, it is counted, checked for spelling, and printed. The amount of time it takes to complete
thechecking is logged in ti_check.
## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

To be able to account for numerical inputs and other punctuation which we have deemed invalid.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

Because word LENGTH and DICTIONARY are # declared as constants (word is an array of LENGTH+1)
