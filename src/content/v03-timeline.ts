import {VIDEO} from '../tokens';
import {v03Audio} from '../generated/v03-audio';
import {v03Scenes} from './v03';

const breathingRoomSec=0.18;

const durationForScene=(scene:typeof v03Scenes[number])=>{
  const generated=v03Audio.enabled?v03Audio.scenes.find((item)=>item.id===scene.id):undefined;
  const fallbackDurationSec=scene.endSec-scene.startSec;
  return generated?generated.durationSec+breathingRoomSec:fallbackDurationSec;
};

export const v03VoicedTimeline=v03Scenes.map((scene,index)=>{
  const generated=v03Audio.enabled?v03Audio.scenes.find((item)=>item.id===scene.id):undefined;
  const durationSec=durationForScene(scene);
  const durationInFrames=Math.max(1,Math.ceil(durationSec*VIDEO.fps));
  const from=v03Scenes.slice(0,index).reduce(
    (sum,previousScene)=>sum+Math.max(1,Math.ceil(durationForScene(previousScene)*VIDEO.fps)),
    0,
  );

  return {
    ...scene,
    from,
    durationInFrames,
    audioPath:generated?.path??null,
    measuredAudioDurationSec:generated?.durationSec??null,
  };
});

export const V03_VOICED_TOTAL_FRAMES=v03VoicedTimeline.reduce(
  (sum,scene)=>sum+scene.durationInFrames,
  0,
);
