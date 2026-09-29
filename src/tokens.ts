export const VIDEO = {
  width: 1080,
  height: 1920,
  fps: 30,
} as const;

export const COLORS = {
  background: '#F7F8FA',
  surface: '#FFFFFF',
  foreground: '#101114',
  muted: '#6B7280',
  border: '#E5E7EB',
  darkSurface: '#111318',
  accent: '#5B6CFF',
  accentSoft: '#EEF0FF',
  success: '#16A34A',
  danger: '#DC2626',
  warning: '#D97706',
} as const;

export const TYPE = {
  fontFamily: 'Arial, Helvetica, sans-serif',
  monoFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
  hero: 104,
  sceneTitle: 72,
  support: 44,
  caption: 46,
  label: 30,
  code: 31,
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

export const SHADOW = '0 24px 70px rgba(16,17,20,0.10)';
