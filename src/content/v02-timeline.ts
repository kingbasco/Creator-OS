import {VIDEO} from '../tokens';
import {v02Audio} from '../generated/v02-audio';
import {v02Scenes} from './v02';

const breathingRoomSec=0.18;

const durationForScene=(scene:typeof v02Scenes[number])=>{
  const generated=v02Audio.enabled?v02Audio.scenes.find((item)=>item.id===scene.id):undefined;
  const fallbackDurationSec=scene.endSec-scene.startSec;
  return generated?generated.durationSec+breathingRoomSec:fallbackDurationSec;
};

export const v02VoicedTimeline=v02Scenes.map((scene,index)=>{
  const generated=v02Audio.enabled?v02Audio.scenes.find((item)=>item.id===scene.id):undefined;
  const durationSec=durationForScene(scene);
  const durationInFrames=Math.max(1,Math.ceil(durationSec*VIDEO.fps));
  const from=v02Scenes.slice(0,index).reduce(
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

export const V02_VOICED_TOTAL_FRAMES=v02VoicedTimeline.reduce(
  (sum,scene)=>sum+scene.durationInFrames,
  0,
);
