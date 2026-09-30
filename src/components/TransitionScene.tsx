import React from 'react';
import {interpolate,useCurrentFrame,useVideoConfig} from 'remotion';
import {COLORS} from '../tokens';
import {clamp} from '../utils';

export type TransitionKind=
  |'camera-push'
  |'repo-handoff'
  |'plan-compress'
  |'dark-mask'
  |'terminal-flow'
  |'review-aperture'
  |'system-sweep'
  |'none';

type Props=React.PropsWithChildren<{
  enterFrames:number;
  baseDurationInFrames:number;
  exitFrames:number;
  enterKind?:TransitionKind;
  exitKind?:TransitionKind;
  zIndex:number;
}>;

const progress=(frame:number,start:number,end:number)=>
  interpolate(frame,[start,end],[0,1],clamp);

const enterStyle=(kind:TransitionKind,p:number):React.CSSProperties=>{
  switch(kind){
    case 'camera-push':
      return {
        transform:`scale(${interpolate(p,[0,1],[.93,1],clamp)}) translateY(${interpolate(p,[0,1],[80,0],clamp)}px)`,
        clipPath:`inset(${interpolate(p,[0,1],[8,0],clamp)}% ${interpolate(p,[0,1],[6,0],clamp)}% round ${interpolate(p,[0,1],[52,0],clamp)}px)`,
      };
    case 'repo-handoff':
      return {
        transform:`translateX(${interpolate(p,[0,1],[150,0],clamp)}px) scale(${interpolate(p,[0,1],[.985,1],clamp)})`,
        clipPath:`inset(0 ${interpolate(p,[0,1],[14,0],clamp)}% 0 0 round 28px)`,
      };
    case 'plan-compress':
      return {
        transform:`scale(${interpolate(p,[0,1],[1.06,1],clamp)}) translateY(${interpolate(p,[0,1],[-38,0],clamp)}px)`,
        clipPath:`inset(${interpolate(p,[0,1],[5,0],clamp)}% ${interpolate(p,[0,1],[4,0],clamp)}% round ${interpolate(p,[0,1],[42,0],clamp)}px)`,
      };
    case 'dark-mask':
      return {
        transform:`translateY(${interpolate(p,[0,1],[180,0],clamp)}px)`,
        clipPath:`inset(${interpolate(p,[0,1],[100,0],clamp)}% 0 0 0 round 36px)`,
      };
    case 'terminal-flow':
      return {
        transform:`translateY(${interpolate(p,[0,1],[190,0],clamp)}px)`,
        clipPath:`inset(${interpolate(p,[0,1],[12,0],clamp)}% 0 0 0 round 26px)`,
      };
    case 'review-aperture':
      return {
        transform:`scale(${interpolate(p,[0,1],[1.035,1],clamp)})`,
        clipPath:`circle(${interpolate(p,[0,1],[18,86],clamp)}% at 72% 54%)`,
      };
    case 'system-sweep':
      return {
        transform:`translateX(${interpolate(p,[0,1],[170,0],clamp)}px)`,
        clipPath:`inset(0 0 0 ${interpolate(p,[0,1],[18,0],clamp)}% round 24px)`,
      };
    default:return {};
  }
};

const exitStyle=(kind:TransitionKind,p:number):React.CSSProperties=>{
  switch(kind){
    case 'camera-push':
      return {transform:`scale(${interpolate(p,[0,1],[1,1.10],clamp)}) translateY(${interpolate(p,[0,1],[0,-54],clamp)}px)`};
    case 'repo-handoff':
      return {transform:`translateX(${interpolate(p,[0,1],[0,-150],clamp)}px) scale(${interpolate(p,[0,1],[1,.985],clamp)})`};
    case 'plan-compress':
      return {transform:`scale(${interpolate(p,[0,1],[1,.94],clamp)}) translateY(${interpolate(p,[0,1],[0,34],clamp)}px)`};
    case 'dark-mask':
      return {transform:`translateY(${interpolate(p,[0,1],[0,-90],clamp)}px) scale(${interpolate(p,[0,1],[1,.985],clamp)})`};
    case 'terminal-flow':
      return {transform:`translateY(${interpolate(p,[0,1],[0,-190],clamp)}px)`};
    case 'review-aperture':
      return {transform:`scale(${interpolate(p,[0,1],[1,1.045],clamp)})`};
    case 'system-sweep':
      return {transform:`translateX(${interpolate(p,[0,1],[0,-110],clamp)}px)`};
    default:return {};
  }
};

export const TransitionScene:React.FC<Props>=({
  children,
  enterFrames,
  baseDurationInFrames,
  exitFrames,
  enterKind='none',
  exitKind='none',
  zIndex,
})=>{
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const enter=enterFrames>0?progress(frame,0,enterFrames):1;
  const exitStart=Math.max(0,enterFrames+baseDurationInFrames-exitFrames);
  const exit=exitFrames>0?progress(frame,exitStart,exitStart+exitFrames):0;

  const entering=enterStyle(enterKind,enter);
  const exiting=exitStyle(exitKind,exit);
  const finalStyle:React.CSSProperties=exit>0?exiting:entering;

  const accentEnter=enterFrames>0?interpolate(enter,[0,1],[1,0],clamp):0;
  const accentExit=exitFrames>0?interpolate(exit,[0,1],[0,1],clamp):0;
  const accent=Math.max(accentEnter,accentExit);

  return <div style={{
    position:'absolute',
    inset:0,
    overflow:'hidden',
    zIndex,
    ...finalStyle,
    willChange:'transform, clip-path',
  }}>
    {children}
    {accent>0.001?<div style={{
      position:'absolute',
      left:0,
      right:0,
      top:0,
      height:6,
      background:`linear-gradient(90deg,transparent,${COLORS.accent},transparent)`,
      opacity:accent*.5,
      transform:`translateX(${interpolate(enter,[0,1],[-45,45],clamp)}%)`,
      pointerEvents:'none',
    }}/>:null}
  </div>;
};
