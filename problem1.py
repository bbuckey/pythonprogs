#usr/bin/env python

import os, sys, math, glob, decimal

loc = "/users/bbuckey/projects/pythonprogs/double_squares.txt"
infile = open(loc,'r')
#z = [float(n) for n in range(0,11)] 
#x = [float(n) for n in range(0,11)] 
n = 100.0

if __name__ == '__main__':
	listl = [n for n in infile.readlines()]
	lista = []
	listb = []
	for n in listl:
		for a in range(0,(int(n)/2)):
			for b in range(0,(int(n)/2)+1):
				if n == 0 and a+b == 0:
					lista.append(a,b)
				if a+b != 0:
					x = float((a*a)+(b*b)) 
					print (a,b)
					print x
					if x == n:
						if (b,a) not in lista:
							lista.append((a,b))
#	lista = list(set(lista))
	print lista
	
