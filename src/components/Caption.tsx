import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, RADIUS, SPACE, TYPE} from '../tokens';
import {clamp, physicalSpring} from '../utils';

export const Caption: React.FC<{text: string; emphasis?: string}> = ({text, emphasis}) => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const p=physicalSpring(frame,fps,4,10);
  const [before, after] = emphasis && text.includes(emphasis) ? text.split(emphasis) : [text, ''];

  return (
    <div style={{
      position:'absolute',
      left:SPACE.x,
      right:SPACE.x,
      bottom:112,
      display:'flex',
      justifyContent:'center',
      textAlign:'center',
      pointerEvents:'none',
      opacity:p,
      transform:`translateY(${interpolate(p,[0,1],[16,0],clamp)}px)`,
    }}>
      <div style={{
        fontFamily:TYPE.fontFamily,
        fontSize:TYPE.caption,
        fontWeight:650,
        lineHeight:1.14,
        letterSpacing:'-0.025em',
        background:'rgba(255,255,255,.92)',
        color:COLORS.foreground,
        border:`1px solid rgba(229,231,235,.9)`,
        borderRadius:RADIUS.md,
        padding:'16px 24px',
        boxShadow:'0 12px 36px rgba(16,17,20,.06)',
        backdropFilter:'blur(14px)',
        maxWidth:900,
      }}>
        {before}
        {emphasis ? <span style={{color:COLORS.accent}}>{emphasis}</span> : null}
        {after}
      </div>
    </div>
  );
};
