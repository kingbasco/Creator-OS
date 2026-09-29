import React from 'react';
import {AbsoluteFill} from 'remotion';
import {COLORS, SPACE, TYPE} from '../tokens';

export const Frame: React.FC<React.PropsWithChildren<{dark?: boolean}>> = ({children, dark=false}) => (
  <AbsoluteFill style={{
    backgroundColor: dark ? COLORS.darkSurface : COLORS.background,
    color: dark ? COLORS.surface : COLORS.foreground,
    fontFamily: TYPE.fontFamily,
    padding: `${SPACE.top}px ${SPACE.x}px ${SPACE.bottom}px`,
    boxSizing: 'border-box',
  }}>
    {children}
  </AbsoluteFill>
);
