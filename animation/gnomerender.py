import bpy,os,re

def render(lang):
  global renderpath,renderpathabs,sndfile
  
  #bpy.context.scene.render.resolution_percentage =
  #bpy.context.scene.render.use_compositing = 0
  bpy.context.scene.render.use_sequencer = 1
  renderpath = '//sequence/'+lang
  
  regexobj = re.search(r"^(.*\/)*(.*)(\.blend)$", bpy.data.filepath)
  bpy.context.scene.render.filepath = "%s/%s/" % (renderpath,regexobj.group(2))
  renderpathabs = "%ssequence/%s/%s" % (regexobj.group(1),lang,regexobj.group(2))
  sndpath = "%s/snd" % (renderpathabs)
  sndfile = "%s/snd.flac" % (sndpath)
  if (not os.path.isdir(renderpathabs)):
    bpy.ops.render.render(animation=True)
  if (not os.path.isdir(sndpath)):
    os.mkdir(sndpath)
    bpy.ops.sound.mixdown(filepath=sndfile)
  else:
    print('already rendered',bpy.context.scene.render.frame_path())

def transcode(lang,x=854,bitrate="300k"):
  global renderpath,renderpathabs,sndfile

  regexobj = re.search(r"^(.*\/)*(.*)(\.blend)$", bpy.data.filepath)
  framepath = renderpathabs
  webmfile = "%s.webm" % (regexobj.group(2))
  transcodepath = "../gnome-help/%s/figures/" % (lang)
  y = round(x/(1280/720))
  
  #print(transcodepath,webmfile,sndfile,framepath)
  transcodecmd = "ffmpeg -r 24 -f image2 -i %s/%%04d.png -i %s -vf scale=%s:%s -b %s %s/%s" % (framepath,sndfile,x,y,bitrate,transcodepath,webmfile)
  #transcodecmd = "gst-launch-1.0 webmmux name=mux ! filesink location=\"%s/%s\"    file://%s ! decodebin ! audioconvert ! vorbisenc bitrate=96000 ! mux.     multifilesrc location=\"%s/%%04d.png\" index=1 caps=\"image/png,framerate=\(fraction\)24/1\" ! pngdec ! videoconvert ! videoscale ! video/x-raw, width=%s,height=%s ! videorate ! vp8enc threads=12 target-bitrate=300000 ! mux." % (transcodepath,webmfile,sndfile,framepath,x,y)
  if (not os.path.isfile(transcodepath+webmfile)):
    os.system(transcodecmd)
  else:
    print('already transcoded',transcodepath + webmfile)

# vim: tabstop=2 expandtab
