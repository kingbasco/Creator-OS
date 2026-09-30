import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import wav from 'wav';
import {DEFAULT_MODEL, SAMPLE_RATE, CHANNELS, SAMPLE_WIDTH_BYTES, synthesizeSpeech} from './lib/gemini-tts.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const dryRun=process.argv.includes('--dry-run');
const voice=process.env.GEMINI_TTS_VOICE || 'Sulafat';
const fallbackModel=process.env.GEMINI_TTS_FALLBACK_MODEL || 'gemini-3.8-flash-tts';

const sourcePath=path.join(root,'src','content','v02.json');
const scenes=JSON.parse(await fs.promises.readFile(sourcePath,'utf8'));

if(!Array.isArray(scenes) || scenes.length!==8){
  throw new Error('V02 voice generation expects exactly 8 scene records.');
}

const words=(value='')=>value.trim().split(/\s+/).filter(Boolean).length;

const extractPcmFromWav=(buffer)=>{
  let offset=12;
  while(offset+8<=buffer.length){
    const id=buffer.toString('ascii',offset,offset+4);
    const size=buffer.readUInt32LE(offset+4);
    if(id==='data'){
      return buffer.subarray(offset+8,offset+8+size);
    }
    offset+=8+size+(size%2);
  }
  throw new Error('Unable to locate PCM data chunk in generated WAV.');
};

const saveWaveFile=async(filename,pcmData)=>{
  await fs.promises.mkdir(path.dirname(filename),{recursive:true});
  await new Promise((resolve,reject)=>{
    const writer=new wav.FileWriter(filename,{
      channels:CHANNELS,
      sampleRate:SAMPLE_RATE,
      bitDepth:SAMPLE_WIDTH_BYTES*8,
    });
    writer.on('finish',resolve);
    writer.on('error',reject);
    writer.write(pcmData);
    writer.end();
  });
};

const rmsAt=(pcm,centerSample,windowSamples)=>{
  const start=Math.max(0,centerSample-Math.floor(windowSamples/2));
  const end=Math.min(Math.floor(pcm.length/2),start+windowSamples);
  let sum=0;
  let count=0;
  for(let i=start;i<end;i++){
    const value=pcm.readInt16LE(i*2);
    sum+=value*value;
    count++;
  }
  return count?Math.sqrt(sum/count):Number.POSITIVE_INFINITY;
};

const findSplitSample=(pcm,firstText,secondText)=>{
  const totalSamples=Math.floor(pcm.length/2);
  const firstWords=Math.max(1,words(firstText));
  const secondWords=Math.max(1,words(secondText));
  const expectedRatio=firstWords/(firstWords+secondWords);
  const expected=Math.round(totalSamples*expectedRatio);
  const radius=Math.round(totalSamples*0.18);
  const min=Math.max(Math.round(totalSamples*0.22),expected-radius);
  const max=Math.min(Math.round(totalSamples*0.78),expected+radius);
  const windowSamples=Math.round(SAMPLE_RATE*0.055);
  const step=Math.max(1,Math.round(SAMPLE_RATE*0.0125));

  let best=expected;
  let bestScore=Number.POSITIVE_INFINITY;

  for(let center=min;center<=max;center+=step){
    const rms=rmsAt(pcm,center,windowSamples);
    const distance=Math.abs(center-expected)/Math.max(1,radius);
    const score=rms*(1+distance*0.22);
    if(score<bestScore){
      bestScore=score;
      best=center;
    }
  }

  return best;
};

if(dryRun){
  console.log(JSON.stringify({
    model:DEFAULT_MODEL,
    voice,
    requestCount:4,
    strategy:'paired scenes with inline pause + silence-aware PCM split',
    pairs:[0,2,4,6].map((i)=>({
      ids:[scenes[i].id,scenes[i+1].id],
      text:`${scenes[i].narration} <short pause><short pause> ${scenes[i+1].narration}`,
    })),
  },null,2));
  process.exit(0);
}

const publicDir=path.join(root,'public','audio','v02');
const tempDir=path.join(root,'out','voice-temp-v02');
await fs.promises.rm(publicDir,{recursive:true,force:true});
await fs.promises.rm(tempDir,{recursive:true,force:true});
await fs.promises.mkdir(publicDir,{recursive:true});
await fs.promises.mkdir(tempDir,{recursive:true});

