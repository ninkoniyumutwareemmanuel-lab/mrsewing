"""Staging CI must verify the event commit without mutating a moving branch."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'.github/workflows/r59-staging-build.yml').read_text()
assert 'branches: [phase1/customer-journey-repairs]' in s
assert "if: github.ref == 'refs/heads/phase1/customer-journey-repairs'" in s
assert 'contents: read' in s and 'contents: write' not in s
assert 'persist-credentials: false' in s
assert not re.search(r'^\s+ref: phase1/',s,re.M),'Checkout must use event SHA'
assert not re.search(r'\bgit (?:push|commit|reset|merge)\b',s),'CI is verification-only'
assert 'run: python scripts/import_owner_terms_v1_1.py' not in s
assert 'python scripts/build_site.py --check' in s and 'git diff --exit-code' in s
assert 'concurrency:' in s and 'cancel-in-progress: true' in s
print('PASS event-commit/staging-only/read-only CI; no automatic PDF activation or generated-push race')
