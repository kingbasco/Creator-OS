import React from 'react';
import {useScaledSceneFrame} from '../sceneTiming';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, FLOAT_SHADOW, RADIUS, TYPE} from '../tokens';
import {clamp, fadeInUp, physicalSpring} from '../utils';
import {ArrowCallout} from './ArrowCallout';
import {MotionBackdrop} from './MotionBackdrop';

export const BrowserFrame: React.FC<{durationInFrames?: number}> = ({durationInFrames}) => {
  const {frame,fps}=useScaledSceneFrame(durationInFrames,11);
  const corrected=physicalSpring(frame,fps,170,18);
  const issueOpacity=interpolate(frame,[0,145,180],[1,1,0],clamp);
  const cursorX=interpolate(frame,[40,88,126,165],[820,570,620,815],clamp);
  const cursorY=interpolate(frame,[40,88,126,165],[650,870,1040,740],clamp);

  return (
    <Frame>
      <MotionBackdrop/>
      <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>
        RUN. INSPECT. <span style={{color:COLORS.accent}}>CORRECT.</span>
      </div>

      <div style={{
        marginTop:92,
        borderRadius:RADIUS.lg,
        background:COLORS.surface,
        border:`1px solid ${COLORS.border}`,
        boxShadow:'0 22px 60px rgba(16,17,20,.08)',
        overflow:'hidden',
        height:1010,
      }}>
        <div style={{height:76,background:COLORS.well,borderBottom:`1px solid ${COLORS.border}`,display:'flex',alignItems:'center',gap:11,padding:'0 24px'}}>
          {[COLORS.danger,COLORS.warning,COLORS.success].map(c=><span key={c} style={{width:13,height:13,borderRadius:99,background:c}}/>)}
          <div style={{marginLeft:22,width:620,height:34,borderRadius:10,background:COLORS.surface,border:`1px solid ${COLORS.border}`,display:'flex',alignItems:'center',padding:'0 16px',fontSize:18,color:COLORS.muted,fontFamily:TYPE.monoFamily}}>
            localhost:5173/reset
          </div>
        </div>

        <div style={{padding:'70px 74px'}}>
          <div style={{fontSize:54,fontWeight:700}}>Reset your password</div>
          <div style={{fontSize:26,color:COLORS.muted,marginTop:12}}>Enter your email and we’ll send you a reset link.</div>
          <div style={{fontSize:21,fontWeight:600,marginTop:54}}>Email address</div>
          <div style={{
            marginTop:12,
            height:76,
            border:`2px solid ${corrected>.72?COLORS.success:COLORS.danger}`,
            borderRadius:RADIUS.md,
            display:'flex',
            alignItems:'center',
            padding:'0 24px',
            fontSize:26,
          }}>
            {corrected>.72?'john@acme.com':'john@'}
          </div>
          <div style={{height:38,marginTop:10,fontSize:20,color:corrected>.72?COLORS.success:COLORS.danger}}>
            {corrected>.72?'Email looks good.':'Please enter a valid email address.'}
          </div>
          <div style={{marginTop:26,height:78,borderRadius:RADIUS.md,background:COLORS.accent,color:'white',display:'grid',placeItems:'center',fontSize:27,fontWeight:700}}>
            Send reset link
          </div>
        </div>
      </div>

      <div style={{opacity:issueOpacity}}>
        <ArrowCallout label="error appears too early" from={{x:725,y:990}} to={{x:505,y:846}} delay={58} align="right"/>
      </div>

      <div style={{
        position:'absolute',
        left:cursorX,
        top:cursorY,
        width:28,
        height:28,
        borderRadius:99,
        background:COLORS.accent,
        boxShadow:`0 0 0 12px ${COLORS.accentSoft}`,
        opacity:issueOpacity,
      }}/>

      <div style={{
        position:'absolute',
        left:510,
        top:1220+(1-corrected)*60,
        width:430,
        padding:28,
        borderRadius:RADIUS.lg,
        background:'rgba(255,255,255,.94)',
        border:`1px solid ${COLORS.border}`,
        boxShadow:FLOAT_SHADOW,
        backdropFilter:'blur(14px)',
        opacity:corrected,
        transform:`rotate(${interpolate(corrected,[0,1],[2,-2],clamp)}deg)`,
      }}>
        <div style={{fontSize:19,fontWeight:700,color:COLORS.accent}}>CORRECTED STATE</div>
        <div style={{fontSize:32,fontWeight:700,marginTop:12}}>Validate after the user acts.</div>
        <div style={{fontSize:22,color:COLORS.muted,marginTop:12,lineHeight:1.4}}>The result is clearer because the error appears at the right moment.</div>
      </div>
    </Frame>
  );
};
