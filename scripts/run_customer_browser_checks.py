#!/usr/bin/env python3
"""Run independent mocked browser checks and expose exact failures in CI summary.

Every failed check still fails the job; other checks continue to provide useful
diagnostics. Only test output/synthetic data is written, never credentials.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/browser-checks'
CHECKS = [
    ('homepage', 'tests/r59_tailoring_browser.cjs', 'artifacts/r59-browser'),
    ('terms', 'tests/terms_popup_browser.cjs', 'artifacts/r55-terms'),
    ('fabric', 'tests/recovery-fabric-browser.cjs', 'artifacts/recovery-fabric'),
    ('legacy-journeys', 'tests/recovery_journeys.cjs', 'artifacts/recovery-journeys'),
    ('guided-dialog', 'tests/tailoring_request_dialog.cjs', 'artifacts/tailoring-dialog'),
    ('custom-tailoring', 'tests/custom_tailoring_landing.cjs', 'artifacts/custom-tailoring'),
    ('gallery', 'tests/customer_gallery_browser.cjs', 'artifacts/gallery-experience'),
    ('shop', 'tests/shop_customer_experience.cjs', 'artifacts/shop-customer'),
    ('home-about', 'tests/home_about_customer_experience.cjs', 'artifacts/home-about'),
    ('architecture-homepage', 'tests/architecture_homepage.cjs', 'artifacts/architecture-homepage'),
    ('services', 'tests/service_landings_browser.cjs', 'artifacts/services'),
    ('navigation', 'tests/customer_navigation.spec.cjs', 'artifacts/navigation'),
    ('ads-sitelinks', 'tests/final_release_sitelinks.cjs', 'artifacts/ads-sitelinks'),
    ('tracking', 'tests/tracking_browser.cjs', 'artifacts/tracking'),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    summary = Path(os.environ['GITHUB_STEP_SUMMARY']) if os.environ.get('GITHUB_STEP_SUMMARY') else OUT / 'summary.md'
    results = []
    for name, script, artifacts in CHECKS:
        env = dict(os.environ)
        env['REVIEW_ARTIFACTS'] = artifacts
        env['RECOVERY_EVIDENCE_DIR'] = artifacts
        base_url = env.get('REVIEW_BASE_URL') or env.get('BASE_URL') or 'http://127.0.0.1:8020'
        env.setdefault('BASE_URL', base_url)
        env.setdefault('REVIEW_BASE_URL', base_url)
        start = time.monotonic()
        try:
            result = subprocess.run(['node', script], cwd=ROOT, env=env, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240)
            code, output = result.returncode, result.stdout
        except subprocess.TimeoutExpired as error:
            code = 124
            output = (error.stdout or b'').decode() if isinstance(error.stdout, bytes) else (error.stdout or '')
            output += '\nBrowser check exceeded 240 seconds.\n'
        (OUT / (name + '.log')).write_text(output)
        row = {'name': name, 'script': script, 'exitCode': code,
               'status': 'PASS' if code == 0 else 'FAIL', 'seconds': round(time.monotonic() - start, 2)}
        results.append(row)
        print(f"{row['status']}: {name} ({row['seconds']}s)", flush=True)
        with summary.open('a') as stream:
            stream.write(f"\n### {name}: {row['status']}\n\n`node {script}` — exit {code}\n")
            if code:
                stream.write('\n```text\n' + output[-7000:].replace('```', "'''") + '\n```\n')
        (OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    return int(any(row['exitCode'] != 0 for row in results))


if __name__ == '__main__':
    sys.exit(main())
