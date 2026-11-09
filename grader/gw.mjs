// Vercel AI Gateway chat helper. The token comes from AI_GATEWAY_API_KEY; never commit it.
const tok=(process.env.AI_GATEWAY_API_KEY||'').trim();
export async function chat(model,messages,{json=false,max=4000}={}){
 if(!tok)throw Error('set AI_GATEWAY_API_KEY');
 for(let a=0;a<3;a++){
  const r=await fetch('https://ai-gateway.vercel.sh/v1/chat/completions',{method:'POST',headers:{authorization:'Bearer '+tok,'content-type':'application/json'},body:JSON.stringify({model,messages,max_tokens:max,...(json?{response_format:{type:'json_object'}}:{})})});
  if(r.ok){const d=await r.json();return d.choices[0].message.content;}
  const t=await r.text();if(a==2)throw Error('gw '+r.status+' '+t.slice(0,200));await new Promise(s=>setTimeout(s,2000));
 }
}
