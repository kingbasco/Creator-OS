import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, FLOAT_SHADOW, RADIUS, TYPE} from '../tokens';
import {clamp, drawProgress, fadeInUp, physicalSpring} from '../utils';
import {MotionBackdrop} from './MotionBackdrop';

export const HeroHook: React.FC = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();

  const app=physicalSpring(frame,fps,6,14);
  const prompt=physicalSpring(frame,fps,15,12);
  const result=physicalSpring(frame,fps,30,12);
  const headline=physicalSpring(frame,fps,38,14);
  const strike=drawProgress(frame,74,13);
  const correction=physicalSpring(frame,fps,88,12);

  return (
    <Frame>
      <MotionBackdrop/>

      <div style={{
        position:'absolute',
        left:92,
        top:220+(1-app)*70,
        width:896,
        height:650,
        borderRadius:RADIUS.lg,
        background:COLORS.surface,
        border:`1px solid ${COLORS.border}`,
        boxShadow:'0 26px 78px rgba(16,17,20,.09)',
        opacity:app,
        transform:`scale(${interpolate(app,[0,1],[.965,1],clamp)})`,
        overflow:'hidden',
      }}>
        <div style={{
          height:74,
          background:COLORS.well,
          borderBottom:`1px solid ${COLORS.border}`,
          display:'flex',
          alignItems:'center',
          gap:11,
          padding:'0 24px',
        }}>
          {[COLORS.danger,COLORS.warning,COLORS.success].map(c=>(
            <span key={c} style={{width:13,height:13,borderRadius:99,background:c}}/>
          ))}
          <div style={{
            marginLeft:18,
            width:490,
            height:32,
            borderRadius:9,
            background:COLORS.surface,
            border:`1px solid ${COLORS.border}`,
          }}/>
        </div>

        <div style={{padding:34,display:'grid',gridTemplateColumns:'1.3fr .7fr',gap:26}}>
          <div style={{
            height:486,
            borderRadius:RADIUS.md,
            background:COLORS.well,
            padding:28,
            display:'flex',
            flexDirection:'column',
            justifyContent:'space-between',
          }}>
            <div>
              <div style={{width:230,height:24,borderRadius:8,background:'#D8DCE5'}}/>
              <div style={{width:390,height:14,borderRadius:8,background:'#E2E5EA',marginTop:18}}/>
              <div style={{width:340,height:14,borderRadius:8,background:'#E2E5EA',marginTop:10}}/>
            </div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:18}}>
              {[0,1].map(i=>(
                <div key={i} style={{height:150,borderRadius:RADIUS.md,background:COLORS.surface,border:`1px solid ${COLORS.border}`}}/>
              ))}
            </div>
          </div>
          <div style={{display:'grid',gap:18}}>
            {[0,1,2].map((i)=>(
              <div key={i} style={{
                borderRadius:RADIUS.md,
                background:i===0?COLORS.accentSoft:COLORS.well,
                border:`1px solid ${i===0?'#D7DBFF':COLORS.border}`,
                padding:20,
              }}>
                <div style={{width:i===0?92:76,height:12,borderRadius:9,background:i===0?COLORS.accent:'#D8DCE5'}}/>
                <div style={{width:'86%',height:9,borderRadius:8,background:'#DDE1E8',marginTop:18}}/>
                <div style={{width:'62%',height:9,borderRadius:8,background:'#E5E7EB',marginTop:9}}/>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div style={{
        position:'absolute',
        left:590,
        top:174+(1-prompt)*54,
        width:360,
        padding:'22px 24px',
        borderRadius:RADIUS.md,
        background:'rgba(255,255,255,.94)',
        border:`1px solid ${COLORS.border}`,
        boxShadow:FLOAT_SHADOW,
        backdropFilter:'blur(14px)',
        opacity:prompt,
        transform:`rotate(${interpolate(prompt,[0,1],[8,3],clamp)}deg)`,
      }}>
        <div style={{fontSize:18,fontWeight:700,color:COLORS.accent}}>PROMPT</div>
        <div style={{fontSize:29,fontWeight:700,marginTop:7}}>Build a clean analytics dashboard.</div>
      </div>

      <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}}>
        <path
          d="M 742 338 C 800 430, 842 500, 806 596"
          fill="none"
          stroke={COLORS.accent}
          strokeWidth={4}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1-drawProgress(frame,25,16)}
        />
      </svg>

      <div style={{
        position:'absolute',
        left:118,
        top:774+(1-result)*42,
        padding:'13px 18px',
        borderRadius:RADIUS.sm,
        background:COLORS.darkSurface,
        color:COLORS.surface,
        fontSize:20,
        fontWeight:650,
        boxShadow:'0 16px 42px rgba(16,17,20,.15)',
        opacity:result,
      }}>
        AI GENERATED THE FIRST PASS
      </div>

      <div style={{
        position:'absolute',
        left:72,
        right:72,
        top:930,
        opacity:headline,
        transform:`translateY(${interpolate(headline,[0,1],[36,0],clamp)}px)`,
      }}>
        <div style={{fontSize:TYPE.hero,fontWeight:700,lineHeight:.94,letterSpacing:'-.055em'}}>
          I BUILT THIS APP
        </div>
        <div style={{
          fontSize:TYPE.hero,
          fontWeight:700,
          lineHeight:.94,
          letterSpacing:'-.055em',
          marginTop:20,
          position:'relative',
          display:'inline-block',
        }}>
          WITHOUT CODING
          <span style={{
            position:'absolute',
            left:0,
            top:'50%',
            height:11,
            width:`${strike*100}%`,
            background:COLORS.accent,
            borderRadius:99,
            transform:'rotate(-1deg)',
          }}/>
        </div>

        <div style={{
          display:'flex',
          alignItems:'center',
          gap:18,
          marginTop:44,
          opacity:correction,
          transform:`translateX(${interpolate(correction,[0,1],[34,0],clamp)}px)`,
        }}>
          <span style={{width:56,height:3,borderRadius:99,background:COLORS.accent}}/>
          <span style={{fontSize:TYPE.sceneTitle,fontWeight:700,color:COLORS.accent,letterSpacing:'-.04em'}}>WITH AI.</span>
        </div>
      </div>
    </Frame>
  );
};
