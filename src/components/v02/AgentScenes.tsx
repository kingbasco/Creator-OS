import React from 'react';
import {interpolate} from 'remotion';
import {Frame} from '../Frame';
import {MotionBackdrop} from '../MotionBackdrop';
import {COLORS, FLOAT_SHADOW, RADIUS, TYPE} from '../../tokens';
import {clamp, drawProgress, fadeInUp, physicalSpring} from '../../utils';
import {useScaledSceneFrame} from '../../sceneTiming';

type SceneProps={durationInFrames?:number};

const panel=(dark=false):React.CSSProperties=>({
  borderRadius:RADIUS.lg,
  background:dark?COLORS.darkSurface:COLORS.surface,
  border:`1px solid ${dark?COLORS.rimDark:COLORS.border}`,
  boxShadow:dark?'0 24px 70px rgba(0,0,0,.22)':'0 18px 48px rgba(16,17,20,.07)',
});

const Mono:React.FC<React.PropsWithChildren<{muted?:boolean;success?:boolean;danger?:boolean}>>=({children,muted,success,danger})=>(
  <span style={{
    fontFamily:TYPE.monoFamily,
    color:danger?COLORS.danger:success?COLORS.success:muted?COLORS.mutedOnDark:'inherit',
  }}>{children}</span>
);

export const AgentHook:React.FC<SceneProps>=({durationInFrames})=>{
  const {frame,fps}=useScaledSceneFrame(durationInFrames,6);
  const codeIn=physicalSpring(frame,fps,4,14);
  const pullback=physicalSpring(frame,fps,45,20);
  const agent=physicalSpring(frame,fps,74,16);
  const line=interpolate(pullback,[0,1],[1.08,.72],clamp);
  return <Frame>
    <MotionBackdrop/>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,lineHeight:1,...fadeInUp(frame,fps)}}>
      AUTOCOMPLETE<br/><span style={{color:COLORS.muted}}>PREDICTS A LINE.</span>
    </div>
    <div style={{
      position:'absolute',left:120,top:430,width:840,height:730,
      ...panel(true),overflow:'hidden',opacity:codeIn,
      transform:`scale(${line}) translateY(${interpolate(pullback,[0,1],[100,0],clamp)}px)`,
      transformOrigin:'50% 28%',
    }}>
      <div style={{height:64,borderBottom:`1px solid ${COLORS.rimDark}`,display:'flex',alignItems:'center',padding:'0 24px',color:COLORS.mutedOnDark,fontSize:20}}>
        <Mono muted>src/auth.ts</Mono>
      </div>
      <div style={{padding:32,fontSize:25,lineHeight:1.9,color:'#E5E7EB'}}>
        <Mono>const reset = async () =&gt; {'{'}</Mono><br/>
        <Mono>&nbsp;&nbsp;await sendResetEmail(</Mono><br/>
        <span style={{display:'inline-block',marginLeft:64,color:'#9AA6FF',background:'rgba(91,108,255,.12)',padding:'0 8px',borderRadius:8}}>email</span><br/>
        <Mono>);</Mono><br/>
        <Mono>{'}'}</Mono>
      </div>
      <div style={{
        position:'absolute',left:48,right:48,bottom:46,height:3,
        background:`linear-gradient(90deg,${COLORS.accent} 0 44%,transparent 44%)`,
        borderRadius:99,
      }}/>
    </div>
    <div style={{
      position:'absolute',left:150,top:1070,width:780,
      opacity:agent,transform:`translateY(${interpolate(agent,[0,1],[60,0],clamp)}px)`,
    }}>
      <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,lineHeight:1.02}}>
        AN AGENT<br/><span style={{color:COLORS.accent}}>PURSUES A GOAL.</span>
      </div>
      <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:14,marginTop:34}}>
        {['REPO','PLAN','TERMINAL','TESTS'].map((x,i)=><div key={x} style={{
          height:92,borderRadius:RADIUS.md,display:'grid',placeItems:'center',
          background:i===0?COLORS.accentSoft:COLORS.surface,border:`1px solid ${COLORS.border}`,
          fontSize:20,fontWeight:700,color:i===0?COLORS.accent:COLORS.foreground,
        }}>{x}</div>)}
      </div>
    </div>
  </Frame>;
};

