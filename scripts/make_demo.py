# Writes data/demo: a made-up 40-question eval in the same shapes as a real run.
# The company, notes, questions, quotes and answers are invented. The per-method
# totals (correct, partial, hard, hidden, evidence, funnel, rank, latency) are set
# to match the real Nov 9, 2026 eval v2 run, so the demo shows the real result
# without any private data. Usage: python3 scripts/make_demo.py
import json,os,random
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'data','demo')
A,B='cards_decisions_v1','elastic_decisions_v1'
WHEN='2026-11-09T22:30:00Z'

# Invented corpus: "Lantern", a four-person team building a bike-repair booking app.
# (id, kind, question, answer, [(quote, speaker, time)], evidence)
Qs=[
 ('q1','fact','What price did we pick for the monthly plan?','$12 a month.',[('twelve dollars a month','Maya','00:04:10')],0),
 ('q2','fact','Which city do we launch in first?','Portland.',[('we start in Portland','Theo','00:02:31')],0),
 ('q3','fact','Who owns the shop onboarding checklist?','Priya.',[('Priya owns the onboarding checklist','Maya','00:11:02')],0),
 ('q4','fact','How long is a standard repair slot?','45 minutes.',[('slots are forty-five minutes','Sam','00:06:48')],0),
 ('q5','quote','What exactly did Theo say about cancellations?','"No fee if you cancel a day ahead."',[('no fee if you cancel a day ahead','Theo','00:09:15')],1),
 ('q6','fact','Which payment provider did we choose?','Stripe.',[('we go with Stripe','Sam','00:03:20')],0),
 ('q7','fact','What is the target for shops signed by January?','25 shops.',[('twenty-five shops by January','Maya','00:01:55')],0),
 ('q8','fact','Where do repair photos get stored?','In the job record, attached by the mechanic.',[('photos live on the job record','Priya','00:07:40')],0),
 ('q9','fact','What did we name the mechanic app?','Wrench.',[('call it Wrench','Theo','00:12:05')],0),
 ('q10','fact','When is the beta feedback session?','Thursday at 3 PM.',[('Thursday at three for beta feedback','Sam','00:00:48')],0),
 ('q11','quote','What number did Priya give for no-show rate?','"About eight percent."',[('about eight percent','Priya','00:05:33')],1),
 ('q12','fact','Which shops are in the pilot?','Spoke & Chain and Rose City Cycles.',[('Spoke & Chain and Rose City Cycles','Maya','00:08:12')],0),
 ('q13','fact','What is the refund window?','14 days.',[('fourteen-day refund window','Sam','00:10:27')],0),
 ('q14','fact','How do customers get reminders?','By text message the evening before.',[('text the evening before','Theo','00:04:59')],0),
 ('q15','fact','What does the free tier include?','One tune-up booking a month.',[('one tune-up booking a month','Maya','00:13:30')],0),
 ('q16','quote','What exactly did Sam say about the waitlist?','"Waitlist opens the minute a slot frees up."',[('waitlist opens the minute a slot frees up','Sam','00:06:02')],1),
 ('q17','fact','Which analytics tool did we pick?','PostHog.',[('PostHog for analytics','Priya','00:02:14')],0),
 ('q18','fact','What is the shop commission?','10% of each booking.',[('ten percent of each booking','Maya','00:07:07')],0),
 ('q19','fact','Who is writing the launch email?','Theo.',[('Theo writes the launch email','Sam','00:14:21')],0),
 ('q20','fact','What did we decide about dark mode?','Ship it at launch.',[('dark mode ships at launch','Priya','00:03:44')],0),
 ('q21','two_meetings','How did the launch date move across the two planning meetings?','March 1, then pushed to March 15.',[('launch on March first','Maya','00:01:12'),('push launch to March fifteenth','Maya','00:02:40')],0),
 ('q22','two_meetings','What did the two shop interviews say about scheduling?','Both want same-day slots; one also wants weekend hours.',[('same-day slots matter most','Priya','00:05:10'),('weekends too, not just same-day','Priya','00:04:02')],0),
 ('q23','two_meetings','How did the pilot size change between the kickoff and the review?','From 3 shops to 2.',[('three pilot shops','Sam','00:00:58'),('down to two pilot shops','Sam','00:03:15')],0),
 ('q24','changed_mind','Did we keep the plan to charge a booking fee?','No; we dropped it for a monthly plan.',[('drop the booking fee','Maya','00:06:30')],0),
 ('q25','changed_mind','What happened to the idea of an Android app first?','We switched to iOS first.',[('iOS first after all','Theo','00:08:44')],0),
 ('q26','changed_mind','Are we still building in-app chat?','No; we replaced it with text messages.',[('replace chat with texts','Sam','00:09:51')],0),
 ('q27','idea_vs_done','Is the referral program live?','No, it is only an idea so far.',[('referrals are just an idea for now','Priya','00:11:40')],0),
 ('q28','idea_vs_done','Has the shop map been built?','Yes, it shipped last week.',[('the shop map shipped last week','Theo','00:01:33')],0),
 ('q29','idea_vs_done','Did we start the loyalty points work?','No, it was parked.',[('loyalty points are parked','Maya','00:12:18')],0),
 ('q30','never_discussed','What did we decide about scooter repairs?','Not in memory.',[],0),
 ('q31','never_discussed','Which investor did we pitch in October?','Not in memory.',[],0),
 ('q32','never_discussed','What is our policy on e-bike batteries?','Not in memory.',[],0),
 ('q33','who_said','Who said the pilot should skip invoicing?','Sam.',[('skip invoicing in the pilot','Sam','00:04:44')],1),
 ('q34','who_said','Who proposed the 45-minute slot length?','Sam.',[('slots are forty-five minutes','Sam','00:06:48')],1),
 ('q35','no_shared_words','What did we say about people who book and never show?','We charge no fee but track the roughly 8% rate.',[('about eight percent','Priya','00:05:33')],0),
 ('q36','no_shared_words','How do riders hear back when a mechanic is free?','The waitlist opens as soon as a slot frees up.',[('waitlist opens the minute a slot frees up','Sam','00:06:02')],0),
 ('q37','decoy_trap','What is the real monthly price (not the draft in the old pricing note)?','$12 a month.',[('twelve dollars a month','Maya','00:04:10')],0),
 ('q38','decoy_trap','Which city is the launch city (not the one in the brainstorm list)?','Portland.',[('we start in Portland','Theo','00:02:31')],0),
 ('q39','exact','What exact refund window did Sam state?','"Fourteen-day refund window."',[('fourteen-day refund window','Sam','00:10:27')],1),
 ('q40','exact','What exact commission did Maya state?','"Ten percent of each booking."',[('ten percent of each booking','Maya','00:07:07')],1),
]
HIDDEN={'q4','q9','q14','q17','q20','q24','q29','q33','q36','q39'}
# Verdicts per method, chosen so the totals match the real run (checked below).
V={A:'CCPWCPWCPWPCWCPWWPWP'+'CWPWCWCPCCCWWCWWCWPC',
   B:'CCCCPPWCCPWCWPPWPWPW'+'CPCCCWCWCCWCPCCCWPCW'}
