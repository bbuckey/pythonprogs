from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from simplehttpclient import post
import cgi
import sys
import threading
import time
import re
import random


callbacks = []
RUNNING = False


def uuid():
	id = ""
	alphanum = "abcdefghijklmnopqrstuvwxyz01234567890"
	for i in range(24):
		index = random.randint(0, 36)
		id = id + alphanum[index]
	return id


class JFPostHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		self.server.stop = True
		RUNNING = False

	def do_POST(self):

		# lazy load the xml responses... i couldn't figure
		# out how to set a class instance variable w/o this exception...
		try:
			xml = self.exchangexml
		except:
			self.exchangexml = open("_eExchange_response.xml").read()
			self.stagexml = open("_Stage_response.xml").read()
			self.reconxml = open("_recon_response.xml").read()
			self.aqpxml = open("_aqp_response.xml").read()
			self.counter = 0
		

		# body of post...
		xml = self.rfile.read(int(self.headers['content-length']))
		print """What we got:
		
		%s""" % xml

		# send the successful post msg from Farm...
		#SUCCESS: f5d1944b-984d-46bb-960d-97bc7d9dc788
		self.send_response(200, "OK")
		self.send_header("Content-Type", "text/xml")
		self.end_headers()
		
		self.counter = self.counter + 1
		guid = uuid()
		self.wfile.write("SUCCESS: " + guid)

		callback = re.search("<string>(.*)</string>", xml)

		# what app got posted to?
		path = self.path
		if path.find("exchange") > -1:
			msg = self.exchangexml    
		elif path.find("stage") > -1:
			msg = self.stagexml
		elif path.find("recon") > -1:
			msg = self.reconxml
		elif path.find("aqp") > -1:
			msg = self.aqpxml
		else:
			msg = "Unknown application: %s" % path
		msg = msg.replace("__GUID__", guid)

		callbackurl = callback.group(1)
		callbacks.append((callbackurl, msg))
			
			
		
class StoppableHttpServer (HTTPServer):
    """http server that reacts to self.stop flag"""
    def serve_forever (self):
        """Handle one request at a time until stopped."""
        self.stop = False
        while not self.stop:
            self.handle_request()


class CallbackThread(threading.Thread):
	def run(self):
		while RUNNING:
			while len(callbacks) > 0:
				c = callbacks.pop(0)
				print "CALLBACK TO", c[0]
				post(c[0], "", c[1])
			time.sleep(1)
            
if __name__ == "__main__":

	RUNNING = True
	callbackThread = CallbackThread()
	callbackThread.setDaemon(True)
	callbackThread.start()

	server = StoppableHttpServer(('localhost', 8080), JFPostHandler)
	print 'Starting FakeJobFarm 2.0 on localhost:8080'
	server.serve_forever()