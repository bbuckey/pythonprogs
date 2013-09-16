#/usr/bin/env python

import calendar, os, sys, datetime, gc, threading
from lxml import etree
from glob import glob

cal = calendar.Calendar()
currdate = datetime.datetime.now()
checkstr = "CcOo"
loc = "/users/bbuckey/projects/testdata"
mrktdb = {}
vmonth = -1
vyear = -1
#ns = etree.FunctionNamespace('http://mydomain.org/myfunctions')
#ns.prefix = 'fn'

pinstr = raw_input("Please enter the value C to run a count for the (C)urrent month or O to enter a (O)ther month: ")
if '\n' in pinstr:
	pinstr = pinstr.replace("\n","")

while pinstr not in checkstr:
	pinstr = raw_input("A invalid value was entered please enter C for the (C)urrent month or O to enter a (O)ther month: ")
	if '\n' in pinstr:
		pinstr = pinstr.replace("\n","")
			
if pinstr in "Cc":
	vmonth = currdate.month
	vyear = currdate.year
elif pinstr in "Oo":
	vmonth = input("Please enter a Month: ")
	vyear = input("Please enter a Year: ")
	while vmonth > currdate.month or vmonth < 1 or vyear > currdate.year or vyear < 2000:
		print("You have entered a invalid month or year")
		vmonth = input("Please enter a month: ")
		vyear = input("Please enter a Year: ")

days = [vday for vday in cal.itermonthdays(vyear, vmonth) if vday != 0]

segments = ["SGRP", "REG"]
extensions = ["xml", "TRAD"]
ext_translations = { "xml" : "HMO", "TRAD" : "TRAD", "" : "" }

def get_icap_docs_for_day(segment, vday, extension):
	return [etree.parse(f) for f in glob("%s/*%s.%d%02d%02d*.%s" % \
					     (loc, segment, vyear, vmonth, vday, extension))]
						 
def get_market_segments(doc):
	return doc("//Sponsor/MarketSegment/text()")

#def get_regions(doc, msegs):
#	if len(msegs) > 0:
#		msegs = "[MarketSegment/text() = '"+msegs+"']"
#	return doc.xpath("//Sponsor"+msegs+"//CarrierIdentifier[Name = 'CARRIER_CODE']/Value/text()")


def get_regions(doc):
	return doc("//CarrierIdentifier[Name = 'CARRIER_CODE']/Value/text()")

def file_adds(doc,mseg,regions):
	if len(mseg) > 0:
		mseg = "[MarketSegment/text() = '"+mseg+"']"
	if len(regions) > 0:
		regions = "[CarrierIdentifiers/CarrierIdentifier[Name = 'CARRIER_CODE' and Value = '"+regions+"']]"
	return 	doc("count(//Sponsor%s//Benefit%s/TransactionType[text() = 'AD' or text() = 'RR'])" % (mseg,regions))
#doc("count(/Sponsors//Sponsor"+mseg+"//Benefit"+regions+"/TransactionType[text() = 'AD' or text() = 'RR'])")


#def file_adds(doc,mseg,regions):
#	for 

def file_changes(doc,mseg,regions):
	if len(mseg) > 0:
		mseg = "[MarketSegment/text() = '"+mseg+"']"
	if len(regions) > 0:
		regions = "[CarrierIdentifiers/CarrierIdentifier[Name = 'CARRIER_CODE' and Value = '"+regions+"']]"
	return doc("count(//Sponsor%s//Benefit%s/TransactionType[text() = 'CH' or text() = 'CSA_CHANGE'])" % (mseg,regions))
#doc("count(/Sponsors//Sponsor"+mseg+"//Benefit"+regions+"/TransactionType[text() = 'CH' or text() = 'CSA_CHANGE'])")

def file_terms(doc,mseg,regions):
	if len(mseg) > 0:
		mseg = "[MarketSegment/text() = '"+mseg+"']"
	if len(regions) > 0:
		regions = "[CarrierIdentifiers/CarrierIdentifier[Name = 'CARRIER_CODE' and Value = '"+regions+"']]"
	return doc("count(//Sponsor%s//Benefit%s/TransactionType[text() = 'CA'])" % (mseg,regions))
#doc("count(/Sponsors//Sponsor"+mseg+"//Benefit"+regions+"/TransactionType[text() = 'CA'])")


def get_file_counts(doc,m,re):
	return [file_adds(doc,m,re),
		file_changes(doc,m,re),
		file_terms(doc,m,re)]
		
def get_totals_for_day(vyear, vmonth, vday):
#	counts = []
	#mrktdb = {}
#	exten = "";
	for segment in segments:
	#	print datetime.datetime.now().time()
	#	print "Segment loop"
		for extension in extensions:
	#		print datetime.datetime.now().time()
	#		print "exentsion loop"
			for doc in get_icap_docs_for_day(segment, vday, extension):
				exten = ""
				if extension == "xml":
					exten = "HMO"
				else:
					exten = extension
			#	xeval = etree.XPathEvaluator(doc,namespaces=ns)
			#	print datetime.datetime.now().time()
			#	print "xml loop"
				xeval = etree.XPathEvaluator(doc,smart_strings=False)
				mrkseg = []
				mrkreg = []
				mrkkey = ""
				mrkseg = list(set(get_market_segments(xeval)))
			#	mrkseg = get_market_segments(xeval)
