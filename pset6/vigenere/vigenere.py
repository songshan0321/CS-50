import sys
from cs50 import get_string


if len(sys.argv) != 2 or sys.argv[1].isalpha() == False:
    print("Usage: ./vigenere k")
    exit(1)

def keyToNum(keychar):
    """Convert keyword into key"""
    if keychar.isupper():
        return ord(keychar)-65
    elif keychar.islower():
        return ord(keychar)-97


keyword = sys.argv[1]
plain = get_string("plaintext: ")
cipher = ""
counter = 0
for i in range(len(plain)):
    if plain[i].isupper():
        index = ord(plain[i])-65
        temp = (index + keyToNum(keyword[counter % len(keyword)]))% 26
        temp += 65
        cipher += chr(temp)
        counter +=1

    elif plain[i].islower():
        index = ord(plain[i])-97
        temp = (index + keyToNum(keyword[counter % len(keyword)]))% 26
        temp += 97
        cipher += chr(temp)
        counter +=1
    else:
        cipher += plain[i]
print("ciphertext: " + cipher)