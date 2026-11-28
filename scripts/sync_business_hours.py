#!/usr/bin/env python3
"""Derive static schema and a shared calendar helper from the confirmed hours.

Schema.org has no recurring last-Saturday OpeningHoursSpecification. Publish
explicit dated exceptions for the current and following calendar year, plus the
perpetual written rule. Booking calculations work for every month, independently
of that static horizon. Regenerate dated schema at least annually.
"""
import argparse
import calendar
from copy import deepcopy
from datetime import date, datetime
from zoneinfo import ZoneInfo
import json
import hashlib
import re
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]


def derive_business(hours, business, *, year):
    """Project one verified calendar source into schema and explanatory text.

    ``year`` is explicit so tests can use fixtures without changing approved
    business records. Existing Saturday/appointment rules are preserved.
    """
    for key in ('regularOpen', 'regularClose', 'umugandaOpen', 'umugandaClose'):
        if not isinstance(hours.get(key), str) or not re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', hours[key]):
            raise ValueError('Opening hours require valid HH:MM values: ' + key)
    if hours['regularOpen'] >= hours['regularClose'] or hours['umugandaOpen'] >= hours['umugandaClose']:
        raise ValueError('Closing time must follow opening time')
    if not isinstance(hours.get('sundayByAppointment'), bool):
        raise ValueError('Sunday appointment setting must be boolean')
    business = deepcopy(business)
    business['openingHoursSpecification']=[{'@type':'OpeningHoursSpecification','dayOfWeek':['https://schema.org/'+d for d in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']],'opens':hours['regularOpen'],'closes':hours['regularClose']}]
    business['disambiguatingDescription']=(f"Monday–Saturday: {hours['regularOpen']}–{hours['regularClose']}. Ordinary Saturday visits do not require an appointment. On the last Saturday of every month (Umuganda), hours are {hours['umugandaOpen']}–{hours['umugandaClose']}, strictly by advance appointment."
        + (' Sunday: by appointment only; no fixed Sunday hours are published.' if hours['sundayByAppointment'] else ''))
    exceptions=[]
    for calendar_year in [year, year+1]:
        for month in range(1,13):
            last=date(calendar_year,month,calendar.monthrange(calendar_year,month)[1]);last=last.replace(day=last.day-(last.weekday()-5)%7)
            exceptions.append({'@type':'OpeningHoursSpecification','validFrom':last.isoformat(),'validThrough':last.isoformat(),'opens':hours['umugandaOpen'],'closes':hours['umugandaClose'],'description':'Umuganda (last Saturday): strictly by advance appointment.'})
    business['specialOpeningHoursSpecification']=exceptions
    return business


def derived_outputs(root=ROOT, *, year=None):
    """Return generated files without writing; use the same projection in CI."""
    root = Path(root)
    hours=json.loads((root/'_data/business-hours.json').read_text())
    business=json.loads((root/'_data/business.json').read_text())
    # contact-v2 owns official social destinations; business.json is their schema
    # projection, not a second editable set of profile URLs.
    social=json.loads((root/'_data/contact-v2.json').read_text())['social']
    if any(urlsplit(value).scheme != 'https' or not urlsplit(value).netloc for value in social.values()):
        raise ValueError('Official social destinations require absolute HTTPS URLs')
    business['sameAs']=list(social.values())
    business=derive_business(hours,business,year=year if year is not None else datetime.now(ZoneInfo('Africa/Kigali')).year)
    outputs={root/'_data/business.json':json.dumps(business,ensure_ascii=False,indent=2)+'\n',root/'assets/business-hours.js':(root/'_templates/business-hours.js').read_text().replace('{{hours}}',json.dumps(hours,separators=(',',':')))}
    # Version the new shared rules and controller together, so cached Phase 2
    # JavaScript cannot silently keep the old Saturday behavior after deployment.
    script_bytes = {'assets/business-hours.js': outputs[root/'assets/business-hours.js'].encode(), 'assets/forms.js': (root/'assets/forms.js').read_bytes()}
    for page in root.glob('booking*.html'):
        source = page.read_text()
        for url, data in script_bytes.items():
            digest = hashlib.sha256(data).hexdigest()[:10]
            source = re.sub(r'src="' + re.escape(url) + r'(?:\?v=[^"]*)?"', f'src="{url}?v={digest}"', source)
        outputs[page] = source
    return outputs


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    outputs=derived_outputs()
    for path,output in outputs.items():
        if args.check:
            if not path.exists() or path.read_text()!=output:raise SystemExit('Hours derivation stale: '+str(path.relative_to(ROOT)))
        else:path.write_text(output)
    print('PASS: confirmed hours/calendar helper and dated Umuganda schema are synchronized.' if args.check else 'Generated shared hours/calendar helper and 24 dated Umuganda exceptions.')


if __name__=='__main__':main()
