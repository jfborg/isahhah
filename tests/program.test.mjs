import assert from 'node:assert/strict';
import {test} from 'node:test';
import {EXERCISES,SESSIONS,SESSION_PREPARATION,LEVELS,buildTimeline,activeSeconds,totalSeconds,included,safetyReasons,variation,CAP} from '../public/program.js';
import {consumeTime} from '../public/clock.js';
function assertTwoMinuteBookends(timeline){
 for(const kind of ['warmup','cooldown']){
  const phase=timeline.filter(x=>x.kind===kind);
  assert.equal(phase.length,4);
  assert.equal(phase.reduce((sum,x)=>sum+x.seconds,0),120);
  assert.ok(phase.every(x=>x.seconds===30));
  assert.deepEqual(kind==='warmup'?timeline.slice(0,4):timeline.slice(-4),phase);
 }
 assert.ok(timeline.slice(-4).some(x=>EXERCISES[x.id].family==='stretch'));
}
export function verifyProgramme(){
 let checks=0;
 for(const level of Object.keys(LEVELS))for(const days of [3,4,5])for(const equipment of [[],['mat','chair']])for(const choice of ['easier','standard','harder']){
  const families=[...new Set(Object.values(EXERCISES).map(e=>e.family))];
  const p={level,days,equipment,variations:Object.fromEntries(families.map(f=>[f,choice])),age:'18-39',pain:'none',floor:'yes',goal:'general'};
  assert.equal(SESSIONS.filter(s=>included(s,days)).length,days*3);
  for(const s of SESSIONS){const t=buildTimeline(s,p);assert.equal(t.filter(x=>x.kind==='work').length,12);assert.equal(t.filter(x=>x.kind==='rest').length,11);assert.equal(t.filter(x=>x.kind==='rest'&&x.seconds===60).length,1);assert.equal(activeSeconds(t),240+12*LEVELS[level]);assert.equal(totalSeconds(t)-activeSeconds(t),360);assert.ok(activeSeconds(t)<=CAP);assert.ok(t.every(x=>!x.id||EXERCISES[x.id]));assertTwoMinuteBookends(t);if(!equipment.includes('chair'))assert.ok(!t.some(x=>x.id==='chairSquat'));checks++;}
 }
 const p={level:'regular',days:5,equipment:['chair'],age:'18-39',pain:'none',floor:'yes',goal:'general'};
 assert.deepEqual(buildTimeline(SESSIONS.find(s=>s.day===8),p).filter(x=>x.kind==='work').map(x=>x.station),[1,2,1,2,3,4,3,4,5,6,5,6]);
 const side=buildTimeline(SESSIONS.find(s=>s.day===3),p).filter(x=>x.kind==='work'&&EXERCISES[x.id].family==='side');assert.deepEqual(side.map(x=>x.id),['sideL','sideR']);
 assert.equal(variation('push',{...p,level:'beginner'}),'wallPush');assert.equal(variation('squat',{...p,level:'beginner',equipment:[]}),'shallowSquat');
 for(const answer of [{age:'under18'},{pain:'current'},{pain:'restriction'},{floor:'no'},{goal:'test'}])assert.ok(safetyReasons({...p,...answer}).length);assert.equal(safetyReasons(p).length,0);
 const baseline={level:'beginner',variations:{push:'easier',squat:'easier'}};const comparison=buildTimeline(SESSIONS.find(s=>s.day===19),p,baseline);assert.equal(activeSeconds(comparison),600);assertTwoMinuteBookends(comparison);assert.ok(comparison.filter(x=>x.original==='push').every(x=>x.id==='wallPush'));
 return checks;
}
test('all three weeks preserve timing, substitutions and safety gates',()=>{assert.equal(verifyProgramme(),810);});
test('active cap, rests, phase boundaries and background suspension',()=>{
 assert.deepEqual(consumeTime({active:899.9,rest:30,remaining:50},'work',1),{active:900,rest:30,remaining:49.89999999999998,suspended:false});
 const r=consumeTime({active:840,rest:30,remaining:30},'rest',1);assert.equal(r.active,840);assert.equal(r.rest,31);
 const boundary=consumeTime({active:10,rest:0,remaining:.1},'work',1);assert.equal(boundary.active,10.1);assert.equal(boundary.remaining,0);
 const suspend=consumeTime({active:10,rest:0,remaining:30},'work',45);assert.equal(suspend.active,10);assert.equal(suspend.remaining,30);assert.equal(suspend.suspended,true);
});

test('session preparation varies, follows the main work and balances both sides',()=>{
 const plans=SESSIONS.map(s=>SESSION_PREPARATION[s.day]);
 assert.equal(plans.length,15);
 assert.equal(new Set(plans.map(p=>p.warmup.join(','))).size,14);
 assert.ok(new Set(plans.map(p=>p.cooldown.slice(1).sort().join(','))).size>=10);
 const expected={1:'stretch',2:'stretch',3:'hipFlexorStretch',5:'gluteStretch',6:'hipFlexorStretch',8:'hamstringStretch',9:'hamstringStretch',10:'quadStretch',12:'gluteStretch',13:'quadStretch',15:'hamstringStretch',16:'gluteStretch',17:'hipFlexorStretch',19:'stretch',20:'hipFlexorStretch'};
 for(const session of SESSIONS){
  const p=SESSION_PREPARATION[session.day],pair=expected[session.day];
  assert.ok(p.warmupNote&&p.cooldownNote&&p.focus);
  assert.ok(p.warmup.every(id=>EXERCISES[id].family!=='stretch'));
  assert.ok(['easyMarch','sideStep','heelDig'].includes(p.cooldown[0]));
  assert.ok(p.cooldown.includes(pair+'L')&&p.cooldown.includes(pair+'R'));
  for(const id of p.cooldown.filter(id=>/[LR]$/.test(id)))assert.ok(p.cooldown.includes(id.slice(0,-1)+(id.endsWith('L')?'R':'L')));
 }
 assert.deepEqual(SESSION_PREPARATION[19].warmup,SESSION_PREPARATION[1].warmup);
 assert.deepEqual(SESSION_PREPARATION[19].cooldown,SESSION_PREPARATION[1].cooldown);
});
