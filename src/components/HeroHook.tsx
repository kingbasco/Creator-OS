import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate, Easing} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, SHADOW, TYPE} from '../tokens';
import {fadeInUp, clamp} from '../utils';
import {FloatingCard} from './FloatingCard';
import {ArrowCallout} from './ArrowCallout';
import {MotionBackdrop} from './MotionBackdrop';

export const HeroHook: React.FC = () => {
  const frame=useCurrentFrame(); const {fps}=useVideoConfig();
  const strike = interpolate(frame,[60,76],[0,100],{...clamp,easing:Easing.out(Easing.cubic)});
  const appScale = interpolate(frame,[0,25],[0.97,1],clamp);
  return <Frame>
    <MotionBackdrop/>
    <FloatingCard x={675} y={250} width={260} delay={8} rotate={5}><div style={{fontSize:28,fontWeight:800,color:COLORS.accent}}>PROMPT</div><div style={{fontSize:24,marginTop:8}}>Build a dashboard</div></FloatingCard>
    <FloatingCard x={80} y={250} width={240} delay={18} rotate={-5}><div style={{fontSize:28,fontWeight:800}}>UI</div><div style={{fontSize:24,marginTop:8,color:COLORS.muted}}>Generated screen</div></FloatingCard>
    <div style={{position:'absolute', inset:140, borderRadius:RADIUS.lg, background:COLORS.surface, boxShadow:SHADOW, opacity:.65, transform:`scale(${appScale})`}}>
      <div style={{height:74,borderBottom:`1px solid ${COLORS.border}`,display:'flex',alignItems:'center',gap:12,padding:'0 26px'}}>
        {[0,1,2].map(i=><span key={i} style={{width:13,height:13,borderRadius:99,background:COLORS.border}}/>)}
      </div>
      <div style={{padding:48,display:'grid',gridTemplateColumns:'1fr 1fr',gap:28}}>
        <div style={{height:420,borderRadius:RADIUS.md,background:'#EEF1F6'}}/>
        <div style={{display:'grid',gap:22}}>{[0,1,2].map(i=><div key={i} style={{height:120,borderRadius:RADIUS.md,background:'#F0F2F5'}}/>)}</div>
      </div>
    </div>
    <ArrowCallout label="AI-generated UI" from={{x:760,y:430}} to={{x:650,y:610}} delay={30}/>
    <div style={{position:'relative',zIndex:2,marginTop:480,...fadeInUp(frame,fps,0,14)}}>
      <div style={{fontSize:TYPE.hero,fontWeight:800,lineHeight:.96,letterSpacing:-4}}>I BUILT THIS APP</div>
      <div style={{fontSize:TYPE.hero,fontWeight:800,lineHeight:.96,letterSpacing:-4,marginTop:18,position:'relative',display:'inline-block'}}>
        WITHOUT CODING
        <span style={{position:'absolute',left:0,top:'51%',height:12,width:`${strike}%`,background:COLORS.accent,borderRadius:20}}/>
      </div>
      <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,marginTop:38,color:COLORS.accent,opacity:interpolate(frame,[76,92],[0,1],clamp)}}>WITH AI.</div>
    </div>
  </Frame>;
};
