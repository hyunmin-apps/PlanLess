#!/usr/bin/env python3
"""Build the app and WidgetKit extension for both Mac architectures."""
import argparse, os, pathlib, plistlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
def run(*args): subprocess.run(list(map(str,args)),check=True,cwd=ROOT)
def main():
 p=argparse.ArgumentParser();p.add_argument('--arch',choices=['universal','arm64','x86_64'],default='universal');p.add_argument('--identity',default='-',help='Developer ID Application identity, or - for local preview');a=p.parse_args()
 if a.identity != '-' and not a.identity.startswith('Developer ID Application:'):
  p.error('Use a Developer ID Application identity for distribution')
 version=(ROOT/'VERSION').read_text().strip();out=ROOT/'build'/a.arch; app=out/'Study Glass.app'; widget=app/'Contents/PlugIns/StudyGlassWidget.appex'
 arches=['arm64','x86_64'] if a.arch=='universal' else [a.arch]
 for bundle in [app,widget]:
  for folder in ['MacOS','Resources']:(bundle/'Contents'/folder).mkdir(parents=True,exist_ok=True)
 # Generate the embedded plan from the one canonical JSON source.
 html=(ROOT/'Resources/index.html').read_text();start=html.index('const PLAN=');end=html.index('const colors=',start)
 html=html[:start]+'const PLAN='+(ROOT/'Resources/plan.json').read_text()+';\n'+html[end:]
 (app/'Contents/Resources/index.html').write_text(html)
 run('cp',ROOT/'Resources/import-plan.js',app/'Contents/Resources/import-plan.js')
 run('cp',ROOT/'Resources/AppIcon.icns',app/'Contents/Resources/AppIcon.icns')
 run('cp',ROOT/'Resources/plan.json',widget/'Contents/Resources/plan.json')
 for name,source,frameworks,bundle in [('StudyGlass','Sources/main.swift',['Cocoa','WebKit','WidgetKit'],app),('StudyGlassWidget','Widget/StudyWidget.swift',['SwiftUI','WidgetKit'],widget)]:
  binaries=[]
  for arch in arches:
   binary=out/(name+'-'+arch);binaries.append(binary)
   args=['xcrun','swiftc','-O','-target',arch+'-apple-macos14.0']
   if name=='StudyGlassWidget':args+=['-parse-as-library','-application-extension','-Xlinker','-e','-Xlinker','_NSExtensionMain']
   args += [source,'-o',binary]
   for f in frameworks:args+=['-framework',f]
   run(*args)
  target=bundle/'Contents/MacOS'/name
  if len(binaries)>1:run('xcrun','lipo','-create',*binaries,'-output',target)
  else:run('cp',binaries[0],target)
  info={'CFBundleExecutable':name,'CFBundleIdentifier':'local.studyglass.desktop'+('.widget' if bundle==widget else ''),'CFBundleName':name,'CFBundleDisplayName':'Study Glass','CFBundlePackageType':'XPC!' if bundle==widget else 'APPL','CFBundleVersion':version,'CFBundleShortVersionString':version,'LSMinimumSystemVersion':'14.0','CFBundleSupportedPlatforms':['MacOSX']}
  if bundle==widget:info['NSExtension']={'NSExtensionPointIdentifier':'com.apple.widgetkit-extension'}
  else:info.update(CFBundleIconFile='AppIcon',NSHighResolutionCapable=True,CFBundleURLTypes=[{'CFBundleURLName':'Study Glass Date','CFBundleURLSchemes':['studyglass']}])
  with (bundle/'Contents/Info.plist').open('wb') as f:plistlib.dump(info,f)
 sign=['codesign','--force','--sign',a.identity]
 if a.identity != '-':sign+=['--options','runtime','--timestamp']
 run(*sign,'--entitlements','Widget/entitlements.plist',widget)
 run(*sign,app)
 run('codesign','--verify','--deep','--strict',app)
 print(app)
if __name__=='__main__':main()
