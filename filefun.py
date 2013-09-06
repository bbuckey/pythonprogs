#/usr/bin/env python

import calendar, os, sys, datetime, gc, random, lxml, glob

lists = []
loc = "/users/bbuckey/projects/_dev/logs/logs"



if __name__ == '__main__':
	print datetime.datetime.now().time()
	os.chdir(loc)
	if not(gc.isenabled()):
		gc.enable()
	lists = glob.glob("*/*")
#	print lists
	for l in lists:
		temp = str(random.randint(1,734802312))
		temp2 = str(datetime.datetime.now().time())
		temp3 = str(l)
#		temp4 = temp3.index(temp3.find("("), temp3.find(")"))		
		print temp3.find(")")
		print temp3.find("(")
		temp4 = temp3[temp3.find("("):temp3.find(")")+1]
		print temp
		print temp2
#		print temp3
		temp5 = "%s-%s_%s" % (temp,temp2,temp4)
#		print l
		temp5 = temp5.replace(":","_")
		temp5 = temp5.replace(".","_")
		os.rename(l,temp5+".xml")
	
