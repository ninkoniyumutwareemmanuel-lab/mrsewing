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
# Refresh shared business projections before any page/schema consumer. --check
# validates the same dependencies without rewriting sources or generated pages.
for script in ['sync_business_hours.py', 'sync_business_schema.py', 'build_technical_assets.py', 'build_tracking_workspace.py', 'build_customer_release.py', 'build_customer_information.py', 'build_source_seo.py', 'build_homepage.py', 'build_contact.py', 'build_about.py', 'build_collections.py', 'build_journey.py', 'build_completion.py', 'build_commerce.py', 'build_clean_urls.py', 'build_public_routes.py', 'build_release_marker.py']:
    subprocess.run([sys.executable, str(ROOT/'scripts'/script), *(['--check'] if args.check else [])], cwd=ROOT, check=True)
# Fail staging builds if legacy URL redirects point to the wrong page or leak to canonical URLs.
subprocess.run([sys.executable, str(ROOT/'tests'/'seo_legacy_redirects.py')], cwd=ROOT, check=True)
subprocess.run([sys.executable, str(ROOT/'tests'/'seo_core_services.py')], cwd=ROOT, check=True)
# An opt-in, branch-restricted review deployment. No project/global configuration
# changes; Main cannot build this review-mode configuration.
subprocess.run([sys.executable, str(ROOT/'scripts'/'build_rebuild_preview.py'), *(['--check'] if args.check else [])], cwd=ROOT, check=True)
