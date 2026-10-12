#!/usr/bin/env python3
import json,pathlib,plistlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[1];app=pathlib.Path(sys.argv[1]);expected=set(sys.argv[2:]) or {'arm64','x86_64'}
for relative in ['Contents/MacOS/StudyGlass','Contents/PlugIns/StudyGlassWidget.appex/Contents/MacOS/StudyGlassWidget']:
 binary=app/relative;arches=set(subprocess.check_output(['lipo','-archs',str(binary)],text=True).split());assert arches==expected,(binary,arches)
 for arch in expected:
  loads=subprocess.check_output(['otool','-arch',arch,'-L',str(binary)],text=True)
  assert '/Users/' not in '\n'.join(loads.splitlines()[1:]),'Non-portable dynamic library'
subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True)
widget=app/'Contents/PlugIns/StudyGlassWidget.appex'
with (widget/'Contents/Info.plist').open('rb') as f:info=plistlib.load(f)
assert info['NSExtension']['NSExtensionPointIdentifier']=='com.apple.widgetkit-extension'
assert info['LSMinimumSystemVersion']=='14.0'
plan=json.loads((root/'Resources/plan.json').read_text());assert plan==[], 'Release must start empty'
html=(app/'Contents/Resources/index.html').read_text();assert 'const PLAN=' in html
embedded=html.split('const PLAN=',1)[1].split('const colors=',1)[0].strip().rstrip(';');assert json.loads(embedded)==plan
assert not list(app.rglob('state.json'));assert not list(app.rglob('study-state.json'))
print('PASS: architectures, portable libraries, nested signatures, WidgetKit metadata, plan parity, no user state')
