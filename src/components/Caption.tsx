import React from 'react';
import {COLORS, RADIUS, SPACE, TYPE} from '../tokens';

export const Caption: React.FC<{text: string; emphasis?: string}> = ({text, emphasis}) => {
  const [before, after] = emphasis && text.includes(emphasis) ? text.split(emphasis) : [text, ''];
  return <div style={{
    position:'absolute', left:SPACE.x, right:SPACE.x, bottom:120,
    display:'flex', justifyContent:'center', textAlign:'center',
  }}>
    <div style={{
      fontSize:TYPE.caption, fontWeight:700, lineHeight:1.15,
      background:'rgba(255,255,255,0.94)', color:COLORS.foreground,
      border:`1px solid ${COLORS.border}`, borderRadius:RADIUS.md,
      padding:'18px 26px', boxShadow:'0 12px 40px rgba(0,0,0,.07)', maxWidth:900,
    }}>
      {before}{emphasis ? <span style={{color:COLORS.accent}}>{emphasis}</span> : null}{after}
    </div>
  </div>;
};
