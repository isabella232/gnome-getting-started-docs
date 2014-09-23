import bpy,os,re,gnomerender
from xml.etree import ElementTree as ET
from bpy.app.handlers import persistent

#changes the text in the searchbox (called before every frame change)
#to unassign: bpy.app.handlers.frame_change_pre.pop(0)

def typewriteit(scene):
    #FIXME make this happen only in scene "launching apps - keyboard"
    typewrite = bpy.data.objects['typewriter'].data.body
    #psani zacina v sekvenci na 618
    if bpy.context.scene.frame_current >= 915:
        i = int((bpy.context.scene.frame_current-915)/3)
    else:
        i = 0
    #print(typewrite, i, typewrite[:i])
    bpy.data.objects['search2'].data.body = typewrite[:i]


def main():
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    if (lang[0]=="#"):
      pass
    else:
      lang = lang.strip()
      xmlfile = ET.parse('../gnome-help/' + lang + '/gs-animation.xml')
      t[lang] = xmlfile.getroot()
      for textobj in t[lang].findall('t'):
        if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
          bpy.data.objects[textobj.get('id')].data.body = textobj.text
      bpy.data.objects['typewriter'].data.body = t[lang].find('t[@id="search2"]').text
      gnomerender.render(lang)
      gnomerender.transcode(lang)
    
if __name__ == '__main__':
  bpy.app.handlers.frame_change_pre.append(typewriteit)
  #bpy.app.handlers.frame_change_pre.pop(0)
  main()

# vim: tabstop=2 expandtab