EV={A:{'q5':1,'q11':0,'q16':0,'q33':0,'q34':1,'q39':0,'q40':1},
    B:{'q5':0,'q11':0,'q16':0,'q33':0,'q34':1,'q39':1,'q40':0}}
# Funnel losses: (found, kept, returned) per gold note; default all True.
LOSS={A:{'q16':[(1,0,0)],'q10':[(1,1,0)],'q22':[(1,1,1),(1,1,0)]},
      B:{'q20':[(0,0,0)]}}
TOTAL_RANK={A:181,B:76}; CAND={A:30,B:10}
LAT={A:(1600,2000),B:(1500,2000)}
REASON={'C':'Matches the key.','P':'Right source, key detail missing.','W':'Answer not supported by the context.'}

def note_id(qid,k):return f'note-{qid}-{k}'
def decoy(i):return f'decoy-{i:02d}'

def ranks_for(m,rng,golds):
  # one rank per question with a found gold note; adjust so the average matches
  r={q:(rng.randint(1,4) if m==B else rng.randint(2,8)) for q in golds}
  keys=sorted(r,key=lambda k:int(k[1:]));diff=TOTAL_RANK[m]-sum(r.values());i=0
  while diff:
    k=keys[i%len(keys)];step=1 if diff>0 else -1
    if 1<=r[k]+step<=CAND[m]:r[k]+=step;diff-=step
    i+=1
  return r

