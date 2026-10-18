"""Original code-drawn pixel sprites. No generated images, fonts, or image inputs.
Run: python3 draw_lesser.py
Pillow is used for hard-edged integer-coordinate raster drawing only.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math,json,zipfile,subprocess,base64
ROOT=Path(__file__).resolve().parent
W=H=128
C={'ink':'#251c2c','edge':'#412534','shadow':'#78313a','rust':'#b34832','orange':'#ed722c','light':'#ffa13d','gold':'#ffc05a','cream':'#ffe4b4','ivory':'#fff4d6','creamshadow':'#d4a175','paw':'#3a293b','pawlight':'#5a3b49','teal':'#178b94','tealdark':'#105463','teallight':'#56c5bf','red':'#e73549','reddark':'#9c2542','redlight':'#ff6b5d','blue':'#087bd9','cyan':'#61e7ff','white':'#ecffff','green':'#50d17c','greenshadow':'#176d49','greenlight':'#bcffa6','wood':'#b8733a','woodlight':'#efbd71','paper':'#fff1cb','paperline':'#aa9476','pink':'#f47bb9'}
NEAREST=Image.Resampling.NEAREST
def canvas():return Image.new('RGBA',(W,H))
def poly(im,pts,fill,outline='ink',width=2):
 d=ImageDraw.Draw(im);p=[(round(x),round(y)) for x,y in pts];d.polygon(p,fill=C.get(fill,fill))
 if outline:d.line(p+[p[0]],fill=C.get(outline,outline),width=width,joint='curve')
def box(im,xy,fill,outline=None,width=1):ImageDraw.Draw(im).rectangle(tuple(round(a) for a in xy),fill=C.get(fill,fill),outline=C.get(outline,outline),width=width)
def line(im,pts,fill,width=1):ImageDraw.Draw(im).line([(round(x),round(y)) for x,y in pts],fill=C.get(fill,fill),width=width,joint='curve')
def ellipse(im,xy,fill,outline=None,width=1):ImageDraw.Draw(im).ellipse(tuple(round(a) for a in xy),fill=C.get(fill,fill),outline=C.get(outline,outline),width=width)
def placed(im,dx=0,dy=0):
 out=canvas();out.alpha_composite(im,(round(dx),round(dy)));return out
def rotate(im,angle,pivot):return im.rotate(angle,resample=NEAREST,center=pivot)
def paw(im,p,up=False):
 x,y=p;poly(im,[(x-5,y-3),(x-3,y-6),(x+3,y-6),(x+6,y-2),(x+5,y+4),(x-2,y+5),(x-5,y+2)],'paw')
 line(im,[(x-2,y-3),(x+2,y-3)],'pawlight',2)
 if up:line(im,[(x-2,y+1),(x+2,y+1)],'edge',1)
def arm(im,shoulder,elbow,end):
 line(im,[shoulder,elbow,end],'ink',10);line(im,[shoulder,elbow,end],'rust',6);line(im,[elbow,end],'paw',6);paw(im,end)
def tail(im,sway):
 # Stepped curled silhouette; stripe masks stay attached to tail geometry.
 t=canvas();pts=[(49,105),(37,110),(24,106),(15,98),(10,86),(10,73),(14,62),(22,55),(30,54),(36,59),(38,69),(34,78),(30,82),(33,88),(44,91),(52,98)]
 poly(t,pts,'orange',None);mask=t.getchannel('A');shade=canvas()
 poly(shade,[(8,75),(15,70),(35,81),(34,91),(15,91)],'shadow',None)
 poly(shade,[(14,57),(24,51),(38,57),(39,65),(30,69)],'shadow',None)
 poly(shade,[(21,96),(29,89),(45,96),(47,107),(36,114)],'shadow',None)
 poly(shade,[(12,70),(16,61),(25,57),(31,58),(27,62),(20,65),(17,73)],'light',None)
 clipped=Image.new('RGBA',(W,H));clipped.paste(shade,(0,0),mask);t.alpha_composite(clipped)
 ImageDraw.Draw(t).line(pts+[pts[0]],fill=C['ink'],width=3,joint='curve')
 im.alpha_composite(rotate(t,sway,(45,101)))
def body(im,dy=0,lean=0,crouch=0,legs='stand'):
 # Legs articulate independently; torso is never scaled.
 if legs=='jump':
  poly(im,[(53,102),(61,102),(61,110),(57,115),(49,114),(47,111)],'paw')
  poly(im,[(74,100),(83,100),(86,107),(82,112),(75,112),(71,108)],'paw')
 elif crouch:
  poly(im,[(48,108),(59,107),(63,113),(60,118),(47,118),(44,115)],'paw')
  poly(im,[(72,107),(84,108),(89,114),(87,118),(73,118),(69,114)],'paw')
 else:
  poly(im,[(51,100),(62,101),(62,114),(65,117),(63,120),(48,120),(47,117)],'paw')
  poly(im,[(73,101),(83,101),(84,114),(89,117),(87,120),(73,120),(71,117)],'paw')
 line(im,[(50,117),(59,117)],'pawlight',2);line(im,[(76,117),(84,117)],'pawlight',2)
 poly(im,[(52,72),(73,70),(84,79),(88,98),(84,107),(76,112),(57,112),(47,105),(45,91)],'orange')
 poly(im,[(50,80),(57,78),(55,98),(59,110),(51,108),(46,102),(46,90)],'rust',None)
 poly(im,[(76,77),(82,81),(85,96),(80,104),(76,107),(78,93)],'light',None)
 poly(im,[(61,83),(71,82),(77,88),(77,97),(72,103),(64,102),(59,96),(59,88)],'cream',None)
 poly(im,[(60,96),(65,100),(72,100),(75,96),(73,103),(64,104)],'creamshadow',None)
def head(im,kind,expression='normal',tilt=0,blink=False):
 h=canvas()
 # Ears, cranium and cheek planes share one drawing across both costumes.
 poly(h,[(42,43),(37,29),(39,20),(44,20),(54,30)],'rust',width=3)
 poly(h,[(77,30),(87,19),(92,20),(95,31),(90,45)],'rust',width=3)
 poly(h,[(42,34),(41,25),(44,25),(50,32),(46,38)],'cream',None)
 poly(h,[(83,31),(89,24),(91,28),(90,36),(86,39)],'cream',None)
 poly(h,[(43,35),(52,29),(64,28),(74,30),(84,34),(92,42),(96,54),(93,65),(85,72),(72,76),(57,75),(45,69),(38,59),(38,47)],'orange',width=3)
 poly(h,[(41,43),(46,36),(55,32),(65,31),(61,35),(51,38),(46,45)],'light',None)
 poly(h,[(87,39),(92,47),(94,56),(90,65),(82,71),(72,74),(55,73),(45,67),(42,61),(50,65),(62,68),(77,67),(87,59)],'rust',None)
 # Cream side masks stay angular, unmistakably a red panda.
 poly(h,[(43,53),(49,51),(55,55),(58,61),(54,66),(48,66),(42,61)],'cream',None)
 poly(h,[(87,52),(92,55),(92,62),(87,66),(81,65),(81,59)],'cream',None)
 poly(h,[(60,59),(65,55),(72,56),(78,61),(83,64),(80,69),(73,72),(63,71),(56,67)],'cream',None)
 poly(h,[(62,68),(72,69),(80,66),(78,70),(72,73),(64,72)],'creamshadow',None)
 box(h,(51,43,56,45),'cream');box(h,(78,43,82,45),'cream')
 ey=54
 if kind=='planner':
  # Separate lenses plus bridge, kept identical in every pose.
  poly(h,[(48,49),(62,49),(63,59),(60,62),(50,61),(48,57)],'rust','ink',2)
  poly(h,[(73,49),(87,49),(87,58),(84,61),(75,61),(73,57)],'rust','ink',2)
  line(h,[(63,52),(72,52)],'ink',2)
 if expression=='happy' or blink:
  line(h,[(51,55),(54,52),(58,55)],'ink',2);line(h,[(76,55),(79,52),(83,55)],'ink',2)
 else:
  box(h,(53,51,57,58),'ink');box(h,(78,51,82,58),'ink')
  box(h,(54,51,55,53),'ivory');box(h,(79,51,80,53),'ivory')
 poly(h,[(65,60),(72,60),(71,63),(68,64),(65,62)],'ink',None)
 if expression=='happy':
  poly(h,[(64,66),(72,67),(77,65),(74,71),(69,72),(65,70)],'ink',None);box(h,(68,70,73,71),'redlight')
 else:line(h,[(68,64),(68,67),(72,68),(75,66)],'ink',1)
 if kind=='passion':
  poly(h,[(39,40),(51,36),(69,36),(87,39),(91,43),(86,46),(70,42),(53,42),(40,46)],'red','reddark',2)
  line(h,[(43,41),(56,38),(72,39),(85,42)],'redlight',2)
  poly(h,[(40,42),(31,36),(25,36),(27,42),(35,47),(29,52),(23,51),(28,46),(33,43)],'red','ink',2)
  poly(h,[(40,43),(34,47),(35,55),(29,59),(34,60),(41,52),(43,47)],'reddark','ink',1)
 im.alpha_composite(rotate(h,tilt,(66,72)))
def scarf(im):
 poly(im,[(47,71),(60,76),(77,76),(87,70),(87,77),(76,83),(58,82),(48,77)],'teal','tealdark',2)
 poly(im,[(60,79),(68,81),(67,96),(61,96),(58,92)],'teal','tealdark',2)
 line(im,[(51,75),(62,79),(76,79),(82,76)],'teallight',2)
def clipboard(im,x,y,angle=0,checked=0):
 a=canvas();poly(a,[(x-9,y-13),(x+10,y-13),(x+10,y+14),(x-9,y+14)],'wood','ink',2)
 box(a,(x-6,y-10,x+7,y+10),'paper');box(a,(x-3,y-15,x+4,y-10),'paperline','ink')
 for yy in [y-5,y,y+5]:
  box(a,(x-4,yy-1,x-2,yy+1),'paperline');line(a,[(x,yy),(x+5,yy)],'paperline',1)
 for j in range(checked):
  yy=y-5+j*5;line(a,[(x-5,yy),(x-3,yy+2),(x,yy-2)],'greenshadow',1)
 im.alpha_composite(rotate(a,angle,(x,y)))
def pencil(im,p,angle=-35):
 x,y=p;end=(x+round(12*math.cos(math.radians(angle))),y+round(12*math.sin(math.radians(angle))))
 line(im,[(x,y),end],'ink',4);line(im,[(x,y),end],'gold',2)
 box(im,(x-1,y-1,x+1,y+1),'redlight')
def bat(im,base,tip):
 bx,by=base;tx,ty=tip;angle=math.atan2(ty-by,tx-bx);nx=-math.sin(angle);ny=math.cos(angle)
 pts=[(bx+nx*2,by+ny*2),(tx+nx*4,ty+ny*4),(tx+math.cos(angle)*3,ty+math.sin(angle)*3),(tx-nx*4,ty-ny*4),(bx-nx*2,by-ny*2)]
 poly(im,pts,'wood','ink',2);line(im,[(bx+nx,by+ny),(tx+nx*2,ty+ny*2)],'woodlight',2)
 for off in [3,6,9]:
  cx=bx+math.cos(angle)*off;cy=by+math.sin(angle)*off;line(im,[(cx-nx*2,cy-ny*2),(cx+nx*2,cy+ny*2)],'rust',1)
def star(im,cx,cy,r):
 poly(im,[(cx,cy-r),(cx+2,cy-2),(cx+r,cy),(cx+2,cy+2),(cx,cy+r),(cx-2,cy+2),(cx-r,cy),(cx-2,cy-2)],'cyan','blue',1)
 poly(im,[(cx,cy-3),(cx+1,cy-1),(cx+3,cy),(cx+1,cy+1),(cx,cy+3),(cx-1,cy+1),(cx-3,cy),(cx-1,cy-1)],'white',None)
def fire(im,i):
 for j,x in enumerate([16,29,101,113]):
  height=[22,29,25,33,26,20][(i+j)%6];bottom=114
  poly(im,[(x-7,bottom),(x-6,bottom-10),(x-2,bottom-16),(x-2,bottom-height),(x+2,bottom-height+6),(x+2,bottom-13),(x+6,bottom-19),(x+8,bottom-7),(x+5,bottom)],'orange',None)
  poly(im,[(x-4,bottom-1),(x-3,bottom-9),(x+1,bottom-15),(x+1,bottom-8),(x+4,bottom-4),(x+3,bottom-1)],'gold',None)
  box(im,(x-1,bottom-5,x+1,bottom-1),'ivory')
  if (i+j)%2==0:box(im,(x+3,bottom-height-6,x+4,bottom-height-4),'light')
def fireworks(im,i):
 if i not in [2,3,4]:return
 radius={2:6,3:14,4:20}[i]
 for j,(cx,cy,col) in enumerate([(25,31,'cyan'),(99,26,'pink'),(62,12,'gold')]):
  for ray in range(8):
   a=ray*math.tau/8+j*.2;rr=radius+(j%2)*2
   p1=(cx+math.cos(a)*max(1,rr-5),cy+math.sin(a)*max(1,rr-5));p2=(cx+math.cos(a)*rr,cy+math.sin(a)*rr)
   line(im,[p1,p2],col,2 if i<4 else 1)
  if i==2:star(im,cx,cy,3)
def v_effect(im,i):
 sizes=[0,9,24,21,12,0];s=sizes[i]
 if not s:return
 icon=Image.new('RGBA',(28,24));d=ImageDraw.Draw(icon)
 d.line([(3,4),(12,20),(25,3)],fill=C['greenshadow'],width=7,joint='curve')
 d.line([(3,3),(12,18),(25,2)],fill=C['green'],width=4,joint='curve')
 d.line([(4,3),(12,15)],fill=C['greenlight'],width=1)
 icon=icon.resize((s,max(1,round(s*24/28))),NEAREST)
 im.alpha_composite(icon,(69-s//2,[0,15,2,4,0,0][i]))
# Poses explicitly specify hand targets and head rotation, not image-wide wobble.
POSES={
'planner-working':[
 {'L':(47,91),'R':(89,91),'clip':(90,93),'pencil':-80,'tilt':0},
 {'L':(57,81),'R':(86,84),'clip':(83,85),'pencil':-15,'tilt':4},
 {'L':(68,84),'R':(88,84),'clip':(83,85),'pencil':-32,'tilt':7},
 {'L':(72,88),'R':(88,85),'clip':(83,85),'pencil':-48,'tilt':5},
 {'L':(47,68),'R':(88,84),'clip':(85,85),'pencil':-68,'tilt':-5},
 {'L':(46,89),'R':(89,91),'clip':(90,93),'pencil':-80,'tilt':0}],
'passion-working':[
 {'L':(46,90),'R':(89,87),'bat':((90,89),(96,115))},
 {'L':(47,91),'R':(90,72),'bat':((91,73),(67,57)),'tilt':3,'crouch':2},
 {'L':(43,75),'R':(89,72),'bat':((90,73),(65,56)),'tilt':-3},
 {'L':(38,48),'R':(90,72),'bat':((91,73),(66,56)),'happy':True,'tilt':-4},
 {'L':(41,65),'R':(90,72),'bat':((91,73),(66,56)),'happy':True,'tilt':2},
 {'L':(46,90),'R':(89,87),'bat':((90,89),(96,115))}],
}
def render(kind,state,i):
 tail_layer=canvas();torso=canvas();face=canvas();limbs=canvas();backfx=canvas();frontfx=canvas()
 p={};dy=0;sway=[0,-3,-6,0,5,2][i]
 if state=='working':p=POSES[kind+'-'+state][i]
 if state=='complete':
  dy=[0,5,-5,-9,3,0][i]
  p={'L':[(47,91),(49,94),(38,64),(35,48),(43,70),(47,91)][i], 'R':[(90,90),(89,94),(95,65),(97,55),(91,77),(90,90)][i], 'tilt':[0,4,-3,-6,3,0][i],'happy':i in [2,3,4], 'crouch':i in [1,4]}
 if state=='idle':p={'L':(47,91),'R':(89,91),'tilt':[0,0,1,1,0,0][i],'blink':i==3}
 tail(tail_layer,sway);body(torso,crouch=p.get('crouch',0),legs='jump' if state=='complete' and i in [2,3] else 'stand')
 head(face,kind,'happy' if p.get('happy') else 'normal',p.get('tilt',0),p.get('blink',False))
 if kind=='planner':scarf(face)
 L=p.get('L',(47,91));R=p.get('R',(89,91))
 arm(limbs,(51,79),(L[0]+3,(79+L[1])//2),L)
 arm(limbs,(83,79),(R[0]-2,(79+R[1])//2),R)
 if kind=='planner':
  clip=p.get('clip',(R[0]+1,R[1]+2));clipboard(limbs,*clip,angle=0 if state!='complete' else [0,5,-8,-12,5,0][i],checked=(2 if state=='complete' else (min(2,max(0,i-1)) if state=='working' else 0)));paw(limbs,R)
  pencil(limbs,L,p.get('pencil',-70));paw(limbs,L)
  if state=='working':
   glow=canvas();star(glow,55,54,[6,6,7,8,7,6][i]);star(glow,80,54,[6,6,7,8,7,6][i]);frontfx.alpha_composite(rotate(glow,p.get('tilt',0),(66,72)))
  if state=='complete':v_effect(frontfx,i)
 else:
  bt=p.get('bat',(R,(R[0]+4,R[1]+25)))
  if state=='complete':bt=(R,(R[0]+3,R[1]+25))
  if state=='working' and i in [1,2,3,4]:
   bat(tail_layer,R,(27,61));paw(limbs,R)
  else:bat(limbs,*bt);paw(limbs,R)
  if state=='working':fire(backfx,i)
  if state=='complete':fireworks(frontfx,i)
 # Behind-body effects, tail, limbs/body silhouette, head, front hand/props, foreground effects.
 layers=[backfx,placed(tail_layer,0,dy),placed(torso,0,dy),placed(face,0,dy),placed(limbs,0,dy),frontfx if state=='complete' else placed(frontfx,0,dy)]
 out=canvas()
 for a in layers:out.alpha_composite(a)
 return out,layers

def export():
 manifest={};timings={'idle':[420,300,300,120,300,460],'working':[300,180,230,320,260,350],'complete':[260,200,150,400,220,500]}
 for kind in ['planner','passion']:
  for state in ['idle','working','complete']:
   key=kind+'-'+state;folder=ROOT/key;folder.mkdir(exist_ok=True);frames=[];layer_frames=[]
   for i in range(6):
    im,ls=render(kind,state,i);im.save(folder/f'frame-{i+1:02}.png');frames.append(im);layer_frames.append(ls)
   frames[0].save(folder/'animation.gif',save_all=True,append_images=frames[1:],duration=timings[state],loop=0,disposal=2)
   big=[x.resize((384,384),NEAREST) for x in frames];big[0].save(folder/'preview.gif',save_all=True,append_images=big[1:],duration=timings[state],loop=0,disposal=2)
   sheet=Image.new('RGBA',(W*6,H))
   for i,im in enumerate(frames):sheet.alpha_composite(im,(i*W,0))
   sheet.save(folder/'sheet.png')
   names=['Back FX','Tail','Body and legs','Head and costume','Arms and props','Front FX']
   data={'pixelorama_version':'v1.2.3-stable','pxo_version':7,'size_x':128,'size_y':128,'color_mode':5,'layers':[{'name':n,'type':0,'visible':True,'opacity':1,'parent':-1} for n in names],'frames':[{'duration':ms//10,'cels':[{'opacity':1,'z_index':0} for n in names]} for ms in timings[state]],'current_frame':0,'current_layer':3,'fps':100,'tags':[{'name':state,'color':'50d17cff','from':1,'to':6}]}
   with zipfile.ZipFile(folder/(key+'.pxo'),'w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('mimetype','application/x-pixelorama');z.writestr('data.json',json.dumps(data))
    for fi,ls in enumerate(layer_frames,1):
     for li,im in enumerate(ls,1):z.writestr(f'image_data/frames/{fi}/layer_{li}',im.tobytes())
    z.write(folder/'frame-01.png','preview.png')
   manifest[key]={'frames':6,'size':[128,128],'durationsMs':timings[state],'layers':names,'source':'draw_lesser.py','generatedImageInputs':False}
   print(key,flush=True)
 (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2));(ROOT/'palette.json').write_text(json.dumps(C,indent=2))
 contact=Image.new('RGBA',(128*6,128*6),(20,23,29,255))
 for y,key in enumerate(manifest):
  for i in range(6):contact.alpha_composite(Image.open(ROOT/key/f'frame-{i+1:02}.png'),(i*128,y*128))
 contact.save(ROOT/'all-frames.png')
if __name__=='__main__':export()
