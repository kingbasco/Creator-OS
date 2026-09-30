import React from 'react';
import {Audio} from '@remotion/media';
import {AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {DesignCanvas} from '../components/DesignCanvas';
import {Caption} from '../components/Caption';
import {COLORS as C, TYPE, SHADOW} from '../tokens';
import {v03Scenes} from '../content/v03';
import {v03VoicedTimeline} from '../content/v03-timeline';
import {V03SoundDesign} from '../components/V03SoundDesign';
import {v03Audio} from '../generated/v03-audio';

type Scene = typeof v03VoicedTimeline[number];
const ease = {extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)} as const;
const Card:React.FC<React.PropsWithChildren<{delay?:number;dark?:boolean}>>=({children,delay=0,dark=false})=>{
  const f=useCurrentFrame();
  const p=interpolate(f,[delay,delay+22],[0,1],ease);
  return <div style={{opacity:p,transform:`translate(${(1-p)*50}px,${(1-p)*35}px)`,padding:32,borderRadius:24,border:`2px solid ${dark?C.rimDark:C.border}`,background:dark?C.darkSurface:C.surface,color:dark?'white':C.foreground,boxShadow:SHADOW,fontSize:38,lineHeight:1.25}}>{children}</div>;
};

const Visual:React.FC<{index:number;duration:number}>=({index,duration})=>{
  const f=useCurrentFrame();
  const progress=interpolate(f,[0,Math.max(1,duration-25)],[0,1],ease);
  if(index===0)return <Card><div style={{fontSize:28,color:C.muted,marginBottom:28}}>workspace / new project</div><b style={{fontSize:54}}>Launch checklist</b>{['Account connected','Data saved','Project created'].map((t,i)=><div key={t} style={{marginTop:36,opacity:interpolate(f,[18+i*22,34+i*22],[0,1],ease),color:C.success}}>✓ {t}</div>)}<div style={{marginTop:42,height:10,background:C.well,borderRadius:6}}><div style={{width:`${progress*100}%`,height:10,background:C.success,borderRadius:6}}/></div></Card>;
  if(index===1)return <><Card><b style={{color:C.accent}}>ONE TESTED ROUTE</b><div style={{marginTop:28,color:C.success}}>Sign in → Submit → Success</div></Card>{['Session expired?','Request repeats?','Network drops?'].map((t,i)=><Card key={t} delay={35+i*20}>{t}</Card>)}</>;
  if(index===2)return <>{[['Bad input','Validate before saving'],['Session expired','Return to sign in'],['Slow network','Retry safely'],['Duplicate request','One intended result']].map(([a,b],i)=><Card key={a} delay={i*20}><div style={{display:'flex',justifyContent:'space-between',gap:20}}><b style={{color:C.warning}}>{a}</b><span style={{fontSize:30,color:C.muted}}>{b}</span></div></Card>)}</>;
  if(index===3)return <><Card><span style={{fontSize:28,color:C.muted}}>ILLUSTRATIVE ACCESS CHECK</span><div style={{marginTop:26}}>User A requests a record</div></Card><Card delay={22} dark><div style={{fontSize:30,color:C.mutedOnDark}}>DATABASE / POLICY BOUNDARY</div><div style={{marginTop:28,color:C.success}}>Own record → Allowed</div><div style={{marginTop:28,color:f<75?C.danger:C.success}}>{f<75?'Another user’s row → Too open':'Another user’s row → Denied'}</div><div style={{marginTop:30,fontSize:30}}>Verify user identity and enforce access.</div></Card></>;
  if(index===4)return <>{['PREVIEW','PRODUCTION'].map((t,i)=><Card key={t} delay={i*24}><div style={{fontSize:30,color:C.muted}}>{t}</div><div style={{marginTop:30,fontSize:44,color:i?C.warning:C.success}}>{i?'Required setting missing':'Configuration present'}</div><div style={{marginTop:24,height:10,background:i?C.warning:C.success,width:i?'45%':'100%',borderRadius:6}}/></Card>)}<div style={{fontSize:30,color:C.muted}}>Example configurations. No credentials shown.</div></>;
  if(index===5)return <><Card dark><div style={{color:C.danger,fontSize:30}}>REQUEST FAILED</div><pre style={{fontFamily:TYPE.monoFamily,fontSize:30,whiteSpace:'pre-wrap',marginBottom:0}}>request_id: demo-042{'\n'}reason: missing configuration</pre></Card>{['Test reproduces the failure','Log points to the cause','Monitoring flags the event'].map((t,i)=><Card key={t} delay={25+i*22}><span style={{color:C.accent}}>{t}</span></Card>)}</>;
  if(index===6)return <>{['Edge cases tested','Access boundaries checked','Environments verified','Tests pass','Monitoring connected'].map((t,i)=><Card key={t} delay={i*24}><span style={{color:C.success}}>✓ </span>{t}</Card>)}<div style={{fontSize:32,color:C.muted}}>Human review: check the evidence.</div></>;
  return <><div style={{fontSize:70,fontWeight:700,color:C.muted}}>DEMO</div><div style={{fontSize:86,fontWeight:750,color:C.accent,transform:`translateX(${(1-progress)*20}px)`}}>RELIABILITY</div><div style={{fontSize:86,fontWeight:750}}>PRODUCT</div><Card delay={55}><div style={{color:C.accent,fontSize:30}}>NEXT / MCP</div><div style={{marginTop:25}}>AI connects to the tools around your app.</div></Card></>;
};

