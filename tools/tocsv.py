#
# Convert imglab XML image annotation files to CSV with image sizes
#
#  Use: filter-bb.py file1 file2 ...
#

import sys
import os
import re
import xml.etree.ElementTree as ET

def readxmlfile(name):
	tree = ET.parse(name)
	root = tree.getroot()
	return tree, root

def main(argv):
	tree, root = readxmlfile(argv[0])
	imgs = root.find('images')
	for i in imgs.findall('image'):
		xs = 0
		ys = 0
		dope = os.popen("identify %s" % i.get('file')).read()
		m = re.search(' ([0-9]+)x([0-9]+) ',dope)
		if m:
			xs = int(m.group(1))
			ys = int(m.group(2))
		for b in i.findall('box'):
			l = int(b.get('left'))
			t = int(b.get('top'))
			h = int(b.get('height'))
			w = int(b.get('width'))
			xmax = l + w
			ymax = t + h
			print "%s,%d,%d,%s,%d,%d,%d,%d" % (i.get('file'),xs,ys,'cone',l,t,xmax,ymax)


if __name__ == "__main__":
	main(sys.argv[1:])
