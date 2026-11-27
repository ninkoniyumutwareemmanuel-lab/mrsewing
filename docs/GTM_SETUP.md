# Existing Google Tag Manager container — setup and verification

Prepared for the owner's **GTM-WHR49M4D**, native Google Ads account tag **AW-18587874562**, using the six exact conversion labels supplied on26November2026. This is a repository-prepared import draft, not a new container, actual account export, published workspace or receipt certificate. No advertising account was modified.

## Files and source ownership

- Authoritative website mapping: `_data/advertising-measurement.json`.
- Deterministic draft generator: `scripts/build_tracking_workspace.py`.
- Internal import file: `.github/tracking/gtm-workspace.json`.
- Local contract tests: `tests/tracking_workspace.py`.

Run `python scripts/build_tracking_workspace.py`, then `python scripts/build_tracking_workspace.py --check` and `python tests/tracking_workspace.py`. The generated JSON is kept outside the public artifact; it contains no access token, private account ID or customer information. Unknown internal numeric GTM account/container/workspace IDs are deliberately not fabricated. The operator chooses the existing destination during import.

## Import without overwriting another workspace

1. Sign in to the owner's existing **GTM-WHR49M4D** web container. Export and preserve its current workspace/version first. Inspect existing tags, pending edits, consent setup and environments; the repository does not reveal them.
2. Compare native Google tag/Conversion Linker and each existing Ads conversion tag against this draft. If equivalent tags or triggers already exist, reuse/reconcile them instead of adding duplicate firing paths. In particular, do not add both a direct Google Ads conversion implementation and a duplicate GTM tag or duplicate GA4 primary import.
3. In **Admin → Import Container**, choose `.github/tracking/gtm-workspace.json` and an isolated review workspace in this existing container. Choose **Merge**, never overwrite. Review every addition/conflict. Do not blindly rename an existing equivalent `MR Sewing — …` tag and thereby duplicate it. Do not alter unrelated tags or edits. A prior imported MR Sewing setup should be updated after comparison, not imported a second time as another complete copy.
4. Verify that GTM accepts the JSON and native tag templates. Actual GTM import/Preview access is unavailable here; the local tests validate structure/references/privacy conditions, not Google's importer or account publication. If the UI rejects a native-template field, preserve the current workspace and recreate the settings below through its native editor rather than replacing an unrelated configuration.
5. Preview and validate consent/events using an authorized isolated test setup. Staging must never send production advertising events; the website intentionally blocks production vendor transport on staging. Use synthetic intercepted local tests for website logic, then a separately authorized official-domain test/diagnostic procedure for actual receipt. Do not lift staging guards merely to make tags appear in Preview.
6. Publish only after the website release gates and account-side review/testing pass. Publishing the container is a distinct action; a website commit or container ID does not publish it. Campaign budgets/status/targeting remain unchanged.

## Required runtime contract and tags

The website initializes `window.dataLayer` once and starts the existing GTM container only after fresh measurement consent in an allowed production context. Standard `gtm.start` and `gtm.js` initialization is required; the supplied two-line asynchronous script reference alone is not a complete consent-aware bootstrap. No pre-consent or no-JavaScript advertising iframe is added. The site remains usable if consent is rejected or a tag request fails.

Before container load, the website queues Consent Mode defaults denied for `ad_storage`, `ad_user_data`, `ad_personalization` and `analytics_storage`. Fresh optional measurement acceptance grants only the configured Google measurement purposes; **ad_personalization and analytics_storage remain denied**. GA4 has no known measurement ID and is not created. Enhanced conversions, advanced matching and customer uploads remain disabled. Global data-layer settings additionally disable enhanced conversions/personalization and enable ads-data redaction. Do not change these merely to increase match quality.

The prepared native Google tag (`googtag`, `tagId=AW-18587874562`) and native Conversion Linker (`gclidw`, cross-domain linking off) fire only on **`mr_measurement_ready`**, once per document. They are not All Pages tags. If the container already has valid equivalent tags, reconcile/reuse them rather than duplicating them.

Every trigger requires:

- Exact matching custom event name.
- Data Layer Variable `mr_measurement_allowed` equal to `true`.
- Data Layer Variable `mr_consent_google` equal to `true`.
- Page Hostname matching `^(mrsewingfashion\.com|www\.mrsewingfashion\.com)$`.
- Additional native tag consent checks for `ad_storage` and `ad_user_data`.

No additional check requires personalization or analytics consent to be granted. Declining either purpose must not be bypassed. The website-side privacy/safe-context gate remains necessary; GTM host filters alone cannot sanitize an arbitrary URL or form field.

