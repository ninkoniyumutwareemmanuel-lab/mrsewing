#!/usr/bin/env python3
"""Prepare a human review or locally publish its explicitly approved PDF.

No browser upload, commit, push or deployment is performed by this command.
Unapproved PDF/review files stay outside this repository.
"""
import argparse
import json
from pathlib import Path
import subprocess
from policy_documents import ROOT, REGISTRY, publish_document, receive_document, activate_received_document, activation_review_template, review_template, validate_registry


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
    receive = commands.add_parser('receive', help='Register an owner-approved uploaded PDF for staging review without inventing its official effective date.')
    receive.add_argument('--pdf', required=True)
    receive.add_argument('--review', required=True)
    receive.add_argument('--write', action='store_true')
    activate = commands.add_parser('activate', help='Activate the same received version only after a confirmed actual official publication event and fresh operational reconciliation.')
    activate.add_argument('--version', required=True)
    activate.add_argument('--review', required=True)
    activate.add_argument('--write', action='store_true')
    activation_prepare = commands.add_parser('prepare-activation', help='Prepare operational/publication review while preserving existing content approval.')
    activation_prepare.add_argument('--version', required=True)
    activation_prepare.add_argument('--official-publication-date', required=True)
    activation_prepare.add_argument('--review-out', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'check':
            validate_registry()
            print('PASS: approved policy document registry and files; no publication performed.')
            return
        staging_branch()
        if args.command == 'prepare-activation':
            target = outside(args.review_out, 'pending activation review record')
            record = activation_review_template(args.version, args.official_publication_date)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('x', encoding='utf-8') as stream:
                stream.write(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
            print('Activation review created at ' + str(target) + '. Existing content approval is retained; actual publication and operational reconciliation are still pending.')
            return
        if args.command == 'activate':
            review = json.loads(outside(args.review, 'activation review record').read_text())
            record = activate_received_document(args.version, review, write=args.write)
            print(('RECEIVED PDF ACTIVATED LOCALLY' if args.write else 'ACTIVATION DRY RUN PASSED — no repository files changed') + ': ' + record['publishedPath'])
            return
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
        record = (receive_document if args.command == 'receive' else publish_document)(pdf, review, write=args.write)
        label = 'APPROVED PDF REVIEW REGISTERED LOCALLY' if args.command == 'receive' else 'APPROVED PDF WRITTEN LOCALLY'
        print((label if args.write else 'DRY RUN PASSED — no repository files changed') + ': ' + record['publishedPath'])
        if args.write:
            print('Registry: ' + REGISTRY + '. Rebuild, test and inspect staging. This command did not commit, push or deploy.')
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from error


if __name__ == '__main__':
    main()
