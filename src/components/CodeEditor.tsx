import React from 'react';
import {useScaledSceneFrame} from '../sceneTiming';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {clamp, fadeInUp, physicalSpring} from '../utils';
import {MotionBackdrop} from './MotionBackdrop';

const files=[
  ['src/routes/reset.tsx','+48  -12'],
  ['src/components/ResetForm.tsx','+28  -6'],
  ['src/lib/validation.ts','+12  -2'],
] as const;

const lines=[
  "import {ValidEmail} from '@/lib/validation';",
  "import {sendResetEmail} from '@/lib/auth';",
  '',
  'const formData = await request.formData();',
  "const email = formData.get('email') as string;",
  'if (!ValidEmail(email)) {',
  "  return json({error: 'Invalid email address'});",
  '}',
  'await sendResetEmail(email);',
];

export const CodeEditor: React.FC<{durationInFrames?: number}> = ({durationInFrames}) => {
  const {frame,fps}=useScaledSceneFrame(durationInFrames,11);
  const reveal=interpolate(frame,[55,105],[0,1],clamp);

  return (
    <Frame dark>
      <MotionBackdrop dark/>
      <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>
        DESCRIBE INTENT.<br/><span style={{color:'#9AA6FF'}}>AI PROPOSES.</span>
      </div>

      <div style={{
        marginTop:86,
        display:'grid',
        gridTemplateRows:'auto 1fr',
        gap:24,
        minHeight:1120,
      }}>
        <div style={{
          padding:28,
          borderRadius:RADIUS.lg,
          background:'#171A21',
          border:`1px solid ${COLORS.rimDark}`,
          opacity:physicalSpring(frame,fps,10,12),
        }}>
          <div style={{fontSize:22,color:COLORS.mutedOnDark,fontWeight:600}}>YOUR REQUEST</div>
          <div style={{fontSize:38,fontWeight:700,lineHeight:1.15,marginTop:14,maxWidth:820}}>
            Add password reset with email validation and a confirmation state.
          </div>
          <div style={{marginTop:24,display:'flex',gap:12,flexWrap:'wrap'}}>
            {['Use existing UI','Validate email','Add success state'].map((x,i)=>(
              <div key={x} style={{
                padding:'11px 16px',
                borderRadius:RADIUS.sm,
                background:i===0?COLORS.accent:'transparent',
                border:`1px solid ${i===0?COLORS.accent:COLORS.rimDark}`,
                color:i===0?'white':COLORS.mutedOnDark,
                fontSize:20,
                fontWeight:600,
              }}>{x}</div>
            ))}
          </div>
        </div>

        <div style={{
          display:'grid',
          gridTemplateColumns:'280px 1fr',
          minHeight:790,
          borderRadius:RADIUS.lg,
          background:'#171A21',
          border:`1px solid ${COLORS.rimDark}`,
          overflow:'hidden',
          opacity:physicalSpring(frame,fps,26,14),
          boxShadow:'0 30px 90px rgba(0,0,0,.28)',
        }}>
          <div style={{borderRight:`1px solid ${COLORS.rimDark}`,padding:24}}>
            <div style={{fontSize:22,fontWeight:700}}>FILES CHANGED <span style={{color:'#9AA6FF'}}>3</span></div>
            <div style={{marginTop:28,display:'grid',gap:28}}>
              {files.map(([name,delta],i)=>(
                <div key={name} style={{opacity:i===0?1:.58}}>
                  <div style={{fontSize:18,lineHeight:1.35,color:COLORS.surface,wordBreak:'break-word'}}>{name}</div>
                  <div style={{fontSize:17,color:i===0?COLORS.success:COLORS.mutedOnDark,marginTop:8,fontFamily:TYPE.monoFamily}}>{delta}</div>
                </div>
              ))}
            </div>
          </div>
          <div style={{padding:26,fontFamily:TYPE.monoFamily,fontSize:20,lineHeight:1.72}}>
            <div style={{display:'flex',justifyContent:'space-between',color:COLORS.mutedOnDark,marginBottom:20}}>
              <span>DIFF</span><span>reset.tsx</span>
            </div>
            {lines.map((line,i)=>{
              const visible=i/Math.max(1,lines.length-1)<=reveal;
              const changed=i===0||i===1||(i>=5&&i<=7);
              return (
                <div key={`${i}-${line}`} style={{
                  minHeight:34,
                  padding:'1px 8px',
                  margin:'0 -8px',
                  background:changed&&visible?'rgba(22,163,74,.14)':'transparent',
                  color:visible?(changed?'#8FE6AC':'#E5E7EB'):'#59606D',
                  opacity:visible?1:.14,
                }}>
                  <span style={{display:'inline-block',width:34,color:'#697180'}}>{i+15}</span>{line || ' '}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </Frame>
  );
};
