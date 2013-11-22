#/usr/bin/env python

import calendar, os, sys, datetime, gc, glob,random, codecs


powerball = [i for i in range(1,47)]
picks = [i for i in range(1,57)]
allpicks = {}
loc = "2005-2011meganumbers.txt"
infile = open(loc,'r')
llist = [n.strip('\n').split('\t') for n in infile.readlines()]
flist = [(n[5],n[0:5]) for n in llist]
powpick = {}
copick = {}



if __name__ == '__main__':
	print powerball
	print picks
	mynums = []
	for i in picks:
		copick[int(i)] = 0
	for i in powerball:
		powpick[int(i)] = 0
#	print len(picks)
#	for j in range(1,6):
#		l = picks[random.randint(0,len(picks)-1)]
#		mynums.append(l)
		#print l
		#print picks - [l]
#		picks.remove(l)
		#print "new picks list"
		#print picks		
	#mynums = [picks[l] for l in [random.randint(0,len(picks)) for j in range(1,6)] picks.remove(picks[l])] #picks[random.randint(0,len(picks))]
#	print mynums
#	print picks
#	allpicks[powerball[random.randint(0,len(powerball)-1)]] = mynums
#	print allpicks
#	print llist
	#for n in llist:
		#for m in n.split('\t'):
	#	print n
	#	print n[0:5]
	#	print n[5]
	for f in flist:
		powpick[int(f[0])] += 1
#		print f[0]
#		print f[1]
		for c in f[1]:
			copick[int(c)] += 1
	for f in powpick.keys():
		print "%d was chosen: %d" % (f,powpick[f])
	for f in copick.keys():
		print "%d was chosen: %d" % (f,copick[f])
#	print len(flist)
#	print powpick
#	print copick
	infile.close()
		
