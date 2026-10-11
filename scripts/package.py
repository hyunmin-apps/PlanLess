#!/usr/bin/env python3
import hashlib,json,pathlib,subprocess,tempfile
from build import ROOT,run
version=(ROOT/'VERSION').read_text().strip();app=ROOT/'build/universal/Study Glass.app';dist=ROOT/'dist';dist.mkdir(exist_ok=True)
if not app.exists():raise SystemExit('Run ./build.sh first')
run('python3','tests/verify.py',app)
name=f'StudyGlass-{version}-macOS-universal'
run('ditto','-c','-k','--sequesterRsrc','--keepParent',app,dist/(name+'.zip'))
with tempfile.TemporaryDirectory(prefix='studyglass-dmg-') as temp:
 staging=pathlib.Path(temp);run('ditto',app,staging/'Study Glass.app');(staging/'Applications').symlink_to('/Applications')
 (staging/'설치 안내.txt').write_text('Study Glass.app을 Applications에 복사하고 한 번 실행하세요.\n바탕화면 우클릭 → 위젯 편집 → Study Glass에서 위젯을 추가합니다.\nmacOS 14 이상 · Apple Silicon 및 Intel\nDeveloper ID 서명과 Apple 공증 전 시험 릴리스입니다.\n')
 run('hdiutil','create','-ov','-volname','Study Glass','-srcfolder',staging,'-format','UDZO',dist/(name+'.dmg'))
assets=[dist/(name+'.zip'),dist/(name+'.dmg')]
manifest=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in assets]
(dist/'SHA256SUMS.txt').write_text(''.join(x['sha256']+'  '+x['file']+'\n' for x in manifest))
(dist/'release-manifest.json').write_text(json.dumps({'version':version,'architectures':['arm64','x86_64'],'minimum_macos':'14.0','signing':'ad-hoc; not notarized','assets':manifest},indent=2)+'\n')
