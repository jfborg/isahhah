"""Low-impact standing demonstrations for the shared Isahhah instructor.

Coordinates are metres in Blender space: X left, -Y forward, Z up.
All clips return to their starting pose. Support feet remain fixed during lifts.
"""
import math
from mathutils import Matrix
from pose_api import V, Q, smooth, pulse

SPECS = {
 'march': {'duration': 3.2, 'view': 'standing'},
 'crossMarch': {'duration': 4, 'view': 'standing'},
 'driveMarch': {'duration': 3.4, 'view': 'standing'},
 'jack': {'duration': 5, 'view': 'standing'},
 'knee': {'duration': 5, 'view': 'standing'},
 'sideStep': {'duration': 6, 'view': 'standing'},
 'doubleStep': {'duration': 8, 'view': 'standing'},
 'punch': {'duration': 4, 'view': 'standing'},
 'uppercut': {'duration': 4, 'view': 'standing'},
 'heelDig': {'duration': 4.5, 'view': 'standing'},
 'heelReach': {'duration': 5, 'view': 'standing'},
 'toeTap': {'duration': 4.5, 'view': 'standing'},
 'curl': {'duration': 5, 'view': 'standing'},
 'forwardMarch': {'duration': 7, 'view': 'standing'},
 'easyMarch': {'duration': 4.5, 'view': 'standing'},
 'circles': {'duration': 6, 'view': 'standing'},
 'ankle': {'duration': 6, 'view': 'standing'},
 'reach': {'duration': 6, 'view': 'standing'},
 'stretchL': {'duration': 6, 'view': 'wall', 'wallY': -.49},
 'stretchR': {'duration': 6, 'view': 'wall', 'wallY': -.49},
 'breathe': {'duration': 7, 'view': 'standing'},
 'chest': {'duration': 7, 'view': 'standing'},
 'standingCrunch': {'duration': 6, 'view': 'standing'},
 'sideLegRaise': {'duration': 7, 'view': 'standing'},
 'backLegRaise': {'duration': 7, 'view': 'standing'},
 'frontKick': {'duration': 6, 'view': 'standing'},
 'boxerStep': {'duration': 5, 'view': 'standing'},
 'stepReach': {'duration': 6, 'view': 'standing'},
}

NEW_EXERCISE_CUES = {
 'standingCrunch': {
  'name': 'Standing cross-body knee lift',
  'cue': 'Lift one knee and bring the opposite elbow gently toward it. Keep the range small, lower with control and alternate. Avoid pulling on your neck.',
  'easier': 'Ordinary low knee march with support',
  'harder': 'Brief balanced pause, without forcing the twist',
 },
 'sideLegRaise': {
  'name': 'Standing side leg raise',
  'cue': 'Stand tall near a wall for balance. Lift one leg a little sideways without leaning, lower slowly and alternate. Keep toes facing forward.',
  'easier': 'Side toe tap with stable support',
  'harder': 'Slower lowering in the same comfortable range',
 },
 'backLegRaise': {
  'name': 'Standing hip extension',
  'cue': 'Stand tall near stable support. Move one leg a little behind you without arching your back, return and alternate. Keep the movement small.',
  'easier': 'Small backward toe tap with support',
  'harder': 'Brief controlled pause without increasing the back arch',
 },
 'frontKick': {
  'name': 'Low controlled front kick',
  'cue': 'Lift one knee a little, extend the lower leg forward without locking the knee, then lower and change sides. Keep kicks low and unhurried.',
  'easier': 'Alternating heel dig with support',
  'harder': 'A short balance pause, not a higher kick',
 },
 'boxerStep': {
  'name': 'Boxer weight shift',
  'cue': 'Keep both feet grounded and knees soft. Shift your weight gently side to side while adding relaxed alternating punches. Keep elbows soft and use no weights.',
  'easier': 'Weight shift without punches',
  'harder': 'A slightly steadier alternating rhythm',
 },
 'stepReach': {
  'name': 'Diagonal step and reach',
  'cue': 'Take a small step diagonally forward with a comfortable opposite-arm reach. Return to the centre and change sides. Keep one foot grounded.',
  'easier': 'Small diagonal toe tap, arms below shoulder height',
  'harder': 'A slightly larger controlled step and reach',
 },
}

