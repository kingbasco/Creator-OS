import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {DEFAULT_MODEL, synthesizeSpeech} from './lib/gemini-tts.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const dryRun=process.argv.includes('--dry-run');

const excerpt=[
  'You’ve probably heard someone say, “I built this app without coding.”',
  'But that isn’t really what happened.',
  'Instead of typing every line, you describe the intent.',
  'The AI proposes a change.',
  'You run it.',
  'You inspect what happened.',
  'Then you correct the direction.',
  'That loop can be incredibly fast.',
  'But speed doesn’t remove responsibility.',
].join(' ');

const auditions=[
  {
    voice:'Sulafat',
    label:'Warm editorial',
    direction:'Warm and composed. Friendly without sounding casual. Around 150 words per minute.',
  },
  {
    voice:'Sadaltager',
    label:'Knowledgeable tech creator',
    direction:'Knowledgeable and assured. Slightly sharper on the hook, then measured and conversational.',
  },
  {
    voice:'Iapetus',
    label:'Clear documentary',
    direction:'Clear, calm, precise, and lightly reflective. Keep the technical phrases effortless.',
  },
];

if(dryRun){
  console.log(JSON.stringify({model:DEFAULT_MODEL,auditions,excerpt},null,2));
  process.exit(0);
}

const outputDir=path.join(root,'out','voice-auditions');
await fs.promises.mkdir(outputDir,{recursive:true});
const manifest=[];

for(const audition of auditions){
  const filename=`${audition.voice.toLowerCase()}-v01-audition.wav`;
  const outputPath=path.join(outputDir,filename);
  console.log(`Generating ${audition.label} (${audition.voice})...`);
  const result=await synthesizeSpeech({
    text:excerpt,
    voice:audition.voice,
    outputPath,
    sceneDirection:audition.direction,
  });
  manifest.push({...audition,filename,durationSec:Number(result.durationSec.toFixed(3)),model:result.model});
}

await fs.promises.writeFile(
  path.join(outputDir,'manifest.json'),
  JSON.stringify({generatedAt:new Date().toISOString(),model:DEFAULT_MODEL,auditions:manifest},null,2),
);

console.log(`Created ${manifest.length} voice auditions in ${outputDir}`);
