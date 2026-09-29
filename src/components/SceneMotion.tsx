import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp} from '../utils';

export const SceneMotion: React.FC<React.PropsWithChildren> = ({children}) => {
  const frame=useCurrentFrame(); const {durationInFrames}=useVideoConfig();
  const intro=interpolate(frame,[0,10],[0,1],clamp);
  const outro=interpolate(frame,[Math.max(0,durationInFrames-10),durationInFrames],[1,0],clamp);
  const alpha=Math.min(intro,outro);
  const scale=interpolate(intro,[0,1],[1.015,1],clamp);
  return <div style={{position:'absolute',inset:0,opacity:alpha,transform:`scale(${scale})`}}>{children}</div>;
};