def latencies(rng,p50,p95):
  lo=[rng.randint(p50-500,p50-60) for _ in range(20)]
  hi=[rng.randint(p50+10,p95-120) for _ in range(18)]
  v=sorted(lo)+[p50]+sorted(hi)[:17]+[p95-10,p95+300]
  v=sorted(v);v[20]=p50;v[38]=p95-10
  return v

def context(q,verdict,returned):
  lines=[]
  for k,(quote,speaker,time) in enumerate(q[4]):
    if not returned[k]:continue
    if verdict=='C' or (verdict=='P' and k==0 and not q[5]):
      lines.append(f'[{note_id(q[0],k)}] {speaker} ({time}): ... and {quote}. We agreed to write it down.')
    else:
      lines.append(f'[{note_id(q[0],k)}] {speaker} ({time}): We talked about this for a while and said we would come back to it.')
  lines.append(f'[{decoy(int(q[0][1:])%35)}] Brainstorm list: ideas, drafts and open questions.')
  return '\n\n'.join(lines)

def answer(q,v):
  if v=='C':return q[3].strip('"')
  if v=='P':return 'The notes touch on this, but the context does not give the full detail.'
  return 'It is not in memory.' if q[4] else 'We decided to handle it case by case.'

def build():
  qs=[];rng=random.Random(9)
  for qid,kind,question,ans,gold,ev in Qs:
    n=int(qid[1:])
    qs.append({'id':qid,'question':question,'kind':kind,'answer':ans,
      'gold':[{'note_id':note_id(qid,k),'must_include':[t],'speaker':s,'time':tm} for k,(t,s,tm) in enumerate(gold)],
      'hard':n>20,'evidence':bool(ev),'split':'hidden' if qid in HIDDEN else 'dev'})
  files={'questions-v2.json':qs}
  for m in (A,B):
    golds=[q[0] for q in Qs if q[4] and not (LOSS[m].get(q[0]) and not LOSS[m][q[0]][0][0])]
    rk=ranks_for(m,rng,golds);lat=latencies(rng,*LAT[m]);rng.shuffle(lat)
    raw,cases,grades=[],[],[]
    for i,q in enumerate(Qs):
      qid=q[0];v=V[m][i];gold=[note_id(qid,k) for k in range(len(q[4]))]
      loss=LOSS[m].get(qid) or [(1,1,1)]*len(gold)
      cand=[decoy(j) for j in range(CAND[m])]
      for k,g in enumerate(gold):
        if loss[k][0]:cand.insert(min(rk.get(qid,1)-1+k,len(cand)),g)
      cand=cand[:CAND[m]]
      judged=[{'id':g,'outcome':'kept' if loss[k][1] else 'dropped','probability':round(0.9-0.05*k if loss[k][1] else 0.31,2)} for k,g in enumerate(gold) if loss[k][0]]
      out=[{'id':g} for k,g in enumerate(gold) if loss[k][2]]+[{'id':cand[-1]}]
      ms=lat[i];search=int(ms*0.35);filt=int(ms*0.5)
      base=[{'stage':'elastic_candidates' if m==B else 'current_search','duration_ms':search,
             'detail':{'hits':[{'id':c} for c in cand]} if m==B else [{'id':c} for c in cand]}]
      raw.append({'evaluation':{'question_id':qid},'latency_ms':ms,
        'trace':{'runs':[{'duration_ms':ms,'degraded':[],'output':out,
          'queries':[{'base':{'stages':base},'stages':[{'stage':'decisions','duration_ms':filt,'detail':{'judged':judged}}]}]}]},
        'response':{'runs':[{'result':{'context':context(q,v,[l[2] for l in loss]),'sources':[{'memory_id':o['id']} for o in out]}}]}})
      cases.append({'id':qid,'latency_ms':ms,'trace_url':None})
      verdict={'C':'correct','P':'partial','W':'wrong'}[v]
      grades.append({'id':qid,'agent_answer':answer(q,v),'verdict':verdict,'reason':REASON[v],
        'evidence':bool(EV[m][qid]) if qid in EV[m] else None})
    files[f'runs/{m}-r1.json']={'timestamp':WHEN,'method':m,'cases':cases}
    files[f'runs/{m}-r1-raw.json']=raw
    files[f'grades/{m}.json']=grades
  # Eval 1: the first 20 questions, regraded with the same judge (real totals: 5/20 and 6/20).
  e1={A:'CCWWWWWCWWWCWCWWWWWW',B:'CCCCWWWCWWWCWWWWWWWW'}
  for m in (A,B):
    files[f'history/eval1/{m}.json']=[{'id':q[0],'verdict':{'C':'correct','P':'partial','W':'wrong'}[e1[m][i]]} for i,q in enumerate(Qs[:20])]
  files['history.json']=[
    {'name':'Eval 1','date':'2026-11-09','questions':20,'note':'Regraded with the same judge','grades_dir':'history/eval1','exact_text':{A:2,B:5}},
    {'name':'Eval 2','date':'2026-11-09','questions':40,'note':'+20 hard, 10 hidden','grades_dir':'grades'}]
  files['meta.json']={'label':'demo data','public':True,
    'note':'Invented questions and notes. Totals match the real Nov 9, 2026 eval v2 run.'}
  return files

