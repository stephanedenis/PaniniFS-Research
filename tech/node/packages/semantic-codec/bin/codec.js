#!/usr/bin/env node
import fs from 'fs';
import crypto from 'crypto';

const DHATUS = [
  'RELATE','MODAL','EXIST','EVAL','COMM','CAUSE','ITER','DECIDE','FEEL'
];

function dhatuVector(text) {
  // Heuristic: project content into 9-dim vector using keyed hashes per dhatu
  const vec = new Array(DHATUS.length).fill(0);
  for (let i = 0; i < DHATUS.length; i++) {
    const h = crypto.createHash('sha256')
      .update(DHATUS[i] + '::' + text)
      .digest();
    // take a few bytes to create a stable weight
    const w = h[0] + h[5] + h[13] + h[21] + h[29];
    vec[i] = w / 1024; // normalize roughly
  }
  // L1 normalize
  const sum = vec.reduce((a,b)=>a+b,0) || 1;
  return vec.map(v => v / sum);
}

function topDhatus(vec, k=3){
  return vec
    .map((v,i)=>({code: DHATUS[i], w:v}))
    .sort((a,b)=>b.w-a.w)
    .slice(0,k);
}

function digest(text){
  const vec = dhatuVector(text);
  const top = topDhatus(vec, 4);
  const sig = crypto.createHash('sha256')
    .update(JSON.stringify(top))
    .digest('hex')
    .slice(0,16);
  return { vec, top, signature:sig };
}

function loadFile(path){
  try { return fs.readFileSync(path); } catch(e){ return null; }
}

function toText(buf, hint){
  if(!buf) return '';
  // For now, treat as utf8 if likely text, else hash-only surrogate
  const text = buf.toString('utf8');
  // crude heuristic: if contains many replacement chars, fallback to hex chunk
  const bad = (text.match(/\uFFFD/g)||[]).length;
  if(bad > 5) return crypto.createHash('sha256').update(buf).digest('hex');
  return text;
}

function explain(path){
  const data = loadFile(path);
  if(!data){
    console.error('File not found:', path);
    process.exit(2);
  }
  const txt = toText(data, path);
  const d = digest(txt);
  console.log(JSON.stringify({ file:path, bytes:data.length, ...d }, null, 2));
}

function pack(path){
  const data = loadFile(path);
  if(!data){
    console.error('File not found:', path);
    process.exit(2);
  }
  const meta = digest(toText(data, path));
  const out = {
    paninifs: 1,
    type: 'semantic-pack',
    file: path,
    bytes: data.length,
    top: meta.top,
    signature: meta.signature
  };
  process.stdout.write(JSON.stringify(out));
}

function usage(){
  console.log('Usage: paninifs-codec <explain|pack> <file>');
}

const [,, cmd, arg] = process.argv;
if(!cmd || !arg){ usage(); process.exit(1); }
if(cmd==='explain') explain(arg);
else if(cmd==='pack') pack(arg);
else { usage(); process.exit(1); }
