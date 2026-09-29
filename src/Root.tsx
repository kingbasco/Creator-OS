import React from 'react';
import {Composition, Folder} from 'remotion';
import {V01} from './compositions/V01';
import {VIDEO} from './tokens';

export const RemotionRoot: React.FC = () => <>
  <Folder name="Creator-OS">
    <Composition
      id="V01-Vibe-Coding-Isnt-Magic"
      component={V01}
      durationInFrames={78*VIDEO.fps}
      fps={VIDEO.fps}
      width={VIDEO.width}
      height={VIDEO.height}
    />
  </Folder>
</>;
