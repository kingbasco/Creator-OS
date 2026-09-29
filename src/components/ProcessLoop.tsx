import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {fadeInUp, physicalSpring, drawProgress} from '../utils';
import {MotionBackdrop} from './MotionBackdrop';

const cards=[
  {title:'PROMPT',sub:'Describe what you want',x:72,y:430,w:350,accent:COLORS.accent},
  {title:'CODE',sub:'AI edits the files',x:575,y:390,w:335,accent:COLORS.accent},
  {title:'RUN',sub:'See the result',x:620,y:760,w:300,accent:COLORS.accent},
  {title:'ERROR',sub:'Find what broke',x:520,y:1110,w:360,accent:COLORS.danger},
  {title:'CORRECT',sub:'Adjust and try again',x:90,y:1120,w:370,accent:COLORS.success},
] as const;

const connectors=[
  'M 420 505 C 500 465, 520 465, 575 465',
  'M 740 520 C 810 575, 805 650, 770 760',
  'M 760 900 C 770 1000, 740 1050, 700 1110',
  'M 520 1190 C 485 1220, 470 1220, 460 1190',
  'M 230 1120 C 110 980, 110 700, 215 565',
];

export const ProcessLoop: React.FC = () => {
  const frame=useCurrentFrame();
  const {fps}=useVideoConfig();

  return (
    <Frame>
      <MotionBackdrop/>
      <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,lineHeight:1.02,...fadeInUp(frame,fps)}}>
        THE LOOP BEHIND<br/><span style={{color:COLORS.accent}}>VIBE CODING</span>
      </div>

      <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}}>
        {connectors.map((d,i)=>{
          const p=drawProgress(frame,28+i*10,16);
          return <path key={d} d={d} fill="none" stroke={COLORS.accent} strokeWidth={4} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1-p}/>;
        })}
      </svg>

      {cards.map((card,i)=>{
        const p=physicalSpring(frame,fps,12+i*9,12);
        return (
          <div key={card.title} style={{
            position:'absolute',
            left:card.x,
            top:card.y+(1-p)*44,
            width:card.w,
            padding:'26px 28px',
            borderRadius:RADIUS.md,
            background:card.title==='PROMPT'||card.title==='CORRECT'?COLORS.accentSoft:COLORS.surface,
            border:`1px solid ${card.title==='ERROR'?COLORS.danger:COLORS.border}`,
            boxShadow:'0 12px 36px rgba(16,17,20,.07)',
            opacity:p,
            transform:`scale(${.97+p*.03})`,
          }}>
            <div style={{display:'flex',alignItems:'center',gap:16}}>
              <span style={{width:34,height:34,borderRadius:99,background:card.accent,display:'block'}}/>
              <div>
                <div style={{fontSize:32,fontWeight:700,color:card.title==='ERROR'?COLORS.danger:COLORS.foreground}}>{card.title}</div>
                <div style={{fontSize:24,color:COLORS.muted,marginTop:5}}>{card.sub}</div>
              </div>
            </div>
          </div>
        );
      })}

      <div style={{
        position:'absolute',
        left:72,
        top:760,
        width:390,
        padding:26,
        borderRadius:RADIUS.md,
        background:COLORS.darkSurface,
        color:COLORS.surface,
        fontFamily:TYPE.monoFamily,
        fontSize:22,
        lineHeight:1.6,
        opacity:physicalSpring(frame,fps,44,12),
        boxShadow:'0 20px 50px rgba(16,17,20,.14)',
      }}>
        <div>$ npm run dev</div>
        <div style={{color:COLORS.mutedOnDark}}>Local: localhost:5173</div>
        <div style={{color:COLORS.success}}>ready in 432ms</div>
      </div>

      <div style={{position:'absolute',left:330,top:890,width:400,textAlign:'center'}}>
        <div style={{fontSize:34,fontWeight:700}}>Output becomes the next input.</div>
        <div style={{fontSize:24,color:COLORS.muted,marginTop:10}}>Iteration is the product.</div>
      </div>
    </Frame>
  );
};
