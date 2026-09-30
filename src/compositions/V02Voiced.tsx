import React from 'react';
import {Audio} from '@remotion/media';
import {AbsoluteFill,Sequence,staticFile} from 'remotion';
import {Caption} from '../components/Caption';
import {SceneMotion} from '../components/SceneMotion';
import {v02Audio} from '../generated/v02-audio';
import {v02VoicedTimeline} from '../content/v02-timeline';
import {
  AgentHook,
  GoalScene,
  InspectScene,
  PlanScene,
  ChangeScene,
  EvaluateScene,
  ReviewScene,
  MentalModelScene,
} from '../components/v02/AgentScenes';

const scenes=[
  AgentHook,
  GoalScene,
  InspectScene,
  PlanScene,
  ChangeScene,
  EvaluateScene,
  ReviewScene,
  MentalModelScene,
];

export const V02Voiced:React.FC=()=>(
  <AbsoluteFill>
    {v02VoicedTimeline.map((scene,i)=>{
      const Component=scenes[i];
      return <Sequence key={scene.id} from={scene.from} durationInFrames={scene.durationInFrames} name={`V02-${scene.id}-voiced`}>
        <SceneMotion durationInFrames={scene.durationInFrames}>
          <Component durationInFrames={scene.durationInFrames}/>
        </SceneMotion>
        {v02Audio.enabled&&scene.audioPath?<Audio src={staticFile(scene.audioPath)}/>:null}
        <Caption text={scene.captionText??scene.narration} emphasis={scene.captionEmphasis}/>
      </Sequence>;
    })}
  </AbsoluteFill>
);
