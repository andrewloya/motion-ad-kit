#!/usr/bin/env python3
"""Every number and offer word the ad shows or says must be in the ad's claims.md, checked today.

python3 <skill>/scripts/claims_check.py <ad folder> [--days 1]

claims.md is a markdown table, one row per claim, written while planning (STRUCTURE.md → Claim → proof):
  | claim | source (where you checked it) | checked |
  |---|---|---|
  | 2,400+ customers | Stripe → Customers, active, 2,431 on the day | 2026-10-08 |
  | free to start | pricing page + signed up as a new user | 2026-10-08 |
It reads the visible text of index.html (not scripts or styles) and every pipeline/narration*.json line, finds each
number (30, 2,400+, $12, 4K, 3x, 50%) and each offer word (free, no card, guarantee, % off, discount, limited), and
FAILS when one isn't in a claim cell, or its row wasn't checked in the last --days days. Numbers in real product
screens are fine if they're true: add them as claims too ("$14 latte on the menu"). A year (2026) and a lone 0/1 are
ignored. Why: two posted LYRC ads printed counts that were wrong because they counted things customers can't see.
"""
import datetime, glob, html, json, os, re, sys
from html.parser import HTMLParser

if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
    print(__doc__); sys.exit(0)
AD = os.path.abspath(sys.argv[1])
DAYS = int(sys.argv[sys.argv.index('--days') + 1]) if '--days' in sys.argv else 1


class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip = 0; self.out = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'head'): self.skip += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'head'): self.skip = max(0, self.skip - 1)
    def handle_data(self, d):
        if not self.skip and d.strip(): self.out.append(d.strip())


said = []
ix = os.path.join(AD, 'index.html')
if os.path.exists(ix):
    t = Text(); t.feed(open(ix).read()); said += [('screen', x) for x in t.out]
for f in glob.glob(os.path.join(AD, 'pipeline', 'narration*.json')):
    for ln in json.load(open(f)):
        said.append(('voice', ln.get('text', '')))

rows = []
cp = os.path.join(AD, 'claims.md')
if os.path.exists(cp):
    for line in open(cp):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) >= 3 and not set(cells[0]) <= set('-: ') and cells[0].lower() != 'claim':
            rows.append(cells)

NUM = re.compile(r'[$€£]?\d[\d,.]*\s?(?:k|K|m|M|x|×|%|\+|s\b|hrs?|min)?\+?')
OFFER = re.compile(r'\b(free|no card|no credit card|guarantee[ds]?|% off|discount|limited|only \d+ left|money.back)\b', re.I)
today = datetime.date.today()


def norm(s):
    return re.sub(r'[\s,]', '', s.lower())


def found(token):
    hits = [r for r in rows if norm(token) in norm(r[0])]
    if not hits:
        return 'NOT IN claims.md'
    for r in hits:
        try:
            d = datetime.date.fromisoformat(r[2][:10])
            if (today - d).days <= DAYS - 1 + 1 and (today - d).days >= 0:
                return None
        except ValueError:
            pass
    return f'checked {hits[0][2] or "never"} (re-check it today)'


fails, seen = [], set()
for where, text in said:
    tokens = [m.group(0).strip() for m in NUM.finditer(html.unescape(text))] + [m.group(0) for m in OFFER.finditer(text)]
    for tok in tokens:
        bare = re.sub(r'[^\d]', '', tok)
        if bare and (re.fullmatch(r'(19|20)\d\d', bare) or bare in ('0', '1')) and not re.search(r'[$€£%x×+k]', tok, re.I):
            continue
        if (where, tok.lower()) in seen:
            continue
        seen.add((where, tok.lower()))
        why = found(tok)
        if why:
            fails.append(f'FAIL {where}: "{tok}" in "{text[:60]}" → {why}')
        else:
            print(f'ok   {where}: "{tok}"')
if not os.path.exists(cp):
    fails.insert(0, f'FAIL no claims.md in {AD}: write one (claim | source | checked) before anything prints a number')
print('\n'.join(fails) if fails else 'ok: every number and offer word is a claim checked today')
sys.exit(1 if fails else 0)
