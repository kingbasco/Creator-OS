import {loadFont} from '@remotion/google-fonts/Geist';

const {fontFamily} = loadFont('normal', {
  subsets: ['latin'],
  weights: ['400', '500', '600', '700'],
});

export const GEIST_FONT = fontFamily;
