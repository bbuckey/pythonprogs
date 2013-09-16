import calendar, os, sys, datetime, codecs
from lxml import etree
from glob import glob

xeparser = etree.XMLParser(recover=True,huge_tree=True,ns_clean=True)
#xeparser = etree.XMLParser(encoding="ISO-8859-1")
#xeparser = etree.XMLParser(recover="true",resolve_entities="false",huge_tree="true")
#xeparser = etree.XMLParser(recover="true",huge_tree="true")



loc = "/Users/bbuckey/projects/results/123/*.xml"

xmlfils = [ x for x in glob(loc)]

if __name__ == '__main__':

	for x in xmlfils:
		print x
		fname = str(x)[str(x).rfind('/'):]
#		os.chdir("/users/bbuckey/desktop/")
		xmloutfl = ("/users/bbuckey/desktop/%s" % fname)
		print xmloutfl
		wf = codecs.open(xmloutfl,"w","utf-8")
		doc = etree.parse(x,xeparser)
		wf.write(etree.tostring(doc,pretty_print=True ))
		wf.flush()
		wf.close()	

