import React from 'react';
import {Audio} from '@remotion/media';
import {Sequence,staticFile} from 'remotion';
import {VIDEO} from '../tokens';
import {v02VoicedTimeline,V02_VOICED_TOTAL_FRAMES} from '../content/v02-timeline';
import {V02_TRANSITION_FRAMES} from '../compositions/V02Flow';

type Cue={
  name:string;
  path:string;
  from:number;
  durationSec:number;
  volume:number;
};

const sec=(value:number)=>Math.round(value*VIDEO.fps);

const sceneFrom=(index:number)=>v02VoicedTimeline[index]?.from??0;
const cue=(name:string,path:string,from:number,durationSec:number,volume:number):Cue=>({
  name,path,from:Math.max(0,Math.round(from)),durationSec,volume,
});

const transitionFiles=[
  'whoosh-forward.wav',
  'whoosh-forward.wav',
  'whoosh-rise.wav',
  'whoosh-mask.wav',
  'whoosh-rise.wav',
  'whoosh-aperture.wav',
  'whoosh-forward.wav',
];

const transitionCues: Cue[]=transitionFiles.map((file,i)=>
  cue(
    `transition-${i+1}`,
    `audio/v02-sfx/${file}`,
    sceneFrom(i+1)-V02_TRANSITION_FRAMES,
    .62,
    i===3?.16:.13,
  )
);

const detailCues:Cue[]=[
  cue('hook-accent','audio/v02-sfx/ui-click.wav',sceneFrom(0)+sec(.55),.11,.13),
  cue('goal-lock','audio/v02-sfx/approve.wav',sceneFrom(0)+sec(3.35),.38,.08),

  cue('task-open','audio/v02-sfx/ui-click.wav',sceneFrom(1)+sec(.55),.11,.11),
  cue('repo-scan-1','audio/v02-sfx/scan-tick.wav',sceneFrom(1)+sec(3.2),.12,.08),
  cue('repo-scan-2','audio/v02-sfx/scan-tick.wav',sceneFrom(1)+sec(4.25),.12,.08),
  cue('repo-scan-3','audio/v02-sfx/scan-tick.wav',sceneFrom(1)+sec(5.3),.12,.08),

  cue('inspect-1','audio/v02-sfx/scan-tick.wav',sceneFrom(2)+sec(1.35),.12,.08),
  cue('inspect-2','audio/v02-sfx/scan-tick.wav',sceneFrom(2)+sec(2.55),.12,.08),
  cue('inspect-3','audio/v02-sfx/scan-tick.wav',sceneFrom(2)+sec(3.75),.12,.08),

  cue('plan-1','audio/v02-sfx/ui-click.wav',sceneFrom(3)+sec(1.25),.11,.075),
  cue('plan-2','audio/v02-sfx/ui-click.wav',sceneFrom(3)+sec(2.15),.11,.07),
  cue('plan-3','audio/v02-sfx/ui-click.wav',sceneFrom(3)+sec(3.05),.11,.065),
  cue('plan-4','audio/v02-sfx/approve.wav',sceneFrom(3)+sec(4.0),.38,.07),

  cue('change-file-1','audio/v02-sfx/scan-tick.wav',sceneFrom(4)+sec(1.0),.12,.065),
  cue('change-file-2','audio/v02-sfx/scan-tick.wav',sceneFrom(4)+sec(1.8),.12,.065),
  cue('change-file-3','audio/v02-sfx/scan-tick.wav',sceneFrom(4)+sec(2.6),.12,.065),

  cue('terminal-run','audio/v02-sfx/terminal-run.wav',sceneFrom(5)+sec(.9),.22,.12),
  cue('test-pass-1','audio/v02-sfx/success.wav',sceneFrom(5)+sec(2.0),.30,.06),
  cue('test-pass-2','audio/v02-sfx/success.wav',sceneFrom(5)+sec(2.8),.30,.06),
  cue('test-fail','audio/v02-sfx/error.wav',sceneFrom(5)+sec(4.15),.34,.095),
  cue('evaluate-loop','audio/v02-sfx/whoosh-mask.wav',sceneFrom(5)+sec(6.25),.62,.085),

  cue('review-build','audio/v02-sfx/success.wav',sceneFrom(6)+sec(1.1),.30,.055),
  cue('review-tests','audio/v02-sfx/success.wav',sceneFrom(6)+sec(1.8),.30,.055),
  cue('review-diff','audio/v02-sfx/success.wav',sceneFrom(6)+sec(2.5),.30,.055),
  cue('human-gate','audio/v02-sfx/approve.wav',sceneFrom(6)+sec(5.0),.38,.105),

  cue('summary-1','audio/v02-sfx/scan-tick.wav',sceneFrom(7)+sec(1.3),.12,.05),
  cue('summary-2','audio/v02-sfx/scan-tick.wav',sceneFrom(7)+sec(1.75),.12,.05),
  cue('summary-3','audio/v02-sfx/scan-tick.wav',sceneFrom(7)+sec(2.2),.12,.05),
  cue('summary-4','audio/v02-sfx/scan-tick.wav',sceneFrom(7)+sec(2.65),.12,.05),
  cue('summary-5','audio/v02-sfx/scan-tick.wav',sceneFrom(7)+sec(3.1),.12,.05),
  cue('summary-6','audio/v02-sfx/scan-tick.wav',sceneFrom(7)+sec(3.55),.12,.05),
  cue('summary-review','audio/v02-sfx/approve.wav',sceneFrom(7)+sec(4.0),.38,.07),
];

export const V02SoundDesign:React.FC=()=>{
  const cues=[...transitionCues,...detailCues];
  return <>
    <Sequence from={0} durationInFrames={V02_VOICED_TOTAL_FRAMES} name="V02-ambient-bed">
      <Audio src={staticFile('audio/v02-sfx/ambient-bed.wav')} volume={.10}/>
    </Sequence>
    {cues.map((item)=>(
      <Sequence
        key={item.name}
        from={item.from}
        durationInFrames={Math.max(1,sec(item.durationSec))}
        name={`V02-sfx-${item.name}`}
      >
        <Audio src={staticFile(item.path)} volume={item.volume}/>
      </Sequence>
    ))}
  </>;
};
