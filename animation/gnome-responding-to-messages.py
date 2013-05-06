import bpy,os,re,gnomerender
from xml.etree import ElementTree as ET

def main():
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    xmlfile = ET.parse('../gnome-help/' + lang + '/gs-animation.xml')
    t[lang] = xmlfile.getroot()
    for textobj in t[lang].findall('t'):
      if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
        bpy.data.objects[textobj.get('id')].data.body = textobj.text
    bpy.data.objects['typewriter'].data.body = t[lang].find('t[@id="bubble.response"]').text
    bpy.data.objects['typewriter2'].data.body = t[lang].find('t[@id="bubble.response2"]').text
    bpy.data.objects['typewriter3'].data.body = t[lang].find('t[@id="bubble.response3"]').text
    bpy.data.objects['user.mt.bubble'].data.body = bpy.data.objects['user'].data.body #needs to be left aligned :/
    gnomerender.render(lang)
    gnomerender.transcode(lang)
    
if __name__ == '__main__':
    main()