const generated=[];
const modelsUsed=new Set();
let activeModel=DEFAULT_MODEL;

const isRateLimit=(error)=>error?.status===429||error?.statusCode===429||String(error?.message||'').includes('429');

for(let i=0;i<scenes.length;i+=2){
  const first=scenes[i];
  const second=scenes[i+1];
  const pairIndex=i/2+1;
  const pairPath=path.join(tempDir,`pair-${pairIndex}.wav`);
  const pairText=`${first.narration} <short pause><short pause> ${second.narration}`;
  const pairDirection=[
    'Read the transcript verbatim.',
    `First paragraph: ${first.voiceDirection||'Keep the established Creator OS narration style.'}`,
    'Honor the inline short-pause tags as a clean silent transition between paragraphs.',
    `Second paragraph: ${second.voiceDirection||'Keep the established Creator OS narration style.'}`,
    'Do not speak scene numbers, labels, stage directions, or pause tags.',
  ].join(' ');

  console.log(`Generating ${first.id} + ${second.id} with ${voice} on ${activeModel}...`);
  try{
    await synthesizeSpeech({
      text:pairText,
      voice,
      outputPath:pairPath,
      sceneDirection:pairDirection,
      model:activeModel,
    });
  }catch(error){
    if(activeModel!==fallbackModel&&isRateLimit(error)){
      console.log(`Primary TTS quota reached. Switching remaining V02 generation to ${fallbackModel}.`);
      activeModel=fallbackModel;
      await synthesizeSpeech({
        text:pairText,
        voice,
        outputPath:pairPath,
        sceneDirection:pairDirection,
        model:activeModel,
      });
    }else{
      throw error;
    }
  }
  modelsUsed.add(activeModel);

  const wavBuffer=await fs.promises.readFile(pairPath);
  const pcm=extractPcmFromWav(wavBuffer);
  const splitSample=findSplitSample(pcm,first.narration,second.narration);
  const splitByte=splitSample*SAMPLE_WIDTH_BYTES;
  const firstPcm=pcm.subarray(0,splitByte);
  const secondPcm=pcm.subarray(splitByte);

  const parts=[
    {scene:first,pcm:firstPcm},
    {scene:second,pcm:secondPcm},
  ];

  for(const part of parts){
    const filename=`${part.scene.id}.wav`;
    const outputPath=path.join(publicDir,filename);
    await saveWaveFile(outputPath,part.pcm);
    generated.push({
      id:part.scene.id,
      path:`audio/v02/${filename}`,
      durationSec:Number((part.pcm.byteLength/(SAMPLE_RATE*CHANNELS*SAMPLE_WIDTH_BYTES)).toFixed(3)),
    });
  }
}

generated.sort((a,b)=>a.id.localeCompare(b.id));

const manifestTs=`import type {SceneId} from '../types';

export type GeneratedSceneAudio = {
  id: SceneId;
  path: string;
  durationSec: number;
};

export const v02Audio = ${JSON.stringify({
  enabled:true,
  provider:'gemini',
  model:Array.from(modelsUsed).join(' + ')||DEFAULT_MODEL,
  voice,
  generatedAt:new Date().toISOString(),
  scenes:generated,
},null,2)} as const;
`;

await fs.promises.writeFile(
  path.join(root,'src','generated','v02-audio.ts'),
  manifestTs,
);

await fs.promises.writeFile(
  path.join(publicDir,'manifest.json'),
  JSON.stringify({
    generatedAt:new Date().toISOString(),
    provider:'gemini',
    model:Array.from(modelsUsed).join(' + ')||DEFAULT_MODEL,
    modelsUsed:Array.from(modelsUsed),
    voice,
    requestsUsed:4,
    splitStrategy:'paired scenes with inline pause + silence-aware PCM split',
    scenes:generated,
    totalSpeechSec:Number(generated.reduce((sum,item)=>sum+item.durationSec,0).toFixed(3)),
  },null,2),
);

await fs.promises.rm(tempDir,{recursive:true,force:true});
console.log(`Generated all V02 voice scenes with ${voice} in 4 TTS requests.`);
