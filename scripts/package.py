#!/usr/bin/env python3
"""Package explicitly labelled previews, or require notarization before distribution."""
import argparse,hashlib,json,pathlib,plistlib,subprocess,tempfile
from build import ROOT,run
p=argparse.ArgumentParser()
p.add_argument('--notary-profile',help='Keychain profile; requires an already signed, notarized and stapled app')
a=p.parse_args()
version=(ROOT/'VERSION').read_text().strip();app=ROOT/'build/universal/Study Glass.app';dist=ROOT/'dist';dist.mkdir(exist_ok=True)
if not app.exists():raise SystemExit('Run ./build.sh first')
with (app/'Contents/Info.plist').open('rb') as f:info=plistlib.load(f)
if info['CFBundleShortVersionString']!=version:raise SystemExit('Stale build: VERSION and app version differ; rebuild first')
run('python3','tests/verify.py',app)
assessment=subprocess.run(['spctl','--assess','--type','execute','--verbose=4',str(app)],capture_output=True,text=True)
signature=subprocess.check_output(['codesign','-d','--verbose=4',str(app)],stderr=subprocess.STDOUT,text=True)
if a.notary_profile:
 if 'Authority=Developer ID Application:' not in signature:raise SystemExit('Developer ID Application signature required')
 run('xcrun','stapler','validate',app)
 if assessment.returncode:raise SystemExit('Gatekeeper rejected app: '+assessment.stderr)
 label='notarized';guide='Study Glass.app을 Applications로 복사한 뒤 실행하세요.\nmacOS 14 이상 · Apple Silicon / Intel\n바탕화면 우클릭 → 위젯 편집 → Study Glass\n'
else:
 label='UNNOTARIZED-preview';guide=(ROOT/'docs/INSTALL.txt').read_text()
name=f'StudyGlass-{version}-macOS-universal-{label}'
# ZIP and DMG contain the same app and first-install instructions.
with tempfile.TemporaryDirectory(prefix='studyglass-package-') as temp:
 staging=pathlib.Path(temp);run('ditto',app,staging/'Study Glass.app')
 (staging/'먼저 읽기 - 설치 안내.txt').write_text(guide)
 run('ditto','-c','-k','--sequesterRsrc',staging,dist/(name+'.zip'))
 (staging/'Applications').symlink_to('/Applications')
 run('hdiutil','create','-ov','-volname','Study Glass','-srcfolder',staging,'-format','UDZO',dist/(name+'.dmg'))
if a.notary_profile:
 result=json.loads(subprocess.check_output(['xcrun','notarytool','submit',str(dist/(name+'.dmg')),'--keychain-profile',a.notary_profile,'--wait','--output-format','json'],text=True))
 if result.get('status')!='Accepted':raise SystemExit('DMG notarization failed: '+json.dumps(result))
 run('xcrun','stapler','staple',dist/(name+'.dmg'))
 run('xcrun','stapler','validate',dist/(name+'.dmg'))
(dist/'INSTALL.txt').write_text(guide)
assets=[dist/(name+'.zip'),dist/(name+'.dmg'),dist/'INSTALL.txt']
if not a.notary_profile:
 installer=dist/f'StudyGlass-{version}-Install.command'
 template=(ROOT/'scripts/install.command.in').read_text()
 template=template.replace('@VERSION@',version).replace('@ARCHIVE@',name+'.zip').replace('@SHA256@',hashlib.sha256((dist/(name+'.zip')).read_bytes()).hexdigest())
 installer.write_text(template);installer.chmod(0o755);assets.append(installer)
manifest=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in assets]
(dist/'SHA256SUMS.txt').write_text(''.join(x['sha256']+'  '+x['file']+'\n' for x in manifest))
(dist/'release-manifest.json').write_text(json.dumps({'version':version,'architectures':['arm64','x86_64'],'minimum_macos':'14.0','signing':'Developer ID; notarized and stapled' if a.notary_profile else 'ad-hoc; NOT notarized','gatekeeper':{'accepted':assessment.returncode==0,'output':assessment.stderr.strip().replace(str(app),'Study Glass.app')},'assets':manifest},indent=2)+'\n')
print('Packaged',name)
