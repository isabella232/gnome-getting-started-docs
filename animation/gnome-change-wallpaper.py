import bpy,os,re
from xml.etree import ElementTree as ET

 
def render(lang):
  global renderpath
  
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  bpy.context.scene.render.use_sequencer = 1
  renderpath = '//sequence/'+lang
  sndfile = renderpath+'/snd/snd.flac'
  if (not renderpath):
    os.mkdir(renderpath)
  if (not renderpath+'/snd'):
    os.mkdir(renderpath+'/snd')
  regexobj = re.search(r"^(.*\/)*(.*)(\.blend)$", bpy.data.filepath)
  bpy.context.scene.render.filepath = "%s/%s/" % (renderpath,regexobj.group(2))
  if (not os.path.isfile(bpy.context.scene.render.frame_path())):
    bpy.ops.render.render(animation=True)
    bpy.ops.sound.mixdown(filepath=sndfile)
  else:
    print('already rendered',bpy.context.scene.render.frame_path())

def transcode(lang):
  global renderpath
  #FIXME
  #theora gst-launch-1.0 oggmux name=mux ! filesink location="../video.webm"    file:///home/jimmac/src/git/gnome/gnome-getting-started-docs/animation/sequence/C/changing-wallpaper/snd/test.flac ! decodebin ! audioconvert ! vorbisenc ! mux.     multifilesrc location="/home/jimmac/src/git/gnome/gnome-getting-started-docs/animation/sequence/C/changing-wallpaper/%04d.png" index=1 caps="image/png,framerate=\(fraction\)25/1" ! pngdec ! videoconvert ! videorate ! theoraenc ! mux.
  #webm gst-launch-1.0 webmmux name=mux ! filesink location="../video.webm"    file:///home/jimmac/src/git/gnome/gnome-getting-started-docs/animation/sequence/C/changing-wallpaper/snd/test.flac ! decodebin ! audioconvert ! vorbisenc ! mux.     multifilesrc location="/home/jimmac/src/git/gnome/gnome-getting-started-docs/animation/sequence/C/changing-wallpaper/%04d.png" index=1 caps="image/png,framerate=\(fraction\)25/1" ! pngdec ! videoconvert ! videoscale ! videorate ! vp8enc threads=4 ! mux.
  regexobj = re.search(r"^(.*\/)*(.*)(\.blend)$", bpy.data.filepath)
  framepath = "%ssequence/%s/%s" % (regexobj.group(1),lang,regexobj.group(2))
  webmfile = "%s.webm" % (regexobj.group(2))
  sndfile = "%ssequence/%s/%s/snd/snd.flac" % (regexobj.group(1),lang,regexobj.group(2))
  transcodepath = "../getting-started/%s/figures/" % (lang)
  
  #print(transcodepath,webmfile,sndfile,framepath)
  transcodecmd = "gst-launch-1.0 webmmux name=mux ! filesink location=\"%s/%s\"    file://%s ! decodebin ! audioconvert ! vorbisenc ! mux.     multifilesrc location=\"%s/%%04d.png\" index=1 caps=\"image/png,framerate=\(fraction\)25/1\" ! pngdec ! videoconvert ! videoscale ! videorate ! vp8enc threads=4 ! mux." % (transcodepath,webmfile,sndfile,framepath)
  if (not os.path.isfile(transcodepath+webmfile)):
    os.system(transcodecmd)
  else:
    print('already transcoded',transcodepath + webmfile)  
  
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
    transcode(lang)
    
if __name__ == '__main__':
    main()
