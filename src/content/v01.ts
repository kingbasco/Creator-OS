import type {SceneSpec} from '../types';

export const v01Scenes: SceneSpec[] = [
 {id:'S01',startSec:0,endSec:5,narration:'You’ve probably heard someone say, “I built this app without coding.” But that isn’t really what happened.',onScreenText:'I BUILT THIS APP WITHOUT CODING.',captionEmphasis:'without coding'},
 {id:'S02',startSec:5,endSec:16,narration:'In 2025, Andrej Karpathy coined “vibe coding” for a loose way of building where you describe what you want, let the AI write the code, run it, feed errors back, and keep moving—sometimes without really reading the code.',onScreenText:'PROMPT → CODE → RUN → ERROR → PROMPT',captionEmphasis:'feed errors back'},
 {id:'S03',startSec:16,endSec:24,narration:'Today, people use the phrase more broadly, but the useful idea is simple: your job moves up a level.',onScreenText:'YOUR ROLE MOVES UP A LEVEL',captionEmphasis:'moves up a level'},
 {id:'S04',startSec:24,endSec:35,narration:'Instead of typing every line, you describe the intent. The AI proposes a change.',onScreenText:'DESCRIBE INTENT → AI PROPOSES',captionEmphasis:'describe the intent'},
 {id:'S05',startSec:35,endSec:46,narration:'You run it. You inspect what happened. Then you correct the direction.',onScreenText:'RUN → INSPECT → CORRECT',captionEmphasis:'correct the direction'},
 {id:'S06',startSec:46,endSec:55,narration:'That loop can be incredibly fast. But speed doesn’t remove responsibility.',onScreenText:'FAST ≠ FINISHED',captionEmphasis:'responsibility'},
 {id:'S07',startSec:55,endSec:68,narration:'The AI can execute. You still decide what should exist, whether the result is correct, and whether the thing is safe enough to ship.',onScreenText:'AI: EXECUTE • YOU: DECIDE / VERIFY / OWN',captionEmphasis:'You still decide'},
 {id:'S08',startSec:68,endSec:78,narration:'So vibe coding isn’t magic, and it isn’t “no coding.” It’s building software through direction, iteration, and judgment. Next, I’ll show you what an AI coding agent is actually doing behind the scenes.',onScreenText:'DIRECTION → ITERATION → JUDGMENT',captionEmphasis:'direction, iteration, and judgment'},
];
