import React from 'react';
import {AbsoluteFill} from 'remotion';
import {VIDEO} from '../tokens';
import {v02Scenes} from '../content/v02';
import {DesignCanvas} from '../components/DesignCanvas';
import {V02Flow} from './V02Flow';
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

const timeline=v02Scenes.map((scene)=>({
  ...scene,
  from:Math.round(scene.startSec*VIDEO.fps),
  durationInFrames:Math.round((scene.endSec-scene.startSec)*VIDEO.fps),
}));

export const V02:React.FC=()=>(
  <DesignCanvas>
    <AbsoluteFill>
      <V02Flow timeline={timeline} scenes={scenes}/>
    </AbsoluteFill>
  </DesignCanvas>
);
