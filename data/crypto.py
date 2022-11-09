###################################################
#                                                 #
# Program: crypto                                 #
#                                                 #
# Purpose: encrypts and decrypts data             #
#                                                 #
# Author: Jonathan Hull         Date: 18 Dec 2020 #
#                                                 #
###################################################

from os import path
import sys
import random

###################################################
#                                                 #
# function key_gen:                               #
#                                                 #
# purpose: generate a new key                     #
#                                                 #
###################################################
def key_gen(l):
    min_val = 0
    max_val = 1114111 - 200

    key = ""
    for i in range(l):
        key = key + chr(random.randint(min_val, max_val))

    return key

###################################################
#                                                 #
# function in_code:                               #
#                                                 #
# purpose: encrypt data for secure storage        #
#                                                 #
###################################################
def in_code(k, s):
    out = ""
    i = 0
    for c in s:
        out = out + chr(ord(c) + ord(k[i % len(k)]))
        i = i + 1
    return out

###################################################
#                                                 #
# function de_code:                               #
#                                                 #
# purpose: decrypt data from secure storage       #
#                                                 #
###################################################
def de_code(k, s):
    out = ""
    i = 0
    for c in s:
        out = out + chr(ord(c) - ord(k[i %len(k)]))
        i = i + 1
    return out

###################################################
#                                                 #
# function main:                                  #
#                                                 #
# purpose: when ran as main program creates a new #
#          key and stores it in new_key.py so it  #
#          does not overwrite a current key.      #
#                                                 #
###################################################
if __name__ == "__main__":
    string = "This is some test data. If the data does not look like this at the end of this output something has gone wrong."
    print(string)
    if len(sys.argv) > 1:
        try:
            key = key_gen(int(sys.argv[1]))
        except:
            key = key_gen(64)
    else:
        key = key_gen(64)
    key = key.replace('\n', '')
    print("New key is: " + key)
    key_file = open("new_key.py", "w+")
    key_file.write("def key():")
    key_file.write("\treturn \"{}\"".format(key))
    key_file.close()

    import new_key
    coded = in_code(new_key.key(), string)
    print("Coded = {}".format(coded))
    print("Decoded = {}".format(de_code(new_key.key(), coded)))




