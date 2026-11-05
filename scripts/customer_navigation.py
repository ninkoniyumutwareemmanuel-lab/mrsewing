"""Small semantic breadcrumbs; no sequential request-state mutation."""
from html import escape
def breadcrumb(items):
 return '<nav class="customer-breadcrumb" aria-label="Breadcrumb"><ol>'+''.join('<li>'+('<a href="'+escape(url,quote=True)+'">'+escape(label)+'</a>' if url else '<span aria-current="page">'+escape(label)+'</span>')+'</li>' for label,url in items)+'</ol></nav>'
