#!/usr/bin/env python3
"""Derive static schema and a shared calendar helper from the confirmed hours.

Schema.org has no recurring last-Saturday OpeningHoursSpecification. Publish
explicit dated exceptions for the current and following calendar year, plus the
perpetual written rule. Booking calculations work for every month, independently
of that static horizon. Regenerate dated schema at least annually.
"""
import argparse
import calendar
from datetime import date, datetime
from zoneinfo import ZoneInfo
import json
import hashlib
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    hours=json.loads((ROOT/'_data/business-hours.json').read_text())
    business=json.loads((ROOT/'_data/business.json').read_text())
    business['openingHoursSpecification']=[{'@type':'OpeningHoursSpecification','dayOfWeek':['https://schema.org/'+d for d in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']],'opens':hours['regularOpen'],'closes':hours['regularClose']}]
    business['disambiguatingDescription']='Monday–Saturday: 09:00–17:00. Ordinary Saturday visits do not require an appointment. On the last Saturday of every month (Umuganda), hours are 12:00–17:00, strictly by advance appointment. Sunday: by appointment only; no fixed Sunday hours are published.'
    exceptions=[]
    kigali_year = datetime.now(ZoneInfo('Africa/Kigali')).year
    for year in [kigali_year, kigali_year+1]:
        for month in range(1,13):
            last=date(year,month,calendar.monthrange(year,month)[1]);last=last.replace(day=last.day-(last.weekday()-5)%7)
            exceptions.append({'@type':'OpeningHoursSpecification','validFrom':last.isoformat(),'validThrough':last.isoformat(),'opens':hours['umugandaOpen'],'closes':hours['umugandaClose'],'description':'Umuganda (last Saturday): strictly by advance appointment.'})
    business['specialOpeningHoursSpecification']=exceptions
    outputs={ROOT/'_data/business.json':json.dumps(business,ensure_ascii=False,indent=2)+'\n',ROOT/'assets/business-hours.js':(ROOT/'_templates/business-hours.js').read_text().replace('{{hours}}',json.dumps(hours,separators=(',',':')))}
    # Version the new shared rules and controller together, so cached Phase 2
    # JavaScript cannot silently keep the old Saturday behavior after deployment.
    script_bytes = {'assets/business-hours.js': outputs[ROOT/'assets/business-hours.js'].encode(), 'assets/forms.js': (ROOT/'assets/forms.js').read_bytes()}
    for page in ROOT.glob('booking*.html'):
        source = page.read_text()
        for url, data in script_bytes.items():
            digest = hashlib.sha256(data).hexdigest()[:10]
            source = re.sub(r'src="' + re.escape(url) + r'(?:\?v=[^"]*)?"', f'src="{url}?v={digest}"', source)
        outputs[page] = source
    for path,output in outputs.items():
        if args.check:
            if not path.exists() or path.read_text()!=output:raise SystemExit('Hours derivation stale: '+str(path.relative_to(ROOT)))
        else:path.write_text(output)
    print('PASS: confirmed hours/calendar helper and dated Umuganda schema are synchronized.' if args.check else 'Generated shared hours/calendar helper and 24 dated Umuganda exceptions.')


if __name__=='__main__':main()
