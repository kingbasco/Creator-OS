import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {DEFAULT_MODEL, synthesizeSpeech} from './lib/gemini-tts.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const dryRun=process.argv.includes('--dry-run');
const voice=process.env.GEMINI_TTS_VOICE || 'Sulafat';

const sourcePath=path.join(root,'src','content','v01.json');
const scenes=JSON.parse(await fs.promises.readFile(sourcePath,'utf8'));

if(!Array.isArray(scenes) || scenes.length!==8){
  throw new Error('V01 voice generation expects exactly 8 scene records.');
}

if(dryRun){
  console.log(JSON.stringify({
    model:DEFAULT_MODEL,
    voice,
    scenes:scenes.map(({id,narration,voiceDirection})=>({id,narration,voiceDirection})),
  },null,2));
  process.exit(0);
}

const publicDir=path.join(root,'public','audio','v01');
await fs.promises.rm(publicDir,{recursive:true,force:true});
await fs.promises.mkdir(publicDir,{recursive:true});

const generated=[];

for(const scene of scenes){
  const filename=`${scene.id}.wav`;
  const outputPath=path.join(publicDir,filename);
  console.log(`Generating ${scene.id} with ${voice}...`);
  const result=await synthesizeSpeech({
    text:scene.narration,
    voice,
    outputPath,
    sceneDirection:scene.voiceDirection || '',
  });
  generated.push({
    id:scene.id,
    path:`audio/v01/${filename}`,
    durationSec:Number(result.durationSec.toFixed(3)),
  });
}

const manifestTs=`import type {SceneId} from '../types';

export type GeneratedSceneAudio = {
  id: SceneId;
  path: string;
  durationSec: number;
};

export const v01Audio = ${JSON.stringify({
  enabled:true,
  provider:'gemini',
  model:DEFAULT_MODEL,
  voice,
  generatedAt:new Date().toISOString(),
  scenes:generated,
},null,2)} as const;
`;

await fs.promises.writeFile(
  path.join(root,'src','generated','v01-audio.ts'),
  manifestTs,
);

await fs.promises.writeFile(
  path.join(publicDir,'manifest.json'),
  JSON.stringify({
    generatedAt:new Date().toISOString(),
    provider:'gemini',
    model:DEFAULT_MODEL,
    voice,
    scenes:generated,
    totalSpeechSec:Number(generated.reduce((sum,item)=>sum+item.durationSec,0).toFixed(3)),
  },null,2),
);

console.log(`Generated all V01 voice scenes with ${voice}.`);
