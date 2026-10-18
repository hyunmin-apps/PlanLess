from pathlib import Path
import subprocess,json,zipfile,math,shutil,sys
R=Path(__file__).resolve().parent;OLD=R.parent/'lesser-motion-v5';FF='/opt/homebrew/bin/ffmpeg';PX='/tmp/plan-captain-tools/Pixelorama.app/Contents/MacOS/Pixelorama';S=128
pal=[tuple(bytes.fromhex(h))+(255,) for h in json.loads((OLD/'palette.json').read_text())];cache={}
def run(*a,input=None):
 p=subprocess.run(list(map(str,a)),input=input,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise RuntimeError(p.stderr.decode()[-1800:])
 return p.stdout
def resize(b,sw,sh,dw,dh):
 out=bytearray(dw*dh*4)
 for y in range(dh):
  for x in range(dw):
   q=((y*sh//dh)*sw+x*sw//dw)*4;n=(y*dw+x)*4;out[n:n+4]=b[q:q+4]
 return out
def overlay(a,b,x,y,w,h):
 for yy in range(h):
  for xx in range(w):
   q=(yy*w+xx)*4
   if b[q+3] and 0<=x+xx<S and 0<=y+yy<S:
    n=((y+yy)*S+x+xx)*4;a[n:n+4]=b[q:q+4]
def png(p,b):run(FF,'-y','-v','error','-f','rawvideo','-pixel_format','rgba','-video_size','128x128','-i','-','-frames:v','1',p,input=b)
v=run(FF,'-v','error','-i',OLD/'completion-V.png','-f','rawvideo','-pix_fmt','rgba','-')
report={}
for c in ['planner','passion']:
 key=c+'-idle';shutil.copytree(OLD/key,R/key,dirs_exist_ok=True);report[key]={'size':[128,128],'frames':24,'fps':12,'unchangedFromV5':True}
for job in json.loads(Path(sys.argv[1]).read_text()):
 name=job['name'];src=Path(job['path']);folder=R/name;folder.mkdir(exist_ok=True);shutil.copy2(src,folder/'source-atlas.png')
 meta=json.loads(run('/opt/homebrew/bin/ffprobe','-v','error','-show_streams','-of','json',src))['streams'][0];w,h=meta['width']//6,meta['height']//4
 layers=[];merged=[]
 for i in range(24):
  raw=run(FF,'-v','error','-i',src,'-vf',f'crop={w}:{h}:{i%6*w}:{i//6*h},scale=104:104:force_original_aspect_ratio=decrease:flags=area,format=rgba,pad=128:128:(ow-iw)/2:oh-ih-2:color=0x00000000','-f','rawvideo','-pix_fmt','rgba','-')
  body=bytearray(S*S*4);fx=bytearray(S*S*4)
  for n in range(0,len(raw),4):
   r,g,b,a=raw[n:n+4]
   if a<150:continue
   k=(r,g,b)
   if k not in cache:cache[k]=min(pal,key=lambda c:sum((c[j]-k[j])**2 for j in range(3)))
   body[n:n+4]=bytes(cache[k])
  # Remove isolated dark fragments from atlas gutters, preserving character and colored flames.
  seen=set()
  for seed in range(S*S):
   if seed in seen or not body[seed*4+3]:continue
   stack=[seed];seen.add(seed);component=[];bright=False
   while stack:
    pos=stack.pop();component.append(pos);rgb=body[pos*4:pos*4+3]
    if max(rgb)>140:bright=True
    xx=pos%S;yy=pos//S
    for nx,ny in [(xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)]:
     np=ny*S+nx
     if 0<=nx<S and 0<=ny<S and np not in seen and body[np*4+3]:seen.add(np);stack.append(np)
   if not bright and len(component)<100:
    for pos in component:body[pos*4:pos*4+4]=bytes(4)
  if name=='planner-complete':
   sizes=[0,0,0,0,0,0,5,10,17,23,27,25,23,24,24,24,24,23,20,16,10,5,0,0];sz=sizes[i]
   if sz:
    lift=[0,0,0,0,0,0,1,2,3,4,5,6,7,7,6,5,5,6,7,8,9,10,0,0][i]
    overlay(fx,resize(v,24,24,sz,sz),78-sz//2,12-lift+(24-sz)//2,sz,sz)
  if name=='passion-complete':
   # Fire aura is absent from completion source. Fireworks are separate particles.
   for burst,(cx,cy,start) in enumerate([(29,30,7),(99,24,9),(63,13,11)]):
    age=i-start
    if not 0<=age<10:continue
    radius=3+age*2.0
    colors=[(96,215,237,255),(242,196,84,255),(230,76,166,255)]
    for ray in range(8):
     theta=ray*math.tau/8+burst*.3
     xx=round(cx+radius*math.cos(theta));yy=round(cy+radius*math.sin(theta)+max(0,age-5)*.7)
     size=2 if age<7 else 1
     for dy in range(size):
      for dx in range(size):
       if 0<=xx+dx<S and 0<=yy+dy<S:
        q=((yy+dy)*S+xx+dx)*4;fx[q:q+4]=bytes(colors[burst])
     for tail in range(1,5 if age<7 else 2):
      tx=round(cx+(radius-tail)*math.cos(theta));ty=round(cy+(radius-tail)*math.sin(theta)+max(0,age-5)*.7)
      if 0<=tx<S and 0<=ty<S:q=(ty*S+tx)*4;fx[q:q+4]=bytes(colors[burst])
  out=bytearray(body);overlay(out,fx,0,0,S,S);png(folder/f'frame-{i+1:02}.png',out);layers.append([bytes(body),bytes(fx)]);merged.append(bytes(out))
 data={'pixelorama_version':'v1.2.3-stable','pxo_version':7,'size_x':S,'size_y':S,'color_mode':5,'layers':[{'name':n,'type':0,'visible':True,'opacity':1,'parent':-1} for n in ['Pose animation','Completion effect']],'frames':[{'duration':1,'cels':[{'opacity':1,'z_index':0} for j in range(2)]} for i in range(24)],'current_frame':0,'current_layer':0,'fps':12,'tags':[{'name':name,'color':'48c76bff','from':1,'to':24}]}
 p=folder/f'{name}.pxo'
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('mimetype','application/x-pixelorama');z.writestr('data.json',json.dumps(data))
  for fi,ls in enumerate(layers,1):
   for li,b in enumerate(ls,1):z.writestr(f'image_data/frames/{fi}/layer_{li}',b)
  z.write(folder/'frame-01.png','preview.png')
 run(PX,'--headless','--rendering-method','gl_compatibility','--quit','--','--export','--output',folder/f'{name}.gif',p)
 run(FF,'-v','error','-i',folder/f'{name}.gif','-f','null','-')
 run(FF,'-y','-v','error','-i',folder/f'{name}.gif','-vf','scale=384:384:flags=neighbor','-loop','0',folder/'preview.gif')
 report[name]={'size':[128,128],'frames':24,'fps':12,'uniquePoses':len(set(x[0] for x in layers)),'VAbsentAtEnd':not any(layers[-1][1]),'source':src.name}
 print(name,report[name],flush=True)
(R/'manifest.json').write_text(json.dumps(report,indent=2));shutil.copy2(OLD/'palette.json',R/'palette.json')
