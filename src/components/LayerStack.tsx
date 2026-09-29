import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, FLOAT_SHADOW, RADIUS, TYPE} from '../tokens';
import {clamp, drawProgress, fadeInUp, physicalSpring} from '../utils';
import {MotionBackdrop} from './MotionBackdrop';

const layers=[
  {label:'INTERFACE',detail:'What the user sees'},
  {label:'APP LOGIC',detail:'What the product does'},
  {label:'API / BACKEND',detail:'How systems connect'},
  {label:'DATA + AUTH',detail:'What the product trusts'},
] as const;

export const LayerStack: React.FC = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();
  const pullback=physicalSpring(frame,fps,28,20);
  const you=physicalSpring(frame,fps,74,16);

  const systemScale=interpolate(pullback,[0,1],[1.12,.84],clamp);
  const systemY=interpolate(pullback,[0,1],[250,470],clamp);
  const systemOpacity=interpolate(pullback,[0,1],[1,.78],clamp);

  return (
    <Frame>
      <MotionBackdrop/>

      <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,lineHeight:1.02,...fadeInUp(frame,fps)}}>
        YOUR ROLE MOVES<br/><span style={{color:COLORS.accent}}>UP A LEVEL</span>
      </div>
      <div style={{fontSize:28,color:COLORS.muted,marginTop:24,maxWidth:790,lineHeight:1.35}}>
        Less time typing every line. More time directing the whole system.
      </div>

      <div style={{
        position:'absolute',
        left:82,
        top:systemY,
        width:916,
        height:980,
        opacity:systemOpacity,
        transform:`scale(${systemScale})`,
        transformOrigin:'50% 20%',
      }}>
        {layers.map((layer,i)=>{
          const p=physicalSpring(frame,fps,10+i*9,13);
          const top=i*176;
          const width=840-i*54;
          const left=(916-width)/2;
          const active=i===0;
          return (
            <div key={layer.label} style={{
              position:'absolute',
              left,
              top:top+(1-p)*46,
              width,
              height:142,
              padding:'24px 30px',
              borderRadius:RADIUS.lg,
              background:active?COLORS.accent:COLORS.surface,
              color:active?COLORS.surface:COLORS.foreground,
              border:active?'none':`1px solid ${COLORS.border}`,
              boxShadow:'0 18px 48px rgba(16,17,20,.07)',
              opacity:p,
              transform:`rotate(${[-1.2,.6,-.5,.8][i]}deg)`,
              boxSizing:'border-box',
            }}>
              <div style={{fontSize:30,fontWeight:700}}>{layer.label}</div>
              <div style={{fontSize:21,color:active?'rgba(255,255,255,.72)':COLORS.muted,marginTop:10}}>{layer.detail}</div>
            </div>
          );
        })}

        <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}}>
          <path
            d="M 458 620 C 458 720, 458 770, 458 846"
            fill="none"
            stroke={COLORS.accent}
            strokeWidth={4}
            strokeLinecap="round"
            pathLength={1}
            strokeDasharray={1}
            strokeDashoffset={1-drawProgress(frame,66,14)}
            opacity={.55}
          />
        </svg>
      </div>

      <div style={{
        position:'absolute',
        left:190,
        top:840+(1-you)*90,
        width:700,
        padding:'34px 38px',
        borderRadius:RADIUS.lg,
        background:'rgba(255,255,255,.95)',
        border:`1px solid ${COLORS.border}`,
        boxShadow:FLOAT_SHADOW,
        backdropFilter:'blur(14px)',
        opacity:you,
        transform:`scale(${interpolate(you,[0,1],[.95,1],clamp)})`,
      }}>
        <div style={{display:'flex',alignItems:'center',justifyContent:'space-between'}}>
          <div>
            <div style={{fontSize:19,fontWeight:700,color:COLORS.accent}}>YOUR JOB</div>
            <div style={{fontSize:50,fontWeight:700,letterSpacing:'-.04em',marginTop:8}}>Direct the system.</div>
          </div>
          <div style={{
            width:76,
            height:76,
            borderRadius:99,
            background:COLORS.accentSoft,
            display:'grid',
            placeItems:'center',
          }}>
            <svg width="34" height="34" viewBox="0 0 34 34" fill="none">
              <path d="M17 27V8M9 16l8-8 8 8" stroke={COLORS.accent} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
        </div>
        <div style={{fontSize:24,color:COLORS.muted,lineHeight:1.4,marginTop:18}}>
          Intent, trade-offs, review, and judgment move to the foreground.
        </div>
      </div>
    </Frame>
  );
};
