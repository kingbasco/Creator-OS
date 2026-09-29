import {useCurrentFrame, useVideoConfig} from 'remotion';

export const useScaledSceneFrame = (
  durationInFrames: number | undefined,
  originalDurationSec: number,
) => {
  const currentFrame=useCurrentFrame();
  const {fps}=useVideoConfig();

  if (!durationInFrames || durationInFrames <= 0) {
    return {frame:currentFrame,fps};
  }

  return {
    frame:currentFrame*((originalDurationSec*fps)/durationInFrames),
    fps,
  };
};
