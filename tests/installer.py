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
 text=text.replace('APP_DIR="${HOME}/Applications"','APP_DIR='+shlex.quote(str(dest))).replace('/usr/bin/curl',shlex.quote(str(curl))).replace('/usr/bin/open',shlex.quote(str(opener)))
 text=text.replace('"$LSREGISTER"','/usr/bin/true').replace('/usr/bin/pluginkit','/usr/bin/true')
 # Stub process enumeration, identity lookup and signals; never touch the user's app.
 alive=p/'alive';mode=p/'mode';signals=p/'signals'
 pg=p/'pgrep';pg.write_text('#!/bin/bash\n[ -f '+shlex.quote(str(alive))+' ] && echo 424242\n');pg.chmod(0o755)
 ps=p/'ps';ps.write_text('#!/bin/bash\n[ -f '+shlex.quote(str(alive))+' ] || exit 1\ncat '+shlex.quote(str(p/'process-path'))+'\n');ps.chmod(0o755)
 killer=p/'kill';killer.write_text('#!/bin/bash\necho "$1" >> '+shlex.quote(str(signals))+'\nm=$(cat '+shlex.quote(str(mode))+')\nif [ "$m" = term ] || { [ "$m" = force ] && [ "$1" = -KILL ]; }; then rm -f '+shlex.quote(str(alive))+'; fi\n');killer.chmod(0o755)
 text=text.replace('/usr/bin/pgrep',shlex.quote(str(pg))).replace('/bin/ps',shlex.quote(str(ps))).replace('/bin/kill',shlex.quote(str(killer))).replace('/bin/sleep 1','/usr/bin/true')
 script=p/'install.command' ;script.write_text(text)
 def run(script,answer):return subprocess.run(['/bin/bash',str(script)],input=answer,text=True,capture_output=True)
 r=run(script,'n\n');assert r.returncode==0 and not dest.exists(),r.stderr
 bad=p/'bad.command';bad.write_text(text.replace(hashlib.sha256(archive.read_bytes()).hexdigest(),'0'*64))
 r=run(bad,'y\n');assert r.returncode!=0 and not dest.exists(),r.stderr
 r=run(script,'y\n');assert r.returncode==0,r.stdout+r.stderr
 app=dest/'Study Glass.app';assert app.exists() and log.exists()
 subprocess.run(['/usr/bin/xattr','-w','com.apple.quarantine','0083;00000000;Test;',str(app)],check=True)
 r=run(script,'y\n');assert r.returncode==0,r.stdout+r.stderr
 assert not list(dest.glob('StudyGlass-backup.*/Study Glass.app'))
 assert len(list(dest.glob('StudyGlass-backup.*/StudyGlass-preserved.zip')))==1
 assert 'com.apple.quarantine' not in subprocess.check_output(['/usr/bin/xattr',str(app)],text=True)
 subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True)
 (p/'process-path').write_text(str(app/'Contents/MacOS/StudyGlass')+'\n')
 for how,expected in [('term',['-TERM']),('force',['-TERM','-KILL'])]:
  mode.write_text(how);alive.touch();signals.unlink(missing_ok=True)
  r=run(script,'y\n');assert r.returncode==0,r.stdout+r.stderr
  assert signals.read_text().splitlines()==expected and not alive.exists()
 # Cancellation or a bad download never signals an app.
 alive.touch();signals.unlink(missing_ok=True)
 assert run(script,'n\n').returncode==0 and not signals.exists()
 assert run(bad,'y\n').returncode!=0 and not signals.exists()
 mode.write_text('stuck');r=run(script,'y\n');assert r.returncode!=0 and app.exists()
 signals.unlink();(p/'process-path').write_text('/usr/bin/unrelated\n')
 r=run(script,'y\n');assert r.returncode==0 and not signals.exists()
 alive.unlink()
 # Legacy backup apps are archived and removed; unrelated apps are untouched.
 legacy=dest/'StudyGlass-backup.legacy'/'Study Glass.app';legacy.parent.mkdir()
 subprocess.run(['ditto',str(app),str(legacy)],check=True)
 r=run(script,'y\n');assert r.returncode==0,r.stdout+r.stderr
 assert not legacy.exists() and list(legacy.parent.glob('*.zip'))
 # A failed final rename must restore the previous installation.
 mover=p/'mv';mover.write_text('#!/bin/bash\ncase "$1" in *studyglass-stage*) exit 1;; esac\nexec /bin/mv "$@"\n');mover.chmod(0o755)
 rollback=p/'rollback.command';rollback.write_text(text.replace('/bin/mv',shlex.quote(str(mover))))
 r=run(rollback,'y\n');assert r.returncode!=0 and app.exists(),r.stdout+r.stderr
 subprocess.run(['/usr/bin/codesign','--verify','--deep','--strict',str(app)],check=True)
 print('PASS: cancellation, hash mismatch, install, scoped quarantine removal, backup, automatic termination, forced termination, cancellation safety, unrelated process protection, stuck-process refusal, rollback')
