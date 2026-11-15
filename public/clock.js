import {CAP} from './program.js';
// One tick never crosses a phase boundary, counts hidden time, or exceeds the cap.
export function consumeTime(state,kind,elapsed){
 if(!Number.isFinite(elapsed)||elapsed<0||elapsed>2)return {...state,suspended:true};
 const active=Math.max(0,Math.min(CAP,state.active));
 const used=Math.max(0,Math.min(elapsed,state.remaining,kind==='rest'?Infinity:CAP-active));
 return {active:active+(kind==='rest'?0:used),rest:state.rest+(kind==='rest'?used:0),remaining:Math.max(0,state.remaining-used),suspended:false};
}
