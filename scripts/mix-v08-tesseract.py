import json
import math
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCENES=json.loads((ROOT/'src/content/v08.json').read_text())
MANIFEST=json.loads((ROOT/'public/audio/v08/manifest.json').read_text())
VISUAL=ROOT/'out/v08-tesseract-visual-1080p.mp4'
OUT=ROOT/'out/v08-final-mix-4k.mp4'
TMP=ROOT/'out/v08-scenes'
TMP.mkdir(parents=True,exist_ok=True)

def run(args):
    subprocess.run(args,check=True)

audio={x['id']:x for x in MANIFEST['scenes']}
timed=[]
cursor=0.0
for scene in SCENES:
    a=audio[scene['id']]
    base=scene['endSec']-scene['startSec']
    target=max(base,float(a['durationSec'])+0.30)
    ratio=target/base
    if ratio>1.35:
        raise RuntimeError(f"{scene['id']} would need more than 35% visual slowdown")
    timed.append({**scene,'base':base,'target':target,'ratio':ratio,'finalStart':cursor,'audio':a})
    cursor+=target

parts=[]
for i,item in enumerate(timed):
    out=TMP/f"scene-{i:02d}.mkv"
    wav=ROOT/'public'/item['audio']['path']
    run([
        'ffmpeg','-y',
        '-ss',str(item['startSec']),'-t',str(item['base']),'-i',str(VISUAL),
        '-i',str(wav),
        '-filter_complex',
        f"[0:v]setpts=(PTS-STARTPTS)*{item['ratio']:.8f},scale=2160:3840:flags=lanczos[v];"
        f"[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"apad=pad_dur={item['target']:.6f},atrim=0:{item['target']:.6f}[a]",
        '-map','[v]','-map','[a]','-r','30',
        '-c:v','libx264','-preset','medium','-crf','15',
        '-c:a','pcm_s16le','-t',f"{item['target']:.6f}",str(out)
    ])
    parts.append(out)

concat=TMP/'concat.txt'
concat.write_text(''.join(f"file '{p.as_posix()}'\n" for p in parts))
voice_timed=ROOT/'out/v08-voice-timed-4k.mkv'
run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(voice_timed)])

sfx=ROOT/'public/audio/v08-sfx'
cues=[
    ('whoosh-rise.wav',timed[0]['finalStart']+2.4,0.05),
    ('scan-tick.wav',timed[1]['finalStart']+3.0,0.045),
    ('whoosh-forward.wav',timed[2]['finalStart']+3.0,0.05),
    ('ui-click.wav',timed[3]['finalStart']+4.0,0.05),
    ('whoosh-mask.wav',timed[4]['finalStart']+2.4,0.05),
    ('approve.wav',timed[5]['finalStart']+4.8,0.055),
    ('success.wav',timed[5]['finalStart']+7.2,0.05),
    ('scan-tick.wav',timed[6]['finalStart']+2.5,0.045),
    ('whoosh-rise.wav',timed[7]['finalStart']+1.0,0.045),
    ('success.wav',timed[7]['finalStart']+8.5,0.05),
]

args=['ffmpeg','-y','-i',str(voice_timed),'-stream_loop','-1','-i',str(sfx/'ambient-bed.wav')]
for name,_,__ in cues:
    args+=['-i',str(sfx/name)]
filters=[
    '[0:a]volume=1[narr]',
    f"[1:a]atrim=0:{cursor:.6f},afade=t=in:st=0:d=1.2,"
    f"afade=t=out:st={max(0,cursor-1.5):.6f}:d=1.5,volume=.055[bed]"
]
labels=['[narr]','[bed]']
for i,(_,at,volume) in enumerate(cues):
    ms=max(0,round(at*1000))
    label=f'cue{i}'
    filters.append(
        f"[{i+2}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
        f"adelay={ms}|{ms},volume={volume}[{label}]"
    )
    labels.append(f'[{label}]')
filters.append(''.join(labels)+f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,"
               f"atrim=0:{cursor:.6f}[mix]")
args+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[mix]',
       '-c:v','copy','-c:a','aac','-b:a','320k','-ar','48000','-ac','2','-shortest',str(OUT)]
run(args)

(ROOT/'out/v08-timing.json').write_text(json.dumps({
    'totalDurationSec':cursor,
    'scenes':[
        {'id':x['id'],'base':x['base'],'speech':x['audio']['durationSec'],
         'target':x['target'],'finalStart':x['finalStart']}
        for x in timed
    ]
},indent=2))
print(f"Built {OUT} at {cursor:.2f}s")