SIDES = [('l', 1), ('r', -1)]
TAU = 2 * math.pi

def hand_direction(p,side,direction):
 r=p.r['hand_'+side]
 return (r['t']-r['h']).rotation_difference(V(direction))

def wall_hand(p,side):
 """Fingers point up and the broad palm plane lies against the wall."""
 sign=1 if side=='l' else -1
 long=(p.r['middle_01_'+side]['h']-p.r['hand_'+side]['h']).normalized()
 across=p.r['pinky_01_'+side]['h']-p.r['index_01_'+side]['h']
 across=(across-long*across.dot(long)).normalized()
 normal=across.cross(long).normalized()
 source=Matrix((across,long,normal)).transposed()
 target=Matrix(((sign,0,0),(0,0,1),(0,-sign,0))).transposed()
 return (target@source.inverted()).to_quaternion()

def loose_fists(p):
 """Curl the finger joints locally while leaving the thumb outside."""
 for side,sign in SIDES:
  for finger in ['index','middle','ring','pinky']:
   for joint,angle in [(1,52),(2,58),(3,35)]:
    b=p.rig.pose.bones[f'{finger}_{joint:02d}_{side}']
    b.rotation_quaternion=Q((1,0,0),angle)
  for joint,angle in [(1,15),(2,25),(3,18)]:
   b=p.rig.pose.bones[f'thumb_{joint:02d}_{side}']
   b.rotation_quaternion=Q((1,0,0),angle)

def alternate(t):
 """One smooth excursion per side, with zero velocity at handover."""
 phase = (t % 1) * 2
 side = 'l' if phase < 1 else 'r'
 u = phase % 1
 return side, math.sin(math.pi * u) ** 2, u

def base(p, shift=(0, 0, 0), lean=0):
 # A slight knee bend leaves reach margin for controlled weight transfer.
 p.torso(p.origin + V((shift[0], shift[1], shift[2] - .028)), Q((1, 0, 0), lean))

def feet(p, offsets=None, rotations=None):
 offsets=offsets or {}; rotations=rotations or {}
 for side,sign in SIDES:
  p.leg(side, p.r['foot_'+side]['h'] + V(offsets.get(side,(0,0,0))), foot_q=rotations.get(side))

def easy_arms(p, swing=0, drive=1):
 for side,sign in SIDES:
  s=swing*sign*drive
  p.arm_dirs(side,(sign*.13, -.10-s*.65, -.98),(-sign*.10,-.22-s*.75,-.94+abs(s)*.30))

def raised_arm(p,side,a,sideways=False):
 sign=1 if side=='l' else -1
 if sideways:
  angle=math.radians(12+115*a)
  p.arm_dirs(side,(sign*math.sin(angle),-.08,-math.cos(angle)),(sign*math.sin(angle),-.12,-math.cos(angle)))
 else:
  angle=math.radians(10+135*a)
  p.arm_dirs(side,(sign*.12,-math.sin(angle),-math.cos(angle)),(sign*.10,-math.sin(angle+.1),-math.cos(angle+.1)))

def march(p,id,t):
 moving,a,u=alternate(t);sign=1 if moving=='l' else -1
 height={'easyMarch':.065,'march':.14,'driveMarch':.17,'crossMarch':.23,'knee':.27,'standingCrunch':.27}.get(id,.14)
 forward={'easyMarch':.045,'march':.09,'driveMarch':.10,'crossMarch':.14,'knee':.15,'standingCrunch':.15}.get(id,.09)
 base(p,(-sign*.055*a,0,-.006*a))
 feet(p,{moving:(0,-forward*a,height*a)})
 easy_arms(p,(-sign*a),1.3 if id=='driveMarch' else .7)
 if id=='crossMarch':
  opposite='r' if moving=='l' else 'l'
  p.arm_dirs(opposite,(sign*.22,-.55*a,-1+.35*a),(sign*.55*a,-.65*a,-1+.10*a))
 if id=='knee':easy_arms(p,0)
 if id=='standingCrunch':
  # Opposite elbow approaches the lifted knee; head and trunk stay long.
  for side,s in SIDES:
   touch=1 if side!=moving else 0
   p.arm_dirs(side,(s*(.65-.30*a*bool(touch)),-.22-.55*a*bool(touch),-.55),(-s*.4,-.45,.85))

