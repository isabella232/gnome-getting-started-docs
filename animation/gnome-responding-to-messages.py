import bpy,os,re,gnomerender
from xml.etree import ElementTree as ET

def typewriteit(scene):
  typewrite = bpy.data.objects['typewriter'].data.body
  typewrite2 = bpy.data.objects['typewriter2'].data.body
  typewrite3 = bpy.data.objects['typewriter3'].data.body
  #psani zacina v sekvenci na 152
  if bpy.context.scene.frame_current >= 152:
    i = int((bpy.context.scene.frame_current-152)/2)
  else:
    i = 0
  if bpy.context.scene.frame_current >= 640:
    j = int((bpy.context.scene.frame_current-640)/2)
  else:
    j = 0
  if bpy.context.scene.frame_current >= 1024:
    k = int((bpy.context.scene.frame_current-1024)/2)
    #print(k,typewrite3)
  else:
    k = 0
  #print(typewrite, i, typewrite[:i])
  bpy.data.objects['bubble.response'].data.body = typewrite[:i]
  bpy.data.objects['bubble.response2'].data.body = typewrite2[:j]
  bpy.data.objects['bubble.response3'].data.body = typewrite3[:k]

def main():
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    if (lang[0]=="#"):
      pass
    else:
      xmlfile = ET.parse('../gnome-help/' + lang + '/gs-animation.xml')
      t[lang] = xmlfile.getroot()
      for textobj in t[lang].findall('t'):
        if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
          bpy.data.objects[textobj.get('id')].data.body = textobj.text
      bpy.data.objects['typewriter'].data.body = t[lang].find('t[@id="bubble.response"]').text
      bpy.data.objects['typewriter2'].data.body = t[lang].find('t[@id="bubble.response2"]').text
      bpy.data.objects['typewriter3'].data.body = t[lang].find('t[@id="bubble.response3"]').text
      #bpy.data.objects['user.mt.bubble'].data.body = bpy.data.objects['user'].data.body #needs to be left aligned :/
      gnomerender.render(lang)
      gnomerender.transcode(lang)
    
if __name__ == '__main__':
  bpy.app.handlers.frame_change_pre.append(typewriteit)
  main()

# vim: tabstop=2 expandtab
