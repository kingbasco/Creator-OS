import React from 'react';
import {Composition, Folder} from 'remotion';
import {V01} from './compositions/V01';
import {V01Voiced} from './compositions/V01Voiced';
import {V02} from './compositions/V02';
import {V02Voiced} from './compositions/V02Voiced';
import {V02Final} from './compositions/V02Final';
import {V01_VOICED_TOTAL_FRAMES} from './content/v01-timeline';
import {V02_VOICED_TOTAL_FRAMES} from './content/v02-timeline';
import {V03, V03Voiced, V03Final} from './compositions/V03';
import {V03_VOICED_TOTAL_FRAMES} from './content/v03-timeline';
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
    <Composition
      id="V01-Vibe-Coding-Isnt-Magic-Voiced"
      component={V01Voiced}
      durationInFrames={V01_VOICED_TOTAL_FRAMES}
      fps={VIDEO.fps}
      width={VIDEO.width}
      height={VIDEO.height}
    />
    <Composition
      id="V02-What-An-AI-Coding-Agent-Actually-Does"
      component={V02}
      durationInFrames={82*VIDEO.fps}
      fps={VIDEO.fps}
      width={VIDEO.width}
      height={VIDEO.height}
    />
    <Composition
      id="V02-What-An-AI-Coding-Agent-Actually-Does-4K"
      component={V02}
      durationInFrames={82*VIDEO.fps}
      fps={VIDEO.fps}
      width={2160}
      height={3840}
    />
    <Composition
      id="V02-What-An-AI-Coding-Agent-Actually-Does-Voiced"
      component={V02Voiced}
      durationInFrames={V02_VOICED_TOTAL_FRAMES}
      fps={VIDEO.fps}
      width={VIDEO.width}
      height={VIDEO.height}
    />
    <Composition
      id="V02-What-An-AI-Coding-Agent-Actually-Does-Voiced-4K"
      component={V02Voiced}
      durationInFrames={V02_VOICED_TOTAL_FRAMES}
      fps={VIDEO.fps}
      width={2160}
      height={3840}
    />
    <Composition
      id="V02-What-An-AI-Coding-Agent-Actually-Does-Final-4K"
      component={V02Final}
      durationInFrames={V02_VOICED_TOTAL_FRAMES}
      fps={VIDEO.fps}
      width={2160}
      height={3840}
    />
    <Composition id="V03-Demo-To-Product" component={V03} durationInFrames={84*VIDEO.fps} fps={VIDEO.fps} width={1080} height={1920}/>
    <Composition id="V03-Demo-To-Product-4K" component={V03} durationInFrames={84*VIDEO.fps} fps={VIDEO.fps} width={2160} height={3840}/>
    <Composition id="V03-Demo-To-Product-Voiced-4K" component={V03Voiced} durationInFrames={V03_VOICED_TOTAL_FRAMES} fps={VIDEO.fps} width={2160} height={3840}/>
    <Composition id="V03-Demo-To-Product-Final-4K" component={V03Final} durationInFrames={V03_VOICED_TOTAL_FRAMES} fps={VIDEO.fps} width={2160} height={3840}/>
  </Folder>
</>;