export const GoalScene:React.FC<SceneProps>=({durationInFrames})=>{
  const {frame,fps}=useScaledSceneFrame(durationInFrames,10);
  const goal=physicalSpring(frame,fps,10,14);
  const scan=drawProgress(frame,55,42);
  const repo=physicalSpring(frame,fps,38,16);
  return <Frame>
    <MotionBackdrop/>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>START WITH A <span style={{color:COLORS.accent}}>GOAL</span></div>
    <div style={{
      position:'absolute',left:100,top:390,width:880,padding:34,
      ...panel(false),background:COLORS.accentSoft,borderColor:'#D7DBFF',
      opacity:goal,transform:`translateY(${interpolate(goal,[0,1],[44,0],clamp)}px)`,
    }}>
      <div style={{fontSize:19,color:COLORS.accent,fontWeight:700}}>TASK</div>
      <div style={{fontSize:48,fontWeight:700,letterSpacing:'-.035em',marginTop:8}}>Add password reset</div>
      <div style={{fontSize:24,color:COLORS.muted,lineHeight:1.4,marginTop:15}}>Use existing auth patterns. Add validation and a clear success state.</div>
    </div>
    <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}}>
      <path d="M 540 650 C 540 720 540 760 540 830" fill="none" stroke={COLORS.accent} strokeWidth={4} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1-scan}/>
      <circle cx={540} cy={830} r={9} fill={COLORS.accent} opacity={scan}/>
    </svg>
    <div style={{
      position:'absolute',left:160,top:830,width:760,height:610,padding:28,
      ...panel(false),opacity:repo,transform:`scale(${interpolate(repo,[0,1],[.97,1],clamp)})`,
    }}>
      <div style={{fontSize:20,color:COLORS.muted,fontWeight:700}}>REPOSITORY</div>
      {['src/routes','src/components','src/lib','tests'].map((name,i)=>{
        const active=Math.min(1,Math.max(0,(scan-(i*.18))/.25));
        return <div key={name} style={{
          height:96,marginTop:20,borderRadius:RADIUS.md,padding:'0 24px',
          display:'flex',alignItems:'center',justifyContent:'space-between',
          background:active>.35?COLORS.accentSoft:COLORS.well,
          border:`1px solid ${active>.35?'#D7DBFF':COLORS.border}`,
        }}>
          <Mono><span style={{color:active>.35?COLORS.accent:COLORS.foreground}}>{name}</span></Mono>
          <span style={{width:14,height:14,borderRadius:99,background:active>.35?COLORS.accent:COLORS.border}}/>
        </div>;
      })}
    </div>
  </Frame>;
};

export const InspectScene:React.FC<SceneProps>=({durationInFrames})=>{
  const {frame,fps}=useScaledSceneFrame(durationInFrames,11);
  const items=[
    ['routes/reset.tsx','Route','reset action'],
    ['components/ResetForm.tsx','UI','form states'],
    ['lib/validation.ts','Validation','email rules'],
  ] as const;
  const cursor=interpolate(frame,[22,55,90,125],[500,606,712,712],clamp);
  return <Frame>
    <MotionBackdrop/>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>INSPECT THE <span style={{color:COLORS.accent}}>REPOSITORY</span></div>
    <div style={{position:'absolute',left:86,top:410,width:440,height:960,padding:26,...panel(false)}}>
      <div style={{fontSize:20,fontWeight:700,color:COLORS.muted}}>PROJECT</div>
      {['routes/reset.tsx','components/ResetForm.tsx','lib/validation.ts','lib/auth.ts','tests/reset.test.ts'].map((x,i)=>{
        const active=i<3?physicalSpring(frame,fps,28+i*26,12):0;
        return <div key={x} style={{
          marginTop:18,height:88,borderRadius:RADIUS.md,padding:'0 20px',display:'flex',alignItems:'center',
          background:active>.4?COLORS.accentSoft:COLORS.well,
          border:`1px solid ${active>.4?'#D7DBFF':COLORS.border}`,
          color:active>.4?COLORS.accent:COLORS.muted,
        }}><Mono>{x}</Mono></div>;
      })}
      <div style={{
        position:'absolute',left:496,top:cursor,width:18,height:18,borderRadius:99,
        background:COLORS.accent,boxShadow:`0 0 0 12px ${COLORS.accentSoft}`,
      }}/>
    </div>
    <div style={{position:'absolute',left:570,top:410,width:420,height:960}}>
      <div style={{fontSize:20,fontWeight:700,color:COLORS.muted,marginBottom:18}}>CONTEXT COLLECTED</div>
      {items.map(([file,title,copy],i)=>{
        const p=physicalSpring(frame,fps,44+i*30,14);
        return <div key={file} style={{
          marginBottom:28,padding:28,...panel(false),opacity:p,
          transform:`translateX(${interpolate(p,[0,1],[50,0],clamp)}px)`,
        }}>
          <div style={{fontSize:17,fontWeight:700,color:COLORS.accent}}>{title.toUpperCase()}</div>
          <div style={{fontSize:34,fontWeight:700,marginTop:8}}>{copy}</div>
          <div style={{fontSize:18,color:COLORS.muted,marginTop:12}}><Mono>{file}</Mono></div>
        </div>;
      })}
      <div style={{fontSize:33,fontWeight:700,lineHeight:1.15,marginTop:54}}>Inspect before changing.</div>
    </div>
  </Frame>;
};

