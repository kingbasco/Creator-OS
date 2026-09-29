import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, FLOAT_SHADOW, RADIUS, TYPE} from '../tokens';
import {clamp, drawProgress, physicalSpring} from '../utils';
import {MotionBackdrop} from './MotionBackdrop';

const words=[
  {label:'DIRECTION',x:88,y:410,rotate:-3},
  {label:'ITERATION',x:400,y:640,rotate:2},
  {label:'JUDGMENT',x:122,y:870,rotate:-1},
] as const;

export const EpisodeEndcard: React.FC = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const synthesis=physicalSpring(frame,fps,72,18);
  const next=physicalSpring(frame,fps,128,18);

  return (
    <Frame>
      <MotionBackdrop/>

      <div style={{position:'absolute',left:72,right:72,top:180}}>
        <div style={{fontSize:28,color:COLORS.muted,fontWeight:600}}>VIBE CODING IS</div>
        <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,letterSpacing:'-.04em',marginTop:12}}>
          NOT MAGIC.
        </div>
      </div>

      {words.map((word,i)=>{
        const p=physicalSpring(frame,fps,12+i*14,14);
        const targetX=146;
        const targetY=530+i*154;
        const x=interpolate(synthesis,[0,1],[word.x,targetX],clamp);
        const y=interpolate(synthesis,[0,1],[word.y,targetY],clamp);
        const rotation=interpolate(synthesis,[0,1],[word.rotate,0],clamp);
        return (
          <div key={word.label} style={{
            position:'absolute',
            left:x,
            top:y,
            width:790,
            padding:'26px 30px',
            borderRadius:RADIUS.lg,
            background:i===2?COLORS.accent:COLORS.surface,
            color:i===2?COLORS.surface:COLORS.foreground,
            border:i===2?'none':`1px solid ${COLORS.border}`,
            boxShadow:'0 16px 48px rgba(16,17,20,.08)',
            fontSize:64,
            fontWeight:700,
            letterSpacing:'-.045em',
            opacity:p,
            transform:`rotate(${rotation}deg) scale(${interpolate(p,[0,1],[.96,1],clamp)})`,
            transformOrigin:'16% 50%',
          }}>
            <span style={{display:'inline-block',width:70,fontSize:18,color:i===2?'rgba(255,255,255,.72)':COLORS.muted}}>0{i+1}</span>
            {word.label}
          </div>
        );
      })}

      <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none',opacity:synthesis}}>
        <path
          d="M 112 582 L 112 892"
          fill="none"
          stroke={COLORS.accent}
          strokeWidth={4}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1-drawProgress(frame,82,18)}
        />
      </svg>

      <div style={{
        position:'absolute',
        left:108,
        top:1130+(1-next)*80,
        width:864,
        padding:'38px 40px',
        borderRadius:RADIUS.lg,
        background:COLORS.darkSurface,
        color:COLORS.surface,
        border:`1px solid ${COLORS.rimDark}`,
        boxShadow:FLOAT_SHADOW,
        opacity:next,
        transform:`scale(${interpolate(next,[0,1],[.97,1],clamp)})`,
      }}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
          <div style={{fontSize:20,color:'#AAB4FF',fontWeight:700}}>NEXT • V02</div>
          <div style={{
            width:54,
            height:54,
            borderRadius:99,
            background:COLORS.accent,
            display:'grid',
            placeItems:'center',
          }}>
            <svg width="26" height="26" viewBox="0 0 26 26" fill="none">
              <path d="M5 13h15M14 7l6 6-6 6" stroke="white" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
        </div>
        <div style={{fontSize:48,fontWeight:700,lineHeight:1.08,letterSpacing:'-.035em',marginTop:24}}>
          What an AI coding agent is actually doing.
        </div>
        <div style={{fontSize:23,color:COLORS.mutedOnDark,lineHeight:1.4,marginTop:20,maxWidth:680}}>
          The next episode goes behind the interface and into the agent loop.
        </div>
      </div>
    </Frame>
  );
};
