#/usr/bin/env python

import calendar, os, sys, datetime, gc, glob,random, codecs
from lxml import etree
xeparser = etree.XMLParser(recover=True,huge_tree=True,ns_clean=True)

lists = []
stated = dict()
#unicode(u'\u2026', errors='ignore')
loc = "/users/bbuckey/projects/_dev/logs/logs"



if __name__ == '__main__':
#--	print datetime.datetime.now().time()
	wf = codecs.open("/users/bbuckey/projects/_dev/logs/logs/totallogs3.txt","w","utf-8")
	os.chdir(loc)
	if not(gc.isenabled()):
		gc.enable()
	lists = glob.glob("*/*.xml")
#--	print lists
#--	list2 = [etree.parse(l) 
	h = ""
	list2 = list()
	list3 = list()	
	for l in lists:
		try:
			doc = etree.parse(l,xeparser)
			xeval = etree.XPathEvaluator(doc)
			list2 = list(set(xeval("//@sender")))
			list3 = list(set(xeval("//@time")))
		except:
			pass
		finally:
			h = str(l)
#--		h = str(h)
#--		print h
			h = h[h.find("("):h.find(")")+1]
#--		print list3
#--		print list2
			for l3 in list3:
				for l2 in list2:
#--					h = h.index(h.find("("), h.find(")")+1)
					keydi = "on %s : %s : %s" % (h,l3,l2[0:2])
#--					print keydi
					temp33 = ("//*[@sender = '%s' and @time = '%s' ]//text()") % (str(l2), str(l3))
	#--			print temp33
#--				print keydi
					list4 = xeval(temp33)
#--				print list4
					if len(list4) > 0:
#--					list5 = [ str(n2) for n2 in list4]
						stated[keydi]=list4
	listkey = [ s for s in stated.keys()]
#--	print listkey[0:5]
	listkey.sort()
#--	print listkey[0:5]
#--	x = 0
#--	while x < 
#--	print listkey
	for l in listkey:
		wf.write("%s\n" % l)
		for l2 in stated[l]:
#--			print stated[l]
#--			print l
#--			print l2
#--			l3 = l2.replace("","..")
#--			l3 = str(l2)
			wf.write(l2)
			wf.write("\n")
#--			print l2
	wf.flush()
	wf.close()	
		
#--	events = ("start","data")
#--	print list2
#	for doc in list2:
#		xeval = etree.XPathEvaluator(doc)
#		print xeval("*")
#		print xeval("//text()")


#		for d in doc.iterfind("*"):
#			print d.event
#			print d.tag
#			print d
#			print d
#		for event, d in etree.iterparse(doc,events=events)
#			print "%s : %s" % (event, d.tag)
		


#		temp = str(random.randint(1,734802312))
#		temp2 = str(datetime.datetime.now().time())
#		temp3 = str(l)
#		temp4 = temp3.index(temp3.find("("), temp3.find(")"))		
#		print temp3.find(")")
#		print temp3.find("(")
#		temp4 = temp3[temp3.find("("):temp3.find(")")+1]
#		print temp
#		print temp2
#		print temp3
#		temp5 = "%s-%s_%s.xml" % (temp,temp2,temp4)
#		os.rename(l,temp5)
	
