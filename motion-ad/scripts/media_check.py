#!/usr/bin/env python3
"""media_check.py [index.html] — every <video>: does its file last as long as the composition plays it?
A clip that runs out holds its last frame (from the LYRC build: the wall "become[s] static at this point"). Prints each clip that
runs short and by how much; exit 1 if any does."""
import re, subprocess, sys, os
html = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
base = os.path.dirname(os.path.abspath(html)); bad = 0; dur = {}
for tag in re.findall(r'<video\b[^>]*>', open(html).read()):
    a = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
    src = os.path.join(base, a['src'])
    if src not in dur:
        dur[src] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout or 0)
    need = float(a.get('data-media-start', 0)) + float(a.get('data-duration', 0))
    if need > dur[src] + 1 / 60:
        bad += 1
        print(f"FREEZES {a.get('id', '?'):8} {a['src']:40} plays {need:6.2f} s of a {dur[src]:5.2f} s file — last {need - dur[src]:.2f} s frozen (comp {float(a.get('data-start', 0)) + dur[src] - float(a.get('data-media-start', 0)):.2f}→{float(a.get('data-start', 0)) + float(a.get('data-duration', 0)):.2f})")
print(f'{len(re.findall(r"<video", open(html).read()))} videos, {bad} run short' + (' — ok' if not bad else ''))
sys.exit(1 if bad else 0)
