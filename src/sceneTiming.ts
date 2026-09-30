import {useCurrentFrame, useVideoConfig} from 'remotion';

export const useScaledSceneFrame = (
  durationInFrames: number | undefined,
  originalDurationSec: number,
  frameOffset = 0,
) => {
  const rawFrame=useCurrentFrame();
  const currentFrame=Math.max(0,Math.min(
    Math.max(0,(durationInFrames ?? 1)-1),
    rawFrame-frameOffset,
  ));
  const {fps}=useVideoConfig();

  if (!durationInFrames || durationInFrames <= 0) {
    return {frame:currentFrame,fps};
  }

  return {
    frame:currentFrame*((originalDurationSec*fps)/durationInFrames),
    fps,
  };
};