| Owner conversion action | Website event | Exact Ads conversion label | Active condition | Recommended account role |
|---|---|---|---|---|
| Whatsap Contact | `whatsapp_contact_click` | `zHM6CL_CjsAdEILqsZ9F` | Deliberate official-business WhatsApp contact click, not generic sharing or redirect | Primary initially, explicitly contact intent |
| Click to call | `website_call_click` | `tT1uCMLCjsAdEILqsZ9F` | Deliberate official telephone link click | Secondary initially |
| Book appointment | `appointment_confirmed` | `_QXPCMXCjsAdEILqsZ9F` | **Paused, no trigger:** current website requests do not confirm appointments | Inactive; Primary only after real confirmation infrastructure |
| Get directions | `directions_click` | `55vTCMjCjsAdEILqsZ9F` | Deliberate click on the verified business directions link | Secondary |
| Request quote | `quote_request_success` | `ZHLFCMvCjsAdEILqsZ9F` | Positive supported quotation-provider result, once; not opening/reviewing/failure | Primary |
| Submit lead form | `lead_form_success` | `p9FJCM7CjsAdEILqsZ9F` | Positive eligible non-quotation enquiry result, once | Primary |

All native Ads conversion tags (`awct`) use conversion ID **18587874562** and `transactionId={{MR Sewing — event_id}}`. Quote and general lead must be mutually exclusive for one accepted enquiry. No value/currency/product/customer-data/enhanced-conversion variable is supplied. The owner's existing temporary USD1 action value is not revenue, profit, a purchase or an advertising fee; no return-on-ad-spend calculation can be inferred from it.

Data Layer Variables use Version2 and read only `event_id`, `mr_measurement_allowed`, `mr_consent_google`. No form payload, customer contact, measurement, private design text, raw query, referrer or WhatsApp message is a conversion parameter. Supporting design/fabric/journey events are not conversion triggers in this draft. No GA4 event tag, Purchase tag, automatic form-submit conversion or impression-based directions/call conversion exists.

## Exact manual fallback if an import template needs UI review

Create/reconcile these entries in the existing review workspace using native GTM editors:

1. Three Data Layer Variables, Version2: the keys above. Enable built-in Page Hostname.
2. Six guarded Custom Event triggers: readiness plus five currently active conversion events. Do not create an active appointment trigger.
3. One Google tag for AW-18587874562 and one Conversion Linker using guarded readiness trigger and consent checks.
4. Six native Google Ads Conversion Tracking tags with the exact ID/labels in the table and event ID as Transaction ID. Pause Book appointment and leave it without a firing trigger. Attach each other tag to its matching guarded event. Keep enhanced conversions and product reporting off.
5. In Google Ads, review Primary/Secondary, Count One where appropriate for leads/contact intent, account-default versus PMax-specific goals and duplicate GA4 imports. Keep only the intended Contact goal and true request goals in the campaign as approved. Do not change USD1.50 daily budget, bidding, targeting or activation in this task.

## Verification checklist — not account receipt proof

- Reject consent: no vendor load or conversion; necessary services still work.
- Accept fresh permitted consent: one container initialization/readiness event; no unrelated container loaded.
- Repeated click/iframe/review/refresh cannot duplicate one accepted request event. `event_id` supplies the same transaction key for a given emitted action.
- Generic social sharing, page views, failed requests, validation errors and unconfirmed appointment preferences produce no successful enquiry/appointment conversion.
- One positive eligible quotation maps only to Request quote; one eligible non-quotation enquiry maps only to Submit lead form.
- Official WhatsApp/telephone/directions clicks use only their corresponding action; they do not claim conversation, arrival or sale.
- Review actual Tag Assistant/container tags and Google Ads diagnostics in authorized testing; inspect consent, event payload, deduplication and receipt in the correct account. No fabricated purchases or test leads into live campaign reporting.
- Preserve existing Meta infrastructure; these native Ads tags do not send Meta or server events. No CAPI token is included.

## Documentation evidence and limits

Official web guides were attempted at `developers.google.com/tag-platform/tag-manager/web`, `developers.google.com/tag-platform/security/guides/consent`, and Google Help6105160/6106960; this managed environment returned CONNECT403, so their current page contents were **not** claimed read.

The official Google API client discovery document at `https://raw.githubusercontent.com/googleapis/google-api-python-client/main/googleapiclient/discovery_cache/documents/tagmanager.v2.json` **was read** on27November2026. It supports the container/tag/trigger/variable relationships and the `TagConsentSetting.consentType` LIST-of-Parameter shape used here. Its API enum spelling differs from the export-format enum spelling; it is not Google's UI import validator or proof that this prepared native-template draft was imported. Native tag-template settings, actual workspace conflicts/publication and advertising receipt still require account-side validation. Sanitized access/schema evidence is in the internal review package, not public website assets.
