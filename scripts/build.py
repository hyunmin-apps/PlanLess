#!/usr/bin/env python3
"""Build the app and WidgetKit extension for both Mac architectures."""
import argparse, os, pathlib, plistlib, subprocess, shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
def run(*args): subprocess.run(list(map(str,args)),check=True,cwd=ROOT)
def main():
 p=argparse.ArgumentParser();p.add_argument('--arch',choices=['universal','arm64','x86_64'],default='universal');p.add_argument('--identity',default='-',help='Developer ID Application identity, or - for local preview');a=p.parse_args()
 if a.identity != '-' and not a.identity.startswith('Developer ID Application:'):
  p.error('Use a Developer ID Application identity for distribution')
 version=(ROOT/'VERSION').read_text().strip();out=ROOT/'build'/a.arch; app=out/'PlanLess.app'; widget=app/'Contents/PlugIns/PlanLessWidget.appex'
 arches=['arm64','x86_64'] if a.arch=='universal' else [a.arch]
 for bundle in [app,widget]:
  for folder in ['MacOS','Resources']:(bundle/'Contents'/folder).mkdir(parents=True,exist_ok=True)
 # Generate the embedded plan from the one canonical JSON source.
 html=(ROOT/'Resources/index.html').read_text();start=html.index('const PLAN=');end=html.index('const colors=',start)
 html=html[:start]+'const PLAN='+(ROOT/'Resources/plan.json').read_text()+';\n'+html[end:]
 (app/'Contents/Resources/index.html').write_text(html)
 for asset in ['companion.js','companion.css']:run('cp',ROOT/'Resources'/asset,app/'Contents/Resources'/asset)
 run('cp',ROOT/'Resources/rollover.js',app/'Contents/Resources/rollover.js')
 run('cp',ROOT/'Resources/import-plan.js',app/'Contents/Resources/import-plan.js')
 for old_icon in ['AppIcon.icns','PlanLessIcon.icns']:(app/'Contents/Resources'/old_icon).unlink(missing_ok=True)
 run('cp',ROOT/'Resources/AppIcon.icns',app/'Contents/Resources/PlanLessPlannerIcon.icns')
 run('cp',ROOT/'Resources/plan.json',widget/'Contents/Resources/plan.json')
 run('cp',ROOT/'Resources/plan.json',app/'Contents/Resources/plan.json')
 for bundle in [app,widget]:shutil.copytree(ROOT/'Resources/Mascots',bundle/'Contents/Resources/Mascots',dirs_exist_ok=True)
 for name,source,frameworks,bundle in [('PlanLess','Sources/main.swift',['Cocoa','WebKit','WidgetKit'],app),('PlanLessWidget','Widget/PlanLessWidget.swift',['SwiftUI','WidgetKit'],widget)]:
  binaries=[]
  for arch in arches:
   binary=out/(name+'-'+arch);binaries.append(binary)
   args=['xcrun','swiftc','-O','-target',arch+'-apple-macos14.0']
   if name=='PlanLessWidget':args+=['-parse-as-library','-application-extension','-Xlinker','-e','-Xlinker','_NSExtensionMain']
   args += [source]
   if name=='PlanLess':args += ['Sources/MascotState.swift','Sources/Companion.swift']
   args += ['-o',binary]
   for f in frameworks:args+=['-framework',f]
   run(*args)
  target=bundle/'Contents/MacOS'/name
  if len(binaries)>1:run('xcrun','lipo','-create',*binaries,'-output',target)
  else:run('cp',binaries[0],target)
  # Bundle identifiers intentionally remain stable for placed widgets and preferences.
  info={'CFBundleExecutable':name,'CFBundleIdentifier':'local.studyglass.desktop'+('.widget' if bundle==widget else ''),'CFBundleName':name,'CFBundleDisplayName':'PlanLess','CFBundlePackageType':'XPC!' if bundle==widget else 'APPL','CFBundleVersion':version,'CFBundleShortVersionString':version,'LSMinimumSystemVersion':'14.0','CFBundleSupportedPlatforms':['MacOSX']}
  if bundle==widget:info['NSExtension']={'NSExtensionPointIdentifier':'com.apple.widgetkit-extension'}
  else:info.update(CFBundleIconFile='PlanLessPlannerIcon',NSHighResolutionCapable=True,CFBundleURLTypes=[{'CFBundleURLName':'PlanLess Date','CFBundleURLSchemes':['planless','studyglass']}])
  with (bundle/'Contents/Info.plist').open('wb') as f:plistlib.dump(info,f)
 sign=['codesign','--force','--sign',a.identity]
 if a.identity != '-':sign+=['--options','runtime','--timestamp']
 run(*sign,'--entitlements','Widget/entitlements.plist',widget)
 run(*sign,app)
 run('codesign','--verify','--deep','--strict',app)
 print(app)
if __name__=='__main__':main()
