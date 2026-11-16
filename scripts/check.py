#!/usr/bin/env python3
"""Check generated local targets, fragment identifiers, and public-file boundaries."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids = set(); self.links = []; self.duplicates = []; self.images = []; self.task_cards = []; self.current_card = None; self.media = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'article' and 'task-card' in a.get('class','').split():
            self.current_card = {'image_count':0, 'media':[]}; self.task_cards.append(self.current_card)
        if tag == 'img':
            self.images.append(a)
            if self.current_card is not None: self.current_card['image_count'] += 1
        if tag == 'figure' and 'data-task-media' in a:
            self.media.append(a['data-task-media'])
            if self.current_card is not None: self.current_card['media'].append(a['data-task-media'])
        if 'id' in a:
            if a['id'] in self.ids: self.duplicates.append(a['id'])
            self.ids.add(a['id'])
        for key in ['href','src']:
            if key in a: self.links.append(a[key])
    def handle_endtag(self, tag):
        if tag == 'article': self.current_card = None

def main():
    errors = []; pages = {p: Page(p.read_text()) for p in SITE.rglob('*.html')}; count = 0
    for path, page in pages.items():
        if page.duplicates: errors.append(f'duplicate IDs: {path}: {page.duplicates}')
        for image in page.images:
            if not image.get('alt') or not image.get('width') or not image.get('height'): errors.append(f'image missing description or dimensions: {path}')
        if path.parent.name == 'task_cards' and path.name != 'README.html' and not page.media:
            errors.append(f'task detail has no simulation image: {path}')
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
    home = pages[SITE/'index.html']
    tasks = [json.loads(s) for s in (ROOT/'content/survey/data/tasks.jsonl').read_text().splitlines() if s.strip()]
    if len(home.task_cards) != len(tasks) or any(c['image_count'] < 1 or not c['media'] for c in home.task_cards): errors.append('guide task image coverage incomplete')
    media = json.loads((ROOT/'content/task_media.json').read_text())
    for key,item in media.items():
        if not item.get('sources') or not item.get('context') or not item.get('credit'): errors.append(f'image provenance incomplete: {key}')
        for image in item['images']:
            path = SITE/'assets/tasks'/image['file']
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != image['sha256']: errors.append(f'image hash mismatch: {key}')
    summary = {'html_pages':len(pages),'local_links_and_assets':count,'guide_tasks_with_images':sum(c['image_count']>0 for c in home.task_cards),'detail_pages_with_images':sum(p.parent.name=='task_cards' and p.name!='README.html' and bool(page.media) for p,page in pages.items()),'unique_image_files':sum(len(x['images']) for x in media.values()),'errors':errors}
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if errors: raise SystemExit(1)

if __name__ == '__main__': main()
