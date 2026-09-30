import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const manifestPath=path.join(root,'public','audio','v02','manifest.json');
const manifest=JSON.parse(await fs.promises.readFile(manifestPath,'utf8'));

if(!Array.isArray(manifest.scenes)||manifest.scenes.length!==8){
  throw new Error('V02 audio manifest must contain exactly 8 scenes.');
}

const content=`import type {SceneId} from '../types';

export type GeneratedSceneAudio = {
  id: SceneId;
  path: string;
  durationSec: number;
};

export const v02Audio = ${JSON.stringify({
  enabled:true,
  provider:manifest.provider||'gemini',
  model:manifest.model||'gemini-3.8-flash-tts',
  voice:manifest.voice||'Sulafat',
  generatedAt:manifest.generatedAt||null,
  scenes:manifest.scenes,
},null,2)} as const;
`;

await fs.promises.writeFile(
  path.join(root,'src','generated','v02-audio.ts'),
  content,
);
console.log(`Hydrated V02 audio timing for ${manifest.scenes.length} scenes.`);
