import React from 'react';

export const MotionBackdrop: React.FC<{dark?:boolean}> = ({dark=false}) => {
  const line=dark?'rgba(255,255,255,.045)':'rgba(16,17,20,.035)';
  const wash=dark?'rgba(91,108,255,.08)':'rgba(91,108,255,.055)';

  return (
    <div style={{position:'absolute',inset:0,overflow:'hidden',pointerEvents:'none'}}>
      <div style={{
        position:'absolute',
        inset:0,
        backgroundImage:`
          linear-gradient(${line} 1px, transparent 1px),
          linear-gradient(90deg,${line} 1px, transparent 1px)
        `,
        backgroundSize:'96px 96px',
        maskImage:'linear-gradient(to bottom, rgba(0,0,0,.55), transparent 72%)',
      }}/>
      <div style={{
        position:'absolute',
        width:760,
        height:420,
        left:160,
        top:180,
        background:`radial-gradient(ellipse at center, ${wash}, transparent 70%)`,
        opacity:.9,
      }}/>
    </div>
  );
};
