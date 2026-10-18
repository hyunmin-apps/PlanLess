"""Resource parity and sprite packaging checks; visual review is separate."""
from pathlib import Path
from PIL import Image
import json
root=Path(__file__).resolve().parents[1];assets=root/'Resources/Mascots'
meta=json.loads((assets/'animations.json').read_text())
for character in ['planner','passion']:
 for mode in ['working','complete','idle']:
  expected=12 if mode=='idle' else 6
  files=sorted((assets/character/mode).glob('*.png'));assert len(files)==expected
  for path in files:
   im=Image.open(path);assert im.size==(80,80) and im.mode=='RGBA'
   assert set(im.getchannel('A').getdata()) <= {0,255}
   bounds=im.getbbox();assert bounds and 0<bounds[0]<bounds[2]<80 and 0<bounds[1]<bounds[3]<80, path
   if mode=='idle':assert bounds[3]==74
   else:assert path.read_bytes()==(root/'design/lesser-motion-v8'/(character+'-'+mode)/path.name).read_bytes()
  assert len(meta['characters'][character][mode])==expected
 assert sum(meta['characters'][character]['complete'])==1500
print('PASS: approved motion unchanged, correct frame counts/timings, transparent 80px sprites, idle baseline, no clipped sprite edges')
