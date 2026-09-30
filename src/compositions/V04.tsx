import React from 'react';
import {Audio} from '@remotion/media';
import {AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {DesignCanvas} from '../components/DesignCanvas';
import {Caption} from '../components/Caption';
import {COLORS as C, TYPE, SHADOW} from '../tokens';
import {v04Scenes} from '../content/v04';
import {v04VoicedTimeline} from '../content/v04-timeline';
import {v04Audio} from '../generated/v04-audio';

const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)} as const;
const reveal=(f:number,start=0)=>interpolate(f,[start,start+22],[0,1],clamp);
const Box:React.FC<React.PropsWithChildren<{label:string;delay?:number;accent?:boolean}>>=({label,delay=0,accent=false,children})=>{
 const f=useCurrentFrame(),p=reveal(f,delay);
 return <div style={{opacity:p,transform:`translateY(${(1-p)*35}px)`,padding:32,borderRadius:24,border:`2px solid ${accent?C.accent:C.border}`,background:accent?C.accentSoft:C.surface,boxShadow:SHADOW}}>
  <div style={{fontSize:28,color:accent?C.accent:C.muted,fontWeight:650,marginBottom:14}}>{label}</div>
  <div style={{fontSize:42,lineHeight:1.3,fontWeight:650}}>{children}</div>
 </div>;
};
const Connector:React.FC<{reverse?:boolean;delay?:number;label?:string}>=({reverse=false,delay=0,label=''})=>{
 const f=useCurrentFrame(),p=reveal(f,delay);
 const travel=interpolate(f,[delay+20,delay+80],[reverse?1:0,reverse?0:1],clamp);
 return <div style={{height:100,position:'relative',opacity:p,display:'flex',alignItems:'center',justifyContent:'center'}}>
 <svg width="80" height="100" style={{position:'absolute',left:90}} viewBox="0 0 80 100">
  <path d={reverse?'M40 92 V10 M24 26 L40 10 L56 26':'M40 8 V90 M24 74 L40 90 L56 74'} fill="none" stroke={C.accent} strokeWidth="5" strokeLinecap="round" strokeLinejoin="round"/>
  <circle cx="40" cy={10+travel*80} r="8" fill={C.accent}/>
 </svg><span style={{fontSize:28,color:C.accent,paddingLeft:70}}>{label}</span></div>;
};
const Visual:React.FC<{index:number}>=({index})=>{
 const f=useCurrentFrame();
 if(index===0)return <><Box label="AI APPLICATION" accent>“Find my project file.”</Box><Connector label="MCP" delay={20}/><Box label="CONNECTED CAPABILITIES" delay={35}>Files · Database · Services</Box></>;
 if(index===1)return <><Box label="HOST / AI APPLICATION">Your app <div style={{marginTop:24,padding:24,background:C.well,borderRadius:16,color:C.accent}}>MCP client</div></Box><Connector delay={22} label="standard exchange"/><Box label="MCP SERVER" delay={40}>Exposes tools and context</Box></>;
 if(index===2)return <><Box label="CLIENT → SERVER" accent>tools/list</Box><Connector label="available capabilities" delay={20}/><Box label="TOOL DESCRIPTION" delay={40}><code style={{fontSize:38}}>search_files(query)</code><div style={{fontSize:30,color:C.muted,marginTop:24}}>Input: search query<br/>Result: matching files</div></Box></>;
 if(index===3)return <><Box label="USER GOAL">Find the production brief</Box><Connector label="tools/call" delay={18}/><Box label="ILLUSTRATIVE TOOL INPUT" delay={40} accent><code style={{fontSize:34}}>search_files</code><div style={{fontSize:32,marginTop:20,fontFamily:TYPE.monoFamily}}>query: “production brief”</div></Box><Connector label="connected file system" delay={65}/></>;
 if(index===4)return <><Box label="CONNECTED SYSTEM">production-brief.md</Box><Connector reverse label="tool result" delay={18}/><Box label="AI APPLICATION" delay={40} accent>Uses the returned context<div style={{fontSize:30,color:C.muted,marginTop:24}}>“Here is the brief you asked for.”</div></Box></>;
 if(index===5)return <><Box label="AI CLIENT" accent>One common exchange</Box><Connector label="specific server capabilities" delay={20}/>{['File search','Database query','Service API'].map((t,i)=><Box key={t} label={'MCP SERVER / '+(i+1)} delay={40+i*20}>{t}</Box>)}</>;
 if(index===6)return <><Box label="2026-07-28 / STATELESS CORE">Metadata travels with each request</Box><Connector label="access remains controlled" delay={20}/><Box label="PERMISSION BOUNDARY" delay={40} accent>Allowed tools and data<div style={{fontSize:32,color:C.muted,marginTop:22}}>Review sensitive actions</div></Box><div style={{fontSize:28,color:C.muted,marginTop:26}}>A protocol is not blanket permission.</div></>;
 return <><div style={{fontSize:108,fontWeight:750,letterSpacing:'-.05em',color:C.accent,opacity:reveal(f)}}>MCP</div><div style={{fontSize:58,lineHeight:1.2,margin:'24px 0 48px'}}>AI client ↔ Server ↔ Tools</div><Box label="THE MENTAL MODEL" delay={25}>A program exposing capabilities</Box><div style={{marginTop:48,fontSize:38,color:C.muted}}>Next / The layers behind your app</div></>;
};
type Scene=typeof v04VoicedTimeline[number];
const Film:React.FC<{voiced?:boolean}>=({voiced=false})=>{
 const frame=useCurrentFrame();
 const timeline:Scene[]=voiced?v04VoicedTimeline:v04Scenes.map(s=>({...s,from:s.startSec*30,durationInFrames:(s.endSec-s.startSec)*30,audioPath:null,measuredAudioDurationSec:null}));
 const total=timeline.reduce((n,s)=>n+s.durationInFrames,0);
 return <DesignCanvas><AbsoluteFill style={{fontFamily:TYPE.fontFamily,color:C.foreground}}>
 {timeline.map((scene,index)=><Sequence key={scene.id} from={scene.from} durationInFrames={scene.durationInFrames} name={'V04-'+scene.id}><SceneLayer scene={scene} index={index}/>{voiced&&scene.audioPath?<Audio src={staticFile(scene.audioPath)}/>:null}<Caption text={scene.captionText??scene.narration}/></Sequence>)}
 <div style={{position:'absolute',left:88,top:100,width:904,height:6,background:C.border,borderRadius:8}}><div style={{height:6,width:`${frame/total*100}%`,background:C.accent,borderRadius:8}}/></div>
 </AbsoluteFill></DesignCanvas>;
};
const SceneLayer:React.FC<{scene:Scene;index:number}>=({scene,index})=>{
 const f=useCurrentFrame(),entry=reveal(f),exit=index===7?0:interpolate(f,[scene.durationInFrames-14,scene.durationInFrames],[0,1],clamp);
 return <AbsoluteFill style={{opacity:entry*(1-exit),transform:`translateY(${(1-entry)*35-exit*25}px)`}}>
 <div style={{position:'absolute',top:175,left:88,right:88,fontSize:86,fontWeight:750,lineHeight:1.12,letterSpacing:'-.04em'}}>{scene.onScreenText}</div>
 <div style={{position:'absolute',top:475,left:88,right:88,display:'flex',flexDirection:'column',gap:12}}><Visual index={index}/></div>
 </AbsoluteFill>;
};
export const V04:React.FC=()=> <Film/>;
export const V04Voiced:React.FC=()=>{
 if(!v04Audio.enabled||v04VoicedTimeline.some(s=>!s.audioPath))throw new Error('V04 narration is unavailable. Supply verified audio before final rendering.');
 return <Film voiced/>;
};

