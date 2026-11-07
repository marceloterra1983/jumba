import re,sys
src,dst=sys.argv[1],sys.argv[2]
lines=open(src,encoding='utf-8').read().splitlines()
out=[];seen=set();last_mark=-60;t=0;buf=[]
ts=re.compile(r'^(\d+):(\d\d):(\d\d)\.\d+ -->')
for l in lines:
    m=ts.match(l)
    if m:
        t=int(m[1])*3600+int(m[2])*60+int(m[3]);continue
    if not l.strip() or l.startswith(('WEBVTT','Kind:','Language:')) or '<c>' in l or re.search(r'<\d\d:',l): continue
    txt=re.sub(r'<[^>]+>','',l).strip()
    if not txt or txt in seen: continue
    seen.add(txt)
    if t-last_mark>=60:
        if buf: out.append(' '.join(buf));buf=[]
        out.append(f'\n[{t//3600:d}:{t%3600//60:02d}:{t%60:02d}]');last_mark=t
    buf.append(txt)
if buf: out.append(' '.join(buf))
open(dst,'w',encoding='utf-8').write('\n'.join(out).strip()+'\n')
