#!/usr/bin/env bash
# Skill contract + helper tests (run before Cowork marketplace push).
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m pytest tests/ -q "$@"
