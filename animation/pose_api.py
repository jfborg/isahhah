"""Blender-coordinate pose authoring: X left, -Y forward, Z up; metres."""
import math
from mathutils import Vector, Matrix, Quaternion
V=Vector
def Q(axis,degrees):return Quaternion(axis,math.radians(degrees))
def smooth(x):return x*x*(3-2*x)
def pulse(t):return .5-.5*math.cos(2*math.pi*t)
class Pose:
 def __init__(self,rig):
  self.rig=rig
  self.r={b.name:{'h':b.head_local.copy(),'t':b.tail_local.copy(),'m':b.matrix_local.copy()} for b in rig.data.bones}
  self.origin=self.r['pelvis']['h'].copy();self.errors=[];self.reset()
 def reset(self):
  for b in self.rig.pose.bones:b.rotation_mode='QUATERNION';b.matrix_basis=Matrix.Identity(4)
  self.m={n:r['m'].copy() for n,r in self.r.items()};self.rot=Quaternion();self.pelvis=self.origin.copy()
 def bone(self,name,head,tail=None,q=None):
  head=V(head);r=self.r[name];b=self.rig.pose.bones[name]
  if q is None:q=(r['t']-r['h']).rotation_difference(V(tail)-head)
  m=(q.to_matrix()@r['m'].to_3x3()).to_4x4();m.translation=head
  parent=b.parent.name if b.parent else None
  b.matrix_basis=r['m'].inverted()@(self.r[parent]['m']@self.m[parent].inverted() if parent else Matrix.Identity(4))@m
  self.m[name]=m;return q
 def point(self,p):return self.pelvis+self.rot@(V(p)-self.origin)
 def joint(self,name):return self.point(self.r[name]['h'])
 def torso(self,pelvis=None,q=None):
  self.pelvis=V(pelvis) if pelvis is not None else self.origin.copy();self.rot=q or Quaternion()
  for n in ['pelvis','spine_01','spine_02','spine_03','clavicle_l','clavicle_r','neck_01','head']:self.bone(n,self.joint(n),q=self.rot)
 def length(self,n):return (self.r[n]['t']-self.r[n]['h']).length
 def bend(self,start,end,l1,l2,hint):
  axis=V(end)-V(start);dist=axis.length
  if dist>l1+l2+.001:self.errors.append(round(dist-l1-l2,5))
  dist=min(max(dist,.0001),l1+l2-.00001);axis.normalize()
  reach=(l1*l1-l2*l2+dist*dist)/(2*dist)
  projected=V(hint)-axis*V(hint).dot(axis)
  if projected.length<.001:projected=V((1,0,0))-axis*axis.x
  return V(start)+axis*reach+projected.normalized()*math.sqrt(max(0,l1*l1-reach*reach))
 def leg(self,side,ankle,hint=(0,-1,0),foot_q=None):
  thigh,calf,foot,ball=[n+'_'+side for n in ['thigh','calf','foot','ball']]
  hip=self.joint(thigh);ankle=V(ankle);q=foot_q or Quaternion()
  knee=self.bend(hip,ankle,self.length(thigh),self.length(calf),hint)
  self.bone(thigh,hip,knee);self.bone(calf,knee,ankle);self.bone(foot,ankle,q=q)
  self.bone(ball,ankle+q@(self.r[ball]['h']-self.r[foot]['h']),q=q)
 def arm(self,side,wrist,hint=None,hand_q=None):
  upper,lower,hand=[n+'_'+side for n in ['upperarm','lowerarm','hand']]
  shoulder=self.joint(upper);wrist=V(wrist);sign=1 if side=='l' else -1
  elbow=self.bend(shoulder,wrist,self.length(upper),self.length(lower),hint or (sign,0,0))
  self.bone(upper,shoulder,elbow);q=self.bone(lower,elbow,wrist);self.bone(hand,wrist,q=hand_q or q)
 def arm_dirs(self,side,upper_dir,lower_dir,hand_q=None):
  upper,lower,hand=[n+'_'+side for n in ['upperarm','lowerarm','hand']]
  shoulder=self.joint(upper);elbow=shoulder+V(upper_dir).normalized()*self.length(upper);wrist=elbow+V(lower_dir).normalized()*self.length(lower)
  self.bone(upper,shoulder,elbow);q=self.bone(lower,elbow,wrist);self.bone(hand,wrist,q=hand_q or q)
 def standing_legs(self):
  for side in ['l','r']:self.leg(side,self.r['foot_'+side]['h'])
 def relaxed_arms(self):
  for side,sign in [('l',1),('r',-1)]:self.arm_dirs(side,(sign*.12,-.13,-.98),(-sign*.1,-.30,-.95))
