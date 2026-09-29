import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {VIDEO} from '../tokens';
import {v01Scenes} from '../content/v01';
import {Caption} from '../components/Caption';
import {HeroHook} from '../components/HeroHook';
import {ProcessLoop} from '../components/ProcessLoop';
import {LayerStack} from '../components/LayerStack';
import {CodeEditor} from '../components/CodeEditor';
import {BrowserFrame} from '../components/BrowserFrame';
import {Checklist} from '../components/Checklist';
import {ComparisonSplit} from '../components/ComparisonSplit';
import {EpisodeEndcard} from '../components/EpisodeEndcard';
import {SceneMotion} from '../components/SceneMotion';

const scenes=[HeroHook,ProcessLoop,LayerStack,CodeEditor,BrowserFrame,Checklist,ComparisonSplit,EpisodeEndcard];

export const V01: React.FC = () => <AbsoluteFill>
  {v01Scenes.map((scene,i)=>{
    const Component=scenes[i];
    const from=Math.round(scene.startSec*VIDEO.fps);
    const durationInFrames=Math.round((scene.endSec-scene.startSec)*VIDEO.fps);
    return <Sequence key={scene.id} from={from} durationInFrames={durationInFrames} name={scene.id}>
      <SceneMotion><Component /></SceneMotion>
      <Caption text={scene.narration} emphasis={scene.captionEmphasis}/>
    </Sequence>;
  })}
</AbsoluteFill>;
