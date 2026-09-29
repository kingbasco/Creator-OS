import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {COLORS, RADIUS, SHADOW} from '../tokens';
import {clamp} from '../utils';

type Props = React.PropsWithChildren<{
  x:number; y:number; width:number; delay?:number; rotate?:number; dark?:boolean; float?:number;
}>;

export const FloatingCard: React.FC<Props> = ({x,y,width,delay=0,rotate=0,dark=false,float=10,children}) => {
  const frame=useCurrentFrame();
  const enter=interpolate(frame,[delay,delay+16],[0,1],clamp);
  const rise=interpolate(frame,[delay,delay+16],[44,0],clamp);
  const drift=Math.sin((frame-delay)/20)*float;
  return <div style={{position:'absolute',left:x,top:y+rise+drift,width,padding:22,borderRadius:RADIUS.md,background:dark?COLORS.darkSurface:COLORS.surface,color:dark?'white':COLORS.foreground,border:`1px solid ${dark?'#2A303C':COLORS.border}`,boxShadow:SHADOW,opacity:enter,transform:`rotate(${rotate*(1-enter)}deg) scale(${0.94+enter*.06})`}}>{children}</div>;
};
