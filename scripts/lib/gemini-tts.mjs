import fs from 'node:fs';
import path from 'node:path';
import {GoogleGenAI} from '@google/genai';
import wav from 'wav';

export const SAMPLE_RATE = 24000;
export const CHANNELS = 1;
export const SAMPLE_WIDTH_BYTES = 2;

export const DEFAULT_MODEL = process.env.GEMINI_TTS_MODEL || 'gemini-3.8-flash-lite-tts';

export const CHANNEL_STYLE = [
  'Warm, clear, intelligent, conversational tech explainer.',
  'Neutral international English.',
  'Natural mid pitch and medium-low energy.',
  'Aim for roughly 145 to 155 words per minute.',
  'Use short micro-pauses at sentence boundaries and visual concept shifts.',
  'Emphasize only the phrase that carries the concept.',
  'Do not sound like a movie trailer, radio commercial, motivational speaker, or breathless short-form narrator.',
  'Do not add, remove, summarize, or paraphrase the transcript.',
  'Pronounce AI as A-I.',
].join(' ');

const ensureKey = () => {
  if (!process.env.GEMINI_API_KEY) {
    throw new Error(
      'GEMINI_API_KEY is missing. Add it as a local environment variable or a GitHub Actions secret. Never commit the key.',
    );
  }
};

const saveWaveFile = async (filename, pcmData) => {
  await fs.promises.mkdir(path.dirname(filename), {recursive: true});
  await new Promise((resolve, reject) => {
    const writer = new wav.FileWriter(filename, {
      channels: CHANNELS,
      sampleRate: SAMPLE_RATE,
      bitDepth: SAMPLE_WIDTH_BYTES * 8,
    });
    writer.on('finish', resolve);
    writer.on('error', reject);
    writer.write(pcmData);
    writer.end();
  });
};

export const synthesizeSpeech = async ({
  text,
  voice,
  outputPath,
  sceneDirection = '',
  model = DEFAULT_MODEL,
}) => {
  ensureKey();

  const client = new GoogleGenAI({apiKey: process.env.GEMINI_API_KEY});
  const style = sceneDirection
    ? `${CHANNEL_STYLE} Scene-specific direction: ${sceneDirection}`
    : CHANNEL_STYLE;

  const interaction = await client.interactions.create({
    model,
    input: [{
      type: 'user_input',
      content: [{
        type: 'text',
        text,
        annotations: [{
          type: 'speech_metadata',
          style,
        }],
      }],
    }],
    response_format: {
      type: 'audio',
      mime_type: 'audio/l16',
      sample_rate: SAMPLE_RATE,
    },
    generation_config: {
      speech_config: [
        {voice},
      ],
    },
  });

  const encoded = interaction.output_audio?.data;
  if (!encoded) {
    throw new Error(`Gemini returned no audio for ${outputPath}`);
  }

  const pcm = Buffer.from(encoded, 'base64');
  await saveWaveFile(outputPath, pcm);

  return {
    durationSec: pcm.byteLength / (SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH_BYTES),
    bytes: pcm.byteLength,
    model,
    voice,
  };
};
