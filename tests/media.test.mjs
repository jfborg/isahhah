import assert from 'node:assert/strict';
import {test} from 'node:test';
import {readFileSync,existsSync,statSync} from 'node:fs';
import {EXERCISES,SESSIONS,variation,LEVELS,buildTimeline} from '../public/program.js';
const root=new URL('../public/',import.meta.url);
const read=p=>readFileSync(new URL(p,root));
const media=JSON.parse(read('media.json'));
const library=JSON.parse(read('media/3d/library.json'));
const data=read('media/3d/instructor.glb');
const gltf=JSON.parse(data.subarray(20,20+data.readUInt32LE(12)).toString());
test('every selectable guide has a real animation and a readable coaching recording',()=>{
 const names=new Set(gltf.animations.map(a=>a.name));
 const ids=Object.keys(EXERCISES).filter(id=>id!=='sideRound');
 assert.equal(ids.length,72);assert.equal(names.size,72);
 for(const id of ids){
  assert.ok(names.has(id),`Missing GLB clip: ${id}`);assert.ok(library.clips[id]);assert.ok(media.animations[id]);
  assert.equal(typeof media.audio[id],'string');const file=new URL(media.audio[id].slice(1),root);assert.ok(existsSync(file));assert.ok(statSync(file).size>2000);
  const animation=gltf.animations.find(a=>a.name===id);assert.ok(animation.channels.length>0);
  const duration=Math.max(...animation.samplers.map(s=>gltf.accessors[s.input].max[0]));assert.ok(duration>=2&&duration<=15,`${id}: ${duration}`);
 }
 for(const cue of ['rest','switch'])assert.ok(existsSync(new URL(media.audio[cue].slice(1),root)));
});
test('every assigned warm-up, work, regression and cooldown has a matching demonstration',()=>{
 const families=[...new Set(Object.values(EXERCISES).map(e=>e.family))];
 for(const level of Object.keys(LEVELS))for(const choice of ['easier','standard','harder'])for(const session of SESSIONS){
  const p={level,equipment:['mat','chair'],variations:Object.fromEntries(families.map(f=>[f,choice]))};
  for(const phase of buildTimeline(session,p))if(phase.id)assert.ok(library.clips[phase.id],`${session.day}: ${phase.id}`);
 }
 assert.deepEqual(SESSIONS.find(s=>s.day===19).moves,SESSIONS.find(s=>s.day===1).moves);
});
test('custom app icons and install manifest point to existing assets',()=>{
 const manifest=JSON.parse(read('manifest.webmanifest'));
 assert.equal(manifest.short_name,'isahhah');
 for(const icon of manifest.icons){const b=read(icon.src.slice(1));assert.equal(b.readUInt32BE(16),Number(icon.sizes.split('x')[0]));}
 assert.match(read('index.html').toString(),/apple-touch-icon/);assert.ok(existsSync(new URL('icons/apple-touch-icon.png',root)));
});