const SceneLayer:React.FC<{scene:Scene;index:number;enter:number}>=({scene,index,enter})=>{
  const f=useCurrentFrame();
  const p=interpolate(f,[0,Math.max(1,enter)],[0,1],ease);
  const exit=index===7?0:interpolate(f,[enter+scene.durationInFrames-18,enter+scene.durationInFrames],[0,1],ease);
  return <AbsoluteFill style={{background:C.background,opacity:p*(1-exit),transform:`translateY(${(1-p)*80-exit*60}px)`}}>
    <div style={{position:'absolute',top:170,left:88,right:88,fontSize:90,fontWeight:750,letterSpacing:'-.04em',lineHeight:1.08}}>{scene.onScreenText}</div>
    <div style={{position:'absolute',top:500,left:88,right:88,display:'flex',flexDirection:'column',gap:24}}><Visual index={index} duration={scene.durationInFrames}/></div>
  </AbsoluteFill>;
};

const Film:React.FC<{voiced?:boolean}>=({voiced=false})=>{
  const frame=useCurrentFrame();
  const timeline:Scene[]=voiced?v03VoicedTimeline:v03Scenes.map(s=>({...s,from:s.startSec*30,durationInFrames:(s.endSec-s.startSec)*30,audioPath:null,measuredAudioDurationSec:null}));
  const total=timeline.reduce((n,s)=>n+s.durationInFrames,0);
  return <DesignCanvas><AbsoluteFill style={{fontFamily:TYPE.fontFamily,color:C.foreground}}>
    {timeline.map((scene,index)=>{const enter=index?18:0;return <React.Fragment key={scene.id}>
      <Sequence from={scene.from-enter} durationInFrames={scene.durationInFrames+enter} name={`V03-${scene.id}-visual`}><SceneLayer scene={scene} index={index} enter={enter}/></Sequence>
      <Sequence from={scene.from} durationInFrames={scene.durationInFrames} name={`V03-${scene.id}-narration`}>
        {voiced&&scene.audioPath?<Audio src={staticFile(scene.audioPath)}/>:null}
        <Caption text={scene.captionText??scene.narration}/>
      </Sequence>
    </React.Fragment>;})}
    <div style={{position:'absolute',left:88,top:100,width:904,height:6,background:C.border,borderRadius:8}}><div style={{height:6,width:`${frame/total*100}%`,background:C.accent,borderRadius:8}}/></div>
  </AbsoluteFill></DesignCanvas>;
};
export const V03:React.FC=()=> <Film/>;
export const V03Voiced:React.FC=()=>{
  if(!v03Audio.enabled||v03VoicedTimeline.some(s=>!s.audioPath))throw new Error('V03 narration is unavailable. Run voice:v03 before rendering the voiced composition.');
  return <Film voiced/>;
};

export const V03Final:React.FC=()=> <><V03Voiced/><V03SoundDesign/></>;
