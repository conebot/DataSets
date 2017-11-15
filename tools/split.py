#
# Split XML image annotation file into subfiles
# (imglab format)
#
# Use: split.py xml-file proportion-1 proportion-2 ...
#

import sys
import xml.etree.ElementTree as ET
from random import shuffle

def readxmlfile(name):
	tree = ET.parse(name)
	root = tree.getroot()
	return tree, root


def main(argv):
	tree, root = readxmlfile(argv[0])
	imgs = root.find('images')
	imglist = imgs.findall('image')
	proportions = []
	total = 0.0
	shuffle(imglist)
	for p in argv[1:]:
		proportions.append(int(p))
		total += int(p)
	if total == 0:
		proportions = [60, 20, 20]
		total = 100.0
	imglists = []
	ind = 0
	for p in proportions:
		num = int(len(imglist) * p/total)
		l = []
		for i in range(ind,ind + num):
			l.append(imglist[i])
		imglists.append(l)

	for l in range(0,len(imglists)):
		for ri in imgs.findall('image'):
			imgs.remove(ri)
		for i in imglists[l]:
			imgs.append(i)
		tree.write('set-%d.xml' % l)

if __name__ == "__main__":
	main(sys.argv[1:])
