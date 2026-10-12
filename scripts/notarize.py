#!/usr/bin/env python3
"""Build, sign and notarize using an existing Developer ID and Keychain profile."""
import argparse,json,subprocess,tempfile,pathlib
from build import ROOT,run
p=argparse.ArgumentParser();p.add_argument('--identity',required=True);p.add_argument('--keychain-profile',required=True);a=p.parse_args()
run('python3','scripts/build.py','--identity',a.identity)
app=ROOT/'build/universal/Study Glass.app'
with tempfile.TemporaryDirectory(prefix='studyglass-notary-') as temp:
 archive=pathlib.Path(temp)/'StudyGlass.zip'
 run('ditto','-c','-k','--sequesterRsrc','--keepParent',app,archive)
 result=json.loads(subprocess.check_output(['xcrun','notarytool','submit',str(archive),'--keychain-profile',a.keychain_profile,'--wait','--output-format','json'],text=True))
 if result.get('status')!='Accepted':raise SystemExit('Notarization failed: '+json.dumps(result))
run('xcrun','stapler','staple',app)
run('python3','scripts/package.py','--notary-profile',a.keychain_profile)
