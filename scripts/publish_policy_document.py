#!/usr/bin/env python3
"""Prepare a human review or locally publish its explicitly approved PDF.

No browser upload, commit, push or deployment is performed by this command.
Unapproved PDF/review files stay outside this repository.
"""
import argparse
import json
from pathlib import Path
import subprocess
from policy_documents import ROOT, REGISTRY, publish_document, review_template, validate_registry


def outside(value, label):
    path = Path(value).expanduser().resolve()
    if path.is_relative_to(ROOT.resolve()):
        raise ValueError('Keep the ' + label + ' outside the deployed repository.')
    return path


def staging_branch():
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'phase1/customer-journey-repairs':
        raise ValueError('Document publication is restricted to phase1/customer-journey-repairs; main is not authorized.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('check', help='Validate current registry, approved files and source reconciliation.')
    prepare = commands.add_parser('prepare', help='Create an unapproved review record outside the repository.')
    prepare.add_argument('--pdf', required=True)
    prepare.add_argument('--version', required=True)
    prepare.add_argument('--effective-date', required=True)
    prepare.add_argument('--review-out', required=True)
    publish = commands.add_parser('publish', help='Validate approved replacement; dry-run unless --write is supplied.')
    publish.add_argument('--pdf', required=True)
    publish.add_argument('--review', required=True)
    publish.add_argument('--write', action='store_true', help='Copy immutable approved PDF and update registry locally on staging.')
    args = parser.parse_args()
    try:
        if args.command == 'check':
            validate_registry()
            print('PASS: approved policy document registry and files; no publication performed.')
            return
        staging_branch()
        pdf = outside(args.pdf, 'PDF review copy')
        if args.command == 'prepare':
            target = outside(args.review_out, 'pending review record')
            record = review_template(pdf, args.version, args.effective_date)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('x', encoding='utf-8') as stream:
                stream.write(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
            print('Review template created at ' + str(target) + '. It is pending and cannot be published until genuinely approved.')
            return
        review_path = outside(args.review, 'review record')
        review = json.loads(review_path.read_text())
        record = publish_document(pdf, review, write=args.write)
        print(('APPROVED PDF WRITTEN LOCALLY' if args.write else 'DRY RUN PASSED — no repository files changed') + ': ' + record['publishedPath'])
        if args.write:
            print('Registry: ' + REGISTRY + '. Rebuild, test and inspect staging. This command did not commit, push or deploy.')
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from error


if __name__ == '__main__':
    main()
