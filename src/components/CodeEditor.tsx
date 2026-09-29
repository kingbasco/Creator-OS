import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame} from './Frame';
import {COLORS, RADIUS, TYPE} from '../tokens';
import {fadeInUp, clamp} from '../utils';

export const CodeEditor: React.FC = () => {
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const progress=interpolate(frame,[22,70],[0,1],clamp);
 const code=[
  "export async function resetPassword(email) {",
  "  const user = await findUser(email);",
  "  const token = await createResetToken(user.id);",
  "  return sendResetEmail(email, token);",
  "}",
 ];
 return <Frame dark>
  <div style={{fontSize:TYPE.sceneTitle,fontWeight:800,...fadeInUp(frame,fps)}}>DESCRIBE INTENT.<br/><span style={{color:'#9AA6FF'}}>AI PROPOSES.</span></div>
  <div style={{marginTop:90,padding:32,borderRadius:RADIUS.lg,background:'#171A21',border:'1px solid #282D39',boxShadow:'0 30px 90px rgba(0,0,0,.35)'}}>
   <div style={{display:'grid',gridTemplateColumns:'240px 1fr',minHeight:760}}>
    <div style={{borderRight:'1px solid #2B303A',paddingRight:24,fontSize:26,color:'#A8B0BF',lineHeight:1.9}}>
      <div style={{color:'white',fontWeight:700}}>src/</div><div>auth.ts</div><div>email.ts</div><div>routes.ts</div>
    </div>
    <div style={{paddingLeft:34,fontFamily:TYPE.monoFamily,fontSize:TYPE.code,lineHeight:1.7}}>
      <div style={{color:'#9299A8',marginBottom:26}}>Change: Add password reset</div>
      {code.map((l,i)=><div key={l} style={{opacity:i/(code.length-1)<=progress?1:.12,color:i===2?'#AAB4FF':'#E5E7EB'}}>{l}</div>)}
    </div>
   </div>
  </div>
 </Frame>;
};
