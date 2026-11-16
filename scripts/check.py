#!/usr/bin/env python3
"""Check generated local targets, fragment identifiers, and public-file boundaries."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids = set(); self.links = []; self.duplicates = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids: self.duplicates.append(a['id'])
            self.ids.add(a['id'])
        for key in ['href','src']:
            if key in a: self.links.append(a[key])

def main():
    errors = []; pages = {p: Page(p.read_text()) for p in SITE.rglob('*.html')}; count = 0
    for path, page in pages.items():
        if page.duplicates: errors.append(f'duplicate IDs: {path}: {page.duplicates}')
        for link in page.links:
            u = urlsplit(link)
            if u.scheme or u.netloc: continue
            target = (path.parent / unquote(u.path)).resolve() if u.path else path
            count += 1
            if not target.is_relative_to(SITE): errors.append(f'outside site: {path}: {link}')
            elif not target.exists(): errors.append(f'missing target: {path}: {link}')
            elif u.fragment and target.suffix == '.html' and unquote(u.fragment) not in pages[target].ids:
                errors.append(f'missing fragment: {path}: {link}')
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '.venv' in path.parts: continue
        if path.suffix in ['.html','.js','.css','.md','.json','.jsonl','.txt']:
            text = path.read_text()
            if re.search(r'/home/|/tmp/|(?:ghp|gho|github_pat)_[A-Za-z0-9_]{20,}|wandb\.ai/|forge\.coreweave\.com/',text): errors.append(f'non-public material: {path}')
    summary = {'html_pages':len(pages),'local_links_and_assets':count,'errors':errors}
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if errors: raise SystemExit(1)

if __name__ == '__main__': main()
