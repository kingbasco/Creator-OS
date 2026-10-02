"""Reuse a private narration ZIP from Drive; no AI generation or spending."""
import argparse
import hashlib
import importlib.util
import io
import json
import re
import urllib.request
import wave
import zipfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('worker', Path(__file__).with_name('calendar-worker.py'))
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
parser = argparse.ArgumentParser()
parser.add_argument('--file-id', required=True)
args = parser.parse_args()
if not re.fullmatch(r'[A-Za-z0-9_-]{10,150}', args.file_id):
    raise RuntimeError('A Drive narration package ID is required for final rendering.')
google = worker.Google()
request = urllib.request.Request('https://www.googleapis.com/drive/v3/files/' + args.file_id + '?alt=media', headers={'Authorization': 'Bearer ' + google.token})
with urllib.request.urlopen(request, timeout=55) as response:
    data = response.read(64 * 1024 * 1024 + 1)
if len(data) > 64 * 1024 * 1024:
    raise RuntimeError('Narration package exceeds 64 MB.')
root = Path(__file__).resolve().parents[1]
audio_dir = root / 'public/audio/v06'
audio_dir.mkdir(parents=True, exist_ok=True)
expected = {'manifest.json'} | {'S' + str(i).zfill(2) + '.wav' for i in range(1, 9)}
with zipfile.ZipFile(io.BytesIO(data)) as archive:
    infos = [i for i in archive.infolist() if not i.is_dir()]
    if len(infos) != 9 or {i.filename for i in infos} != expected or sum(i.file_size for i in infos) > 64 * 1024 * 1024:
        raise RuntimeError('Narration ZIP must contain only manifest.json and S01–S08.wav at its root.')
    for item in infos:
        (audio_dir / item.filename).write_bytes(archive.read(item))
manifest = json.loads((audio_dir / 'manifest.json').read_text())
digest = hashlib.sha256((root / 'src/content/v06.json').read_bytes()).hexdigest()
if manifest.get('scriptSha256') != digest:
    raise RuntimeError('Narration package does not match the current V06 transcript.')
scenes = []
for i in range(1, 9):
    scene_id = 'S' + str(i).zfill(2)
    with wave.open(str(audio_dir / (scene_id + '.wav'))) as audio:
        if audio.getnchannels() != 1 or audio.getframerate() != 24000 or audio.getsampwidth() != 2:
            raise RuntimeError('Narration WAV must be mono, 24 kHz, 16-bit PCM.')
        duration = audio.getnframes() / audio.getframerate()
        if not 1 <= duration <= 25:
            raise RuntimeError('Narration scene duration is outside expected bounds.')
    scenes.append({'id': scene_id, 'path': 'audio/v06/' + scene_id + '.wav', 'durationSec': duration})
(root / 'src/generated/v06-audio.ts').write_text('export const v06Audio = ' + json.dumps({'enabled': True, 'scenes': scenes}) + ' as const;\n')
print('Reused and verified V06 narration; no AI API called.')
