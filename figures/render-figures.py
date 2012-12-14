#!/usr/bin/env python

import glob
import os
from xml.etree import ElementTree

TEMP = './tmp.svg'

def rebrand(fname, brand):
  svg = ElementTree.parse(fname)
  for e in svg.iterfind(".//{http://www.w3.org/2000/svg}rect[@id='background']"):
    e.set('style', 'fill:url(#%s);' % (brand,))
  svg.write(TEMP)

for fname in glob.glob('*svg'):
  print fname
  rebrand(fname, "BLANK") #BLANK, GNOME, RHEL7
  os.system("inkscape --vacuum-defs -l ../getting-started/C/figures/%s %s" % (fname, TEMP))
  os.unlink(TEMP)
