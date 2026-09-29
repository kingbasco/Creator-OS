import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {fadeInUp, clamp} from '../utils';

const items=['Works','Correct','Secure','Ready to ship'];
export const Checklist: React.FC = () => {
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const meter=interpolate(frame,[0,70],[0,100],clamp);
 return <Frame>
  <div style={{fontSize:TYPE.hero,fontWeight:850,lineHeight:.95,...fadeInUp(frame,fps)}}>FAST<br/><span style={{color:COLORS.accent}}>≠ FINISHED</span></div>
  <div style={{marginTop:120}}>
    <div style={{fontSize:TYPE.label,fontWeight:800,marginBottom:20}}>BUILD SPEED</div>
    <div style={{height:34,background:'#E7E9EE',borderRadius:99,overflow:'hidden'}}><div style={{width:`${meter}%`,height:'100%',background:COLORS.accent,borderRadius:99}}/></div>
    <div style={{textAlign:'right',fontSize:36,fontWeight:800,marginTop:12}}>{Math.round(meter)}%</div>
  </div>
  <div style={{marginTop:80,display:'grid',gap:24}}>{items.map((x,i)=><div key={x} style={{display:'flex',alignItems:'center',gap:24,padding:'28px 30px',background:COLORS.surface,border:`1px solid ${COLORS.border}`,borderRadius:RADIUS.md,fontSize:TYPE.support,fontWeight:700}}><span style={{width:42,height:42,borderRadius:99,display:'grid',placeItems:'center',background:i===0?COLORS.success:'#EEF0F3',color:i===0?'white':COLORS.muted,fontSize:25}}>{i===0?'✓':'·'}</span>{x}</div>)}</div>
 </Frame>;
};