def stepping(p,id,t):
 moving,a,u=alternate(t);sign=1 if moving=='l' else -1
 if id=='jack':
  base(p,(sign*.07*a,0,-.025*a));feet(p,{moving:(sign*.25*a,0,.035*math.sin(TAU*u)**2)})
  for side,s in SIDES:raised_arm(p,side,a,True)
 elif id=='stepReach':
  base(p,(sign*.06*a,-.05*a,-.018*a))
  feet(p,{moving:(sign*.16*a,-.15*a,.035*math.sin(TAU*u)**2)})
  p.relaxed_arms();raised_arm(p,'r' if moving=='l' else 'l',a*.75)
 elif id=='toeTap':
  base(p,(-sign*.04*a,0,-.015*a));feet(p,{moving:(sign*.18*a,0,.018*a)},{moving:Q((1,0,0),10*a)})
  easy_arms(p,sign*a*.2)
 elif id in ['heelDig','heelReach']:
  base(p,(-sign*.035*a,0,-.035*a))
  feet(p,{moving:(0,-.19*a,.004*a+.03*math.sin(TAU*u)**2)},{moving:Q((1,0,0),-12*a)})
  if id=='heelReach':
   for side,s in SIDES:raised_arm(p,side,a*.8)
  else:easy_arms(p,-sign*a*.45)

def travel(p,id,t):
 # Discrete foot placements with a planted opposite foot at every step.
 # Step-touch: left outward, right follows, right returns, left follows.
 amount=.16
 if id=='doubleStep':
  actions=[('l',amount),('r',amount),('l',amount),('r',amount),('r',-amount),('l',-amount),('r',-amount),('l',-amount)]
 elif id=='forwardMarch':
  actions=[('l',-.14),('r',-.14),('l',-.14),('r',-.14),('l',.14),('r',.14),('l',.14),('r',.14)]
 else:actions=[('l',amount),('r',amount),('r',-amount),('l',-amount)]
 phase=(t%1)*len(actions);index=min(int(phase),len(actions)-1);u=phase-index
 offsets={'l':V((0,0,0)),'r':V((0,0,0))}
 axis=1 if id=='forwardMarch' else 0
 for side,step in actions[:index]:offsets[side][axis]+=step
 side,step=actions[index];offsets[side][axis]+=step*smooth(u);offsets[side].z=.045*math.sin(math.pi*u)**2
 middle=(offsets['l']+offsets['r'])/2
 base(p,(middle.x,middle.y,-.008*math.sin(math.pi*u)**2))
 feet(p,offsets)
 swing=math.sin(TAU*t*(2 if len(actions)==8 else 1))
 if id=='forwardMarch':easy_arms(p,swing*.45)
 else:
  for arm,s in SIDES:raised_arm(p,arm,.22+.2*abs(swing),True)

def curl(p,t):
 moving,a,u=alternate(t);sign=1 if moving=='l' else -1
 base(p,(-sign*.05*a,0,-.01*a))
 # Bend at the knee, with the thigh remaining close to vertical.
 feet(p,{moving:(0,.26*a,.16*a)},{moving:Q((1,0,0),-32*a)})
 easy_arms(p,sign*.3*a)

def leg_raise(p,id,t):
 moving,a,u=alternate(t);sign=1 if moving=='l' else -1
 base(p,(-sign*.065*a,0,-.02*a))
 off=(sign*.19*a,0,.07*a) if id=='sideLegRaise' else (0,.15*a,.055*a)
 feet(p,{moving:off})
 for side,s in SIDES:p.arm_dirs(side,(s*.25,-.05,-.96),(-s*.10,-.12,-.99))

