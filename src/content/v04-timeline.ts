import {VIDEO} from '../tokens';
import {v04Audio} from '../generated/v04-audio';
import {v04Scenes} from './v04';

const breathingRoomSec=0.18;

const durationForScene=(scene:typeof v04Scenes[number])=>{
  const generated=v04Audio.enabled?v04Audio.scenes.find((item)=>item.id===scene.id):undefined;
  const fallbackDurationSec=scene.endSec-scene.startSec;
  return generated?generated.durationSec+breathingRoomSec:fallbackDurationSec;
};

export const v04VoicedTimeline=v04Scenes.map((scene,index)=>{
  const generated=v04Audio.enabled?v04Audio.scenes.find((item)=>item.id===scene.id):undefined;
  const durationSec=durationForScene(scene);
  const durationInFrames=Math.max(1,Math.ceil(durationSec*VIDEO.fps));
  const from=v04Scenes.slice(0,index).reduce(
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

export const V04_VOICED_TOTAL_FRAMES=v04VoicedTimeline.reduce(
  (sum,scene)=>sum+scene.durationInFrames,
  0,
);

