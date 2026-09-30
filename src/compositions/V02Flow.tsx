import React from 'react';
import {Sequence} from 'remotion';
import {Caption} from '../components/Caption';
import {TransitionScene,type TransitionKind} from '../components/TransitionScene';
import type {SceneSpec} from '../types';
import type {V02SceneProps} from '../components/v02/AgentScenes';

export const V02_TRANSITION_FRAMES=18;

export const V02_TRANSITIONS:TransitionKind[]=[
  'camera-push',
  'repo-handoff',
  'plan-compress',
  'dark-mask',
  'terminal-flow',
  'review-aperture',
  'system-sweep',
];

type TimelineScene=SceneSpec&{
  from:number;
  durationInFrames:number;
  audioPath?:string|null;
};

type Props={
  timeline:TimelineScene[];
  scenes:Array<React.FC<V02SceneProps>>;
  renderAudio?:(scene:TimelineScene)=>React.ReactNode;
  nameSuffix?:string;
};

export const V02Flow:React.FC<Props>=({timeline,scenes,renderAudio,nameSuffix=''})=><>
  {timeline.map((scene,i)=>{
    const Component=scenes[i];
    const enterFrames=i===0?0:V02_TRANSITION_FRAMES;
    const exitFrames=i===timeline.length-1?0:V02_TRANSITION_FRAMES;
    const visualFrom=Math.max(0,scene.from-enterFrames);
    const visualDuration=scene.durationInFrames+enterFrames+exitFrames;
    const visualSceneDuration=scene.durationInFrames+enterFrames;

    return <React.Fragment key={scene.id}>
      <Sequence
        from={visualFrom}
        durationInFrames={visualDuration}
        name={`V02-${scene.id}-visual${nameSuffix}`}
      >
        <TransitionScene
          enterFrames={enterFrames}
          baseDurationInFrames={scene.durationInFrames}
          exitFrames={exitFrames}
          enterKind={i===0?'none':V02_TRANSITIONS[i-1]}
          exitKind={i===timeline.length-1?'none':V02_TRANSITIONS[i]}
          zIndex={i+1}
        >
          <Component durationInFrames={visualSceneDuration} frameOffset={0}/>
        </TransitionScene>
      </Sequence>

      <Sequence
        from={scene.from}
        durationInFrames={scene.durationInFrames}
        name={`V02-${scene.id}-content${nameSuffix}`}
      >
        {renderAudio?renderAudio(scene):null}
        <Caption text={scene.captionText??scene.narration} emphasis={scene.captionEmphasis}/>
      </Sequence>
    </React.Fragment>;
  })}
</>;
