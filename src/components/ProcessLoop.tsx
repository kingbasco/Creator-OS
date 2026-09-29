import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {fadeInUp, springScale} from '../utils';

const steps=[['PROMPT','Describe intent'],['CODE','AI edits'],['RUN','Execute'],['ERROR','Inspect'],['PROMPT','Correct']];
export const ProcessLoop: React.FC = () => {
  const frame=useCurrentFrame(); const {fps}=useVideoConfig();
  return <Frame>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:800,lineHeight:1.02,...fadeInUp(frame,fps)}}>THE LOOP BEHIND<br/><span style={{color:COLORS.accent}}>VIBE CODING</span></div>
    <div style={{marginTop:150,display:'grid',gap:25}}>
      {steps.map((s,i)=>{
        const scale=springScale(frame,fps,i*10);
        return <div key={`${s[0]}-${i}`} style={{transform:`scale(${scale})`,display:'grid',gridTemplateColumns:'210px 1fr',alignItems:'center',gap:24,padding:'28px 30px',background:COLORS.surface,border:`1px solid ${COLORS.border}`,borderRadius:RADIUS.md}}>
          <div style={{fontSize:TYPE.label,fontWeight:800,color:i===3?COLORS.danger:COLORS.accent}}>{s[0]}</div>
          <div style={{fontSize:TYPE.support,fontWeight:600}}>{s[1]}</div>
        </div>;
      })}
    </div>
  </Frame>;
};
