#!/usr/bin/env python3
"""Rebuild all V2 component consumers, then clean URLs. Legacy layouts unchanged."""
import argparse
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--check', action='store_true')
args = p.parse_args()
for script in ['build_homepage.py', 'build_contact.py', 'build_clean_urls.py']:
    subprocess.run([sys.executable, str(ROOT/'scripts'/script), *(['--check'] if args.check else [])], cwd=ROOT, check=True)