def check(files):
  qs=files['questions-v2.json'];Q={q['id']:q for q in qs}
  want={A:dict(correct=15,partial=10,hard=9,hidden=2,nsw=0,ev=3,found=37,kept=36,ret=34,rank=4.9,orig=6,e1=5),
        B:dict(correct=19,partial=10,hard=12,hidden=6,nsw=2,ev=2,found=36,kept=36,ret=36,rank=2.1,orig=7,e1=6)}
  for m,w in want.items():
    g=files[f'grades/{m}.json'];c=[x for x in g if x['verdict']=='correct']
    got=dict(correct=len(c),partial=sum(x['verdict']=='partial' for x in g),
      hard=sum(Q[x['id']]['hard'] for x in c),hidden=sum(Q[x['id']]['split']=='hidden' for x in c),
      nsw=sum(Q[x['id']]['kind']=='no_shared_words' for x in c),ev=sum(x['evidence'] is True for x in g),
      orig=sum(int(x['id'][1:])<=20 for x in c),
      e1=sum(x['verdict']=='correct' for x in files[f'history/eval1/{m}.json']))
    f=k=r=0;ranks=[]
    for x in files[f'runs/{m}-r1-raw.json']:
      q=Q[x['evaluation']['question_id']];gold=[gd['note_id'] for gd in q['gold']]
      if not gold:continue
      run=x['trace']['runs'][0];st=run['queries'][0]
      d=st['base']['stages'][0]['detail'];cand=[h['id'] for h in (d['hits'] if isinstance(d,dict) else d)]
      judged={j['id']:j['outcome'] for j in st['stages'][0]['detail']['judged']};out={o['id'] for o in run['output']}
      f+=all(gd in cand for gd in gold);k+=all(judged.get(gd)=='kept' for gd in gold);r+=all(gd in out for gd in gold)
      rs=[cand.index(gd)+1 for gd in gold if gd in cand]
      if rs:ranks.append(min(rs))
    got.update(found=f,kept=k,ret=r,rank=round(sum(ranks)/len(ranks),1))
    assert got==w,(m,got,w)
    ms=sorted(c['latency_ms'] for c in files[f'runs/{m}-r1.json']['cases'])
    assert (round(ms[20]/1000,1),round(ms[38]/1000,1))==tuple(v/1000 for v in LAT[m]),(m,ms[20],ms[38])

files=build();check(files)
for p,v in files.items():
  path=os.path.join(OUT,p);os.makedirs(os.path.dirname(path),exist_ok=True)
  with open(path,'w') as f:json.dump(v,f,indent=1);f.write('\n')
print('wrote',OUT)
