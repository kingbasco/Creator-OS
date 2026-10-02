#!/usr/bin/env python3
import argparse, json, math, mimetypes, os, subprocess, urllib.parse, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MODEL=Path("/tmp/piper/voice.onnx")
CONFIG=Path("/tmp/piper/voice.onnx.json")

def run(cmd, *, input_text=None, stdout=None, stderr=None):
    return subprocess.run(cmd, input=input_text, text=input_text is not None, check=True, stdout=stdout, stderr=stderr)

def probe_duration(path):
    out=subprocess.check_output([
        "ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",str(path)
    ], text=True).strip()
    return float(out)

def tempo_chain(factor):
    parts=[]
    while factor > 2.0:
        parts.append("atempo=2.0")
        factor/=2.0
    while factor < 0.5:
        parts.append("atempo=0.5")
        factor/=0.5
    parts.append(f"atempo={factor:.6f}")
    return ",".join(parts)

def synth_scene(text, out_path, target_sec):
    raw=out_path.with_suffix(".raw.wav")
    p=subprocess.run([
        "piper","--model",str(MODEL),"--config",str(CONFIG),"--output_file",str(raw)
    ], input=text, text=True, check=True)
    raw_dur=probe_duration(raw)
    factor=max(1.0, raw_dur/max(1.0,target_sec))
    filt=[]
    if factor>1.001:
        filt.append(tempo_chain(factor))
    filt += ["aresample=48000","aformat=sample_fmts=fltp:channel_layouts=stereo"]
    run(["ffmpeg","-y","-v","error","-i",str(raw),"-af",",".join(filt),"-c:a","pcm_s16le",str(out_path)])
    raw.unlink(missing_ok=True)
    return {"rawDuration":raw_dur,"target":target_sec,"tempo":factor,"finalDuration":probe_duration(out_path)}

def make_whoosh(path):
    run([
        "ffmpeg","-y","-v","error",
        "-f","lavfi","-i","anoisesrc=color=pink:duration=0.24:amplitude=0.04",
        "-af","highpass=f=700,lowpass=f=5200,afade=t=in:st=0:d=0.025,afade=t=out:st=0.05:d=0.19,volume=0.28,aformat=channel_layouts=stereo,aresample=48000",
        "-c:a","pcm_s16le",str(path)
    ])

def mix_audio(scene_files, scenes, duration, out_path, work):
    whoosh=work/"whoosh.wav"
    make_whoosh(whoosh)
    cmd=["ffmpeg","-y","-v","error"]
    for p in scene_files:
        cmd += ["-i",str(p)]
    cmd += ["-i",str(whoosh)]
    filters=[]
    mix_labels=[]
    for i,scene in enumerate(scenes):
        delay=max(0,int((float(scene["startSec"])+0.28)*1000))
        label=f"v{i}"
        filters.append(f"[{i}:a]adelay={delay}|{delay},volume=1.0[{label}]")
        mix_labels.append(f"[{label}]")
    fx_labels=[]
    fx_input=len(scene_files)
    boundaries=[int(float(s["startSec"])*1000) for s in scenes[1:]]
    split_labels="".join(f"[w{i}]" for i in range(len(boundaries)))
    filters.append(f"[{fx_input}:a]asplit={len(boundaries)}{split_labels}")
    for i,delay in enumerate(boundaries):
        filters.append(f"[w{i}]adelay={delay}|{delay},volume=0.40[fx{i}]")
        fx_labels.append(f"[fx{i}]")
    filters.append(
        "".join(mix_labels+fx_labels)
        +f"amix=inputs={len(mix_labels)+len(fx_labels)}:duration=longest:dropout_transition=0:normalize=0,"
         "alimiter=limit=0.92,loudnorm=I=-14:LRA=9:TP=-1.5,"
         f"atrim=0:{duration:.3f},apad=pad_dur=0.1[aout]"
    )
    cmd += ["-filter_complex",";".join(filters),"-map","[aout]","-t",f"{duration:.3f}","-c:a","pcm_s16le",str(out_path)]
    run(cmd)

