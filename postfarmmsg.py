import simplehttpclient, os, re, sys, json, codecs
import fnmatch 
import glob
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import time
import textwrap
from xml.dom.minidom import parse 

def parse_properties(pfile):
	result = {}
	lines = pfile.readlines()
	for line in lines:
		line = line.replace(os.linesep,'').strip()
		if '#' in line:
			if line.find('#') == 0 or line.find('#') == 1:
				line = ""
			else:
				line = str(line[0:line.find('#')+1]).strip()
		if len(line) == 0:
			continue
		else:
		#	line = codecs.encode(line)
			kv = line.split('=')
			result[str(kv[0])] = str(kv[1])
	return result
	
class JFXML:

	def __init__(self):
		self.xml = ""

	def setServiceXml(self,fpath):
		print fpath
		thxl = open(fpath,'r+')
		temper = parse(thxl)
#		print "result from read()"
#		print temper
#		print temper[0:]
#		print str(temper[0:])
		self.xml = temper.toxml()
		thxl.close()

	def setServiceXmlReadln(self,fpath):
		print fpath
		thxl = open(fpath,'r+')
		temper = thxl.readlines()
		print "result from readlines()"
		print temper
		print temper[0:]
		print "try read"
		self.xml = temper.zip()
		thxl.close()

	def withCallback(self, callback):
		self.xml = self.xml.replace("</ServiceRequest>", "<callbacks><string>%s</string></callbacks></ServiceRequest>" % callback)
		#return self
    
	def getXml(self):
		return self

	def resetXml(self):
		self.xml = ""

	def __str__(self):
		return self.xml

  
if __name__ == "__main__":
	f = open("jobfarmcall.properties", 'r+')
	props = {}
	props = parse_properties(f)
	print "you have entered the following properties values"
	print props
	extractq = ("%s/%s" % (props['queue.url'],props['bundle.name']))
	if not props.has_key('callback.url'):
		callback = ""
	#	pass
	else:
		callback = props['callback.url']
	server = props['server.url']
	looper = True
	JF_DROP = props['drop.location']
	if not os.path.exists(JF_DROP):
		os.makedirs(JF_DROP)
	os.chdir(JF_DROP)
	f.close()
	lists = []
	theXl = JFXML()
	timer = time.clock()
	while(looper):
		lists = []
		try:
			lists = glob.glob("*.*")
		except:
			time.sleep(10) ##sleep for 10 sec
			lists = []
		else:
			timer = time.clock()
			for x in lists:
				if fnmatch.fnmatch(x.upper(), 'EXIT.*'):
					looper = False
					time.sleep(1)
					os.remove(os.path.join(JF_DROP,x))
					break;
				else:
					time.sleep(10)
					theXl.setServiceXml(os.path.join(JF_DROP,x))
					print "%s/%s" % (JF_DROP,x)
					if len(callback) > 0:
						theXl.withCallback(callback)
					print "getXML call and value"
					print theXl.getXml()
					print "The call back value"
					valrec = simplehttpclient.post(server,extractq,str(theXl.getXml()))
					print valrec	
					time.sleep(10)
					os.remove(os.path.join(JF_DROP,x))
		finally:
			if (time.clock() - timer) == 1.0:
				looper = False	
			else :
				time.sleep(10) 

#			theXl.resetXml()
#xm = etree.parse(fpath)
#with open(fpath,"r") as file:
#JF_HOME = os.getenv("BF_JOBFARM_HOME")
	#	if upper(theXml.name) == "EXIT" or :
	#	if fnmatch.fnmatch(fpath.upper(), 'EXIT.*'):
	#		self.xml = "CloseMePlease"
	#		theXml.close()
	#	else:	 
	#		temper = file.read()
	#		print "result from read()"
	#		print temper
	#		self.xml = str(temper) 
		#etree.tostring(theXml.read())
	#	theXml.flush()
	#	etree.parse(f) 
		#theXml.close()
	#	return self
#, parseString
#import uuid

