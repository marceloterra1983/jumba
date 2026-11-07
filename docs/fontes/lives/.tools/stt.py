import os,sys,glob,site
# torna as libs CUDA do pip visíveis ao ctranslate2
for p in glob.glob(os.path.join(site.getsitepackages()[0],'nvidia','*','lib')):
    os.environ['LD_LIBRARY_PATH']=p+':'+os.environ.get('LD_LIBRARY_PATH','')
from faster_whisper import WhisperModel
src,dst=sys.argv[1],sys.argv[2]
m=WhisperModel('large-v3-turbo',device='cuda',compute_type='float16')
import numpy as np
aud=np.fromfile(src,dtype=np.int16).astype(np.float32)/32768.0 if src.endswith('.pcm') else src
segs,info=m.transcribe(aud,language='pt',vad_filter=True,beam_size=5)
last=-60;buf=[];out=[]
for s in segs:
    t=int(s.start)
    if t-last>=60:
        if buf: out.append(' '.join(buf));buf=[]
        out.append(f'\n[{t//3600}:{t%3600//60:02d}:{t%60:02d}]');last=t
    buf.append(s.text.strip())
if buf: out.append(' '.join(buf))
open(dst,'w',encoding='utf-8').write('\n'.join(out).strip()+'\n')
print('ok',info.duration)
