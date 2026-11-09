# Builds the eval dashboard (Original vs Elastic) as one self-contained HTML file.
# Usage: python3 dashboard/build.py [data_dir] [out.html]
#   data_dir holds questions-v2.json, history.json, runs/ and grades/ (default: data/demo).
# Real eval data is private: keep it outside the repo (data/private/ is gitignored).
# Output built from anything but the demo data is written with mode 600.
import json,os,sys,re
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
DATA=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'data','demo'))
OUT=os.path.abspath(sys.argv[2] if len(sys.argv)>2 else os.path.join(ROOT,'out','dashboard.html'))
RUNS=os.path.join(DATA,'runs');GRADES=os.path.join(DATA,'grades')
METHODS=[('cards_decisions_v1','Original'),('elastic_decisions_v1','Elastic')]
qs=json.load(open(os.path.join(DATA,'questions-v2.json')))
QS={q['id']:q for q in qs}
norm=lambda s:re.sub(r'\s+',' ',str(s or '').lower())

def load(p):
  try:return json.load(open(p))
  except (OSError,ValueError):return None

def candidates(m,base,qst):
  cand=[]
  for st in base:
    d=st.get('detail')
    if st['stage']=='fusion' and isinstance(d,dict):cand=[h['id'] for h in d.get('ranked',[]) if h.get('outcome','selected')=='selected']
    if st['stage']=='elastic_candidates' and isinstance(d,dict):cand=[h['id'] for h in d.get('hits',[])]
    if st['stage']=='current_search' and isinstance(d,list):cand=[h['id'] for h in d]
  if not cand:
    for st in qst:
      if st['stage']=='run_candidates' and isinstance(st.get('detail'),list):cand=[h['id'] for h in st['detail']]
  return cand

def row(m,x,case,grade):
  qid=x['evaluation']['question_id'];q=QS[qid];gold=[g['note_id'] for g in q['gold']]
  runs=(x.get('trace') or {}).get('runs') or [{}];r=runs[0]
  qq=(r.get('queries') or [{}])[0];base=(qq.get('base') or {}).get('stages') or [];qst=qq.get('stages') or []
  cand=candidates(m,base,qst)
  ranks=[cand.index(g)+1 if g in cand else None for g in gold]
  dec=next((st for st in qst if st['stage']=='decisions'),{})
  judged={j['id']:j for j in (dec.get('detail') or {}).get('judged',[])}
  keptg=[g in judged and judged[g]['outcome']=='kept' for g in gold]
  probs=[(judged.get(g) or {}).get('probability') for g in gold]
  out={o['id'] for o in r.get('output') or []}
  if not out:out={s.get('memory_id') for s in (x['response']['runs'][0]['result'].get('sources') or [])}
  retg=[g in out for g in gold]
  ctx=x['response']['runs'][0]['result'].get('context') or ''
  nctx=norm(ctx);quoteg=[any(norm(t) in nctx for t in g.get('must_include') or []) for g in q['gold']]
  n=len(gold)
  def step(v):return None if not n else (sum(v)==n)
  verdict=(grade or {}).get('verdict')
  ev=None
  if q.get('evidence'):
    ev=(grade or {}).get('evidence')
    if ev is None and n:ev=all(quoteg)
  steps=[step([x is not None for x in ranks]),step(keptg),step(retg)]
  stage=next((i+1 for i,s in enumerate(steps) if s is False),None)
  if stage is None and verdict in ('wrong','partial'):stage=4
  ms=(case or {}).get('latency_ms') or x.get('latency_ms') or r.get('duration_ms')
  return {'id':qid,'ranks':ranks,'rank':min([k for k in ranks if k],default=None),'candidates':len(cand),
    'found':sum(k is not None for k in ranks),'kept':sum(keptg),'returned':sum(retg),'n':n,
    'steps':steps,'verdict':verdict,'stage':stage,'evidence':ev,'probs':probs,
    'agent_answer':(grade or {}).get('agent_answer'),'reason':(grade or {}).get('reason'),
    'ms':ms,'search_ms':sum(st.get('duration_ms') or 0 for st in base) or None,'filter_ms':dec.get('duration_ms'),
    'degraded':r.get('degraded') or [],'context':ctx[:2400],'trace':(case or {}).get('trace_url')}

methods={};notes=[]
for m,label in METHODS:
  s=load(f'{RUNS}/{m}-r1.json');raw=load(f'{RUNS}/{m}-r1-raw.json')
  if s is None or raw is None:notes.append(f'{label}: run files missing in {RUNS}');continue
  g=load(f'{GRADES}/{m}.json')
  if g is None:notes.append(f'{label}: no grades in {GRADES}')
  grades={x['id']:x for x in g or []}
  cases={c['id']:c for c in s.get('cases',[])}
  rows=[row(m,x,cases.get(x['evaluation']['question_id']),grades.get(x['evaluation']['question_id'])) for x in raw if x['evaluation']['question_id'] in QS]
  order={q['id']:i for i,q in enumerate(qs)};rows.sort(key=lambda r:order[r['id']])
  methods[m]={'label':label,'rows':rows,'timestamp':s.get('timestamp'),'graded':g is not None}

history=[]
for h in load(os.path.join(DATA,'history.json')) or []:
  e={'name':h.get('name'),'date':h.get('date'),'questions':h.get('questions'),'note':h.get('note'),'methods':{}}
  for m,label in METHODS:
    g=load(os.path.join(DATA,h.get('grades_dir') or '',m+'.json'))
    if g is None:e['methods'][m]=None;continue
    orig=[x for x in g if re.fullmatch(r'q([1-9]|1[0-9]|20)',str(x.get('id')))]
    e['methods'][m]={'correct':sum(x.get('verdict')=='correct' for x in g),'partial':sum(x.get('verdict')=='partial' for x in g),'n':h.get('questions') or len(g),
      'orig_correct':sum(x.get('verdict')=='correct' for x in orig),'orig_n':len(orig),'exact_text':(h.get('exact_text') or {}).get(m)}
  history.append(e)
meta=load(os.path.join(DATA,'meta.json')) or {}
rel=lambda p:os.path.relpath(p,ROOT) if p.startswith(ROOT+os.sep) else p
data={'history':history,'run':{'when':min([v['timestamp'] for v in methods.values() if v['timestamp']],default=None),'questions':len(qs),
    'label':meta.get('label'),'rebuild':f'python3 dashboard/build.py {rel(DATA)} {rel(OUT)}'},
  'questions':[{'id':q['id'],'question':q['question'],'kind':q.get('kind'),'answer':q.get('answer'),'hard':bool(q.get('hard')),
    'evidence':bool(q.get('evidence')),'hidden':q.get('split')=='hidden',
    'gold':[{'quotes':g.get('must_include') or [],'speaker':g.get('speaker'),'time':g.get('time')} for g in q['gold']]} for q in qs],
  'methods':methods}
tpl=open(os.path.join(HERE,'template.html')).read()
payload=json.dumps(data).replace('<','\\u003c')
os.makedirs(os.path.dirname(OUT),exist_ok=True)
mode=0o644 if meta.get('public') else 0o600
fd=os.open(OUT,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,mode)
with os.fdopen(fd,'w') as f:f.write(tpl.replace('/*DATA*/null',payload))
os.chmod(OUT,mode)
for t in notes:print('note:',t)
print('wrote',OUT)
