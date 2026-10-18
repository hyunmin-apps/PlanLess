#!/usr/bin/env python3
"""Copy approved motion without changes; package complete idle direction poses."""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json, shutil
from collections import deque

def clean_cell(im):
    """Discard isolated atlas gutter flecks, retaining the connected full pose."""
    a=np.array(im);mask=a[:,:,3]>=220;seen=np.zeros(mask.shape,dtype=bool);largest=[]
    for y,x in zip(*np.where(mask)):
        if seen[y,x]:continue
        queue=deque([(y,x)]);seen[y,x]=True;component=[]
        while queue:
            yy,xx=queue.popleft();component.append((yy,xx))
            for dy,dx in [(a,b) for a in [-1,0,1] for b in [-1,0,1] if a or b]:
                ny,nx=yy+dy,xx+dx
                if 0<=ny<mask.shape[0] and 0<=nx<mask.shape[1] and mask[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx]=True;queue.append((ny,nx))
        if len(component)>len(largest):largest=component
    keep=np.zeros(mask.shape,dtype=bool)
    for y,x in largest:keep[y,x]=True
    a[:,:,3]=np.where(keep,255,0);a[~keep]=0
    return Image.fromarray(a)

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'design/lesser-motion-v8'
IDLE=ROOT/'design/lesser-idle-tracking-v2'
OUT=ROOT/'Resources/Mascots'
palette=np.array([list(bytes.fromhex(s)) for s in json.loads((SRC/'palette.json').read_text())],dtype=np.int32)
manifest={'size':80,'characters':{}}
for c in ['planner','passion']:
    clips={}
    for mode in ['working','complete']:
        name=c+'-'+mode;folder=OUT/c/mode;folder.mkdir(parents=True,exist_ok=True)
        for i in range(1,7):shutil.copy2(SRC/name/f'frame-{i:02}.png',folder/f'frame-{i:02}.png')
        clips[mode]=json.loads((SRC/'manifest.json').read_text())[name]['durationMs']
    # Each gaze is an authored, complete character pose. Do not isolate,
    # rotate or paste the head: neck/scarf/shoulders must stay connected.
    atlas=Image.open(IDLE/(c+'-source-atlas.png')).convert('RGBA');w,h=atlas.width/3,atlas.height/4
    frames=[]
    # Planner upper diagonal cells are semantically reversed in the raw sheet.
    order=[2,1,0,3,4,5,6,7,8,9,10,11] if c=='planner' else list(range(12))
    cells=[]
    for i in order:
        im=atlas.crop((round(i%3*w),round(i//3*h),round((i%3+1)*w),round((i//3+1)*h)))
        im.putalpha(im.getchannel('A').point(lambda a:255 if a>=220 else 0))
        cells.append(clean_cell(im))
    # A rectangular atlas cell is not a square sprite. One common scale keeps
    # the original anatomy and the same size in every direction.
    if c=='passion':
        # The draft's three left cells looked right. Use the verified modest
        # left full-body pose for that sector rather than an extreme neck tilt.
        left=Image.open(IDLE/'passion-left-source.png').convert('RGBA')
        left=left.crop((left.width//3,0,left.width*2//3,left.height))
        left.putalpha(left.getchannel('A').point(lambda a:255 if a>=220 else 0))
        left=clean_cell(left);left=left.crop(left.getbbox())
        target_height=cells[4].getbbox()[3]-cells[4].getbbox()[1]
        left=left.resize((round(left.width*target_height/left.height),target_height),Image.Resampling.NEAREST)
        for index in [0,3,6]:cells[index]=left.copy()
    boxes=[im.getbbox() for im in cells]
    span=max(max(bb[2]-bb[0],bb[3]-bb[1]) for bb in boxes)
    scale=66/span
    for im,bb in zip(cells,boxes):
        im=im.crop(bb)
        im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.BOX)
        im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0))
        a=np.array(im);rgb=a[:,:,:3].astype(np.int32);ix=np.argmin(((rgb[:,:,None,:]-palette[None,None,:,:])**2).sum(axis=3),axis=2);a[:,:,:3]=palette[ix];a[a[:,:,3]==0]=0;im=Image.fromarray(a)
        bb=im.getbbox()
        feet=im.crop((0,max(0,bb[3]-7),im.width,bb[3])).getbbox()
        anchor=(feet[0]+feet[2])/2
        canvas=Image.new('RGBA',(80,80));canvas.paste(im,(round(42-anchor),74-bb[3]));frames.append(canvas)
    # The generated closed-eye planner cell lost the glasses. Hold the
    # verified half-blink complete pose instead of making eyewear disappear.
    if c=='planner':frames[10]=frames[9].copy()
    folder=OUT/c/'idle';folder.mkdir(parents=True,exist_ok=True)
    for i,im in enumerate(frames,1):im.save(folder/f'frame-{i:02}.png')
    clips['idle']=[140]*9+[70,90,70]
    manifest['characters'][c]=clips
    sheet=Image.new('RGBA',(80*3,80*4))
    for i,im in enumerate(frames):sheet.paste(im,(i%3*80,i//3*80))
    sheet.resize((720,960),Image.Resampling.NEAREST).save(IDLE/(c+'-directions.png'))
(OUT/'animations.json').write_text(json.dumps(manifest,indent=2))
(OUT/'timings.js').write_text('window.MASCOT_TIMINGS='+json.dumps(manifest['characters'])+';')
print('Packaged approved motion and 12 complete idle direction poses per character')
