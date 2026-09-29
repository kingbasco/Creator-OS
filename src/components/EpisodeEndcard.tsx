import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {springScale} from '../utils';

export const EpisodeEndcard: React.FC = () => {const frame=useCurrentFrame();const {fps}=useVideoConfig();return <Frame>
 <div style={{display:'flex',flexDirection:'column',justifyContent:'center',height:'100%'}}>
  {['DIRECTION','ITERATION','JUDGMENT'].map((x,i)=><div key={x} style={{fontSize:TYPE.hero,fontWeight:900,lineHeight:1,letterSpacing:-4,color:i===2?COLORS.accent:COLORS.foreground,transform:`scale(${springScale(frame,fps,i*10)})`,transformOrigin:'left center'}}>{x}</div>)}
  <div style={{marginTop:100,padding:36,borderRadius:RADIUS.lg,background:COLORS.darkSurface,color:'white'}}>
   <div style={{fontSize:28,color:'#AAB4FF',fontWeight:800}}>NEXT EPISODE • V02</div>
   <div style={{fontSize:54,fontWeight:800,lineHeight:1.1,marginTop:14}}>What an AI coding agent is actually doing.</div>
  </div>
 </div>
 </Frame>};
