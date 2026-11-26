#!/usr/bin/env python3
"""Run from the MK163 repository root. Scoped, idempotent, checked edits."""
from pathlib import Path
import re
p=Path('CONTINUITY/RED_RUNNING_DAY_LEDGER.md')
s=p.read_text(encoding='utf-8')
rows=s.splitlines(keepends=True)
changes={}
for i,line in enumerate(rows):
 m=re.match(r'^\|\s*(\d+)\s*\|',line)
 if not m:continue
 day=int(m.group(1))
 if not 787<=day<=859:continue
 original=line
 if 787<=day<=817:
  line=line.replace('Staying at Aiselle’s Blue District residence. Leisure, apartment search and the eight-smith capital expansion span this interval. Individual appointments OPEN.', 'Staying at Aiselle’s Blue District residence following Blackstone graduation. Spending time with Aiselle, enjoying leisure, and searching for an apartment. Individual appointments OPEN.')
 elif day==820:line=line.replace('six-smith wholesale partnership','eight-smith wholesale partnership')
 elif day==825:line=line.replace('six-table assembly','eight-table assembly')
 elif day==827:line=line.replace('hires six experienced smiths','hires eight experienced smiths')
 elif 829<=day<=845:line=line.replace('six-smith Yellow District workshop','eight-smith Yellow District workshop')
 elif day==846:line=line.replace('Six trainee robes and Kaira’s demonstration robe complete','Eight robes crafted by the blacksmiths and one robe crafted by Kaira complete (nine robes total)')
 elif 847<=day<=855:line=line.replace('seven training robes','nine completed robes')
 elif day==856:line=line.replace('six-robe production batch','eight-robe production batch')
 if line!=original:
  rows[i]=line;changes[day]=True
expected=set(range(787,818))|{820,825,827}|set(range(829,857))
assert set(changes)==expected,(sorted(expected-set(changes)),sorted(set(changes)-expected))
p.write_text(''.join(rows),encoding='utf-8')
print('Updated',p,'rows:',len(changes))
