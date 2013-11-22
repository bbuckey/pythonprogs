import os, sys, math, glob, decimal

loc = "alphasoup.txt"
infile = open(loc,'r')
#z = [float(n) for n in range(0,11)] 
#x = [float(n) for n in range(0,11)] 


if __name__ == '__main__':
	dictc = dict()
	lista = [a for a in 'HACKERUP']
	listl = [n.rstrip('\n') for n in infile.readlines()]
	y = listl[1]
	listl = listl[1:]
	for a in listl:
		for b in a:
			for c in 'HACKERUP':
				if c in b and dictc.has_key(c):
					dictc[c] += 1
				elif c in b:
					dictc[c] = 1
		dictc.clear()