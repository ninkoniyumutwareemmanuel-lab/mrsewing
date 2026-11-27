"""Compatible retired routes over current approved pages; no second gallery."""
from html import escape
import json

def alias(destination,label,translate_audience=False):
    script=('const u=new URL(location.href);'
            +'u.pathname='+json.dumps(destination)+';')
    if translate_audience:
        script+=('const a=u.searchParams.get("audience"),c=u.searchParams.get("clothing");'
                 'if(!u.searchParams.has("gender")){'
                 'if(["men","women","all"].includes(a))u.searchParams.set("gender",a);'
                 'else if(c==="mens-suits")u.searchParams.set("gender","men");'
                 'else if(c==="womens-suits")u.searchParams.set("gender","women");}'
                 'u.searchParams.delete("audience");u.searchParams.delete("clothing");')
    script+='location.replace(u.pathname+u.search+u.hash);'
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="robots" content="noindex, follow"><link rel="canonical" href="https://mrsewingfashion.com'+destination+'">'
            '<title>'+escape(label)+' | Mr Sewing Fashion</title><meta name="description" content="Continue to the existing approved destination.">'
            '<script>'+script+'</script></head><body><main><h1>'+escape(label)+'</h1><p>This page continues at <a href="'+destination+'">'+escape(label)+'</a>.</p>'
            '<noscript><p>Use the link to continue. Existing selections remain in your browser.</p></noscript></main></body></html>\n')
