import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, FLOAT_SHADOW, RADIUS, TYPE} from '../tokens';
import {clamp, fadeInUp, physicalSpring} from '../utils';
import {MotionBackdrop} from './MotionBackdrop';

const ai=[
  ['Edit files','Update the reset flow'],
  ['Run commands','npm run build'],
  ['Run tests','Check auth + validation'],
] as const;

const human=[
  ['Decide intent','What should exist?'],
  ['Verify result','Is it correct?'],
  ['Own the ship gate','Is it safe enough?'],
] as const;

export const ComparisonSplit: React.FC = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const ship=physicalSpring(frame,fps,210,16);

  return (
    <Frame>
      <MotionBackdrop/>
      <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>
        AI EXECUTES.<br/><span style={{color:COLORS.accent}}>YOU DECIDE.</span>
      </div>

      <div style={{
        marginTop:76,
        padding:30,
        borderRadius:RADIUS.lg,
        background:COLORS.darkSurface,
        color:COLORS.surface,
        border:`1px solid ${COLORS.rimDark}`,
        opacity:physicalSpring(frame,fps,12,14),
      }}>
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div style={{fontSize:26,fontWeight:700}}>AI execution</div>
          <div style={{display:'flex',alignItems:'center',gap:10,color:'#9AA6FF',fontSize:19}}>
            <span style={{width:10,height:10,borderRadius:99,background:COLORS.accent}}/>Running…
          </div>
        </div>
        <div style={{marginTop:24,display:'grid',gap:14}}>
          {ai.map(([title,copy],i)=>{
            const p=physicalSpring(frame,fps,28+i*11,12);
            return (
              <div key={title} style={{display:'grid',gridTemplateColumns:'44px 1fr',gap:16,alignItems:'center',padding:18,borderRadius:RADIUS.md,border:`1px solid ${COLORS.rimDark}`,background:'#171A21',opacity:p,transform:`translateX(${(1-p)*28}px)`}}>
                <span style={{width:22,height:22,borderRadius:99,background:i===0?COLORS.success:COLORS.accent}}/>
                <div><div style={{fontSize:24,fontWeight:700}}>{title}</div><div style={{fontSize:18,color:COLORS.mutedOnDark,marginTop:4}}>{copy}</div></div>
              </div>
            );
          })}
        </div>
        <div style={{height:9,borderRadius:99,background:'#2A2E38',marginTop:24,overflow:'hidden'}}>
          <div style={{height:'100%',width:'86%',background:COLORS.accent,borderRadius:99}}/>
        </div>
      </div>

      <div style={{
        marginTop:24,
        padding:'28px 32px',
        borderRadius:RADIUS.lg,
        background:COLORS.surface,
        border:`1px solid ${COLORS.border}`,
        boxShadow:'0 14px 38px rgba(16,17,20,.06)',
        opacity:physicalSpring(frame,fps,70,14),
      }}>
        <div style={{fontSize:26,fontWeight:700}}>Your responsibility</div>
        <div style={{marginTop:18,display:'grid',gap:0}}>
          {human.map(([title,copy],i)=>(
            <div key={title} style={{padding:'22px 0',borderBottom:i<2?`1px solid ${COLORS.border}`:'none',display:'grid',gridTemplateColumns:'46px 1fr',gap:12}}>
              <span style={{width:28,height:28,borderRadius:99,border:`2px solid ${COLORS.accent}`,display:'grid',placeItems:'center',color:COLORS.accent,fontSize:14,fontWeight:700}}>{i+1}</span>
              <div><div style={{fontSize:25,fontWeight:700}}>{title}</div><div style={{fontSize:19,color:COLORS.muted,marginTop:5}}>{copy}</div></div>
            </div>
          ))}
        </div>
      </div>

      <div style={{
        position:'absolute',
        left:184,
        top:1390+(1-ship)*54,
        width:570,
        padding:30,
        borderRadius:RADIUS.lg,
        background:'rgba(255,255,255,.95)',
        border:`1px solid ${COLORS.border}`,
        boxShadow:FLOAT_SHADOW,
        backdropFilter:'blur(14px)',
        opacity:ship,
        transform:`scale(${interpolate(ship,[0,1],[.96,1],clamp)})`,
      }}>
        <div style={{fontSize:38,fontWeight:700}}>Ship this build?</div>
        <div style={{fontSize:22,color:COLORS.muted,marginTop:8}}>The automation stops at the human decision.</div>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12,marginTop:24}}>
          <div style={{height:58,borderRadius:RADIUS.sm,background:COLORS.accent,color:'white',display:'grid',placeItems:'center',fontSize:21,fontWeight:700}}>Ship</div>
          <div style={{height:58,borderRadius:RADIUS.sm,background:COLORS.well,display:'grid',placeItems:'center',fontSize:21,fontWeight:600}}>Keep iterating</div>
        </div>
      </div>
    </Frame>
  );
};
