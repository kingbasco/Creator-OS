import {Easing, interpolate, spring} from 'remotion';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const MOTION = {
  feedbackFrames: 4,
  stateFrames: 7,
  focalFrames: 12,
  spring: {damping: 28, stiffness: 190, mass: 1},
} as const;

export const physicalSpring = (
  frame: number,
  fps: number,
  delay = 0,
  durationInFrames: number = MOTION.focalFrames,
) =>
  spring({
    fps,
    frame: Math.max(0, frame - delay),
    config: MOTION.spring,
    durationInFrames,
  });

export const fadeInUp = (
  frame: number,
  fps: number,
  start = 0,
  duration: number = MOTION.focalFrames,
) => {
  const p = physicalSpring(frame, fps, start, duration);
  return {
    opacity: interpolate(p, [0, 1], [0, 1], clamp),
    transform: `translateY(${interpolate(p, [0, 1], [28, 0], clamp)}px)`,
  };
};

export const springScale = (frame: number, fps: number, delay = 0) => {
  const p = physicalSpring(frame, fps, delay);
  return interpolate(p, [0, 1], [0.955, 1], clamp);
};

export const drawProgress = (frame: number, start: number, duration = 14) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

export const easeProgress = (frame: number, start: number, duration = 10) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
