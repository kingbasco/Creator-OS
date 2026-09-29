import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, SHADOW, TYPE} from '../tokens';
import {fadeInUp, clamp} from '../utils';

export const BrowserFrame: React.FC = () => {
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const fixed=frame>160;
 const cursorX=interpolate(frame,[40,90,130,160],[720,610,610,780],clamp); const cursorY=interpolate(frame,[40,90,130,160],[650,820,820,630],clamp);
 return <Frame>
   <div style={{fontSize:TYPE.sceneTitle,fontWeight:800,...fadeInUp(frame,fps)}}>RUN → INSPECT → <span style={{color:COLORS.accent}}>CORRECT</span></div>
   <div style={{marginTop:100,borderRadius:RADIUS.lg,background:COLORS.surface,border:`1px solid ${COLORS.border}`,boxShadow:SHADOW,overflow:'hidden',height:980}}>
     <div style={{height:78,borderBottom:`1px solid ${COLORS.border}`,display:'flex',alignItems:'center',gap:12,padding:'0 26px'}}>{[0,1,2].map(i=><span key={i} style={{width:14,height:14,borderRadius:99,background:COLORS.border}}/>)}</div>
     <div style={{padding:56}}>
      <div style={{fontSize:48,fontWeight:800}}>Reset your password</div>
      <div style={{fontSize:32,color:COLORS.muted,marginTop:16}}>Enter your email and we’ll send a reset link.</div>
      <div style={{marginTop:64,height:84,border:`2px solid ${fixed?COLORS.border:COLORS.danger}`,borderRadius:RADIUS.md,display:'flex',alignItems:'center',padding:'0 24px',fontSize:30,color:COLORS.muted}}>name@example.com</div>
      <div style={{marginTop:24,height:84,borderRadius:RADIUS.md,background:COLORS.accent,color:'white',display:'flex',alignItems:'center',justifyContent:'center',fontSize:32,fontWeight:800}}>Send reset link</div>
      {!fixed && <div style={{marginTop:16,fontSize:26,color:COLORS.danger}}>Issue: error state appears before submit</div>}
      {fixed && <div style={{marginTop:16,fontSize:26,color:COLORS.success}}>Corrected: validation waits for user action</div>}
     </div>
   </div>
   <div style={{position:'absolute',left:cursorX,top:cursorY,width:34,height:34,borderRadius:99,border:`5px solid ${COLORS.accent}`,boxShadow:`0 0 0 10px ${COLORS.accentSoft}`}}/>
 </Frame>;
};