def request_json(url, method="GET", headers=None, data=None, timeout=120):
    req=urllib.request.Request(url,data=data,headers=headers or {},method=method)
    with urllib.request.urlopen(req,timeout=timeout) as r:
        body=r.read()
        return json.loads(body.decode("utf-8")) if body else {}

def google_token():
    payload=urllib.parse.urlencode({
        "client_id":os.environ["GOOGLE_CLIENT_ID"],
        "client_secret":os.environ["GOOGLE_CLIENT_SECRET"],
        "refresh_token":os.environ["GOOGLE_REFRESH_TOKEN"],
        "grant_type":"refresh_token",
    }).encode()
    return request_json(
        "https://oauth2.googleapis.com/token","POST",
        {"Content-Type":"application/x-www-form-urlencoded"},payload
    )["access_token"]

def overwrite_drive(path, file_id, final_name):
    token=google_token()
    meta=json.dumps({"name":final_name}).encode()
    request_json(
        f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=id,name,size,webViewLink",
        "PATCH",{"Authorization":f"Bearer {token}","Content-Type":"application/json"},meta
    )
    data=Path(path).read_bytes()
    req=urllib.request.Request(
        f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=media&fields=id,name,size,modifiedTime",
        data=data,
        headers={"Authorization":f"Bearer {token}","Content-Type":"video/mp4","Content-Length":str(len(data))},
        method="PATCH",
    )
    with urllib.request.urlopen(req,timeout=900) as r:
        out=json.loads(r.read().decode("utf-8"))
    out["url"]=f"https://drive.google.com/file/d/{file_id}/view"
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--episode",required=True)
    ap.add_argument("--visual",required=True)
    ap.add_argument("--drive-id",required=True)
    args=ap.parse_args()
    ep=args.episode.lower()
    scenes=json.loads((ROOT/"src"/"content"/f"{ep}.json").read_text())
    work=ROOT/"out"/f"{ep}-local-final"
    work.mkdir(parents=True,exist_ok=True)
    visual=Path(args.visual)
    visual_dur=probe_duration(visual)
    scene_files=[]
    timings=[]
    for i,s in enumerate(scenes):
        target=max(2.0,float(s["endSec"])-float(s["startSec"])-0.85)
        out=work/f"scene-{i+1:02d}.wav"
        timings.append(synth_scene(s["narration"],out,target))
        scene_files.append(out)
    mixed=work/f"{ep}-mix.wav"
    mix_audio(scene_files,scenes,visual_dur,mixed,work)
    final=work/f"{ep}-final-master-4k.mp4"
    run([
        "ffmpeg","-y","-v","error",
        "-i",str(visual),"-i",str(mixed),
        "-map","0:v:0","-map","1:a:0",
        "-vf","scale=2160:3840:flags=lanczos",
        "-c:v","libx264","-preset","fast","-crf","20","-pix_fmt","yuv420p","-r","30",
        "-c:a","aac","-b:a","192k","-ar","48000",
        "-movflags","+faststart","-shortest",str(final)
    ])
    qa=json.loads(subprocess.check_output([
        "ffprobe","-v","error","-show_entries",
        "format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of","json",str(final)
    ],text=True))
    loud=work/f"{ep}-loudness.txt"
    with loud.open("w") as f:
        subprocess.run(["ffmpeg","-hide_banner","-i",str(final),"-filter_complex","ebur128=peak=true","-f","null","-"],stdout=f,stderr=f,check=True)
    final_name=f"{ep}-final-master-4k.mp4"
    drive=overwrite_drive(final,args.drive_id,final_name)
    receipt={
        "episode":ep,"visualDuration":visual_dur,"timings":timings,
        "qa":qa,"drive":drive,"finalName":final_name
    }
    (work/f"{ep}-final-receipt.json").write_text(json.dumps(receipt,indent=2))
    print(json.dumps({"episode":ep,"drive":drive,"qa":qa},indent=2))

if __name__=="__main__":
    main()
