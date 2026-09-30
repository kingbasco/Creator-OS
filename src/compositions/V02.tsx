import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {VIDEO} from '../tokens';
import {v02Scenes} from '../content/v02';
import {Caption} from '../components/Caption';
import {SceneMotion} from '../components/SceneMotion';
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

const scenes=[AgentHook,GoalScene,InspectScene,PlanScene,ChangeScene,EvaluateScene,ReviewScene,MentalModelScene];

export const V02:React.FC=()=>(
  <AbsoluteFill>
    {v02Scenes.map((scene,i)=>{
      const Component=scenes[i];
      const from=Math.round(scene.startSec*VIDEO.fps);
      const durationInFrames=Math.round((scene.endSec-scene.startSec)*VIDEO.fps);
      return <Sequence key={scene.id} from={from} durationInFrames={durationInFrames} name={`V02-${scene.id}`}>
        <SceneMotion durationInFrames={durationInFrames}>
          <Component durationInFrames={durationInFrames}/>
        </SceneMotion>
        <Caption text={scene.captionText ?? scene.narration} emphasis={scene.captionEmphasis}/>
      </Sequence>;
    })}
  </AbsoluteFill>
);
