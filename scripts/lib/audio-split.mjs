import {SAMPLE_RATE, SAMPLE_WIDTH_BYTES} from './gemini-tts.mjs';

export const wordCount=(value='')=>value.trim().split(/\s+/).filter(Boolean).length;

const rmsWindow=(pcm,startSample,endSample)=>{
  let sum=0;
  let count=0;
  for(let i=startSample;i<endSample;i++){
    const value=pcm.readInt16LE(i*SAMPLE_WIDTH_BYTES);
    sum+=value*value;
    count++;
  }
  return count?Math.sqrt(sum/count):Number.POSITIVE_INFINITY;
};

export const findSceneBoundary=(pcm,firstText,secondText)=>{
  const totalSamples=Math.floor(pcm.length/SAMPLE_WIDTH_BYTES);
  const firstWords=Math.max(1,wordCount(firstText));
  const secondWords=Math.max(1,wordCount(secondText));
  const expectedRatio=firstWords/(firstWords+secondWords);
  const expectedSample=Math.round(totalSamples*expectedRatio);

  const windowSamples=Math.round(SAMPLE_RATE*0.02);
  const minQuietWindows=Math.max(4,Math.round(0.10/(windowSamples/SAMPLE_RATE)));
  const threshold=550;
  const windows=[];

  for(let start=0;start+windowSamples<=totalSamples;start+=windowSamples){
    windows.push({
      start,
      end:start+windowSamples,
      rms:rmsWindow(pcm,start,start+windowSamples),
    });
  }

  const segments=[];
  let begin=null;
  for(let i=0;i<windows.length;i++){
    const quiet=windows[i].rms<threshold;
    if(quiet&&begin===null) begin=i;
    if((!quiet||i===windows.length-1)&&begin!==null){
      const endIndex=quiet&&i===windows.length-1?i:i-1;
      const count=endIndex-begin+1;
      if(count>=minQuietWindows){
        const startSample=windows[begin].start;
        const endSample=windows[endIndex].end;
        const centerSample=Math.round((startSample+endSample)/2);
        const ratio=centerSample/totalSamples;
        if(ratio>=0.15&&ratio<=0.85){
          segments.push({
            startSample,
            endSample,
            centerSample,
            durationSec:(endSample-startSample)/SAMPLE_RATE,
            distanceSec:Math.abs(centerSample-expectedSample)/SAMPLE_RATE,
          });
        }
      }
      begin=null;
    }
  }

  if(segments.length===0){
    return {
      splitSample:expectedSample,
      expectedSec:expectedSample/SAMPLE_RATE,
      selected:null,
      candidates:[],
      fallback:true,
    };
  }

  segments.sort((a,b)=>{
    const aScore=a.distanceSec-Math.min(a.durationSec,0.8)*0.12;
    const bScore=b.distanceSec-Math.min(b.durationSec,0.8)*0.12;
    return aScore-bScore;
  });

  const selected=segments[0];
  return {
    splitSample:selected.centerSample,
    expectedSec:expectedSample/SAMPLE_RATE,
    selected,
    candidates:segments.slice(0,6),
    fallback:false,
  };
};
