#usr/bin/env python

import os, sys, math, glob, decimal

loc = "double_squares.txt"
infile = open(loc,'r')
#z = [float(n) for n in range(0,11)] 
#x = [float(n) for n in range(0,11)] 


if __name__ == '__main__':
	listl = [n for n in infile.readlines()]
	lista = []
	listb = []
	dicta = dict()
	z = 0;
	c = 0; 
	for n in listl:
		c += 1;
		dicta[c] = 0;
	for n in listl:
		z += 1
		lista = [ a for a in range(0,int(math.sqrt(float(n))+1))]
		for a in lista:
			for b in lista[lista.index(a):]:
				if n == 0 and a+b == 0:
					listb.append(a,b)
				else:
					x = float((a*a)+(b*b))
					if int(x) == int(n):
						if (b,a) not in listb and (a,b) not in listb:
							dicta[z] += 1
#	lista = list(set(lista))
	print dicta
	
