import {Easing, interpolate, spring} from 'remotion';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

export const fadeInUp = (frame: number, fps: number, start = 0, duration = 12) => {
  const opacity = interpolate(frame, [start, start + duration], [0, 1], clamp);
  const translateY = interpolate(frame, [start, start + duration], [28, 0], {
    ...clamp,
    easing: Easing.out(Easing.cubic),
  });
  return {opacity, transform: `translateY(${translateY}px)`};
};

export const springScale = (frame: number, fps: number, delay = 0) => {
  const p = spring({fps, frame: Math.max(0, frame - delay), config: {damping: 18, stiffness: 160, mass: 0.9}});
  return 0.96 + p * 0.04;
};
