"""Package image-edited v6 key poses as low-resolution PNG/GIF/Pixelorama assets.
Run with Python 3 + Pillow + NumPy. No network, no external temporary input.
"""
from pathlib import Path
import json, zipfile, shutil, hashlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / 'lesser-motion-v6'
SIZE = 80
JOBS = {
    'planner-working': {'durations': [280, 160, 300, 240, 280, 240], 'beats': ['준비', '연필 들기', '쓰기·체크', '만족한 윙크', '연필 들며 강조', '복귀']},
    'planner-complete': {'durations': [180, 160, 120, 280, 160, 600], 'beats': ['마지막 쓰기', '도약 준비', '도약', '기쁜 공중 자세', '착지', '안정']},
    'passion-working': {'durations': [260, 160, 140, 300, 200, 260], 'beats': ['준비', '주먹 당기기', '주먹 올리기', '응원 강조', '끄덕이며 내리기', '복귀']},
    'passion-complete': {'durations': [180, 160, 120, 280, 160, 600], 'beats': ['기쁜 준비', '웅크리기', '도약', '폭죽·공중 자세', '착지', '안정']},
}
SELECTED = json.loads((ROOT / 'selection.json').read_text())

def pixels(name, i, size):
    atlas = Image.open(ROOT / name / 'source-atlas.png').convert('RGBA')
    w, h = atlas.width // 3, atlas.height // 2
    tile = atlas.crop((i % 3 * w, i // 3 * h, (i % 3 + 1) * w, (i // 3 + 1) * h))
    # Remove low-opacity generation halos before area sampling. Character artwork
    # remains the edited raster; no body geometry or replacement poses are drawn.
    tile.putalpha(tile.getchannel('A').point(lambda a: 255 if a >= 240 else 0))
    inner = round(size * .9)
    tile = tile.resize((inner, inner), Image.Resampling.BOX)
    tile.putalpha(tile.getchannel('A').point(lambda a: 255 if a >= 128 else 0))
    out = Image.new('RGBA', (size, size))
    out.paste(tile, ((size-inner)//2, (size-inner)//2))
    return out

def separate(name, im):
    a = np.array(im)
    r, g, b, alpha = [a[:,:,j].astype(int) for j in range(4)]
    effect = np.zeros(alpha.shape, dtype=bool)
    if name == 'planner-complete':
        effect = (g > r * 1.35) & (g > b * 1.15) & (alpha > 0)
    elif name == 'passion-complete':
        # Separate floating firework clusters by connectivity, so warm fur and
        # the wooden bat never get mistaken for gold firework rays.
        unseen=set(zip(*np.nonzero(alpha>0)));components=[]
        while unseen:
            start=unseen.pop();component={start};queue=[start]
            while queue:
                y,x=queue.pop()
                for yy in range(y-1,y+2):
                    for xx in range(x-1,x+2):
                        if (yy,xx) in unseen:unseen.remove((yy,xx));component.add((yy,xx));queue.append((yy,xx))
            components.append(component)
        largest=max(components,key=len)
        for component in components:
            if component is not largest:
                for y,x in component:effect[y,x]=True
    fx = a.copy(); fx[~effect] = 0
    body = a.copy(); body[effect] = 0
    return Image.fromarray(body), Image.fromarray(fx)

raw = {name: [pixels(name, i, SIZE) for i in range(6)] for name in JOBS}
palette_hex = ['211321','39202b','542b31','783631','a0462e','c95126','e66b26','f48732','ffac4d','ffe0b0','fff2cf','c8b887','a28e68','0e3d48','155c66','20868a','42aaa4','9c1736','db3040','f34b4b','b56828','ffbd3b','fff29b','0874b7','12a8e0','60d7ed','ecffff','24824b','48c76b','98ed8c','e64ca6','e77999']
palette = [list(bytes.fromhex(h)) for h in palette_hex]
pal = np.array(palette, dtype=np.int32)
(ROOT/'palette.json').write_text(json.dumps([''.join(f'{v:02x}' for v in c) for c in palette],indent=2))

def remap(im):
    a = np.array(im)
    rgb = a[:,:,:3].astype(np.int32)
    indices = np.argmin(((rgb[:,:,None,:] - pal[None,None,:,:])**2).sum(axis=3),axis=2)
    a[:,:,:3] = pal[indices]
    a[a[:,:,3] == 0] = 0
    return Image.fromarray(a)

def shift(im, dx, dy):
    o=Image.new('RGBA', im.size);o.paste(im,(dx,dy));return o

def save_gif(path, frames, times, scale=1):
    pp = [0,0,0] + sum(palette,[])
    pp += [0] * (768-len(pp))
    fs=[]
    for im in frames:
        a=np.array(im);rgb=a[:,:,:3].astype(np.int32)
        ix=np.argmin(((rgb[:,:,None,:]-pal[None,None,:,:])**2).sum(axis=3),axis=2).astype('uint8')+1
        ix[a[:,:,3]==0]=0
        p=Image.frombytes('P',(im.width,im.height),ix.tobytes());p.putpalette(pp);p.info['transparency']=0
        if scale!=1:p=p.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
        fs.append(p)
    fs[0].save(path,save_all=True,append_images=fs[1:],duration=times,loop=0,transparency=0,disposal=2,optimize=False)

manifest={}
allframes={}
for name,job in JOBS.items():
    folder=ROOT/name;layers=[];frames=[]
    for i,im in enumerate(raw[name]):
        im=remap(im)
        body,fx=separate(name,im)
        if name.endswith('complete') and i in (0,5):fx=Image.new('RGBA',im.size)
        bbox=body.getbbox()
        # Register to one ground baseline. The jump still uses distinct arms,
        # legs, head and tail from the selected artwork; translation adds lift.
        ground = round(SIZE * .93)
        lift = [0,0,7,10,0,0][i] if name.endswith('complete') else 0
        dx=round(SIZE/2-(bbox[0]+bbox[2])/2)
        dy=ground-lift-bbox[3]
        body=shift(body,dx,dy);fx=shift(fx,dx,dy)
        if name=='planner-working':
            # Retouch the existing eye glints on their lens positions. Crisp
            # four-point silhouettes survive the native 80px export.
            a=np.array(body);r,g,b=[a[:,:,j].astype(int) for j in range(3)]
            glint=(b>120)&(g>100)&(b>r*1.4)&(b>g*1.05)&(a[:,:,3]>0)
            unseen=set(zip(*np.nonzero(glint)));eyes=[]
            while unseen:
                start=unseen.pop();component=[start];queue=[start]
                while queue:
                    yy,xx=queue.pop()
                    for y1 in range(yy-1,yy+2):
                        for x1 in range(xx-1,xx+2):
                            if (y1,x1) in unseen:unseen.remove((y1,x1));component.append((y1,x1));queue.append((y1,x1))
                if len(component)>=3:
                    cy,cx=np.array(component).mean(axis=0)
                    if cy<SIZE*.65:eyes.append((round(cx),round(cy)))
            d=ImageDraw.Draw(body)
            for x,y in eyes:
                for xx,yy in [(x-1,y-1),(x+1,y-1),(x-1,y+1),(x+1,y+1)]:d.point((xx,yy),fill='#12a8e0')
                d.line((x-2,y,x+2,y),fill='#60d7ed',width=1)
                d.line((x,y-2,x,y+2),fill='#60d7ed',width=1)
                d.point((x,y),fill='#ecffff')
        if name=='planner-complete':
            # Position the existing V raster in the available headroom. This
            # prevents the top of the V from clipping during the jump.
            fb=fx.getbbox();bb=body.getbbox()
            if fb and fb[1]<2:fx=shift(fx,0,2-fb[1])
        out=Image.alpha_composite(body,fx)
        out.save(folder/f'frame-{i+1:02}.png');body.save(folder/f'body-{i+1:02}.png');fx.save(folder/f'effect-{i+1:02}.png')
        layers.append([body,fx]);frames.append(out)
    allframes[name]=frames
    sheet=Image.new('RGBA',(SIZE*6,SIZE))
    for i,im in enumerate(frames):sheet.paste(im,(SIZE*i,0))
    sheet.save(folder/'spritesheet.png')
    sheet.resize((SIZE*6*3,SIZE*3),Image.Resampling.NEAREST).save(folder/'spritesheet-3x.png')
    save_gif(folder/f'{name}.gif',frames,job['durations'])
    save_gif(folder/'preview.gif',frames,job['durations'],4)
    data={'pixelorama_version':'v1.2.3-stable','pxo_version':7,'size_x':SIZE,'size_y':SIZE,'color_mode':5,'layers':[{'name':n,'type':0,'visible':True,'opacity':1,'parent':-1} for n in ['Edited key poses','Completion effect']],'frames':[{'duration':ms/100,'cels':[{'opacity':1,'z_index':0} for _ in range(2)]} for ms in job['durations']],'current_frame':0,'current_layer':0,'fps':10,'tags':[{'name':name,'color':'48c76bff','from':1,'to':6}]}
    with zipfile.ZipFile(folder/f'{name}.pxo','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('mimetype','application/x-pixelorama');z.writestr('data.json',json.dumps(data))
        for fi,ls in enumerate(layers,1):
            for li,img in enumerate(ls,1):z.writestr(f'image_data/frames/{fi}/layer_{li}',img.tobytes())
        z.write(folder/'frame-01.png','preview.png')
    manifest[name]={'size':[SIZE,SIZE],'frames':6,'durationMs':job['durations'],'totalMs':sum(job['durations']),'selectedV6Frames':SELECTED[name],'beats':job['beats'],'paletteMax':32,'alphaValues':[0,255],'effectPixels':[sum(v>0 for v in ls[1].getchannel('A').getdata()) for ls in layers],'source':'source-atlas.png','method':'built-in image_gen edit of selected v6 poses + deterministic raster packaging'}

# Preserve idle deliverables byte-for-byte. They are not six-frame redesigns.
for c in ('planner','passion'):
    name=c+'-idle';shutil.copytree(OLD/name,ROOT/name,dirs_exist_ok=True)
    fs=sorted((ROOT/name).glob('frame-*.png'))
    allframes[name]=[Image.open(p).convert('RGBA') for p in fs]
    manifest[name]={'size':list(allframes[name][0].size),'frames':len(fs),'durationMs':[1000/12]*len(fs),'unchangedFromV6':True}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))

# Inspectable frame board and side-by-side resolution alternatives.
board=Image.new('RGB',(1440,1120),'#e4ded4');draw=ImageDraw.Draw(board)
for row,(name,job) in enumerate(JOBS.items()):
    draw.text((16,row*280+8),name,fill='#34232e')
    for i,im in enumerate(allframes[name]):
        bg=Image.new('RGBA',(240,240),'#e4ded4');bg.alpha_composite(im.resize((240,240),Image.Resampling.NEAREST));board.paste(bg.convert('RGB'),(i*240,row*280+28));draw.text((i*240+12,row*280+263),f'{i+1} / {job["durations"][i]} ms',fill='#34232e')
board.save(ROOT/'all-frames.png')
comparison=Image.new('RGB',(1152,1152),'#e4ded4');d=ImageDraw.Draw(comparison)
for row,name in enumerate(JOBS):
    for col,s in enumerate([64,80,96]):
        im=remap(pixels(name,0,s)).resize((288,288),Image.Resampling.NEAREST)
        bg=Image.new('RGBA',im.size,'#e4ded4');bg.alpha_composite(im);comparison.paste(bg.convert('RGB'),(col*384+48,row*288))
        d.text((col*384+8,row*288+8),f'{name}: {s}px',fill='#34232e')
comparison.save(ROOT/'resolution-comparison.png')

# Combined animated review: completion settles before the common loop restarts.
events={0,1500,2200}
for job in JOBS.values():
    t=0
    for ms in job['durations']:t+=ms;events.add(t)
events=sorted(events);overview=[];overview_times=[]
for k,t in enumerate(events[:-1]):
    canvas=Image.new('RGB',(640,640),'#e4ded4');d=ImageDraw.Draw(canvas)
    for j,(name,job) in enumerate(JOBS.items()):
        x=j%2*320;y=j//2*320;d.text((x+18,y+10),name.replace('-',' / '),fill='#42323b')
        ms=0;idx=5
        for i,dd in enumerate(job['durations']):
            if t<ms+dd:idx=i;break
            ms+=dd
        im=allframes[name][idx].resize((240,240),Image.Resampling.NEAREST)
        canvas.paste(im,(x+40,y+40),im);d.text((x+18,y+291),f'pose {idx+1} / 6',fill='#796d71')
    overview.append(canvas);overview_times.append(events[k+1]-t)
overview[0].save(ROOT/'overview.gif',save_all=True,append_images=overview[1:],duration=overview_times,loop=0,optimize=False)

# Offline preview data: PNG frames are embedded; opening requires no server.
import base64
web={n:{'frames':['data:image/png;base64,'+base64.b64encode((ROOT/n/f'frame-{i+1:02}.png').read_bytes()).decode() for i in range(len(fs))],'times':manifest[n]['durationMs'],'size':manifest[n]['size'][0]} for n,fs in allframes.items()}
(ROOT/'preview-data.js').write_text('const ASSETS='+json.dumps(web,separators=(',',':'))+';')
(ROOT/'preview.html').write_text((ROOT/'preview-template.html').read_text().replace('/* EMBED_DATA */',(ROOT/'preview-data.js').read_text()))
print(json.dumps({n:{'frames':m['frames'],'size':m['size'],'totalMs':m.get('totalMs')} for n,m in manifest.items()},indent=2))
