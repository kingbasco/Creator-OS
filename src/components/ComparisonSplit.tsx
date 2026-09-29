import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {fadeInUp} from '../utils';
import {FloatingCard} from './FloatingCard';
import {MotionBackdrop} from './MotionBackdrop';

const ai=['Edit files','Run commands','Run tests']; const human=['Decide intent','Verify result','Own the ship gate'];
export const ComparisonSplit: React.FC = () => {const frame=useCurrentFrame(); const {fps}=useVideoConfig(); return <Frame>
 <MotionBackdrop/>
 <div style={{fontSize:TYPE.sceneTitle,fontWeight:850,...fadeInUp(frame,fps)}}>AI CAN EXECUTE.<br/><span style={{color:COLORS.accent}}>YOU STILL DECIDE.</span></div>
 <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:26,marginTop:100}}>
  {[['AI',ai,COLORS.darkSurface,'white'],['YOU',human,COLORS.surface,COLORS.foreground]].map(([title,arr,bg,fg])=><div key={title as string} style={{minHeight:850,padding:34,borderRadius:RADIUS.lg,background:bg as string,color:fg as string,border:`1px solid ${title==='YOU'?COLORS.border:'transparent'}`}}>
    <div style={{fontSize:38,fontWeight:900,color:title==='AI'?'#AAB4FF':COLORS.accent}}>{title as string}</div>
    <div style={{marginTop:44,display:'grid',gap:22}}>{(arr as string[]).map((x,i)=><div key={x} style={{padding:'28px 24px',borderRadius:RADIUS.md,background:title==='AI'?'#1B1F28':'#F8F9FB',border:`1px solid ${title==='AI'?'#2A303C':COLORS.border}`,fontSize:34,fontWeight:700}}>{i+1}. {x}</div>)}</div>
  </div>)}
 </div>
 <FloatingCard x={390} y={1260} width={300} delay={60} rotate={0} dark><div style={{fontSize:24,fontWeight:800,color:'#AAB4FF'}}>FINAL GATE</div><div style={{fontSize:38,fontWeight:900,marginTop:8}}>BUILD → SHIP?</div></FloatingCard>
 </Frame>};
