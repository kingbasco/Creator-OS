import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {fadeInUp, clamp} from '../utils';

const layers=['INTERFACE','APP LOGIC','API / BACKEND','DATA + AUTH'];
export const LayerStack: React.FC = () => {
  const frame=useCurrentFrame(); const {fps}=useVideoConfig();
  return <Frame>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:800,...fadeInUp(frame,fps)}}>YOUR ROLE MOVES<br/><span style={{color:COLORS.accent}}>UP A LEVEL</span></div>
    <div style={{marginTop:160,position:'relative',height:760}}>
      {layers.map((l,i)=>{
        const y=interpolate(frame,[10+i*8,24+i*8],[520-i*95, i*150],clamp);
        const scale=1-i*.025;
        return <div key={l} style={{position:'absolute',left:i*22,right:i*22,top:y,height:122,borderRadius:RADIUS.md,background:i===0?COLORS.accent:COLORS.surface,color:i===0?'white':COLORS.foreground,border:`1px solid ${i===0?COLORS.accent:COLORS.border}`,display:'flex',alignItems:'center',padding:'0 34px',fontSize:TYPE.support,fontWeight:800,transform:`scale(${scale})`,boxShadow:'0 18px 50px rgba(16,17,20,.07)'}}>{l}</div>
      })}
    </div>
  </Frame>;
};
