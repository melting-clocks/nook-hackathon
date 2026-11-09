// Grades what reached the agent: an agent answers from the context only; a judge compares to the answer key.
// Usage: AI_GATEWAY_API_KEY=... node grader/grade.mjs <method> [data_dir]
//   data_dir holds questions-v2.json and runs/<method>-r1-raw.json; writes grades/<method>.json.
import {readFileSync,writeFileSync,existsSync,mkdirSync} from 'node:fs';
import {join} from 'node:path';
import {chat} from './gw.mjs';
const method=process.argv[2],dir=process.argv[3]||'.';
if(!method){console.error('usage: node grader/grade.mjs <method> [data_dir]');process.exit(2)}
const qs=new Map(JSON.parse(readFileSync(join(dir,'questions-v2.json'),'utf8')).map(q=>[q.id,q]));
let raw=JSON.parse(readFileSync(join(dir,`runs/${method}-r1-raw.json`),'utf8'));
const outFile=join(dir,`grades/${method}.json`);
// REGRADE=1 keeps earlier non-error grades and only grades the rest.
const prev=process.env.REGRADE&&existsSync(outFile)?JSON.parse(readFileSync(outFile,'utf8')).filter(g=>g.verdict!=='error'):[];
const done=new Set(prev.map(g=>g.id));raw=raw.filter(x=>!done.has(x.evaluation.question_id));
const norm=s=>String(s||'').toLowerCase().replace(/\s+/g,' ');
const AGENT='anthropic/claude-sonnet-5-5',JUDGE='anthropic/claude-opus-5-5';
async function one(x){
 const q=qs.get(x.evaluation.question_id),ctx=x.response?.runs?.[0]?.result?.context||'';
 const agent=await chat(AGENT,[{role:'system',content:'You are an assistant answering from the user\'s memory. Use ONLY the memory context provided. If the context does not contain the answer, say it is not in memory. Answer in 1-3 sentences; include exact numbers, names and quotes when the question asks for them.'},{role:'user',content:`<memory_context>\n${ctx}\n</memory_context>\n\nQuestion: ${q.question}`}],{max:400});
 const judge=await chat(JUDGE,[{role:'user',content:`Grade an assistant's answer against the answer key.\nQuestion: ${q.question}\nAnswer key: ${q.answer}\n${q.gold.length?'':'(The memory does NOT contain this. Correct = the assistant says it is not in memory / unknown without inventing facts.)\n'}Assistant answer: ${agent}\n\ncorrect = all key facts right, no contradicting claims. partial = some key facts right but missing or vague on others. wrong = incorrect, invented, or says not found when the key has an answer.\nReturn JSON {"verdict":"correct|partial|wrong","reason":"<= 15 words"}`}],{max:1000});
 const j=JSON.parse(judge.slice(judge.indexOf('{'),judge.lastIndexOf('}')+1));
 let evidence=null;
 if(q.evidence&&q.gold.length){const c=norm(ctx);evidence=q.gold.every(g=>g.must_include.some(m=>c.includes(norm(m)))&&(!g.speaker||c.includes(norm(g.speaker))));}
 return {id:q.id,agent_answer:agent,verdict:j.verdict,reason:j.reason,evidence};
}
const out=[...prev];let i=0;
await Promise.all(Array.from({length:6},async()=>{while(i<raw.length){const x=raw[i++];for(let a=0;;a++){try{out.push(await one(x));break}catch(e){if(a>=2){out.push({id:x.evaluation.question_id,verdict:'error',reason:String(e).slice(0,80),evidence:null});break}}}}}));
mkdirSync(join(dir,'grades'),{recursive:true});
writeFileSync(outFile,JSON.stringify(out,null,1),{mode:0o600});
