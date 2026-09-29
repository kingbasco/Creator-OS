import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, physicalSpring} from '../utils';

export const SceneMotion: React.FC<React.PropsWithChildren<{durationInFrames:number}>> = ({children,durationInFrames}) => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const intro=physicalSpring(frame,fps,0,12);
  const outro=interpolate(
    frame,
    [Math.max(0,durationInFrames-8), durationInFrames],
    [0,1],
    clamp,
  );
  const y=interpolate(intro,[0,1],[20,0],clamp)+interpolate(outro,[0,1],[0,16],clamp);
  const scale=interpolate(intro,[0,1],[0.992,1],clamp);
  const opacity=Math.min(intro,1-outro);

  return (
    <div style={{
      position:'absolute',
      inset:0,
      opacity,
      transform:`translateY(${y}px) scale(${scale})`,
      transformOrigin:'50% 50%',
    }}>
      {children}
    </div>
  );
};
