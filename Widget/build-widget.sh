#!/bin/zsh
# Kept for compatibility: build and sign app + extension together.
set -euo pipefail
cd "${0:A:h}/.."
exec python3 scripts/build.py "$@"