export const PlanScene:React.FC<SceneProps>=({durationInFrames})=>{
  const {frame,fps}=useScaledSceneFrame(durationInFrames,10);
  const steps=['Update route','Validate email','Send reset email','Add success state'];
  return <Frame>
    <MotionBackdrop/>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>BUILD A <span style={{color:COLORS.accent}}>PLAN</span></div>
    <div style={{fontSize:28,color:COLORS.muted,marginTop:26,maxWidth:760,lineHeight:1.4}}>Turn repository context into a short, reviewable sequence before the first edit.</div>
    <div style={{position:'absolute',left:150,top:520,width:780,padding:38,...panel(false)}}>
      <div style={{fontSize:19,color:COLORS.accent,fontWeight:700}}>PLAN · 4 STEPS</div>
      <div style={{position:'relative',marginTop:30}}>
        {steps.map((s,i)=>{
          const p=physicalSpring(frame,fps,28+i*24,14);
          return <div key={s} style={{
            position:'relative',height:170,display:'grid',gridTemplateColumns:'70px 1fr',gap:18,
            alignItems:'start',opacity:p,transform:`translateY(${interpolate(p,[0,1],[34,0],clamp)}px)`,
          }}>
            <div style={{
              width:52,height:52,borderRadius:99,display:'grid',placeItems:'center',
              background:i===0?COLORS.accent:COLORS.well,color:i===0?'white':COLORS.muted,
              fontSize:18,fontWeight:700,border:i===0?'none':`1px solid ${COLORS.border}`,
              zIndex:2,
            }}>0{i+1}</div>
            {i<steps.length-1?<div style={{position:'absolute',left:25,top:52,width:2,height:118,background:COLORS.border}}/>:null}
            <div>
              <div style={{fontSize:36,fontWeight:700}}>{s}</div>
              <div style={{fontSize:22,color:COLORS.muted,marginTop:8}}>
                {['Reuse the existing auth route.','Apply the current email rules.','Use the project email utility.','Show a clear completion state.'][i]}
              </div>
            </div>
          </div>;
        })}
      </div>
    </div>
  </Frame>;
};

export const ChangeScene:React.FC<SceneProps>=({durationInFrames})=>{
  const {frame,fps}=useScaledSceneFrame(durationInFrames,12);
  const reveal=interpolate(frame,[40,165],[0,1],clamp);
  const lines=[
    ['+','import {ValidEmail} from \'@/lib/validation\''],
    ['+','import {sendResetEmail} from \'@/lib/auth\''],
    [' ','const email = formData.get(\'email\')'],
    ['+','if (!ValidEmail(email)) {'],
    ['+',"  return json({error: 'Invalid email'})"],
    ['+','}'],
    [' ','await sendResetEmail(email)'],
  ] as const;
  return <Frame dark>
    <MotionBackdrop dark/>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>CHANGE <span style={{color:'#9AA6FF'}}>MULTIPLE FILES</span></div>
    <div style={{fontSize:26,color:COLORS.mutedOnDark,marginTop:24}}>One goal. Coordinated changes across the repository.</div>
    <div style={{position:'absolute',left:72,top:430,width:936,height:1050,display:'grid',gridTemplateColumns:'290px 1fr',overflow:'hidden',...panel(true)}}>
      <div style={{padding:28,borderRight:`1px solid ${COLORS.rimDark}`}}>
        <div style={{fontSize:18,fontWeight:700}}>FILES CHANGED <span style={{color:'#9AA6FF'}}>3</span></div>
        {[
          ['reset.tsx','+48  -12'],
          ['ResetForm.tsx','+28  -6'],
          ['validation.ts','+12  -2'],
        ].map(([name,delta],i)=>{
          const p=physicalSpring(frame,fps,18+i*24,12);
          return <div key={name} style={{marginTop:38,opacity:p}}>
            <Mono><span style={{fontSize:20,color:i===0?'white':COLORS.mutedOnDark}}>{name}</span></Mono>
            <div style={{fontSize:17,color:i===0?COLORS.success:COLORS.mutedOnDark,marginTop:9}}><Mono>{delta}</Mono></div>
          </div>;
        })}
      </div>
      <div style={{padding:30}}>
        <div style={{display:'flex',justifyContent:'space-between',fontSize:18,color:COLORS.mutedOnDark}}>
          <span>DIFF</span><Mono muted>src/routes/reset.tsx</Mono>
        </div>
        <div style={{marginTop:28,fontSize:19,lineHeight:2.05}}>
          {lines.map(([mark,txt],i)=>{
            const threshold=i/Math.max(1,lines.length-1);
            const visible=reveal>=threshold;
            const changed=mark==='+';
            return <div key={i} style={{
              minHeight:49,padding:'0 12px',margin:'0 -12px',
              background:changed&&visible?'rgba(22,163,74,.14)':'transparent',
              color:visible?(changed?'#91E9AE':'#E5E7EB'):'#59606D',
              opacity:visible?1:.13,
            }}>
              <Mono><span style={{display:'inline-block',width:42,color:'#697180'}}>{15+i}</span>{txt}</Mono>
            </div>;
          })}
        </div>
      </div>
    </div>
  </Frame>;
};

