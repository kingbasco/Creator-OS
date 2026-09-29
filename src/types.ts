export type SceneId = 'S01'|'S02'|'S03'|'S04'|'S05'|'S06'|'S07'|'S08';

export type SceneSpec = {
  id: SceneId;
  startSec: number;
  endSec: number;
  narration: string;
  onScreenText: string;
  captionText?: string;
  captionEmphasis?: string;
  voiceDirection?: string;
};
