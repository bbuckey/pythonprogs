#/usr/bin/env python

import calendar, os, sys, datetime, codecs 
from lxml import etree
from glob import glob

xeparser = etree.XMLParser(recover=True,huge_tree=True,ns_clean=True)
loc = "/users/bbuckey/projects/pythonprogs/BCBSNECORELINK_LG_20120106_025642.xml"

def split_sponsors():
	return [etree.parse(f).xpath("//Contract",smart_strings=False) for f in glob(loc)]

def print_splits(spon):
	xmlstr = '<bif:Extraction xmlns:bif="http://www.benefitfocus.com/schemas/bifedi">' 
	xmlstr += "<ProcessId>BCBSNECORELINK_LG_20120106_025607688</ProcessId>"
	xmlstr += "<ExtractionId>BCBSNECORELINK_LG_20120106_025607688</ExtractionId>"
	xmlstr += "<StartTime>20120106_025607000</StartTime>"
	xmlstr += "<EndTime>20120106_025641775</EndTime>"
	xmlstr += "<Operator>twilliams</Operator>"
	xmlstr += "<Database/>"
	xmlstr += "<Environment/>"
	xmlstr += "<Parameters>"
	xmlstr += "<Baseline>false</Baseline>"
	xmlstr += "<FullFile>true</FullFile>"
	xmlstr += "<NoHistorize>true</NoHistorize>"
	xmlstr += "<MapCode>BCBSNECORELINK_LG</MapCode>"
	xmlstr += "<Period>CURRENT</Period>"
	xmlstr += "<LogicalRunDate>20120106</LogicalRunDate>"
	xmlstr += "<SponsorOids>"
	xmlstr += "<SponsorOid>295328331</SponsorOid>"
	xmlstr += "</SponsorOids>"
	xmlstr += "</Parameters>"
	xmlstr += "<EDICarrier>"
	xmlstr += "<Name>BlueCross BlueShield of Nebraska</Name>"
	xmlstr += "<TaxID>000007780</TaxID>"
	xmlstr += "<Sponsors>"
	xmlstr += "<Sponsor>"
	xmlstr += "<Address>"
	xmlstr += "<PrimaryStreet>20220 Harney Street</PrimaryStreet>"
	xmlstr += "<SecondaryStreet/>"
	xmlstr += "<City>Elkhorn</City>"
	xmlstr += "<State>NE</State>"
	xmlstr += "<Country>USA</Country>"
	xmlstr += "<PostalCode>68022</PostalCode>"
	xmlstr += "</Address>"
	xmlstr += "<Name>Vetter Health Services Inc</Name>"
	xmlstr += "<GroupIdentifier>12320000</GroupIdentifier>"
	xmlstr += "<TaxID>999999999</TaxID>"
	xmlstr += "<Contracts>"
	for h in spon:
		xmlstr += etree.tostring(h);
	xmlstr += "</Contracts>"
	xmlstr += "</Sponsor>"
	xmlstr += "</Sponsors>"
	xmlstr += "</EDICarrier>"
	xmlstr += "</bif:Extraction>"
	return etree.tostring(etree.fromstring(xmlstr.strip(),xeparser),pretty_print=True)

if __name__ == '__main__':
	conl = split_sponsors()
	clist = conl.pop() #[b for b in [c for c in conl]]
	x = int(len(clist)/4)
	print len(clist)
	print x
	#for x in range(1,5)
	FILE1 = open("BCBSNECORELINK_LG_20120106_025642_1.xml","w")
	FILE2 = open("BCBSNECORELINK_LG_20120106_025642_2.xml","w")
	FILE3 = open("BCBSNECORELINK_LG_20120106_025642_3.xml","w")
	FILE4 = open("BCBSNECORELINK_LG_20120106_025642_4.xml","w")
	FILE1.writelines(print_splits(clist[0:x*1]))
	FILE1.close()
	FILE2.writelines(print_splits(clist[x+1:x*2]))
	FILE2.close()
	FILE3.writelines(print_splits(clist[(x*2)+1:x*3]))
	FILE3.close()
	FILE4.writelines(print_splits(clist[(x*3)+1:len(clist)]))
	FILE4.close()
	#FILE1.writelines(etree.tostring(print_splits(conl),pretty_print=True ))
	#FILE1.writelines(print_splits(conl))
	#FILE1.close()
	#FILE2.writelines(etree.tostring(print_splits(conl[x+1:len(conl)])),pretty_print=True)
	#FILE1.writelines(print_splits(conl))
	#FILE2.close()
	#del conl
	#return etree.tostring(etree.fromstring(xmlstr.strip()),pretty_print=True )
#cleanup_namespaces(
