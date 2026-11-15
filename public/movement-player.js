import * as THREE from './vendor/three.module.js';
import {GLTFLoader} from './vendor/GLTFLoader.js';
import {OrbitControls} from './vendor/OrbitControls.js';

let shared;
const load=()=>shared??=Promise.all([new GLTFLoader().loadAsync('/media/3d/instructor.glb'),fetch('/media/3d/library.json').then(r=>{if(!r.ok)throw Error('Animation library unavailable');return r.json();})]).catch(error=>{shared=null;throw error;});
let current=null;
export function stopMovement(){current?.dispose();current=null;}
export function pauseMovement(paused){current?.setPaused(paused);}
export function hasMovement(id,media){return Boolean(media.animations?.[id]);}
export async function showMovement(container,id,{paused=false,controls=true,onError=()=>{}}={}){
 stopMovement();if(!container)return;
 const token={disposed:false};current=token;
 token.dispose=()=>{token.disposed=true;};token.setPaused=p=>{paused=p;};
 container.innerHTML='<div class="movement-loading" role="status">Preparing your movement…</div>';
 try{
  const [gltf,library]=await load();if(token.disposed||!container.isConnected)return;
  const spec=library.clips[id],clip=gltf.animations.find(a=>a.name===id);if(!spec||!clip)throw Error('This movement is not available');
  const scene=new THREE.Scene();scene.background=new THREE.Color('#dce1d6');
  const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false,powerPreference:'low-power'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.22;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;
  renderer.domElement.setAttribute('role','img');renderer.domElement.setAttribute('aria-label','Animated exercise demonstration. Use the camera controls to change the view.');
  container.innerHTML='';container.append(renderer.domElement);
  const camera=new THREE.PerspectiveCamera(33,1,.01,30);
  const floorView=spec.view==='floor';const target=new THREE.Vector3(0,floorView?.38:.82,0);
  camera.position.set(floorView?2.1:1.5,floorView?1.8:1.45,floorView?2.6:2.8);camera.lookAt(target);
  const orbit=new OrbitControls(camera,renderer.domElement);orbit.target.copy(target);orbit.enablePan=false;orbit.enableDamping=true;orbit.minDistance=1.7;orbit.maxDistance=5;orbit.maxPolarAngle=Math.PI/2-.05;orbit.enabled=controls;
  scene.add(new THREE.HemisphereLight(0xf9f8e8,0x88947f,2.2));
  const key=new THREE.DirectionalLight(0xfff3dd,3);key.position.set(-2,4,3);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-2;key.shadow.camera.right=2;key.shadow.camera.top=2;key.shadow.camera.bottom=-2;key.shadow.normalBias=.025;key.shadow.bias=-.0003;scene.add(key);
  const fill=new THREE.DirectionalLight(0xd7e4ff,1.1);fill.position.set(3,2,-2);scene.add(fill);
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(40,40),new THREE.MeshStandardMaterial({color:0xdce1d6,roughness:1}));ground.rotation.x=-Math.PI/2;ground.position.y=-.012;ground.receiveShadow=true;scene.add(ground);
  const mat=new THREE.Mesh(new THREE.BoxGeometry(2.4,.018,1.8),new THREE.MeshStandardMaterial({color:0x727e6b,roughness:1}));mat.position.y=-.005;mat.receiveShadow=true;scene.add(mat);
  const model=gltf.scene;scene.add(model);model.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;o.frustumCulled=false;}});
  const props=new THREE.Group();scene.add(props);
  const cube=(x,y,z,w,h,d,color=0x596354)=>{const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),new THREE.MeshStandardMaterial({color,roughness:.8}));o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;props.add(o);return o;};
  const wall=spec.view==='wall'||spec.prop==='backWall';
  if(wall){const z=spec.prop==='backWall'?-.32:-(spec.wallY??-.53);cube(0,.85,z,1.5,1.7,.045,0xbbc5b3);}
  if(spec.prop==='chair'){
   cube(0,.44,-.30,.46,.055,.43);cube(0,.74,-.49,.46,.53,.045);
   for(const x of [-.19,.19])for(const z of [-.47,-.13])cube(x,.21,z,.035,.42,.035);
   cube(0,.9,-.54,1.2,1.8,.04,0xbbc5b3);
  }
  if(spec.prop==='support'){
   cube(.45,.92,.04,.04,1.84,.70,0xbbc5b3);
  }
  const mixer=new THREE.AnimationMixer(model);const action=mixer.clipAction(clip);action.play();mixer.setTime(0);
  let last=performance.now(),raf,playing=!paused;
  token.setPaused=p=>{paused=p;playing=!p;button?.setAttribute('aria-pressed',String(playing));if(button)button.textContent=playing?'Pause demo':'Play demo';};
  let button;
  if(controls){
   const bar=document.createElement('div');bar.className='movement-toolbar';
   button=document.createElement('button');button.type='button';button.textContent=playing?'Pause demo':'Play demo';button.setAttribute('aria-pressed',String(playing));button.addEventListener('click',()=>token.setPaused(!paused));bar.append(button);
   for(const [label,pos]of [['Front',[0,floorView?1.4:1.2,3.7]],['Side',[3.7,floorView?1.4:1.2,0]],['Reset',[floorView?2.1:1.5,floorView?1.8:1.45,floorView?2.6:2.8]]]){const b=document.createElement('button');b.type='button';b.textContent=label;b.addEventListener('click',()=>{camera.position.set(...pos);orbit.target.copy(target);orbit.update();});bar.append(b);}
   container.append(bar);
  }
  const resize=()=>{const w=container.clientWidth,h=Math.max(240,Math.min(w*.67,560));renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();};
  const observer=new ResizeObserver(resize);observer.observe(container);resize();
  const draw=now=>{if(token.disposed)return;const dt=Math.min((now-last)/1000,.08);last=now;if(!paused&&!document.hidden)mixer.update(dt);orbit.update();renderer.render(scene,camera);raf=requestAnimationFrame(draw);};raf=requestAnimationFrame(draw);
  token.dispose=()=>{if(token.disposed)return;token.disposed=true;cancelAnimationFrame(raf);observer.disconnect();orbit.dispose();mixer.stopAllAction();mixer.uncacheRoot(model);scene.remove(model);scene.traverse(o=>{if(o.isMesh){o.geometry.dispose();if(Array.isArray(o.material))o.material.forEach(m=>m.dispose());else o.material.dispose();}});renderer.dispose();};
  container.dataset.ready='true';container.dataset.clip=id;
 }catch(error){if(token.disposed)return;container.innerHTML='<p class="media-note">The 3D demonstration could not load. The written movement cues are available below. Try reopening the guide.</p>';onError(error);}
}
