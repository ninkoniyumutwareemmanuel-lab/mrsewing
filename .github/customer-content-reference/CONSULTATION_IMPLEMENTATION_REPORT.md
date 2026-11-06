# Mr Sewing Fashion — consultation form implementation report

6November2026,Africa/Kigali. Staging only,phase1/customer-journey-repairs.

##Completed

- BookConsultation has exactly3real service options:Custom Tailoring & Suits,Clothing Alterations & Repairs,Garment Care & Cleaning. Global5service navigation anddedicatedVIP/Mobile pages/forms unchanged.
- Required workshop/customer-location/phoneWhatsApp preference. Customer visits conditionally require Hotel/Home/Office orWorkplace/Other andaddress;name/directions optional. Exact owner-approved MobileConsultationNotice displayed andincluded inreview/email. Workshop/phone do not submit irrelevant address fields.
- Required name,phone,service,method,date,time,service requirements andunchecked Terms/Privacy;optionalemail/additional information. Normal schedule uses retained _data/business.json:MonSat09–17Kigali,lastSaturday12–17byadvanceappointment,Sundaybyappointment/no fixedpublished hours. Dates/times inAfrica/Kigali;pastdates/times rejected. Noavailable-slot/fee/appointment promise.
- Dynamic garments/design status/manualoptionalWhatsApp forCustom;repair garment/details/inspection caveat;care garments/quantity/condition/assessment caveat. Inactive controls disabled/excluded frompayload. Common details retained onservice changes;service descriptions restored whenswitchingback.
- Existing review/edit,freeWeb3Forms action/key/recipient configuration preserved. All relevant fields andnotice inpayload. Request Submitted forReview appears only after positive provider response andexplicitly does not confirm appointment/service/order/quotation. Failures retain data. Noautomatic WhatsApp send oruploads.

##Branch safety andpreservation

Atstart,dev81efee6 was62commits behind remote main967401e4f7550fcfb58c3e9b06b01e90898f9e3b withno localchanges. Inspected differences:main’s14priority-page indexing policy andgenerated metadata. Fast-forwarded dev only;no main update/merge into main. Source andendpoint preservation checks confirm unchanged key/action,homepage,Contact,VIP/Mobile dedicated information/forms,prices,private-feature setting,headers,robots andredirects. Noimages,CSS,paidservices,DNS,hosting,credentials orproduction settings changed.

The fullbuild also normalised generated metadata placement onnon-priority pages under main’s existing14page noindex policy;no new indexing policy orcustomer-visible content/design change. Four older regression files had72page/indexability expectations superseded bymain;updated to14/accessiblebutnoindex expectations rather than reverting production’s policy. All16Python suites pass.

##Files

Main sources:scripts/consultation_form.py(new),_templates/consultation.js(new),scripts/customer_site.py(component integration/consultation3service selector),_templates/customer-site.js(scoped validation/payload guard toavoid stale quotation context),generatedassets/consultation.js,assets/customer-site.js,booking.html,booking/index.html. tests/consultation-booking.spec.cjs(new);v1-email-fallback helper updated fornew required fields;4index-policy regression expectations aligned withmain. Dated source reference2026-11-06-03,brief andthisreport preserve owner decisions/history. Other generatedHTML differences are metadata ordering/indexing alignment fromfullbuild,not changes to dedicated services. Exact delivery inventory:changed-files.txt aftercommit.

##Tests

|Check|Result|Scope|
|---|---|---|
|Production build and --check parity|PASS|Generated source/output consistency;Node syntax/Pythoncompile pass|
|16Python regression suites|PASS|Includes route/SEO/metadata/assets/approved-content preservation withmain14page policy|
|Consultation service/method/location combinations|PASS|36mocked successful combinations at390/1440:all3services,workshop/phone,andHotel/Home/Workplace/Other visits|
|Payload review/edit|PASS|Correct active fields,service/method/contact/date/time/notice;inactive address/other-service fields absent;editpreserves details|
|Validation|PASS|Required name/phone/date/time/requirements/address/quantity andunchecked consent;pastKigali dates/times,normalhours,Umuganda,lastSaturday andSundayqualification|
|Service switching|PASS|Commoninformation retained;service-specific description restored onreturn|
|Optional manual design photos|PASS|CustomYesonly;unchecked same-pageTerms modal;approvedWhatsApp250787411501;popup intercepted;no realmessage/upload|
|Provider failures andduplicate protection|PASS|HTTP/rejectedresponses never show success;inputs retained;double-click yieldsone mockrequest|
|Mobile/desktop/accessibility|PASS|320/390/768/1440nooverflow;2axe WCAG2.2AA-tag scans no reported violations;native labelled controls;not fullATcertification|
|Existing email-onlyflows|PASS|7journeys plus3failuremodes retested withmockprovider|
|Navigation|PASS|Contact→BookConsultation,mobilehamburger/Escape,desktop5service header,breadcrumbContact andlegacybooking.html redirect|
|Web3Forms key/action preservation|PASS|Exact equality against inspectedmainbaseline;no key/recipient/provider setting changed|
|Real business inbox receipt|NOT TESTED|Mock tests do not prove email delivery;provider/inbox access unavailable,no realcustomerdata/messages sent|
|Deployed browser interactions|BLOCKED|Managed proxyCONNECT403 before stagingorigin;local tests separate fromCloudflare publication evidence|

##Staging delivery

Exact commit,Cloudflare status,deploymentID andpreviewURL recorded aftercommit/push inexternal finalreviewcopy. No claim that Gitpush alone proves publication orprovider delivery. Existing /booking/ and/booking.html route contract retained forContact/GoogleBusinessProfile;profile itself not modified.

##Owner review

Screenshots(local Chromium):[Mobile form](/workspace/artifacts/consultation/form-390.png),[Desktop form](/workspace/artifacts/consultation/form-1440.png),[Mobile review](/workspace/artifacts/consultation/review-390.png),[Desktop review](/workspace/artifacts/consultation/review-1440.png). Actualdevices/Safari/Firefox andliveinbox delivery notverified. NoGoogleBusinessProfile settings changed. No calendarbackend orautomaticconfirmed availability.

Stop afterstaging. Do notpublish production withoutnew explicit approval.
