import {VIDEO} from '../tokens';
import {v01Audio} from '../generated/v01-audio';
import {v01Scenes} from './v01';

const breathingRoomSec = 0.32;

export const v01VoicedTimeline = v01Scenes.map((scene, index) => {
  const generated = v01Audio.enabled ? v01Audio.scenes.find((item) => item.id === scene.id) : undefined;
  const fallbackDurationSec = scene.endSec - scene.startSec;
  const durationSec = generated ? generated.durationSec + breathingRoomSec : fallbackDurationSec;
  const durationInFrames = Math.max(1, Math.ceil(durationSec * VIDEO.fps));

  const from = v01Scenes.slice(0, index).reduce((sum, previousScene) => {
    const previousGenerated = v01Audio.enabled
      ? v01Audio.scenes.find((item) => item.id === previousScene.id)
      : undefined;
    const previousDurationSec = previousGenerated
      ? previousGenerated.durationSec + breathingRoomSec
      : previousScene.endSec - previousScene.startSec;
    return sum + Math.max(1, Math.ceil(previousDurationSec * VIDEO.fps));
  }, 0);

  return {
    ...scene,
    from,
    durationInFrames,
    audioPath: generated?.path ?? null,
    measuredAudioDurationSec: generated?.durationSec ?? null,
  };
});

export const V01_VOICED_TOTAL_FRAMES = v01VoicedTimeline.reduce(
  (sum, scene) => sum + scene.durationInFrames,
  0,
);
