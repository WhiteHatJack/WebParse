#@WhiteHatJack
#skeleton code to parse/handle website user inputted html using python
#last updated for python 2.7.10

from HTMLParser import HTMLParser
import urllib

#download html from url input (uses urllib)
base_url = raw_input('enter url to parse: ')
sock = urllib.urlopen(base_url)
html_source = sock.read()
sock.close()

#create parser method to override handlers (HTMLParser used now)
class htmlParse(HTMLParser):
	#handle things here
	def handle_starttag(self, tag, attrs):
		#fill in actions based on elements
		print("found starting tag! (update me)")
	def handle_endtag(self, tag):
		#fill in actions based on elements
		print("found ending tag! (update me)")
	def handle_data(self, data):
		print("found some data! (update me)")

#now feed the downloaded html to the parser
parser = htmlParse()
parser.feed(html_source)
