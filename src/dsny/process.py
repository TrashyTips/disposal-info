
import urllib2
import xml.etree.ElementTree as ET
import StringIO
import re
import glob
import errno    
import os


def mkdir(path):
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise


try: 
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from bs4 import BeautifulSoup

def isNotEmbed( tag ):
	return tag.name not in [ 'iframe', 'embed', 'object', 'param' ]

def isNotLink( tag ):
	return tag.name not in [ 'a' ]

def shouldClean( tag ):
	return tag.name not in [ 'iframe', 'embed', 'object', 'param', 'a' ]

def download_and_save():

	urls = [
		"/assets/dsny/zerowaste/residents/what-to-recycle-for-residents.shtml",
		"/assets/dsny/zerowaste/residents/antifreeze.shtml",
		"/assets/dsny/zerowaste/residents/appliances.shtml",
		"/assets/dsny/zerowaste/residents/art-supplies.shtml",
		"/assets/dsny/zerowaste/residents/asbestos.shtml",
		"/assets/dsny/zerowaste/residents/auto-batteries.shtml",
		"/assets/dsny/zerowaste/residents/batteries.shtml",
		"/assets/dsny/zerowaste/residents/gas-tanks.shtml",
		"/assets/dsny/zerowaste/residents/curbside-setout-for-residents.shtml",
		"/assets/dsny/zerowaste/residents/textiles.shtml",
		"/assets/dsny/zerowaste/residents/books-and-media.shtml",
		"/assets/dsny/zerowaste/residents/furniture.shtml",
		"/assets/dsny/zerowaste/residents/yard-waste.shtml",
		"/assets/dsny/zerowaste/residents/lighting.shtml",
		"/assets/dsny/zerowaste/residents/specially-handled-items.shtml",
		"/assets/dsny/zerowaste/residents/electronics.shtml",
		"/assets/dsny/zerowaste/residents/deposit-bottles.shtml",
		"/assets/dsny/zerowaste/residents/home-improvement-waste.shtml",
		"/assets/dsny/zerowaste/residents/cell-phones.shtml",
		"/assets/dsny/zerowaste/residents/childrens-items.shtml",
		"/assets/dsny/zerowaste/residents/christmas-trees.shtml",
		"/assets/dsny/zerowaste/residents/cleaning-products.shtml",
		"/assets/dsny/zerowaste/residents/housewares.shtml",
		"/assets/dsny/zerowaste/businesses/who-picks-up-recycling-and-garbage-for-businesses.shtml",
		"/assets/dsny/zerowaste/residents/cosmetics.shtml",
		"/assets/dsny/zerowaste/residents/non-recyclable-plastics.shtml",
		"/assets/dsny/zerowaste/residents/eyeglasses.shtml",
		"/assets/dsny/zerowaste/residents/corrosive-and-flammable.shtml",
		"/assets/dsny/zerowaste/residents/food-waste.shtml",
		"/assets/dsny/zerowaste/residents/household-medical-waste.shtml",
		"/assets/dsny/zerowaste/businesses/commerical-landscaper-waste.shtml",
		"/assets/dsny/zerowaste/residents/medical-equipment.shtml",
		"/assets/dsny/zerowaste/residents/mercury-containing-devices.shtml",
		"/assets/dsny/zerowaste/residents/motor-oil.shtml",
		"/assets/dsny/zerowaste/residents/musical-instruments.shtml",
		"/assets/dsny/zerowaste/residents/paint.shtml",
		"/assets/dsny/zerowaste/residents/pesticides.shtml",
		"/assets/dsny/zerowaste/residents/ink-and-toner-cartridges.shtml",
		"/assets/dsny/zerowaste/residents/smoke-detectors.shtml",
		"/assets/dsny/zerowaste/residents/sport-equipment.shtml",
		"/assets/dsny/zerowaste/residents/junk-mail.shtml",
		"/assets/dsny/zerowaste/residents/tires.shtml",
		"/assets/dsny/about/laws/vehicle-and-bike-laws.shtml"
	]

	urlTemplate = 'http://www1.nyc.gov%s'
	files = dict()
	xmls = dict()

	W  = '\033[0m'  # white (normal)
	R  = '\033[31m' # red
	G  = '\033[32m' # green
	O  = '\033[33m' # orange
	B  = '\033[34m' # blue
	P  = '\033[35m' # purple
	C  = '\033[36m' # cyan
	GR = '\033[37m' # gray
	T  = '\033[93m' # tan
	ERROR   = R+'ERROR'+W
	SUCCESS = G+'OK   '+W

	for url in urls:
		try:
			files[ url ] = urllib2.urlopen( urlTemplate % (
				url
			)).read()
		except urllib2.HTTPError:
			print '['+ERROR+'] download %s' % url
		else:
			print '['+SUCCESS+'] download %s' % url

	for url in files:
		xml = BeautifulSoup( files[url] )
		html = xml.body.find('div', attrs={'id':'contentsection'})
		xmls[ url ] = html
		#xml = ET.fromstring( files[ url ] )
		#xmls[ url ] = root.findall("[@id='contentsection']")
		#for tag in html.findAll(  ):
		#	del tag.attrs
		with( open(re.sub('/.*/','html_raw/',url), 'w' )) as f:
			f.write( '%s' % html )

if __name__ == '__main__':
	
	# Download and save the recycling info pages
	mkdir( 'html_raw' )
	mkdir( 'html' )
	download_and_save()

	# Modify each page so that it has only the specific content
	for filename in glob.glob( './html_raw/*.shtml' ):
		
		# Load the file
		with open( filename ) as f:
			html = BeautifulSoup( f.read() )

		print 'Loaded %s' % filename
		
		# Remove all classes, ids, etc from the tags
		print '%s' % html.findAll('a')
		for tag in html.findAll( shouldClean ):
			if tag.name == 'a':
				print tag
				continue
			while len(tag.attrs):
				tag.attrs.pop()
		
		# Replace iframes with links to the iframed content
		# This is because youtube iframes load very slowly and really
		# hurt performance
		for iframe in html.findAll( 'iframe' ):
			url = iframe['src']
			while len(iframe.attrs):
				iframe.attrs.pop()
			iframe.name = u'a'
			iframe.attrs.append( (u'href', url) )
			iframe.string = url.encode('utf-8')

		# Remove the 2 outer divs and convert to a string
		try:
			newContent = u''.join( [u'%s' % content for content in html.div.div.contents ] ).encode('utf-8')
		except AttributeError:
			newContent = u''.join( [u'%s' % content for content in html.div.contents ] ).encode('utf-8')
		with open( filename.replace('shtml','html').replace('html_raw','html'), 'w' ) as f:
			f.write( newContent )
