import {GEIST_FONT} from './fonts';

export const VIDEO = {
  width: 1080,
  height: 1920,
  fps: 30,
} as const;

export const COLORS = {
  background: '#F7F8FA',
  surface: '#FFFFFF',
  well: '#F1F3F6',
  foreground: '#101114',
  muted: '#6B7280',
  mutedOnDark: '#A7ACB7',
  border: '#E5E7EB',
  rimDark: '#2A2E38',
  darkSurface: '#111318',
  accent: '#5B6CFF',
  accentSoft: '#EEF0FF',
  success: '#16A34A',
  danger: '#DC2626',
  warning: '#C47A1D',
} as const;

export const TYPE = {
  fontFamily: `${GEIST_FONT}, Arial, Helvetica, sans-serif`,
  monoFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
  hero: 104,
  sceneTitle: 72,
  support: 44,
  caption: 42,
  label: 30,
  code: 30,
} as const;

export const SPACE = {
  x: 72,
  top: 120,
  bottom: 180,
  unit: 8,
} as const;

export const RADIUS = {
  sm: 14,
  md: 20,
  lg: 28,
} as const;

export const SHADOW = '0 1px 2px rgba(16,17,20,.05), 0 18px 48px rgba(16,17,20,.08)';
export const FLOAT_SHADOW = '0 2px 6px rgba(16,17,20,.08), 0 28px 70px rgba(16,17,20,.12)';