#				print mrkseg
				mrkreg = list(set(get_regions(xeval)))
			#	mrkreg = get_regions(xeval)
#				for ms in mrkseg:
#					mrkreg = list(set(get_regions(doc, ms)))
#				print mrkreg
				mrkreg += [""]
				mrkseg += [""]
				#if len(mrkseg) > 0 and len(mrkreg) > 0:
				for ms in mrkseg:
					for mr in mrkreg:
					#		print datetime.datetime.now().time()
					#		print "n*n ms and mr loop"
#					fc = [get_file_counts(doc,ms,mr) for ms in mrkseg for mr in mrkreg]
						fc = get_file_counts(xeval,ms,mr)
#							print ms + " " + mr
#							print fc
						mrkkey = "%s:%s:%s:%s" % (ms,mr,exten,segment)
						if mrktdb.has_key(mrkkey):
							listt = mrktdb[mrkkey]
							fc[0] += listt[0][0]
							fc[1] += listt[0][1]
							fc[2] += listt[0][2]
						mrktdb[mrkkey]=[fc,mr,segment,exten]
			#	elif len(mrkseg) > 0 and not(len(mrkreg) > 0):
#					fc = [get_file_counts(doc,ms,"") for ms in mrkseg]
			#		for ms in mrkseg:
					#	print datetime.datetime.now().time()
					#	print "n loop ms only"
			#			mrkkey = "%s::%s:%s" % (ms,exten,segment)				
			#			fc = get_file_counts(xeval,ms,"")
#					print ms
#					print fc
			#			if mrktdb.has_key(mrkkey):
			#				listt = mrktdb[mrkkey]
			#				fc[0] += listt[0][0]
			#				fc[1] += listt[0][1]
			#				fc[2] += listt[0][2]
			#			mrktdb[mrkkey]=[fc,"",segment,exten]
			#	else:
#					mrkkey = ":"+":"+exten+":"+segment
			#		mrkkey = "::%s:%s" % (exten,segment)
			#		fc = get_file_counts(xeval,"","")
#					print fc
#					print datetime.datetime.now().time()
#					print "no ms or mr, loop"
			#		if mrktdb.has_key(mrkkey):
			#			listt = mrktdb[mrkkey]
			#			fc[0] += listt[0][0]
			#			fc[1] += listt[0][1]
			#			fc[2] += listt[0][2]
			#		mrktdb[mrkkey]=[fc,"",segment,exten]
				del doc
				del xeval
#	print mrktdb
	return mrktdb
#				if len(fc) > 0:
#					cur[0] += fc[0]
#					cur[1] += fc[1]
#					cur[2] += fc[2]
#			counts.append(cur)
#	total = [0, 0, 0, "TOTAL", ""]
#	for cnt in counts:
#		total[0] += cnt[0]
#		total[1] += cnt[1]
#		total[2] += cnt[2]
#	counts.append(total)
#	return counts

def print_totals(mrktdb):
	xmlstr = "<?xml version='1.0' encoding='UTF-8'?>"
	xmlstr += '<aetnacount>'
	if len(mrktdb) > 0:
		xmlstr += '<markets>'
		for valkey in mrktdb.keys():
			klist = valkey.split(":") 
			vlist = mrktdb.get(valkey)
			xmlstr += '<marketsegment type="%s" regions="%s" segment="%s" extension="%s"><counts><count type="ADD">%d</count><count type="CHANGE">%d</count><count type="TERM">%d</count></counts></marketsegment>' % (klist[0],klist[1],klist[2],klist[3],vlist[0][0], vlist[0][1],vlist[0][2])
		xmlstr += '</markets>'
	xmlstr +='</aetnacount>' 
	del mrktdb
#	print xmlstr.strip()
	return etree.fromstring(xmlstr.rstrip())	
	
#		for total in totals:
#			print("%s\t%s\t AD: %d, CH: %d, CA: %d, TOT: %d" % \
#			      (total[3], ext_translations[total[4]], total[0], total[1], total[2], total[1] + total[0] + total[2]))
	

if __name__ == '__main__':
	print datetime.datetime.now().time()
	print "start of script"
#	if not(gc.isenabled()):
#		gc.enable()
	for vday in days:
#		print datetime.datetime.now().time()
#		print "days loop"
		get_totals_for_day(vyear, vmonth, vday)
#		print "Totals for %d/%d" % (vmonth, vday)
#		printmkdict = get_totals_for_day(vyear, vmonth, vday)
#		print_totals(get_totals_for_day(vyear, vmonth, vday))
#	print_totals(mrktdb)
#	print xmlstr
	print(etree.tostring(print_totals(mrktdb),pretty_print=True ))
#	print(etree.tostring(print_totals(mrktdb),pretty_print=False ))
#	print(print_totals(mrktdb))
	print datetime.datetime.now().time()
#	print "and the total time is"
#	print currdate.time() - datetime.datetime.now().time()
	print "end of script"


