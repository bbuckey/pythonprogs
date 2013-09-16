from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
import re
import threading
import simplehttpclient
import os
import time

LOCK_FILE_NAME = "alreadyrunning.lock"



def getGUID(xml):
	guid = re.search('<guid>(.*)</guid>', xml)
	if guid != None:
		return guid.group(1)
	else:
		raise "Missing GUID! %s" % xml
		
def getElapsed(xml):
	m = re.search('<serviceElapsed>(.*)</serviceElapsed>', xml)
	if m != None:
		return int(m.group(1))
	else:
		raise "Missing elapsed! %s" % xml


class CallbackHandler(BaseHTTPRequestHandler):

	# simple shutdown hook.  any GET request stops the server
	def do_GET(self):
		self.send_response(200, "OK")
		self.send_header("Content-Type", "text/xml")
		self.end_headers()
		self.server.stop = True


	def do_POST(self):

		try:
			# body of callback...
			xml = self.rfile.read(int(self.headers['content-length']))

			print "Handling response for %s" % getGUID(xml)
			self.send_response(200, "OK")
			self.send_header("Content-Type", "text/xml")
			self.end_headers()
			self.wfile.write("<thanks>for the callback!</thanks>")
			elapsed = getElapsed(xml)

			results = [{"batch math service": elapsed }]
			outfile = open("JobFarmMonitor", "w")
			outfile.write(str(results))
			outfile.close()
		except:
			print "ERROR!"
		
		os.remove(LOCK_FILE_NAME)
		self.server.stop = True

		
class StoppableHttpServer (HTTPServer):
    def serve_forever (self):
        self.stop = False
        while not self.stop:
            self.handle_request()

class ServerThread(threading.Thread):
	def run(self):
		server = StoppableHttpServer(("localhost", 8888), CallbackHandler)
		server.serve_forever()	



# -------------------------------------------------------------------------------------------------



# we only want one of these running at a time...
if not os.path.exists(LOCK_FILE_NAME):

	lock = open(LOCK_FILE_NAME, "w")
	lock.write(str(time.time()))
	lock.close()	

	serverThread = ServerThread()
	serverThread.start()



	batchaddition = """<ServiceRequest>
		<service class="service.sample.BatchAdditionService">
			<numberOfAdditions>25</numberOfAdditions>
		</service>
	  <requester>123123</requester>
	  <callbacks>
		<string>http://localhost:8888</string>
	  </callbacks>
	</ServiceRequest>"""


	print "Posted %s" % simplehttpclient.post("bfchsfarm004", "queue/internal", batchaddition)
	
else:
	print """
	There is another instance of this programming currently running.
	
	Delete %s to unlock the program so that another instance can run""" % LOCK_FILE_NAME
