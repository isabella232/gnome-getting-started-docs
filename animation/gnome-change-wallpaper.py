import bpy,os
from xml.etree import ElementTree as ET

def render(lang):
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  bpy.context.scene.render.use_sequencer = 1
  renderpath = '../getting-started/'+lang+'/figures'
  if (not renderpath):
    os.mkdir(renderpath)
  bpy.context.scene.render.filepath = "//" + renderpath + '/changing-wallpaper-'
  if (not os.path.isfile(bpy.context.scene.render.frame_path())):
    bpy.ops.render.render(animation=True)
  else:
    print('already rendered')

#translates strings and calls render
def main():
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    xmlfile = ET.parse('../getting-started/' + lang + '/animation.xml')
    t[lang] = xmlfile.getroot()
  
  for lang in t:
    for textobj in t[lang].findall('t'):
      if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
        bpy.data.objects[textobj.get('id')].data.body = textobj.text
    bpy.data.objects['usermenuuser'].data.body = bpy.data.objects['user'].data.body #due to different alignment
    render(lang)
    
if __name__ == '__main__':
    #bpy.app.handlers.frame_change_pre.append(typewriteit)
    main()
    #bpy.app.handlers.frame_change_pre.pop(0)