def front_kick(p,t):
 moving,a,u=alternate(t);sign=1 if moving=='l' else -1
 base(p,(-sign*.05*a,0,-.02*a))
 # Knee lift followed by a low extension; never snap or lock the knee.
 extension=math.sin(math.pi*u)**6
 feet(p,{moving:(0,-.30*extension-.08*a,.17*a)},{moving:Q((1,0,0),-8*extension)})
 easy_arms(p,sign*.15*a)

def boxing(p,id,t):
 moving,a,u=alternate(t);sign=1 if moving=='l' else -1
 weight=.065*math.sin(TAU*t) if id=='boxerStep' else .018*math.sin(TAU*t)
 base(p,(weight,0,-.02));feet(p)
 for side,s in SIDES:
  extension=a if side==moving else 0
  if id=='uppercut':
   direction=V((-s*.15,-.45,.90))
   p.arm_dirs(side,(s*.18,-.22-.45*extension,-.88+.35*extension),direction,hand_q=hand_direction(p,side,direction))
  else:
   direction=V((-s*.18,-.35-.65*extension,.88*(1-extension)))
   p.arm_dirs(side,(s*.16,-.25-.73*extension,-.85+.80*extension),direction,hand_q=hand_direction(p,side,direction))
 loose_fists(p)

def calf_stretch(p,id,t):
 rear='l' if id=='stretchL' else 'r';front='r' if rear=='l' else 'l'
 base(p,(0,-.035,-.07),8)
 feet(p,{rear:(0,.22,0),front:(0,-.13,0)})
 for side,sign in SIDES:p.arm(side,(sign*.17,-.43,1.03),hint=(sign,-.2,0),hand_q=wall_hand(p,side))

def mobility(p,id,t):
 a=pulse(t)
 if id=='ankle':
  angle=9*math.sin(TAU*t);q=Q((1,0,0),angle);targets={}
  for side,sign in SIDES:
   ankle=p.r['foot_'+side]['h'];ball=p.r['ball_'+side]['h']
   pivot=ball if angle>=0 else V((ankle.x,ankle.y+.028,.008))
   targets[side]=pivot+q@(ankle-pivot)
  rise=sum(targets[s].z-p.r['foot_'+s]['h'].z for s in targets)/2
  base(p,(0,0,rise))
  for side,sign in SIDES:p.leg(side,targets[side],foot_q=q)
  easy_arms(p,0);return
 base(p,(0,0,.002*a));feet(p)
 if id=='reach':
  moving,a,u=alternate(t)
  for side,s in SIDES:raised_arm(p,side,a*.8 if side==moving else 0)
 elif id=='circles':
  # Small relaxed arm swings preserve the shoulder joints' shared anchors.
  phase=TAU*t
  for side,s in SIDES:
   p.arm_dirs(side,(s*.18,.18*math.sin(phase),-.98),(-s*.08,.24*math.sin(phase+.35),-.97))
 elif id=='chest':
  a=.75+.01*math.sin(TAU*t)  # Gentle static opening; avoid repeated bouncing.
  for side,s in SIDES:p.arm_dirs(side,(s*(.24+.18*a),.12*a,-.95), (s*.20,.25*a,-.95))
 else:
  for side,s in SIDES:p.arm_dirs(side,(s*.12,-.10,-.98),(-s*.08,-.22+.025*a,-.97))

def pose(p,id,t):
 if id not in SPECS:return False
 t=t%1
 if id in ['march','crossMarch','driveMarch','knee','easyMarch','standingCrunch']:march(p,id,t)
 elif id in ['jack','heelDig','heelReach','toeTap','stepReach']:stepping(p,id,t)
 elif id in ['sideStep','doubleStep','forwardMarch']:travel(p,id,t)
 elif id=='curl':curl(p,t)
 elif id in ['sideLegRaise','backLegRaise']:leg_raise(p,id,t)
 elif id=='frontKick':front_kick(p,t)
 elif id in ['punch','uppercut','boxerStep']:boxing(p,id,t)
 elif id in ['stretchL','stretchR']:calf_stretch(p,id,t)
 else:mobility(p,id,t)
 return True
