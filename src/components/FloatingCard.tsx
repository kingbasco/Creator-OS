import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORS, FLOAT_SHADOW, RADIUS} from '../tokens';
import {clamp, physicalSpring} from '../utils';

type Props = React.PropsWithChildren<{
  x:number;
  y:number;
  width:number;
  delay?:number;
  rotate?:number;
  dark?:boolean;
  float?:number;
}>;

export const FloatingCard: React.FC<Props> = ({
  x,
  y,
  width,
  delay=0,
  rotate=0,
  dark=false,
  children,
}) => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const p=physicalSpring(frame,fps,delay,12);
  const travel=interpolate(p,[0,1],[54,0],clamp);
  const startRotation=rotate+(rotate>=0?4:-4);
  const rotation=interpolate(p,[0,1],[startRotation,rotate],clamp);

  return (
    <div style={{
      position:'absolute',
      left:x,
      top:y+travel,
      width,
      padding:22,
      borderRadius:RADIUS.md,
      background:dark?COLORS.darkSurface:'rgba(255,255,255,.94)',
      color:dark?COLORS.surface:COLORS.foreground,
      border:`1px solid ${dark?COLORS.rimDark:'rgba(229,231,235,.9)'}`,
      boxShadow:FLOAT_SHADOW,
      backdropFilter:dark?undefined:'blur(14px)',
      opacity:p,
      transform:`rotate(${rotation}deg) scale(${interpolate(p,[0,1],[.96,1],clamp)})`,
      transformOrigin:'50% 70%',
    }}>
      {children}
    </div>
  );
};
