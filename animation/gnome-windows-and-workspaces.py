import bpy,os,re
from xml.etree import ElementTree as ET

def render(lang):
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  bpy.context.scene.render.use_sequencer = 1
  renderpath = '//sequence/'+lang
  if (not renderpath):
    os.mkdir(renderpath)
  bpy.context.scene.render.filepath = "//" + renderpath + '/windows-and-workspaces-'
  if (not os.path.isfile(bpy.context.scene.render.frame_path())):
    bpy.ops.render.render(animation=True)
  else:
    print('already rendered')
  transcodepath = "../getting-started/" + lang + "/figures/"
  regexobj = re.search(r"^(.*\/)(.*)-(\d*)-(\d*)(\.avi)$", bpy.context.scene.render.frame_path())
  webmfile = regexobj.group(2) + ".webm"
  transcodecmd = "ffmpeg -y -i " + bpy.context.scene.render.frame_path() + " -b:v 8000k " + transcodepath + webmfile
  if (not os.path.isfile(transcodepath+webmfile)):
    os.system(transcodecmd)
  else:
    print('already transcoded',transcodepath + webmfile)
        
#translates strings and calls render
def main():
  global typewrite
  
  t = {}
  #unfortunately no decent fonts have ↲
  langs = open('language-whitelist.txt').readlines()
  for lang in langs:
    lang = lang.strip()
    xmlfile = ET.parse('../getting-started/' + lang + '/animation.xml')
    t[lang] = xmlfile.getroot()
    for textobj in t[lang].findall('t'):
      if textobj.get('id') in bpy.data.objects: #prelozit jestli existuje jako index
        bpy.data.objects[textobj.get('id')].data.body = textobj.text
    render(lang)
    
if __name__ == '__main__':
    main()
