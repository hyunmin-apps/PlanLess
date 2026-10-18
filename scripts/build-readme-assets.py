#!/usr/bin/env python3
"""Build theme-aware README artwork from the approved, unchanged mascot frames."""
from pathlib import Path
import base64, json, re
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/readme'
OUT.mkdir(parents=True, exist_ok=True)
meta = json.loads((ROOT / 'Resources/Mascots/animations.json').read_text())

def image_uri(path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()

def build(theme):
    dark = theme == 'dark'
    c = dict(bg='#142422', ink='#eef8ef', muted='#a2bdb3', accent='#a9e5bc', border='#36504a', card='#1e3330', row='#263f38', highlight='#335c49', soft='#243e36', orange='#f6bb81') if dark else dict(bg='#eff6ed', ink='#183a2b', muted='#667d6b', accent='#2d704d', border='#d5e2d2', card='#ffffff', row='#f6f8f2', highlight='#e1efdb', soft='#e3ecdd', orange='#b36636')
    times = meta['characters']['planner']['working']
    total = sum(times)
    rules=[]; frames=[]; at=0
    for i, ms in enumerate(times):
        start, end = at/total*100, (at+ms)/total*100
        points = (f'0%,{end:.5f}%{{opacity:1}}{end+.0001:.5f}%,100%{{opacity:0}}' if i==0 else f'0%,{max(0,start-.0001):.5f}%{{opacity:0}}{start:.5f}%,{end:.5f}%{{opacity:1}}' + (f'{end+.0001:.5f}%,100%{{opacity:0}}' if i<len(times)-1 else ''))
        rules.append(f'@keyframes frame{i}{{{points}}}.frame{i}{{animation:frame{i} {total}ms steps(1,end) infinite}}')
        uri = image_uri(ROOT/f'Resources/Mascots/planner/working/frame-{i+1:02}.png')
        frames.append(f'<image class="sprite frame{i}" href="{uri}" x="902" y="286" width="188" height="188" style="image-rendering:pixelated"/>')
        at += ms
    days=''
    for i, (d,n) in enumerate(zip(['M','T','W','T','F','S','S'],range(12,19))):
        x=633+i*64
        active=i==6
        days+=f'<rect x="{x}" y="180" width="53" height="59" rx="14" fill="{c["highlight"] if active else c["row"]}"/><text x="{x+26.5}" y="200" text-anchor="middle" font-size="10" fill="{c["muted"]}">{d}</text><text x="{x+26.5}" y="222" text-anchor="middle" font-size="16" font-weight="650" fill="{c["ink"]}">{n}</text>'
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="570" viewBox="0 0 1200 570" role="img" aria-labelledby="title desc">
<title id="title">PlanLess — 계획은 가볍게, 실천은 바로</title>
<desc id="desc">Plan less. Do more. 청록 스카프를 한 계획단장 레서와 예시 할 일 세 개를 넣은 사용 흐름 일러스트입니다. 실제 사용자 계획이나 앱 스크린샷이 아닙니다.</desc>
<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="{c['border']}"/></pattern><linearGradient id="glow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{c['bg']}"/><stop offset="1" stop-color="{c['soft']}"/></linearGradient></defs>
<style>text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Apple SD Gothic Neo','Noto Sans CJK KR',sans-serif}}.sprite{{opacity:0}}{''.join(rules)}@media(prefers-reduced-motion:reduce){{.sprite{{animation:none!important;opacity:0}}.frame0{{opacity:1}}}}</style>
<rect width="1200" height="570" rx="32" fill="url(#glow)"/>
<rect x="570" y="0" width="630" height="570" fill="url(#dots)" opacity=".65"/>
<circle cx="1160" cy="80" r="190" fill="{c['soft']}"/>
<rect x="48" y="47" width="9" height="9" rx="4.5" fill="{c['accent']}"/>
<text x="69" y="57" font-size="13" font-weight="700" letter-spacing="2" fill="{c['accent']}">PLANLESS / A SMALL START</text>
<text x="46" y="198" font-size="83" font-weight="750" letter-spacing="-5" fill="{c['ink']}">Plan less.</text>
<text x="46" y="288" font-size="83" font-weight="750" letter-spacing="-5" fill="{c['accent']}">Do more.</text>
<text x="50" y="348" font-size="24" font-weight="600" letter-spacing="-1" fill="{c['ink']}">계획은 가볍게, 실천은 바로.</text>
<text x="50" y="385" font-size="17" fill="{c['muted']}">오늘 할 일 하나, 레서와 함께 시작해요.</text>
<rect x="50" y="445" width="117" height="34" rx="17" fill="{c['card']}" stroke="{c['border']}"/>
<text x="108.5" y="467" text-anchor="middle" font-size="12" font-weight="650" fill="{c['accent']}">LESS PLANNING</text>
<path d="M180 462h38m-7-6 7 6-7 6" fill="none" stroke="{c['accent']}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<text x="231" y="466" font-size="12" letter-spacing="1" font-weight="650" fill="{c['muted']}">MORE DOING</text>
<rect x="600" y="103" width="535" height="412" rx="29" fill="{c['border']}" opacity=".4"/>
<rect x="590" y="92" width="535" height="412" rx="28" fill="{c['card']}" stroke="{c['border']}"/>
<circle cx="616" cy="120" r="4" fill="#ef9f8f"/><circle cx="631" cy="120" r="4" fill="#e9cb86"/><circle cx="646" cy="120" r="4" fill="#a5c898"/>
<text x="1100" y="125" text-anchor="end" fill="{c['muted']}" font-size="11" letter-spacing="1">PLANLESS</text>
<text x="633" y="159" font-size="18" font-weight="700" fill="{c['ink']}">Today, one thing at a time.</text>
{days}
<rect x="633" y="265" width="253" height="58" rx="13" fill="{c['row']}"/>
<rect x="647" y="284" width="19" height="19" rx="6" fill="{c['accent']}"/>
<path d="m652 293 4 4 6-8" fill="none" stroke="{c['card']}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
<text x="678" y="288" font-size="10" fill="{c['muted']}">READING</text>
<text x="678" y="307" font-size="13" fill="{c['muted']}" text-decoration="line-through">Read 10 pages</text>
<rect x="633" y="332" width="253" height="58" rx="13" fill="{c['highlight']}" stroke="{c['border']}"/>
<rect x="647" y="351" width="19" height="19" rx="6" fill="none" stroke="{c['accent']}" stroke-width="1.6"/>
<path d="M651 366v-11h5v11z" fill="{c['accent']}"/>
<text x="678" y="355" font-size="10" fill="{c['accent']}">IN PROGRESS</text>
<text x="678" y="374" font-size="13" font-weight="600" fill="{c['ink']}">One practice problem</text>
<rect x="633" y="399" width="253" height="58" rx="13" fill="{c['row']}"/>
<rect x="647" y="418" width="19" height="19" rx="6" fill="none" stroke="{c['border']}" stroke-width="1.5"/>
<text x="678" y="422" font-size="10" fill="{c['muted']}">UP NEXT</text>
<text x="678" y="441" font-size="13" fill="{c['ink']}">Wrap up for today</text>
<rect x="926" y="257" width="148" height="27" rx="13.5" fill="{c['row']}"/>
<text x="1000" y="275" text-anchor="middle" font-size="11" fill="{c['accent']}">YOU'VE GOT THIS.</text>
{''.join(frames)}
<text x="633" y="483" font-size="10" fill="{c['muted']}">ILLUSTRATED WORKFLOW · SAMPLE TASKS</text>
<text x="50" y="537" font-size="10" letter-spacing="1.5" fill="{c['muted']}">A LOCAL MACOS PLANNER, WITH A LITTLE RED PANDA.</text>
</svg>'''
    (OUT/f'hero-{theme}.svg').write_text(svg)

def build_mobile(theme):
    dark=theme=='dark'
    c=dict(bg='#142422', ink='#eef8ef', muted='#a2bdb3', accent='#a9e5bc', border='#36504a', card='#1e3330', row='#263f38', highlight='#335c49') if dark else dict(bg='#eff6ed', ink='#183a2b', muted='#667d6b', accent='#2d704d', border='#d5e2d2', card='#fff', row='#f6f8f2', highlight='#e1efdb')
    original=(OUT/f'hero-{theme}.svg').read_text()
    style=re.search(r'<style>.*?</style>',original,re.S).group()
    frames=''.join(re.findall(r'<image class="sprite.*?/>',original)).replace('x="902" y="286" width="188" height="188"','x="369" y="329" width="205" height="205"')
    (OUT/f'hero-mobile-{theme}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="620" viewBox="0 0 640 620" role="img" aria-labelledby="title desc">
<title id="title">PlanLess — 계획은 가볍게, 실천은 바로</title><desc id="desc">작은 화면에 맞춘 사용 흐름 일러스트. 예시 할 일과 승인된 계획단장 레서의 진행 프레임.</desc>{style}
<rect width="640" height="620" rx="30" fill="{c['bg']}"/>
<circle cx="47" cy="41" r="4" fill="{c['accent']}"/><text x="63" y="46" font-size="13" letter-spacing="2" fill="{c['accent']}">PLANLESS / A SMALL START</text>
<text x="40" y="132" font-size="66" font-weight="750" letter-spacing="-3" fill="{c['ink']}">Plan less.</text>
<text x="40" y="205" font-size="66" font-weight="750" letter-spacing="-3" fill="{c['accent']}">Do more.</text>
<text x="44" y="251" font-size="25" font-weight="600" fill="{c['ink']}">계획은 가볍게, 실천은 바로.</text>
<rect x="38" y="291" width="564" height="266" rx="25" fill="{c['card']}" stroke="{c['border']}"/>
<text x="62" y="327" font-size="15" letter-spacing="2" fill="{c['muted']}">TODAY / ONE THING AT A TIME</text>
<rect x="61" y="352" width="292" height="73" rx="15" fill="{c['row']}"/>
<rect x="77" y="376" width="25" height="25" rx="7" fill="{c['accent']}"/><path d="m83 388 5 5 8-11" stroke="{c['card']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
<text x="116" y="383" font-size="12" fill="{c['muted']}">READING</text><text x="116" y="408" font-size="21" fill="{c['muted']}" text-decoration="line-through">Read 10 pages</text>
<rect x="61" y="436" width="292" height="91" rx="15" fill="{c['highlight']}"/><text x="79" y="465" font-size="12" font-weight="650" fill="{c['accent']}">IN PROGRESS</text><text x="79" y="497" font-size="21" font-weight="650" fill="{c['ink']}">One practice problem</text>{frames}
<text x="42" y="592" font-size="12" letter-spacing="1" fill="{c['muted']}">ILLUSTRATED WORKFLOW · SAMPLE TASKS</text>
</svg>''')

for theme in ['light','dark']:
    build(theme)
    build_mobile(theme)
print('Built responsive light/dark hero illustrations using the approved mascot frames')
