#!/usr/bin/env python3
"""Build/check the document viewer and approved PDFs; never emit draft PDFs."""
import argparse
from policy_documents import ROOT, outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = outputs()
    for path, value in files.items():
        content = value if isinstance(value, bytes) else value.encode('utf-8')
        if args.check:
            if not path.is_file() or path.read_bytes() != content:
                raise SystemExit('Stale policy document output: ' + str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    print('PASS: policy document registry, viewer assets and approved PDF outputs ' + ('synchronized' if args.check else 'generated'))


if __name__ == '__main__':
    main()
