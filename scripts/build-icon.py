#!/usr/bin/env python3
"""Export the selected PlanLess artwork at standard macOS icon sizes."""
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'design/planless-icon/source.png'
resources = ROOT / 'Resources'
iconset = resources / 'AppIcon.iconset'
iconset.mkdir(exist_ok=True)
def resize(size, output):
    subprocess.run(['sips', '-z', str(size), str(size), str(source), '--out', str(output)], check=True, stdout=subprocess.DEVNULL)
resize(1024, resources / 'AppIcon.png')
for size in [16, 32, 128, 256, 512]:
    resize(size, iconset / f'icon_{size}x{size}.png')
    resize(size * 2, iconset / f'icon_{size}x{size}@2x.png')
subprocess.run(['iconutil', '-c', 'icns', str(iconset), '-o', str(resources / 'AppIcon.icns')], check=True)
print('Exported PlanLess PNG, ten standard icon sizes, and ICNS')