export const EvaluateScene:React.FC<SceneProps>=({durationInFrames})=>{
  const {frame,fps}=useScaledSceneFrame(durationInFrames,12);
  const failure=physicalSpring(frame,fps,115,14);
  const loop=drawProgress(frame,142,28);
  return <Frame dark>
    <MotionBackdrop dark/>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>RUN. TEST. <span style={{color:'#9AA6FF'}}>EVALUATE.</span></div>
    <div style={{position:'absolute',left:90,top:440,width:900,height:820,padding:32,...panel(true)}}>
      <div style={{fontSize:18,color:COLORS.mutedOnDark,fontWeight:700}}>TERMINAL</div>
      <div style={{fontSize:24,lineHeight:1.9,marginTop:28}}>
        <Mono>$ npm run test</Mono><br/>
        <span style={{opacity:physicalSpring(frame,fps,30,10)}}><Mono success>✓ auth route</Mono><br/></span>
        <span style={{opacity:physicalSpring(frame,fps,52,10)}}><Mono success>✓ reset form</Mono><br/></span>
        <span style={{opacity:physicalSpring(frame,fps,78,10)}}><Mono danger>✕ invalid email state</Mono><br/></span>
        <span style={{opacity:physicalSpring(frame,fps,98,10)}}><Mono danger>1 failed · 11 passed</Mono></span>
      </div>
      <div style={{
        marginTop:50,padding:26,borderRadius:RADIUS.md,background:'rgba(220,38,38,.08)',
        border:`1px solid ${COLORS.danger}`,opacity:failure,
      }}>
        <div style={{fontSize:16,fontWeight:700,color:COLORS.danger}}>FAILURE BECOMES NEW CONTEXT</div>
        <div style={{fontSize:32,fontWeight:700,marginTop:8}}>Validation fires too early.</div>
      </div>
    </div>
    <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}}>
      <path d="M 790 1330 C 580 1440, 270 1370, 260 1160" fill="none" stroke="#9AA6FF" strokeWidth={4} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1-loop}/>
      <circle cx={260} cy={1160} r={10} fill="#9AA6FF" opacity={loop}/>
    </svg>
    <div style={{position:'absolute',left:160,top:1400,width:760,fontSize:34,fontWeight:700,textAlign:'center',opacity:loop}}>
      Read the result. Use it. Keep going.
    </div>
  </Frame>;
};

