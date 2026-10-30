#!/usr/bin/env python3
"""Local simulation of generated Pages redirects/headers. Not a Cloudflare deployment."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit
from pathlib import Path
import argparse
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(ROOT),**k)
 def do_GET(self):
  url=urlsplit(self.path)
  for line in (ROOT/'_redirects').read_text().splitlines():
   if not line or line.startswith('#'):continue
   source,target,status=line.split()
   if url.path==source:
    self.send_response(int(status));self.send_header('Location',target+('?' +url.query if url.query else ''));self.end_headers();return
  super().do_GET()
 def end_headers(self):
  host=self.headers.get('Host','').split(':')[0]
  if host=='mrsewing-staging.pages.dev' or host.endswith('.mrsewing-staging.pages.dev'):self.send_header('X-Robots-Tag','noindex, nofollow, noarchive')
  super().end_headers()
 def log_message(self,*a):pass
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8001);a=p.parse_args();ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
