import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {clamp, drawProgress, physicalSpring} from '../utils';

type Props = {
  label: string;
  from: {x: number; y: number};
  to: {x: number; y: number};
  delay?: number;
  color?: string;
  align?: 'left'|'right';
};

export const ArrowCallout: React.FC<Props> = ({
  label,
  from,
  to,
  delay=0,
  color=COLORS.accent,
  align='left',
}) => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const p=drawProgress(frame,delay,14);
  const tag=physicalSpring(frame,fps,delay+7,10);
  const dx=to.x-from.x;
  const dy=to.y-from.y;
  const bend=Math.min(110,Math.max(42,Math.abs(dx)*.18));
  const c1x=from.x+(dx>=0?bend:-bend);
  const c1y=from.y+dy*.18;
  const c2x=to.x-(dx>=0?bend:-bend);
  const c2y=to.y-dy*.18;
  const tagLeft=align==='left'?from.x:from.x-220;

  return (
    <>
      <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',overflow:'visible',pointerEvents:'none'}}>
        <path
          d={`M ${from.x} ${from.y} C ${c1x} ${c1y}, ${c2x} ${c2y}, ${to.x} ${to.y}`}
          fill="none"
          stroke={color}
          strokeWidth={4}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1-p}
        />
        <circle cx={to.x} cy={to.y} r={10} fill={color} opacity={p}/>
        <circle cx={to.x} cy={to.y} r={22} fill="none" stroke={color} strokeWidth={2} opacity={p*.22}/>
      </svg>
      <div style={{
        position:'absolute',
        left:tagLeft,
        top:from.y-62,
        padding:'10px 16px',
        background:'rgba(255,255,255,.94)',
        border:`1px solid ${COLORS.border}`,
        borderRadius:RADIUS.sm,
        fontSize:TYPE.label-5,
        fontWeight:700,
        color:COLORS.foreground,
        opacity:tag,
        transform:`translateY(${interpolate(tag,[0,1],[12,0],clamp)}px)`,
        boxShadow:'0 12px 34px rgba(16,17,20,.08)',
        backdropFilter:'blur(12px)',
      }}>
        {label}
      </div>
    </>
  );
};
