#!/usr/bin/env python3
"""Exercise installer against a local release ZIP in an isolated destination.
Network, process detection and app opening are stubbed; copy/signature/xattr use macOS.
Usage: python3 tests/installer.py path/to/release.zip VERSION
"""
import hashlib,pathlib,subprocess,sys,tempfile,shlex
root=pathlib.Path(__file__).resolve().parents[1]
archive=pathlib.Path(sys.argv[1]).resolve();version=sys.argv[2]
with tempfile.TemporaryDirectory(prefix='studyglass-installer-test-') as directory:
 p=pathlib.Path(directory);dest=p/'Applications';log=p/'opened'
 curl=p/'curl';curl.write_text('#!/bin/bash\nset -e\nwhile [ "$1" != --output ]; do shift; done\ncp '+shlex.quote(str(archive))+' "$2"\n');curl.chmod(0o755)
 opener=p/'open';opener.write_text('#!/bin/bash\nprintf "%s\\n" "$1" >> '+shlex.quote(str(log))+'\n');opener.chmod(0o755)
 text=(root/'scripts/install.command.in').read_text().replace('@VERSION@',version).replace('@ARCHIVE@',archive.name).replace('@SHA256@',hashlib.sha256(archive.read_bytes()).hexdigest())
 text=text.replace('APP_DIR="${HOME}/Applications"','APP_DIR='+shlex.quote(str(dest))).replace('/usr/bin/curl',shlex.quote(str(curl))).replace('/usr/bin/open',shlex.quote(str(opener))).replace('/usr/bin/pgrep -x StudyGlass','/usr/bin/false')
 script=p/'install.command';script.write_text(text)
 def run(script,answer):return subprocess.run(['/bin/bash',str(script)],input=answer,text=True,capture_output=True)
 r=run(script,'n\n');assert r.returncode==0 and not dest.exists(),r.stderr
 bad=p/'bad.command';bad.write_text(text.replace(hashlib.sha256(archive.read_bytes()).hexdigest(),'0'*64))
 r=run(bad,'y\n');assert r.returncode!=0 and not dest.exists(),r.stderr
 r=run(script,'y\n');assert r.returncode==0,r.stdout+r.stderr
 app=dest/'Study Glass.app';assert app.exists() and log.exists()
 subprocess.run(['/usr/bin/xattr','-w','com.apple.quarantine','0083;00000000;Test;',str(app)],check=True)
 r=run(script,'y\n');assert r.returncode==0,r.stdout+r.stderr
 assert len(list(dest.glob('StudyGlass-backup.*/Study Glass.app')))==1
 assert 'com.apple.quarantine' not in subprocess.check_output(['/usr/bin/xattr',str(app)],text=True)
 subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True)
 running=p/'running.command';running.write_text(text.replace('/usr/bin/false','/usr/bin/true'))
 r=run(running,'y\n');assert r.returncode!=0 and len(list(dest.glob('StudyGlass-backup.*')))==1
 # A failed final rename must restore the previous installation.
 mover=p/'mv';mover.write_text('#!/bin/bash\ncase "$1" in *studyglass-stage*) exit 1;; esac\nexec /bin/mv "$@"\n');mover.chmod(0o755)
 rollback=p/'rollback.command';rollback.write_text(text.replace('/bin/mv',shlex.quote(str(mover))))
 r=run(rollback,'y\n');assert r.returncode!=0 and app.exists(),r.stdout+r.stderr
 subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True)
 print('PASS: cancellation, hash mismatch, install, scoped quarantine removal, backup, running-app refusal, rollback')
