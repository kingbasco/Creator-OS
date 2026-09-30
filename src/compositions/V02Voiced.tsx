import React from 'react';
import {Audio} from '@remotion/media';
import {AbsoluteFill,staticFile} from 'remotion';
import {DesignCanvas} from '../components/DesignCanvas';
import {v02Audio} from '../generated/v02-audio';
import {v02VoicedTimeline} from '../content/v02-timeline';
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
  <DesignCanvas>
    <AbsoluteFill>
      <V02Flow
        timeline={v02VoicedTimeline}
        scenes={scenes}
        nameSuffix="-voiced"
        renderAudio={(scene)=>
          v02Audio.enabled&&scene.audioPath
            ? <Audio src={staticFile(scene.audioPath)}/>
            : null
        }
      />
    </AbsoluteFill>
  </DesignCanvas>
);
