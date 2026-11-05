import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

const palette = {paper:'#F6F4EC', plum:'#29083D', purple:'#75439A', lavender:'#C7A6D9', gold:'#E6BD55'};
const progress=(frame:number,start:number,end:number)=>interpolate(frame,[start,end],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.inOut(Easing.cubic)});
const visibility=(frame:number,start:number,end:number)=>progress(frame,start,start+12)*(1-progress(frame,end-12,end));

const Paper=()=> <AbsoluteFill style={{backgroundColor:palette.paper}}>
  <svg width="100%" height="100%" style={{position:'absolute',opacity:.15}}>
    <filter id="paper-grain"><feTurbulence type="fractalNoise" baseFrequency=".62" numOctaves="3" seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
    <rect width="100%" height="100%" filter="url(#paper-grain)" opacity=".18"/>
  </svg>
</AbsoluteFill>;

const Coin=({rotation=0}:{rotation?:number})=><svg width="550" height="550" viewBox="0 0 550 550" style={{overflow:'visible',transform:`rotate(${rotation}deg)`,filter:'drop-shadow(0 24px 16px rgba(41,8,61,.18))'}}>
  <defs><radialGradient id="gold-face" cx="27%" cy="20%" r="90%"><stop stopColor="#fff5c8"/><stop offset=".3" stopColor="#f2d27c"/><stop offset=".65" stopColor="#d6a13d"/><stop offset="1" stopColor="#a57323"/></radialGradient></defs>
  <circle cx="275" cy="290" r="235" fill="#9d6c27"/><circle cx="275" cy="270" r="235" fill="url(#gold-face)" stroke="#b98430" strokeWidth="12"/>
  <circle cx="275" cy="270" r="205" fill="none" stroke="#fff0a6" strokeWidth="7"/><circle cx="275" cy="270" r="185" fill="none" stroke="#ac7b34" strokeWidth="3" strokeDasharray="5 12"/>
  <text x="275" y="360" textAnchor="middle" fontFamily="Georgia,serif" fontSize="240" fontWeight="bold" fill="#9d6b20">₿</text>
  <text x="270" y="353" textAnchor="middle" fontFamily="Georgia,serif" fontSize="240" fontWeight="bold" fill="#fff0b0">₿</text>
</svg>;

const Bank=()=> <svg width="610" height="560" viewBox="0 0 610 560" style={{filter:'drop-shadow(0 22px 12px rgba(41,8,61,.18))'}}>
  <path d="M70 165 L305 35 L540 165 Z" fill="#51236f" stroke="#29083D" strokeWidth="9"/>
  <rect x="105" y="175" width="400" height="43" fill="#a47abb"/>
  {[145,245,345,445].map(x=><g key={x}><rect x={x-25} y="222" width="50" height="238" fill="#8751a1"/><path d={`M${x-10} 240 V440`} stroke="#c7a6d9" strokeWidth="9"/></g>)}
  <rect x="70" y="460" width="470" height="43" fill="#51236f"/><rect x="40" y="503" width="530" height="33" fill="#29083D"/>
</svg>;

const Network=({p}:{p:number})=>{const pts=[[300,60],[105,220],[495,220],[160,465],[440,465]];const edges=[[0,1],[0,2],[1,2],[1,3],[2,4],[3,4],[0,4]];return <svg width="600" height="550" viewBox="0 0 600 550" style={{filter:'drop-shadow(0 13px 8px rgba(41,8,61,.14))'}}>
  {edges.map(([a,b],i)=><line key={i} x1={pts[a][0]} y1={pts[a][1]} x2={pts[b][0]} y2={pts[b][1]} stroke={palette.purple} strokeWidth="8" pathLength={1} strokeDasharray="1" strokeDashoffset={1-p}/>)}
  {pts.map(([x,y],i)=><g key={i} transform={`translate(${x} ${y}) scale(${Math.max(.001,progress(p,i*.1,i*.1+.35))})`}><circle r="48" fill={palette.plum}/><circle r="31" fill={palette.lavender}/><circle r="11" fill={palette.gold}/></g>)}
</svg>};

