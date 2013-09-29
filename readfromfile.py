# File: readline-example-1.py

file = open("sample.txt")

while 1:
    line = file.readline()
    if not line:
	break
    pass # do something

#This snippet reads the file line by line. If readline reaches the end of the file, it returns an empty string. Otherwise, it returns the line of text, including the trailing newline character.

#On my test machine, using a 10 megabyte sample text file, this script reads about 32,000 lines per second.
#Using the fileinput module

#If you think the while loop is ugly, you can hide the readline call in a wrapper class. The standard fileinput module contains an input class which does exactly that.

# File: readline-example-2.py

#import fileinput

#for line in fileinput.input("sample.txt"):
 #   pass
# File: readline-example-3.py

#file = open("sample.txt")

#while 1:
 #   lines = file.readlines(100000)
 #   if not lines:
#	break
 #   for line in lines:
#	pass # do somethingv

# File: readline-example-5.py

#file = open("sample.txt")

#for line in file:
 #   pass # do something

#In Python 2.1, you have to use the xreadlines iterator factory instead:

# File: readline-example-4.py

#file = open("sample.txt")

#for line in file.xreadlines():
#    pass # do something