export const ReviewScene:React.FC<SceneProps>=({durationInFrames})=>{
  const {frame,fps}=useScaledSceneFrame(durationInFrames,12);
  const gate=physicalSpring(frame,fps,105,18);
  return <Frame>
    <MotionBackdrop/>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,...fadeInUp(frame,fps)}}>THE AGENT EXECUTES.<br/><span style={{color:COLORS.accent}}>YOU VERIFY.</span></div>
    <div style={{position:'absolute',left:72,top:460,width:560,padding:30,...panel(false)}}>
      <div style={{fontSize:19,fontWeight:700,color:COLORS.muted}}>AUTOMATED CHECKS</div>
      {[
        ['Build','Passed'],
        ['Tests','Passed'],
        ['Diff','Ready for review'],
      ].map(([title,copy],i)=>{
        const p=physicalSpring(frame,fps,22+i*20,12);
        return <div key={title} style={{
          marginTop:22,padding:24,borderRadius:RADIUS.md,background:COLORS.well,
          display:'grid',gridTemplateColumns:'44px 1fr',gap:16,alignItems:'center',opacity:p,
        }}>
          <div style={{width:30,height:30,borderRadius:99,background:COLORS.success,display:'grid',placeItems:'center',color:'white',fontWeight:800}}>✓</div>
          <div><div style={{fontSize:27,fontWeight:700}}>{title}</div><div style={{fontSize:19,color:COLORS.muted,marginTop:4}}>{copy}</div></div>
        </div>;
      })}
      <div style={{height:9,borderRadius:99,background:COLORS.border,marginTop:30,overflow:'hidden'}}>
        <div style={{height:'100%',width:'100%',background:COLORS.success}}/>
      </div>
    </div>
    <div style={{
      position:'absolute',left:670,top:520,width:338,padding:30,...panel(false),
      boxShadow:FLOAT_SHADOW,opacity:gate,transform:`translateX(${interpolate(gate,[0,1],[70,0],clamp)}px)`,
    }}>
      <div style={{fontSize:17,color:COLORS.accent,fontWeight:700}}>HUMAN GATE</div>
      <div style={{fontSize:39,fontWeight:700,lineHeight:1.08,marginTop:18}}>Does this match what we asked for?</div>
      <div style={{fontSize:24,color:COLORS.muted,lineHeight:1.6,marginTop:26}}>Correct?<br/>Secure?<br/>Safe to ship?</div>
      <div style={{height:70,borderRadius:RADIUS.md,background:COLORS.accent,color:'white',display:'grid',placeItems:'center',fontSize:24,fontWeight:700,marginTop:32}}>Approve</div>
    </div>
  </Frame>;
};

export const MentalModelScene:React.FC<SceneProps>=({durationInFrames})=>{
  const {frame,fps}=useScaledSceneFrame(durationInFrames,9);
  const labels=['GOAL','INSPECT','PLAN','CHANGE','TEST','EVALUATE','REVIEW'];
  const settle=physicalSpring(frame,fps,28,18);
  const teaser=physicalSpring(frame,fps,126,16);
  return <Frame>
    <MotionBackdrop/>
    <div style={{fontSize:TYPE.sceneTitle,fontWeight:700,lineHeight:1.02,...fadeInUp(frame,fps)}}>
      FROM NEXT-LINE PREDICTION<br/><span style={{color:COLORS.accent}}>TO GOAL-DRIVEN EXECUTION.</span>
    </div>
    <div style={{position:'absolute',left:72,right:72,top:650,height:500}}>
      {labels.map((label,i)=>{
        const p=physicalSpring(frame,fps,12+i*8,12);
        const x=i%4;
        const row=Math.floor(i/4);
        const finalX=20+x*225+(row?110:0);
        const finalY=80+row*180;
        const startX=interpolate(p,[0,1],[finalX+(i%2?80:-60),finalX],clamp);
        return <React.Fragment key={label}>
          <div style={{
            position:'absolute',left:startX,top:finalY+(1-p)*50,width:190,height:82,
            borderRadius:RADIUS.md,display:'grid',placeItems:'center',
            background:i===0||i===labels.length-1?COLORS.accentSoft:COLORS.surface,
            border:`1px solid ${COLORS.border}`,fontSize:20,fontWeight:700,
            color:i===0||i===labels.length-1?COLORS.accent:COLORS.foreground,opacity:p,
            boxShadow:'0 10px 30px rgba(16,17,20,.05)',
          }}>{label}</div>
          {i<labels.length-1?<div style={{
            position:'absolute',left:finalX+190,top:finalY+39,width:35,height:3,
            background:COLORS.accent,opacity:settle,
          }}/>:null}
        </React.Fragment>;
      })}
    </div>
    <div style={{
      position:'absolute',left:108,top:1280,width:864,padding:38,
      ...panel(true),opacity:teaser,transform:`translateY(${interpolate(teaser,[0,1],[60,0],clamp)}px)`,
    }}>
      <div style={{fontSize:18,color:'#AAB4FF',fontWeight:700}}>NEXT · V03</div>
      <div style={{fontSize:46,fontWeight:700,lineHeight:1.08,color:'white',marginTop:16}}>Why a perfect-looking demo can still be fragile underneath.</div>
      <div style={{fontSize:22,color:COLORS.mutedOnDark,lineHeight:1.4,marginTop:16}}>We’ll look beneath the interface at reliability, edge cases, and security.</div>
    </div>
  </Frame>;
};
