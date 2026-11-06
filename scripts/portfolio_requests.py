"""Quotation references derived only from genuine permission-approved portfolio records."""
from urllib.parse import unquote,urlencode
from html import escape

def model():
    from build_journey import projects
    from build_collections import load
    from suit_references import assignment
    designs=load()[0];out={}
    for p in projects():
        main=p['images'][0]['src']
        match=next((d for d in designs if any(unquote(i['src'])==main for i in d['images'])),None)
        if not match:raise ValueError('Approved portfolio photo needs its existing quotation reference: '+p['slug'])
        category=assignment(match['id'])
        out[p['slug']]={'name':p['title'],'designRef':match['id'],'route':'/our-work/'+p['slug']+'/','image':main,'images':[{k:i[k] for k in ['src','alt','width','height']}|{'url':__import__('selected_designs').image_url(i['src'])} for i in p['images']],**({'category':category['gender'],'suitCategory':category['id']} if category else {'category':match['gender']} if match['gender'] in ['men','women'] else {})}
    return out

def enquiry(project):
    d=model()[project['slug']]
    params={'service':'custom-tailoring','order':'standard','project':project['slug'],'design':d['designRef'],'photo':d['images'][0]['url']}
    params.update({k:d[k] for k in ['category','suitCategory'] if k in d})
    return '<a class="journey-enquiry" href="/services/custom-tailoring/fabric/?'+escape(urlencode(params),quote=True)+'">Inquire About This Design <span class="home-arrow" aria-hidden="true"></span></a>'
