import bpy,sys,json,math,time,os
from pathlib import Path
from mathutils import Matrix
ROOT=Path(__file__).resolve().parent;BASE=ROOT/'source';APP=ROOT.parent;OUT=APP/'public/media/3d';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT))
from pose_api import Pose
import leg_motions,standing_motions
modules=[leg_motions,standing_motions]
if (ROOT/'floor_motions.py').exists():
 import floor_motions
 modules.append(floor_motions)
specs={id:dict(spec) for mod in modules for id,spec in mod.SPECS.items()}
only=os.environ.get('ONLY_CLIPS')
if only:specs={k:v for k,v in specs.items() if k in only.split(',')}
bpy.ops.wm.open_mainfile(filepath=str(BASE/'instructor.blend'))
s=bpy.context.scene;rig=next(o for o in s.objects if o.type=='ARMATURE');rig.name='InstructorRig'
rig.animation_data_clear()
for action in list(bpy.data.actions):bpy.data.actions.remove(action)
p=Pose(rig);p.reset();bpy.context.view_layer.update()
characters=[o for o in s.objects if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)]
# Bake only modelling modifiers in the rest pose; preserve the skin weights.
for o in characters:
 for m in o.modifiers:
  if m.type=='ARMATURE':m.show_viewport=False;m.show_render=False
 bpy.context.view_layer.update()
 deps=bpy.context.evaluated_depsgraph_get();new=bpy.data.meshes.new_from_object(o.evaluated_get(deps),preserve_all_data_layers=True,depsgraph=deps)
 o.data=new
 for m in list(o.modifiers):
  if m.type!='ARMATURE':o.modifiers.remove(m)
  else:m.show_viewport=True;m.show_render=True
 o.shape_key_clear()
 for poly in o.data.polygons:poly.use_smooth=True
# Export-compatible dark hair colour; retain the transparency of the hair cards.
for o in characters:
 if 'hair' not in o.name.lower():continue
 for mat in o.data.materials:
  if not mat.use_nodes:continue
  for n in mat.node_tree.nodes:
   if n.type=='BSDF_PRINCIPLED':
    for link in list(n.inputs['Base Color'].links):mat.node_tree.links.remove(link)
    n.inputs['Base Color'].default_value=(.055,.032,.022,1)
 for mat in o.data.materials:mat.surface_render_method='DITHERED'
for image in bpy.data.images:
 if image.size[0]>2048 or image.size[1]>2048:
  ratio=min(2048/image.size[0],2048/image.size[1]);image.scale(round(image.size[0]*ratio),round(image.size[1]*ratio));image.pack()
main=list(rig.pose.bones)
fps=12;s.render.fps=fps;rig.animation_data_create();checks={};start=time.monotonic()
for id,spec in specs.items():
 action=bpy.data.actions.new(id);action.use_fake_user=True;rig.animation_data.action=action
 duration=spec['duration'];steps=round(duration*fps);p.errors=[];ends=[]
 for i in range(steps+1):
  p.reset();t=i/steps
  for mod in modules:
   if mod.pose(p,id,t):break
  else:raise RuntimeError('Missing pose '+id)
  for b in main:
   if b.name.startswith(('index_','middle_','ring_','pinky_','thumb_')) and i not in [0,steps]:continue
   b.keyframe_insert('location',frame=i,group=b.name);b.keyframe_insert('rotation_quaternion',frame=i,group=b.name)
  if i in [0,steps]:ends.append({b.name:list(b.matrix_basis) for b in main})
 # Explicit linear interpolation avoids overshoot between authored poses.
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for fc in bag.fcurves:
      for key in fc.keyframe_points:key.interpolation='LINEAR'
 err=max((abs(ends[0][n][r][c]-ends[1][n][r][c])for n in ends[0]for r in range(4)for c in range(4)),default=0)
 checks[id]={'frames':steps+1,'duration':duration,'max_unreachable_m':max(p.errors,default=0),'loop_matrix_error':err}
 print('CLIP_READY',id,json.dumps(checks[id]),flush=True)
rig.animation_data.action=None;p.reset();bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
for o in [rig]+characters:o.select_set(True)
bpy.context.view_layer.objects.active=rig
path=OUT/('instructor-test.glb' if only else 'instructor.glb')
bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='ACTIONS',export_anim_single_armature=True,export_force_sampling=False,export_frame_range=False,export_skins=True,export_morph=False,export_apply=False,export_cameras=False,export_lights=False,export_yup=True)
(ROOT/('checks-test.json'if only else 'checks.json')).write_text(json.dumps(checks,indent=2))
if not only:
 (OUT/'library.json').write_text(json.dumps({'model':'/media/3d/instructor.glb','clips':specs},indent=2))
 (ROOT/'build').mkdir(exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'build/exercise-library.blend'))
from pack_web import pack
pack(path)
print('LIBRARY_READY',len(specs),path.stat().st_size,'bytes',round(time.monotonic()-start,1),'seconds',flush=True)
