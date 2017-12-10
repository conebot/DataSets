#
# Catenate XML image annotation files
# (imglab format)
#
#  Use: combone.py file1 file2 ...
#

import sys
import xml.etree.ElementTree as ET

def readxmlfile(name):
	tree = ET.parse(name)
	root = tree.getroot()
	return tree, root


def main(argv):
	tree, root = readxmlfile(argv[0])
	imgs = root.find('images')
	for a in range(1,len(argv)):
		t, r = readxmlfile(argv[a])
		imgs2 = r.find('images')
		for i in imgs2.findall('image'):
			imgs.append(i)
	tree.write(sys.stdout)
	# newline
	print

if __name__ == "__main__":
	main(sys.argv[1:])
