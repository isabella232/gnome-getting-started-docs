import bpy,os,re,gnomerender
from xml.etree import ElementTree as ET
#from bpy.app.handlers import persistent

def typewriteit(scene):
  #FIXME make this happen only in scene "launching apps - keyboard"
  typewrite = bpy.data.objects['typewriter'].data.body
  #psani zacina v sekvenci na 630
  if bpy.context.scene.frame_current >= 630:
    i = int((bpy.context.scene.frame_current- 630)/3)
  else:
    i = 0
  #print(typewrite, i, typewrite[:i])
  bpy.data.objects['search'].data.body = typewrite[:i]

def main():
  global typewrite
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    #t[lang] = yaml.load(open('translations/'+file))
    if (lang[0]=="#"):
      pass
    else:
      xmlfile = ET.parse('../gnome-help/' + lang + '/gs-animation.xml')
      t[lang] = xmlfile.getroot()

      for textobj in t[lang].findall('t'):
        if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
          bpy.data.objects[textobj.get('id')].data.body = textobj.text
      bpy.data.objects['typewriter'].data.body = t[lang].find('t[@id="search"]').text
      gnomerender.render(lang)
      gnomerender.transcode(lang)
    
if __name__ == '__main__':
  bpy.app.handlers.frame_change_pre.append(typewriteit)
  main()

# vim: tabstop=2 expandtab
