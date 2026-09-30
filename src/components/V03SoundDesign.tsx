import React from 'react';
import {Audio} from '@remotion/media';
import {Sequence, staticFile, interpolate} from 'remotion';
import {v03VoicedTimeline as timeline, V03_VOICED_TOTAL_FRAMES as total} from '../content/v03-timeline';

// Match each cue to an authored visual reveal. Narration stays dominant.
const cues = [
  {scene:0,offset:34,file:'success.wav',frames:9,volume:.07},
  {scene:2,offset:20,file:'error.wav',frames:11,volume:.06},
  {scene:3,offset:75,file:'approve.wav',frames:12,volume:.07},
  {scene:4,offset:24,file:'error.wav',frames:11,volume:.06},
  {scene:5,offset:25,file:'terminal-run.wav',frames:7,volume:.08},
  {scene:6,offset:96,file:'approve.wav',frames:12,volume:.08},
];
export const V03SoundDesign:React.FC=()=> <>
  <Sequence durationInFrames={total} name="V03-quiet-ambient-bed">
    <Audio src={staticFile('audio/v03-sfx/ambient-bed.wav')} loop
      volume={f=>.07*Math.min(interpolate(f,[0,30],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),interpolate(f,[Math.max(1,total-45),total],[1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}))}/>
  </Sequence>
  {timeline.slice(1).map((s,i)=><Sequence key={s.id} from={Math.max(0,s.from-18)} durationInFrames={19} name={`V03-transition-${s.id}`}>
    <Audio src={staticFile(`audio/v03-sfx/${i===2?'whoosh-mask.wav':'whoosh-rise.wav'}`)} volume={.07}/>
  </Sequence>)}
  {cues.filter(c=>c.offset+c.frames<timeline[c.scene].durationInFrames).map(c=><Sequence key={`${c.scene}-${c.offset}`} from={timeline[c.scene].from+c.offset} durationInFrames={c.frames} name={`V03-cue-${c.scene}-${c.file}`}>
    <Audio src={staticFile(`audio/v03-sfx/${c.file}`)} volume={c.volume}/>
  </Sequence>)}
</>;
