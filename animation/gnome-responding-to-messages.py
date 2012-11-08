import bpy,os,re
from xml.etree import ElementTree as ET

def typewriteit(scene):
  typewrite = bpy.data.objects['typewriter'].data.body
  typewrite2 = bpy.data.objects['typewriter2'].data.body
  #psani zacina v sekvenci na 152
  if bpy.context.scene.frame_current >= 152:
    i = int((bpy.context.scene.frame_current-152)/2)
  else:
    i = 0
  if bpy.context.scene.frame_current >= 640:
    j = int((bpy.context.scene.frame_current-640)/2)
  else:
    j = 0
  #print(typewrite, i, typewrite[:i])
  bpy.data.objects['bubble.response'].data.body = typewrite[:i]
  bpy.data.objects['mt.bubble.response'].data.body = typewrite2[:j]

def render(lang):
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  bpy.context.scene.render.use_sequencer = 1
  renderpath = '//sequence/'+lang
  if (not renderpath):
    os.mkdir(renderpath)
  bpy.context.scene.render.filepath = "//" + renderpath + '/responding-to-messages-'
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
    bpy.data.objects['typewriter'].data.body = t[lang].find('t[@id="bubble.response"]').text
    bpy.data.objects['typewriter2'].data.body = t[lang].find('t[@id="bubble.response"]').text
    bpy.data.objects['user.mt.bubble'].data.body = bpy.data.objects['user'].data.body #needs to be left aligned :/
    render(lang)
    
if __name__ == '__main__':
    bpy.app.handlers.frame_change_pre.append(typewriteit)
    main()
    bpy.app.handlers.frame_change_pre.pop(0)
