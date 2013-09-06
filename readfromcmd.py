#/usr/bin/env python

import sys, os

x = [i for i in sys.argv[1:]]

if __name__ == '__main__':
	for i in x:
		print i
	print "SPACE"
	print x[0]
	
