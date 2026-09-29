import React from 'react';
import {useCurrentFrame} from 'remotion';
import {COLORS} from '../tokens';

export const MotionBackdrop: React.FC<{dark?:boolean}> = ({dark=false}) => {
  const frame=useCurrentFrame();
  const drift=(frame%240)/240;
  const line=dark?'rgba(255,255,255,.055)':'rgba(16,17,20,.045)';
  return <div style={{position:'absolute',inset:0,overflow:'hidden',pointerEvents:'none'}}>
    <div style={{position:'absolute',inset:-80,backgroundImage:`linear-gradient(${line} 1px, transparent 1px),linear-gradient(90deg,${line} 1px, transparent 1px)`,backgroundSize:'72px 72px',transform:`translate(${drift*-28}px,${drift*-18}px)`}}/>
    <div style={{position:'absolute',width:420,height:420,borderRadius:999,left:-180,top:320,background:COLORS.accentSoft,opacity:dark ? 0.04 : 0.45,filter:'blur(10px)'}}/>
  </div>;
};
