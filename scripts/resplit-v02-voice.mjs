import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import wav from 'wav';
import {SAMPLE_RATE, CHANNELS, SAMPLE_WIDTH_BYTES} from './lib/gemini-tts.mjs';
import {findSceneBoundary} from './lib/audio-split.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const scenes=JSON.parse(await fs.promises.readFile(path.join(root,'src','content','v02.json'),'utf8'));
const audioDir=path.join(root,'public','audio','v02');
const manifestPath=path.join(audioDir,'manifest.json');
const manifest=JSON.parse(await fs.promises.readFile(manifestPath,'utf8'));

const readPcm=async(filePath)=>{
  const buffer=await fs.promises.readFile(filePath);
  let offset=12;
  while(offset+8<=buffer.length){
    const id=buffer.toString('ascii',offset,offset+4);
    const size=buffer.readUInt32LE(offset+4);
    if(id==='data') return buffer.subarray(offset+8,Math.min(buffer.length,offset+8+size));
    offset+=8+size+(size%2);
  }
  throw new Error(`No PCM data chunk in ${filePath}`);
};

const saveWave=async(filePath,pcm)=>{
  await new Promise((resolve,reject)=>{
    const writer=new wav.FileWriter(filePath,{channels:CHANNELS,sampleRate:SAMPLE_RATE,bitDepth:SAMPLE_WIDTH_BYTES*8});
    writer.on('finish',resolve);
    writer.on('error',reject);
    writer.write(pcm);
    writer.end();
  });
};

const qa=[];

for(let i=0;i<scenes.length;i+=2){
  const first=scenes[i];
  const second=scenes[i+1];
  const firstPath=path.join(audioDir,`${first.id}.wav`);
  const secondPath=path.join(audioDir,`${second.id}.wav`);
  const pair=Buffer.concat([await readPcm(firstPath),await readPcm(secondPath)]);
  const alignment=findSceneBoundary(pair,first.narration,second.narration);
  const splitByte=alignment.splitSample*SAMPLE_WIDTH_BYTES;
  const firstPcm=pair.subarray(0,splitByte);
  const secondPcm=pair.subarray(splitByte);
  await saveWave(firstPath,firstPcm);
  await saveWave(secondPath,secondPcm);
  qa.push({
    pair:`${first.id}+${second.id}`,
    expectedSec:Number(alignment.expectedSec.toFixed(3)),
    splitSec:Number((alignment.splitSample/SAMPLE_RATE).toFixed(3)),
    silenceDurationSec:alignment.selected?Number(alignment.selected.durationSec.toFixed(3)):null,
    fallback:alignment.fallback,
  });
}

const generated=[];
for(const scene of scenes){
  const pcm=await readPcm(path.join(audioDir,`${scene.id}.wav`));
  generated.push({
    id:scene.id,
    path:`audio/v02/${scene.id}.wav`,
    durationSec:Number((pcm.byteLength/(SAMPLE_RATE*CHANNELS*SAMPLE_WIDTH_BYTES)).toFixed(3)),
  });
}

manifest.scenes=generated;
manifest.totalSpeechSec=Number(generated.reduce((sum,item)=>sum+item.durationSec,0).toFixed(3));
manifest.splitStrategy='paired TTS + inline pause + nearest-silence alignment v2';
manifest.alignmentQA=qa;
manifest.retimedAt=new Date().toISOString();
await fs.promises.writeFile(manifestPath,JSON.stringify(manifest,null,2));

const manifestTs=`import type {SceneId} from '../types';

export type GeneratedSceneAudio = {
  id: SceneId;
  path: string;
  durationSec: number;
};

export const v02Audio = ${JSON.stringify({
  enabled:true,
  provider:manifest.provider,
  model:manifest.model,
  voice:manifest.voice,
  generatedAt:manifest.generatedAt,
  scenes:generated,
},null,2)} as const;
`;

await fs.promises.writeFile(path.join(root,'src','generated','v02-audio.ts'),manifestTs);
console.log(JSON.stringify({qa,scenes:generated,totalSpeechSec:manifest.totalSpeechSec},null,2));
