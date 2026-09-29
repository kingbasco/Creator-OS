import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {clamp} from '../utils';

type Props = {
  label: string;
  from: {x: number; y: number};
  to: {x: number; y: number};
  delay?: number;
  color?: string;
  align?: 'left'|'right';
};

export const ArrowCallout: React.FC<Props> = ({label, from, to, delay=0, color=COLORS.accent, align='left'}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [delay, delay+16], [0,1], clamp);
  const opacity = interpolate(frame, [delay, delay+8], [0,1], clamp);
  const dx=to.x-from.x; const dy=to.y-from.y;
  const len=Math.max(1,Math.hypot(dx,dy));
  const angle=Math.atan2(dy,dx)*180/Math.PI;
  const tagLeft = align==='left' ? from.x : from.x-220;
  return <>
    <div style={{position:'absolute',left:from.x,top:from.y,width:len,height:4,background:color,borderRadius:99,transformOrigin:'0 50%',transform:`rotate(${angle}deg) scaleX(${p})`,opacity}}/>
    <div style={{position:'absolute',left:to.x-9,top:to.y-9,width:18,height:18,borderRadius:99,background:color,boxShadow:`0 0 0 10px ${COLORS.accentSoft}`,opacity}}/>
    <div style={{position:'absolute',left:tagLeft,top:from.y-58,padding:'10px 16px',background:COLORS.surface,border:`1px solid ${COLORS.border}`,borderRadius:RADIUS.sm,fontSize:TYPE.label-4,fontWeight:800,color:COLORS.foreground,opacity,boxShadow:'0 12px 34px rgba(16,17,20,.08)'}}>{label}</div>
  </>;
};
