# -*- coding: utf-8 -*-
"""
Created on Thu May 26 13:32:49 2022

@author: Thomas Mishler
"""

"""
Objectives:
    - Understand what the terminal is and how to run a written python program
    - Understand basic usage of random numbers
    - Understand basic string parsing
    - Understand basic file input and out with open() and .close()
    - Understand how to build a class
    - Understand how to build and parse a text file
    - Programming philosophy: Understand defensive programming
"""

"""
Instructions:
    - Copy this whole file into your own directory
    - Remove the instructor's name from the top and place your name
        - do the same with creation date
    - Follow the problem specifications that follow and make a python
      document that can run without any errors
    - If you want some extra practice, proceed to the extra practice document
"""
import random

# Problem 1
# Print a random whole number in the range of [1,10] (inclusive)
print(random.randint(1,10))

# Problem 2
# Print all of the perfect squares in the range of [1,10000]
# Note: you should use a loop (100 print statements will get you 0 points),
#       but you don't have to use 'for i in range(10000)' as your statement
a = 1
while (a <= 100):
    print(a*a)
    a=a+1

# Problem 3
# Open the file `abab.txt` and print the total number of times the character
# 'b' appears in the file
# This shouldn't be hard-coded. You should be printing from a variable!
# Don't forget to close the file when you're done!
# Note: you're allowed to look at how the file was generated if you want
myFile = open("abab.txt", "r")
rawtxt = myFile.read()
print(rawtxt)
myFile.close() #protect the file
a=0
for i in rawtxt:
    if i == "b":
        a = a+1
print(a)

# Problem 4
# Open the file `abab.txt` and print the following:
    # the longest sequence of 'a's in the file
    # the longest sequence of 'b's in the file
myFile = open("abab.txt", "r")
rawtxt = myFile.read()
myFile.close() #protect the file
a_count=0
b_count=0
a_record=0
b_record=0
for i in rawtxt:
    if i == "a":
        a_count=a_count+1
        b_count=0
        if a_count >= a_record:
            a_record = a_count
    else:
        b_count=b_count+1
        a_count=0
        if b_count >= b_record:
            b_record = b_count
aboys=""
for i in range(a_record):
    aboys=aboys+"a"
print(aboys)
bboys=""
for i in range(b_record):
    bboys=bboys+"b"
print(bboys)