const Blockchain=({p}:{p:number})=><svg width="800" height="440" viewBox="0 0 800 440" style={{filter:'drop-shadow(0 18px 12px rgba(41,8,61,.14))'}}>
  {[0,1,2,3].map(i=>{const a=progress(p,i*.17,i*.17+.36),x=30+i*195;return <g key={i} opacity={a} transform={`translate(${x} ${(1-a)*-110})`}>
    <path d="M0 85 L70 30 L158 80 L88 140Z" fill="#e3d2ef" stroke="#75439A" strokeWidth="5"/>
    <path d="M0 85 L88 140 V270 L0 213Z" fill="#a97bc1" stroke="#75439A" strokeWidth="5"/>
    <path d="M88 140 L158 80 V212 L88 270Z" fill="#c7a6d9" stroke="#75439A" strokeWidth="5"/>
    <text x="43" y="195" fontSize="64" fontWeight="bold" fill={palette.gold}>₿</text>
    {i<3&&<path d="M158 160 H193" stroke={palette.purple} strokeWidth="9"/>}
  </g>})}
</svg>;

const Center=({children,opacity=1,scale=1,top=760}:{children:React.ReactNode,opacity?:number,scale?:number,top?:number})=><div style={{position:'absolute',top,left:0,right:0,display:'flex',justifyContent:'center',opacity,transform:`scale(${scale})`}}>{children}</div>;
const Title=({frame,start,end,lines}:{frame:number,start:number,end:number,lines:string[]})=><div style={{position:'absolute',top:335,left:65,right:65,textAlign:'center',fontFamily:'Inter,Arial,sans-serif',fontWeight:800,fontSize:76,lineHeight:1.05,letterSpacing:-3,color:palette.plum,opacity:visibility(frame,start,end),transform:`translateY(${(1-progress(frame,start,start+15))*32}px)`}}>{lines.map(line=><div key={line}>{line}</div>)}</div>;

export const BitcoinExplainerV3:React.FC=()=>{
  const f=useCurrentFrame(),{fps}=useVideoConfig();
  const fall=spring({frame:f,fps,config:{damping:15,stiffness:90,mass:1.4}});
  const bankIn=progress(f,62,80),bankOut=progress(f,94,114);
  const netIn=progress(f,96,126),netOut=progress(f,131,148);
  const blocksIn=progress(f,137,190),blocksOut=progress(f,216,242);
  const outro=progress(f,229,258);
  return <AbsoluteFill><Paper/>
    <div style={{position:'absolute',top:82,left:70,color:palette.purple,fontFamily:'Inter,Arial,sans-serif',fontSize:26,fontWeight:700,letterSpacing:5}}>CREATOR OS / EXPLAINED</div>
    <Title frame={f} start={0} end={70} lines={['WHAT IF MONEY','NEEDED NO BANK?']}/>
    <Title frame={f} start={68} end={141} lines={['NO CENTRAL BANK.']}/>
    <Title frame={f} start={139} end={229} lines={['POWERED BY','BLOCKCHAIN.']}/>
    <Center top={730} opacity={1-bankIn} scale={.7+.3*fall}><Coin rotation={-15+15*fall}/></Center>
    <Center top={730} opacity={bankIn*(1-bankOut)} scale={.8+.2*bankIn}><Bank/></Center>
    <Center top={730} opacity={netIn*(1-netOut)}><Network p={netIn}/></Center>
    <Center top={790} opacity={blocksIn*(1-blocksOut)} scale={.85+.15*blocksIn}><Blockchain p={blocksIn}/></Center>
    <div style={{position:'absolute',top:300,left:0,right:0,textAlign:'center',opacity:outro,color:palette.plum,fontFamily:'Inter,Arial,sans-serif'}}>
      <div style={{fontSize:115,fontWeight:800,letterSpacing:-5}}>BITCOIN</div>
      <div style={{fontSize:38,fontWeight:500,letterSpacing:1}}>DECENTRALIZED DIGITAL MONEY.</div>
    </div>
    <Center top={790} opacity={outro} scale={.5+.5*outro}><div style={{position:'absolute',width:680,height:680,borderRadius:'50%',background:'#e7d8ef',opacity:.7}}/><Coin rotation={progress(f,235,270)*18}/></Center>
    <div style={{position:'absolute',bottom:110,left:70,right:70,height:3,background:'#dacdde'}}><div style={{height:'100%',width:`${f/299*100}%`,background:palette.purple}}/></div>
  </AbsoluteFill>;
};
