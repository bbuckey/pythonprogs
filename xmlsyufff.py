#/usr/bin/env python

import calendar, os, sys, datetime
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

mrktbd = dict()
segments = ["SGRP", "REG"]
extensions = ["xml", "TRAD"]
ext_translations = { "xml" : "HMO", "TRAD" : "TRAD", "" : "" }

def get_icap_docs_for_day(segment, vday, extension):
	return [etree.parse(f) for f in glob("%s/*%s.%d%02d%02d*.%s" % \
					     (loc, segment, vyear, vmonth, vday, extension))]
						 
#def get_market_segments(doc):
#	return doc.xpath("distinct-values(//Sponsors/Sponsor/MarketSegment/text())")

#def get_regions(doc, msegs):
#	return doc.xpath("distinct-values(//Sponsors/Sponsor[MarketSegment/text() = "+msegs+"]//Benefit/CarrierIdentifiers/CarrierIdentifier[Name = 'CARRIER_CODE']/Value/text())")
	
def file_adds(doc):
	return doc.xpath("count(//Benefit/TransactionType[text() = 'AD' or text() = 'RR'])")

def file_changes(doc):
	return doc.xpath("count(//Benefit/TransactionType[text() = 'CH' or text() = 'CSA_CHANGE'])")

def file_terms(doc):
	return doc.xpath("count(//Benefit/TransactionType[text() = 'CA'])")

def get_file_counts(doc):
	return [file_adds(doc),
		file_changes(doc),
		file_terms(doc)]
		
def get_totals_for_day(vyear, vmonth, vday):
	counts = []
	mrktseg = []
	mrktreg = []
	for segment in segments:
		for extension in extensions:
			cur = [0, 0, 0, segment, extension]
			for doc in get_icap_docs_for_day(segment, vday, extension):
	#			mrktseg = get_market_segments(doc)
	#			for ms in mrktseg:
	#				mrktreg = get_regions(doc, ms)
	#				for mr in mrktreg
				fc = get_file_counts(doc)
	#					mrktdb[ms]=[fc,mr,segment,extension]	
				if len(fc) > 0:
					cur[0] += fc[0]
					cur[1] += fc[1]
					cur[2] += fc[2]
			counts.append(cur)
	total = [0, 0, 0, "TOTAL", ""]
	for cnt in counts:
		total[0] += cnt[0]
		total[1] += cnt[1]
		total[2] += cnt[2]
	counts.append(total)
	return counts

def print_totals(totals):
	if len(totals) == 0:
		print "No data for this day."
	else:
		for total in totals:
			print("%s\t%s\t AD: %d, CH: %d, CA: %d, TOT: %d" % \
			      (total[3], ext_translations[total[4]], total[0], total[1], total[2], total[1] + total[0] + total[2]))
	

if __name__ == '__main__':
	for vday in days:
		print "Totals for %d/%d" % (vmonth, vday)
		print_totals(get_totals_for_day(vyear, vmonth, vday))
