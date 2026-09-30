import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import wav from 'wav';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const outDir=path.join(root,'public','audio','v04-sfx');
const sampleRate=48000;
const channels=2;

await fs.promises.rm(outDir,{recursive:true,force:true});
await fs.promises.mkdir(outDir,{recursive:true});

let seed=20260930;
const rand=()=>{
  seed=(seed*1664525+1013904223)>>>0;
  return seed/4294967296;
};
const clamp=(v)=>Math.max(-1,Math.min(1,v));

const writeStereo=async(name,durationSec,fn)=>{
  const frames=Math.max(1,Math.floor(durationSec*sampleRate));
  const buffer=Buffer.alloc(frames*channels*2);
  for(let i=0;i<frames;i++){
    const t=i/sampleRate;
    const [l,r]=fn(t,i,frames);
    buffer.writeInt16LE(Math.round(clamp(l)*32767),(i*channels)*2);
    buffer.writeInt16LE(Math.round(clamp(r)*32767),(i*channels+1)*2);
  }
  const file=path.join(outDir,name);
  await new Promise((resolve,reject)=>{
    const writer=new wav.FileWriter(file,{channels,sampleRate,bitDepth:16});
    writer.on('finish',resolve);
    writer.on('error',reject);
    writer.end(buffer);
  });
  return {name,durationSec};
};

const env=(t,d,a=.012,r=.16)=>{
  const attack=Math.min(1,t/Math.max(.001,a));
  const release=Math.min(1,(d-t)/Math.max(.001,r));
  return Math.max(0,Math.min(attack,release,1));
};
const pan=(x,p)=>{
  const left=Math.sqrt((1-p)/2);
  const right=Math.sqrt((1+p)/2);
  return [x*left,x*right];
};
const tone=(freq,t)=>Math.sin(Math.PI*2*freq*t);

const assets=[];

assets.push(await writeStereo('ui-click.wav',.11,(t)=>{
  const e=env(t,.11,.003,.085);
  const x=(tone(1250,t)*.55+tone(790,t)*.25)*e*.42;
  return pan(x,-.08);
}));

assets.push(await writeStereo('scan-tick.wav',.12,(t)=>{
  const e=env(t,.12,.002,.095);
  const x=(tone(1040,t)*.7+tone(1560,t)*.18)*e*.34;
  return pan(x,.16);
}));

assets.push(await writeStereo('success.wav',.30,(t)=>{
  const first=t<.15?tone(660,t):0;
  const second=t>.085?tone(880,t-.085):0;
  const e=env(t,.30,.008,.20);
  const x=(first*.40+second*.34)*e;
  return pan(x,.10);
}));

assets.push(await writeStereo('error.wav',.34,(t)=>{
  const e=env(t,.34,.005,.25);
  const x=(tone(210,t)*.38+tone(146,t)*.22+tone(420,t)*.08)*e;
  return pan(x,-.06);
}));

assets.push(await writeStereo('approve.wav',.38,(t)=>{
  const e=env(t,.38,.005,.26);
  const x=(tone(520,t)*.23+tone(780,t)*.27+tone(1040,t)*.14)*e;
  return pan(x,.12);
}));

const whoosh=async(name,{duration=.62,panFrom=-.7,panTo=.7,brightness=1}={})=>{
  let low=0;
  return writeStereo(name,duration,(t)=>{
    const p=t/duration;
    const shape=Math.sin(Math.PI*p);
    const noise=(rand()*2-1);
    low=low*.86+noise*.14;
    const airy=(noise-low)*brightness;
    const tonal=tone(120+360*p,t)*.10;
    const x=(airy*.20+low*.13+tonal)*shape*.52;
    return pan(x,panFrom+(panTo-panFrom)*p);
  });
};

assets.push(await whoosh('whoosh-forward.wav',{panFrom:-.75,panTo:.75,brightness:1.15}));
assets.push(await whoosh('whoosh-rise.wav',{panFrom:0,panTo:.2,brightness:.85}));
assets.push(await whoosh('whoosh-mask.wav',{panFrom:.15,panTo:-.15,brightness:.65}));
assets.push(await whoosh('whoosh-aperture.wav',{panFrom:.55,panTo:0,brightness:.95}));

assets.push(await writeStereo('terminal-run.wav',.22,(t)=>{
  const e=env(t,.22,.004,.15);
  const x=(tone(360,t)*.15+tone(720,t)*.10+(rand()*2-1)*.035)*e;
  return pan(x,-.16);
}));

assets.push(await writeStereo('ambient-bed.wav',180,(t)=>{
  const swell=.55+.45*Math.sin(Math.PI*2*t/19);
  const x=(
    tone(110,t)*.018+
    tone(165,t)*.011+
    tone(220,t)*.006+
    tone(330,t)*.003
  )*swell;
  const l=x*(.96+.04*Math.sin(Math.PI*2*t/11));
  const r=x*(.96+.04*Math.cos(Math.PI*2*t/13));
  return [l,r];
}));

await fs.promises.writeFile(
  path.join(outDir,'manifest.json'),
  JSON.stringify({generatedAt:new Date().toISOString(),sampleRate,channels,assets},null,2),
);
console.log(`Generated ${assets.length} Creator OS V04 sound assets.`);
