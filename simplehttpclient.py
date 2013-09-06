import httplib

def postit(server, url, xml):

	http = httplib.HTTP(server)
	http.putrequest("POST", url)
	http.putheader("User-Agent", "Simple")
	http.putheader("Host", server)
	http.putheader("Content-Length", "%d" % len(xml))
	http.putheader("Pragma", "no-cache")
	http.endheaders()
	http.send(xml)

	# get the HTTP response
	reply, message, headers = http.getreply()

	# print any reponse that's not 200 success
	if int(reply) != 200:
		print "Reply: ", reply, message
	else:
		result = http.getfile().read()

		#SUCCESS: f5d1944b-984d-46bb-960d-97bc7d9dc788
		result = result.replace("SUCCESS: ", "")
		return result

def post(server, url, xml):
	if type(xml) == str:
		return postit(server, url, xml)
	else:
		guids = []
		for x in xml:
			guids.append(postit(server, url, x))
		return guids
		
def get(server, url):
	http = httplib.HTTP(server)
	http.putrequest("GET", url)
	http.putheader("User-Agent", "Simple")
	http.putheader("Host", server)
	http.putheader("Pragma", "no-cache")
	http.endheaders()
	http.send("")

	# get the HTTP response
	reply, message, headers = http.getreply()

	# print any reponse that's not 200 success
	if int(reply) != 200:
		print "Reply: ", reply, message
	else:
		result = http.getfile().read()
		return result


def evalpost(server, url, body):
    http = httplib.HTTP(server)
    http.putrequest("POST", url)
    http.putheader("User-Agent", "Simple")
    http.putheader("Host", server)
    http.putheader("Content-Length", "%d" % len(body))
    http.putheader("Pragma", "no-cache")
    http.endheaders()
    http.send(body)
    
    # get the HTTP response
    reply, message, headers = http.getreply()
    
    # print any reponse that's not 200 success
    if int(reply) != 200:
    	print "Reply: ", reply, message
    else:
    	src = http.getfile().read()
        src = src.replace("true", "True")
        src = src.replace("false", "False")
        return eval(src)

		
def evalget(server, url):
    src = get(server, url)
    src = src.replace("true", "True")
    src = src.replace("false", "False")
    return eval(src)
    