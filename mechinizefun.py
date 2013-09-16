import mechanize
import lxml
from lxml import html


request = mechanize.Request("http://www.google.com")
response = mechanize.urlopen(request)
#print response.geturl()
#print response.info()
#print response.read()
x = html.fromstring(str(response.read()))

if __name__ == '__main__':
	print html.
##	print lxml.etree.tostring(x, pretty_print=True) ## prints the html

