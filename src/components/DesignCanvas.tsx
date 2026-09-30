import React from 'react';
import {AbsoluteFill,useVideoConfig} from 'remotion';
import {COLORS,VIDEO} from '../tokens';

export const DesignCanvas:React.FC<React.PropsWithChildren>=({children})=>{
  const {width,height}=useVideoConfig();
  const scale=Math.min(width/VIDEO.width,height/VIDEO.height);
  const left=(width-VIDEO.width*scale)/2;
  const top=(height-VIDEO.height*scale)/2;

  return <AbsoluteFill style={{backgroundColor:COLORS.background,overflow:'hidden'}}>
    <div style={{
      position:'absolute',
      width:VIDEO.width,
      height:VIDEO.height,
      left,
      top,
      transform:`scale(${scale})`,
      transformOrigin:'top left',
    }}>
      {children}
    </div>
  </AbsoluteFill>;
};
