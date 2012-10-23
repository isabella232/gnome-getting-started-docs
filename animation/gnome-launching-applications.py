import bpy,os
from xml.etree import ElementTree as ET

def typewriteit(scene):
  #FIXME make this happen only in scene "launching apps - keyboard"
  typewrite = bpy.data.objects['typewriter'].data.body
  #psani zacina v sekvenci na 563
  if bpy.context.scene.frame_current >= 563:
    i = int((bpy.context.scene.frame_current-563)/3)
  else:
    i = 0
  #print(typewrite, i, typewrite[:i])
  bpy.data.objects['search'].data.body = typewrite[:i]

def render(lang):
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  bpy.context.scene.render.use_sequencer = 1
  renderpath = '../getting-started/'+lang+'/figures'
  if (not renderpath):
    os.mkdir(renderpath)
  bpy.context.scene.render.filepath = "//" + renderpath + '/launching-apps-'
  if (not os.path.isfile(bpy.context.scene.render.frame_path())):
    bpy.ops.render.render(animation=True)
  else:
    print('already rendered')

#translates strings and calls render
def main():
  global typewrite
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    #t[lang] = yaml.load(open('translations/'+file))
    xmlfile = ET.parse('../getting-started/' + lang + '/animation.xml')
    t[lang] = xmlfile.getroot()
    for textobj in t[lang].findall('t'):
      if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
        bpy.data.objects[textobj.get('id')].data.body = textobj.text
    bpy.data.objects['typewriter'].data.body = t[lang].find('t[@id="search"]').text
    render(lang)
    
if __name__ == '__main__':
    bpy.app.handlers.frame_change_pre.append(typewriteit)
    main()
    bpy.app.handlers.frame_change_pre.pop(0)
