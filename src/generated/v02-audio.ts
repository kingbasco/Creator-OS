import type {SceneId} from '../types';

export type GeneratedSceneAudio = {
  id: SceneId;
  path: string;
  durationSec: number;
};

export const v02Audio = {
  enabled: false,
  provider: 'gemini',
  model: 'gemini-3.8-flash-lite-tts',
  voice: 'UNSELECTED',
  generatedAt: null as string | null,
  scenes: [] as GeneratedSceneAudio[],
} as const;
