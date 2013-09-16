#/usr/bin/env python

import calendar, os, sys, datetime, gc
from lxml import etree
from glob import glob

cal = calendar.Calendar()
currdate = datetime.datetime.now()
checkstr = "CcOo"
loc = "/users/bbuckey/projects/testdata"
vmonth = -1
vyear = -1

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

#mrktbd = dict()
segments = ["SGRP", "REG"]
extensions = ["xml", "TRAD"]
ext_translations = { "xml" : "HMO", "TRAD" : "TRAD", "" : "" }

def get_icap_docs_for_day(segment, vday, extension):
	return [etree.parse(f) for f in glob("%s/*%s.%d%02d%02d*.%s" % \
					     (loc, segment, vyear, vmonth, vday, extension))]
						 
def get_market_segments(doc):
	return doc.xpath("//Sponsor/MarketSegment/text()")

#def get_regions(doc, msegs):
#	if len(msegs) > 0:
#		msegs = "[MarketSegment/text() = '"+msegs+"']"
#	return doc.xpath("//Sponsor"+msegs+"//CarrierIdentifier[Name = 'CARRIER_CODE']/Value/text()")

def get_regions(doc):
	return doc.xpath("//CarrierIdentifier[Name = 'CARRIER_CODE']/Value/text()")

def file_adds(doc,mseg,regions):
	if len(mseg) > 0:
		mseg = "[MarketSegment/text() = '"+mseg+"']"
	if len(regions) > 0:
		regions = "[CarrierIdentifiers/CarrierIdentifier[Name = 'CARRIER_CODE' and Value = '"+regions+"']]"
	return doc.xpath("count(//Sponsor"+mseg+"//Benefit"+regions+"/TransactionType[text() = 'AD' or text() = 'RR'])")

def file_changes(doc,mseg,regions):
	if len(mseg) > 0:
		mseg = "[MarketSegment/text() = '"+mseg+"']"
	if len(regions) > 0:
		regions = "[CarrierIdentifiers/CarrierIdentifier[Name = 'CARRIER_CODE' and Value = '"+regions+"']]"
	return doc.xpath("count(//Sponsor"+mseg+"//Benefit"+regions+"/TransactionType[text() = 'CH' or text() = 'CSA_CHANGE'])")

def file_terms(doc,mseg,regions):
	if len(mseg) > 0:
		mseg = "[MarketSegment/text() = '"+mseg+"']"
	if len(regions) > 0:
		regions = "[CarrierIdentifiers/CarrierIdentifier[Name = 'CARRIER_CODE' and Value = '"+regions+"']]"
	return doc.xpath("count(//Sponsor"+mseg+"//Benefit"+regions+"/TransactionType[text() = 'CA'])")

def get_file_counts(doc,m,re):
	return [file_adds(doc,m,re),
		file_changes(doc,m,re),
		file_terms(doc,m,re)]
		
def get_totals_for_day(vyear, vmonth, vday):
#	counts = []
	mrktdb = {}
	for segment in segments:
		for extension in extensions:
			for doc in get_icap_docs_for_day(segment, vday, extension):
				mrkseg = []
				mrkreg = []
				mrkkey = ""
				mrkseg = list(set(get_market_segments(doc)))
				print mrkseg
				mrkreg = list(set(get_regions(doc)))
#				for ms in mrkseg:
#					mrkreg = list(set(get_regions(doc, ms)))
				print mrkreg
				if len(mrkseg) > 0 and len(mrkreg) > 0:
					for ms in mrkseg:
						for mr in mrkreg:
							fc = get_file_counts(doc,ms,mr)
							print ms + " " + mr
							print fc
							mrkkey = ms+":"+mr+":"+extension+":"+segment
							if mrktdb.has_key(mrkkey):
								listt = mrktdb[mrkkey]
								fc[0] += listt[0][0]
								fc[1] += listt[0][1]
								fc[2] += listt[0][2]
							mrktdb[mrkkey]=[fc,mr,segment,extension]
				elif len(mrkseg) > 0 and not(len(mrkreg) > 0):
					for ms in mrkseg:
						mrkkey = ms+":"+":"+extension+":"+segment					
						fc = get_file_counts(doc,ms,"")
						print ms
						print fc
						if mrktdb.has_key(mrkkey):
							listt = mrktdb[mrkkey]
							fc[0] += listt[0][0]
							fc[1] += listt[0][1]
							fc[2] += listt[0][2]
						mrktdb[mrkkey]=[fc,"",segment,extension]
				else:
					mrkkey = ":"+":"+extension+":"+segment
					fc = get_file_counts(doc,"","")
					print fc
					if mrktdb.has_key(mrkkey):
						listt = mrktdb[mrkkey]
						fc[0] += listt[0][0]
						fc[1] += listt[0][1]
						fc[2] += listt[0][2]
					mrktdb[mrkkey]=[fc,"",segment,extension]
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
	if len(mrktdb) == 0:
		print "No data for this day."
	else:
		for valkey in mrktdb.keys():
			print valkey 
			print mrktdb.get(valkey)	
	
#		for total in totals:
#			print("%s\t%s\t AD: %d, CH: %d, CA: %d, TOT: %d" % \
#			      (total[3], ext_translations[total[4]], total[0], total[1], total[2], total[1] + total[0] + total[2]))
	

if __name__ == '__main__':
	print datetime.datetime.now().time()
	if not(gc.isenabled()):
		gc.enable()
	for vday in days:
		print datetime.datetime.now().time()
#		print "Totals for %d/%d" % (vmonth, vday)
#		printmkdict = get_totals_for_day(vyear, vmonth, vday)
		print_totals(get_totals_for_day(vyear, vmonth, vday))
#	print_totals()
	print datetime.datetime.now().time()


