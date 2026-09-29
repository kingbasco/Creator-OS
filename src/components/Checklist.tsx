import React from 'react';
import {useScaledSceneFrame} from '../sceneTiming';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {fadeInUp, physicalSpring} from '../utils';
import {useCurrentFrame, useVideoConfig} from 'remotion';

const gates=[
  {title:'Works',copy:'The core flow runs.',accent:COLORS.accent},
  {title:'Correct',copy:'It handles real use and edge cases.',accent:COLORS.accent},
  {title:'Secure',copy:'It protects user data.',accent:COLORS.accent},
  {title:'Ship',copy:'It is ready for real users.',accent:COLORS.surface},
] as const;

export const Checklist: React.FC<{durationInFrames?: number}> = ({durationInFrames}) => {
  const {frame,fps}=useScaledSceneFrame(durationInFrames,9);

  return (
    <Frame>
      <div style={{fontSize:TYPE.hero,fontWeight:700,lineHeight:.94,...fadeInUp(frame,fps)}}>
        FAST<br/><span style={{color:COLORS.accent}}>≠ FINISHED</span>
      </div>
      <div style={{fontSize:30,color:COLORS.muted,marginTop:34}}>A working build is only the first gate.</div>

      <div style={{position:'relative',height:1100,marginTop:72}}>
        <div style={{position:'absolute',left:74,top:72,bottom:80,width:4,borderRadius:99,background:COLORS.border}}/>
        {gates.map((gate,i)=>{
          const p=physicalSpring(frame,fps,18+i*18,14);
          const ship=i===3;
          return (
            <div key={gate.title} style={{
              position:'absolute',
              left:55+i*18+(1-p)*40,
              top:20+i*245,
              width:780-i*30,
              minHeight:184,
              padding:'30px 34px 30px 72px',
              borderRadius:RADIUS.lg,
              background:ship?COLORS.accent:i===0?COLORS.accentSoft:COLORS.surface,
              color:ship?COLORS.surface:COLORS.foreground,
              border:ship?'none':`1px solid ${COLORS.border}`,
              boxShadow:'0 14px 42px rgba(16,17,20,.07)',
              opacity:p,
              transform:`rotate(${[-1.6,-.7,.5,1.3][i]}deg)`,
              transformOrigin:'12% 50%',
            }}>
              <div style={{position:'absolute',left:-3,top:58,width:42,height:42,borderRadius:99,background:ship?COLORS.surface:COLORS.accent,color:ship?COLORS.accent:COLORS.surface,display:'grid',placeItems:'center',fontSize:19,fontWeight:700}}>
                {i+1}
              </div>
              <div style={{fontSize:44,fontWeight:700}}>{gate.title}</div>
              <div style={{fontSize:25,lineHeight:1.35,color:ship?'rgba(255,255,255,.78)':COLORS.muted,marginTop:12,maxWidth:590}}>{gate.copy}</div>
            </div>
          );
        })}
      </div>
    </Frame>
  );
};
