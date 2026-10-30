#!/usr/bin/env python3
"""Rebuild shared pages, Collections V3, Customer Journey, canonical URLs and SEO outputs."""
import argparse
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--check', action='store_true')
args = p.parse_args()
for script in ['build_customer_information.py', 'build_source_seo.py', 'build_homepage.py', 'build_contact.py', 'build_about.py', 'build_collections.py', 'build_journey.py', 'build_completion.py', 'build_clean_urls.py', 'build_public_routes.py']:
    subprocess.run([sys.executable, str(ROOT/'scripts'/script), *(['--check'] if args.check else [])], cwd=ROOT, check=True)
