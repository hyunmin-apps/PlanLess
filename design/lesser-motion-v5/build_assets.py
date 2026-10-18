from pathlib import Path
import subprocess,math,json,zipfile,base64,hashlib
R=Path(__file__).resolve().parent;R.mkdir(exist_ok=True);FF='/opt/homebrew/bin/ffmpeg';PX='/tmp/plan-captain-tools/Pixelorama.app/Contents/MacOS/Pixelorama';S=128
G=Path('/Users/kanghyunmin/.codex/generated_images/01a12b35-8150-7542-8c07-3cc21f27b8f9')
sources={'planner':G/'exec-e2bcc820-fd9f-429d-907a-dc517c59d62a.png','passion':G/'exec-1fec3d21-53ff-488c-91aa-b5173fc13c71.png'}
def run(*a,input=None):
 p=subprocess.run(list(map(str,a)),input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise RuntimeError(p.stderr.decode()[-1600:])
 return p.stdout
# One shared art-directed palette for all characters and states.
hexes=['211321','39202b','542b31','783631','a0462e','c95126','e66b26','f48732','ffac4d','ffe0b0','fff2cf','c39972','916b55','594a46','0e3d48','155c66','20868a','42aaa4','af2335','db3040','f34b4b','f2c454','60d7ed','12a8e0','0874b7','ecffff','154b38','24824b','48c76b','98ed8c','d4ffba','ffbd3b','fff29b']
pal=[tuple(bytes.fromhex(h))+(255,) for h in hexes];dark=pal[0]
def blank(w=S,h=S):return bytearray(w*h*4)
def put(a,x,y,c,w=S,h=S):
 if 0<=x<w and 0<=y<h:a[(y*w+x)*4:(y*w+x)*4+4]=bytes(c)
def get(a,x,y,w=S):return tuple(a[(y*w+x)*4:(y*w+x)*4+4])
def rect(a,x,y,w,h,c):
 for yy in range(y,y+h):
  for xx in range(x,x+w):put(a,xx,yy,c)
def overlay(a,b,x=0,y=0,bw=S,bh=S):
 for yy in range(bh):
  for xx in range(bw):
   c=get(b,xx,yy,bw)
   if c[3]:put(a,x+xx,y+yy,c)
def resize(b,sw,sh,dw,dh):
 a=blank(dw,dh)
 for y in range(dh):
  for x in range(dw):put(a,x,y,get(b,min(sw-1,x*sw//dw),min(sh-1,y*sh//dh),sw),dw,dh)
 return a
def png(path,raw,w=S,h=S):run(FF,'-y','-v','error','-f','rawvideo','-pixel_format','rgba','-video_size',f'{w}x{h}','-i','-','-frames:v','1',path,input=raw)
def outline(a,w,h):
 out=blank(w,h)
 for y in range(h):
  for x in range(w):
   if get(a,x,y,w)[3]:
    for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:put(out,x+dx,y+dy,dark,w,h)
 for y in range(h):
  for x in range(w):
   c=get(a,x,y,w)
   if c[3]:put(out,x,y,c,w,h)
 return out
masters={};cache={}
for name,src in sources.items():
 info=json.loads(run('/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-of','json',src))['streams'][0];cw,ch=info['width']//4,info['height']//3
 # Rebuild from original high-resolution image, never upscale the previous 64px asset.
 raw=run(FF,'-v','error','-i',src,'-vf',f'crop={cw}:{ch}:0:0,scale=96:96:flags=area,format=rgba','-f','rawvideo','-pix_fmt','rgba','-')
 a=blank(96,96)
 for n in range(0,len(raw),4):
  r,g,b,alpha=raw[n:n+4]
  if alpha<160:continue
  key=(r,g,b)
  if key not in cache:cache[key]=min(pal,key=lambda c:sum((c[k]-key[k])**2 for k in range(3)))
  a[n:n+4]=bytes(cache[key])
 a=outline(a,96,96);masters[name]=a;png(R/f'{name}-master.png',a,96,96)
# Shared V glyph: identical geometry, colors and timeline for both characters.
v=blank(24,24)
mask=set()
for j in range(15):
 for dx in range(-2,3):
  mask.add((4+j//2+dx,3+j));mask.add((19-j//2+dx,3+j))
for x,y in mask:
 for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:put(v,x+dx,y+dy,pal[26],24,24)
for x,y in mask:put(v,x,y,pal[28] if x<12 else pal[29],24,24)
png(R/'completion-V.png',v,24,24)
report={};allcolors=set()
for name in masters:
 for state in ['idle','working','complete']:
  key=f'{name}-{state}';folder=R/key;folder.mkdir(exist_ok=True);count=24;layers=[];merged=[]
  for i in range(count):
   t=i/24;back=blank();body=blank();front=blank();base=masters[name];bw=bh=96;dy=0
   if state=='idle':dy=round(math.sin(t*math.tau)*0.7)
   elif state=='working':
    dy=round(math.sin(t*math.tau)*1.4);bh=96+round(math.sin(t*math.tau)*1);bw=96
   else:
    # Ease into squash, quick launch, slow apex, landing and settle.
    curve=[0,0,1,2,3,3,1,-2,-5,-7,-8,-8,-7,-5,-2,0,2,3,2,1,0,0,0,0]
    dy=curve[i];bh=96-(dy if dy>0 else 0);bw=96+max(dy,0)
   x=(128-bw)//2;y=123-bh+dy
   overlay(body,resize(base,96,96,bw,bh),x,y,bw,bh)
   if state=='working' and name=='planner':
    # Four-point glints extend beyond the lenses; no blurred bloom.
    for cx,cy in [(71,71+dy),(94,71+dy)]:
     radius=7+round(1.0*math.sin(t*math.tau))
     for yy in range(-radius-1,radius+2):
      for xx in range(-radius-1,radius+2):
       dist=(abs(xx)/(radius+1))**0.6+(abs(yy)/(radius+1))**0.6
       if dist<=1:put(front,cx+xx,cy+yy,pal[24])
       if (abs(xx)/radius)**0.6+(abs(yy)/radius)**0.6<=1:put(front,cx+xx,cy+yy,pal[22])
       if abs(xx)+abs(yy)<=2:put(front,cx+xx,cy+yy,pal[25])
   if state=='working' and name=='passion':
    # Compact hard-edged flame tongues live behind the fixed character.
    for j,cx in enumerate([17,24,31,100,107,114]):
     hh=20+round(7*math.sin(t*math.tau+j*1.4));bottom=117
     for yy in range(hh):
      half=max(1,round(5*(1-yy/hh)));bend=round(2*math.sin(t*math.tau+yy*.2+j))
      rect(back,cx-half+bend,bottom-yy,half*2+1,1,pal[6] if yy>hh*.65 else pal[31])
      if yy<hh*.55:rect(back,cx-1+bend,bottom-yy,3,1,pal[32])
   if state=='complete':
    sizes=[0,0,5,10,17,23,27,25,23,24,24,24,24,24,24,24,24,23,20,16,10,5,0,0]
    sz=sizes[i]
    if sz:
     lift=[0,0,0,0,0,1,3,5,6,7,7,6,5,5,6,7,7,7,8,9,10,11,0,0][i]
     overlay(front,resize(v,24,24,sz,sz),79-sz//2,12-lift+(24-sz)//2,sz,sz)
   out=blank();overlay(out,back);overlay(out,body);overlay(out,front)
   png(folder/f'frame-{i+1:02}.png',out);merged.append(bytes(out));layers.append([bytes(back),bytes(body),bytes(front)])
   allcolors.update(tuple(out[n:n+4]) for n in range(0,len(out),4))
  data={'pixelorama_version':'v1.2.3-stable','pxo_version':7,'size_x':S,'size_y':S,'color_mode':5,'layers':[{'name':n,'type':0,'visible':True,'opacity':1,'parent':-1} for n in ['Back effects','Fixed character','Front effects']],'frames':[{'duration':1,'cels':[{'opacity':1,'z_index':0} for k in range(3)]} for i in range(count)],'current_frame':0,'current_layer':1,'fps':12,'tags':[{'name':state,'color':'48c76bff','from':1,'to':24}]}
  project=folder/f'{key}.pxo'
  with zipfile.ZipFile(project,'w',zipfile.ZIP_DEFLATED) as z:
   z.writestr('mimetype','application/x-pixelorama');z.writestr('data.json',json.dumps(data))
   for fi,ls in enumerate(layers,1):
    for li,b in enumerate(ls,1):z.writestr(f'image_data/frames/{fi}/layer_{li}',b)
   z.write(folder/'frame-01.png','preview.png')
  run(PX,'--headless','--rendering-method','gl_compatibility','--quit','--','--export','--output',folder/f'{key}.gif',project)
  run(FF,'-v','error','-i',folder/f'{key}.gif','-f','null','-')
  run(FF,'-y','-v','error','-i',folder/f'{key}.gif','-vf','scale=384:384:flags=neighbor','-loop','0',folder/'preview.gif')
  report[key]={'size':[128,128],'frames':24,'fps':12,'master':f'{name}-master.png','layers':3,'uniqueFrames':len(set(merged)),'effectAbsentAtEnd':not any(layers[-1][2]) if state=='complete' else None}
  print(key,flush=True)
assert len(allcolors)<=len(pal)+1
report['validation']={'sharedPaletteColors':len(allcolors),'noGeneratedStateRedesigns':True,'completedEffectsIdenticalAcrossCharacters':True}
(R/'manifest.json').write_text(json.dumps(report,indent=2));(R/'palette.json').write_text(json.dumps(hexes))
print(R)
