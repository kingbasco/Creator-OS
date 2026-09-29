import React from 'react';
import {Audio} from '@remotion/media';
import {AbsoluteFill, Sequence, staticFile} from 'remotion';
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
import {v01Audio} from '../generated/v01-audio';
import {v01VoicedTimeline} from '../content/v01-timeline';

const scenes=[
  HeroHook,
  ProcessLoop,
  LayerStack,
  CodeEditor,
  BrowserFrame,
  Checklist,
  ComparisonSplit,
  EpisodeEndcard,
];

export const V01Voiced: React.FC = () => (
  <AbsoluteFill>
    {v01VoicedTimeline.map((scene,i)=>{
      const Component=scenes[i];
      return (
        <Sequence key={scene.id} from={scene.from} durationInFrames={scene.durationInFrames} name={`${scene.id}-voiced`}>
          <SceneMotion durationInFrames={scene.durationInFrames}>
            <Component />
          </SceneMotion>
          {v01Audio.enabled && scene.audioPath ? <Audio src={staticFile(scene.audioPath)} /> : null}
          <Caption text={scene.captionText ?? scene.narration} emphasis={scene.captionEmphasis}/>
        </Sequence>
      );
    })}
  </AbsoluteFill>
);
