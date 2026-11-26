# Portable payload-test artifact repair — 26November2026

Baseline `bb89612a`, implementation branch `phase1/customer-journey-repairs`; Main untouched. Isolated Node22 test runtime installed outside repository: **v22.23.5**, `/workspace/tools/node22-recovery/node_modules/node/bin/node`.

## Confirmed finding

`tests/shared-fabric-validation.mjs` wrote its synthetic payload to absolute `/workspace/review/shared-fabric-journey-2026-11-13/example-backend-enquiry.json`. This works in the Codex workspace (owned by uid1000 agent) but is not portable to an ordinary GitHub Ubuntu runner working in its checkout below `/home/runner/work`. Creating `/workspace` under the root filesystem is not a permitted assumption. The other five commands in the security step have no absolute artifact writes.

The actual raw CI error log remains unavailable to this subtask. This is an independently confirmed portability defect and a strongly supported explanation for failure on the second command, not a claim that the remote traceback was retrieved. No Node22 compatibility failure was reproduced: all six tests pass under Node22 before and after the artifact repair in this writable workspace.

## Reproduction and focused repair

A temporary fixture ran the complete original shared-fabric test with unchanged assertions/mocked provider/import targets and mapped only its artifact destination to a root-owned inaccessible path. Under ordinary uid1000 it completed the payload checks and failed at `fs.mkdirSync` with **EACCES**, exit1. `original-permission-fixture.log` preserves that stack. It did not write outside the workspace.

Repaired only the artifact destination: `process.env.REVIEW_ARTIFACTS || path.join('artifacts','shared-fabric')`, then `path.join` for the filename; added Node built-in path import. The resulting default location is writable under the checkout. An explicit override remains supported. No validator, source business data, security assertion, mock, payload rule or submission integration changed. A byte-for-byte comparison after reversing those two path-only edits confirms the rest of the test source is identical; assertion count unchanged.

## Actual results

**PASS all six Node22 security commands:** multi-design-validation, shared-fabric-validation, quotation-completion-validation, recovery_fabric_validation, shop-draft-request-gate, recovery_source_boundary. Per-command exit codes/output are in `repaired-results.json` and `repaired-*.log`.

**PASS default relative output:** `artifacts/shared-fabric/example-backend-enquiry.json` exists and contains the full synthetic example with access_key removed. It is an ignored test artifact, not a published customer record.

**PASS REVIEW_ARTIFACTS override:** reran the complete shared-fabric test with output `/workspace/recovery/2026-11-26/node22-ci/env-output`; sample exists with no access_key. `environment-override.log` preserves the pass.

No real customer request, message, call, payment or provider submission was sent. The parent must rerun/verify the exact remote staging CI after the authorized commit; this local evidence does not establish remote CI success.
