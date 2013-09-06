import mechanize
from lxml import html


request = mechanize.Request("http://www.google.com")
response = mechanize.urlopen(request)
#print response.geturl()
#print response.info()
#print response.read()
x = html.fromstring(str(response.read()))

print x

