#!/usr/bin/env python

import glob
import os
from xml.etree import ElementTree

TEMP = './tmp.svg'

def rebrand(f, brand):
  svg = ElementTree.parse(fname)
  for e in svg.iterfind("/svg/g/rect[@id='background']"):
    print(e)
    e.set('style', 'fill:url(#%s);' % (brand,))
    print svg.dump(e)
  svg.write(TEMP)

for fname in glob.glob('*svg'):
  print fname
  rebrand(fname, "RHEL7")
  os.system("inkscape --vacuum-defs -l ../getting-started/C/figures/%s %s" % (fname, TEMP))
  os.unlink(TEMP)
