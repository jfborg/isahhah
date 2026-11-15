"""Gentle sustained stretches for the shared Isahhah instructor.

These visual guides use comfortable ranges and fixed support points. Each clip
holds its position with very small breathing movement, rather than bouncing.
"""
import math
from mathutils import Quaternion
from pose_api import V, Q
from standing_motions import wall_hand, hand_direction
from floor_motions import _supine, _direct_leg

SPECS = {
 'hamstringStretchL': {'duration': 6, 'view': 'standing'},
 'hamstringStretchR': {'duration': 6, 'view': 'standing'},
 'hipFlexorStretchL': {'duration': 6, 'view': 'wall', 'wallY': -.49},
 'hipFlexorStretchR': {'duration': 6, 'view': 'wall', 'wallY': -.49},
 'quadStretchL': {'duration': 6, 'view': 'wall', 'wallY': -.45},
 'quadStretchR': {'duration': 6, 'view': 'wall', 'wallY': -.45},
 'upperBackStretch': {'duration': 6, 'view': 'standing'},
 'gluteStretchL': {'duration': 6, 'view': 'floor'},
 'gluteStretchR': {'duration': 6, 'view': 'floor'},
}

CUES = {
 'hamstringStretchL':'Place your left heel a little forward, toes raised and knee soft. Bend the other knee slightly and hinge from your hips with a long back. Rest your hands above the knee and hold a mild stretch behind the left thigh.',
 'hamstringStretchR':'Place your right heel a little forward, toes raised and knee soft. Bend the other knee slightly and hinge from your hips with a long back. Rest your hands above the knee and hold a mild stretch behind the right thigh.',
 'hipFlexorStretchL':'Use the wall for support. Step your left foot back with its heel raised. Keep your torso upright, gently tuck your pelvis and shift forward a little. Hold a mild stretch at the front of the left hip without arching your back.',
 'hipFlexorStretchR':'Use the wall for support. Step your right foot back with its heel raised. Keep your torso upright, gently tuck your pelvis and shift forward a little. Hold a mild stretch at the front of the right hip without arching your back.',
 'quadStretchL':'Hold the wall with your right hand. Bend your left knee and gently hold the ankle with your left hand. Keep your knees close and torso tall. Feel a mild stretch at the front of the thigh; release if balance or the knee is uncomfortable.',
 'quadStretchR':'Hold the wall with your left hand. Bend your right knee and gently hold the ankle with your right hand. Keep your knees close and torso tall. Feel a mild stretch at the front of the thigh; release if balance or the knee is uncomfortable.',
 'upperBackStretch':'Reach both hands forward at chest height with elbows soft. Gently spread your shoulder blades and breathe into your upper back. Keep your neck relaxed and avoid forceful rounding.',
 'gluteStretchL':'Lie on your back with your right foot grounded. Hold behind your left thigh and bring the knee gently toward your chest. Keep your head and shoulders relaxed on the mat and hold a comfortable stretch.',
 'gluteStretchR':'Lie on your back with your left foot grounded. Hold behind your right thigh and bring the knee gently toward your chest. Keep your head and shoulders relaxed on the mat and hold a comfortable stretch.',
}

def hamstring(p, side, breath):
 sign=1 if side=='l' else -1
 p.torso(p.origin+V((0,.035,-.040)),Q((1,0,0),31+.15*breath))
 for leg,s in [('l',1),('r',-1)]:
  ankle=p.r['foot_'+leg]['h'].copy()
  ankle.x=s*.14
  if leg==side:ankle.y-=.15
  else:ankle.y+=.035
  p.leg(leg,ankle,foot_q=Q((1,0,0),-18 if leg==side else 0))
 knee=p.m['calf_'+side].translation
 hip=p.joint('thigh_'+side)
 thigh=hip*.78+knee*.22
 for arm,s in [('l',1),('r',-1)]:
  wrist=thigh+V((s*.055,-.11,.055))
  p.arm(arm,wrist,hint=(s,-.1,0),hand_q=hand_direction(p,arm,(0,-.25,-1)))

def hip_flexor(p, side, breath):
 p.torso(p.origin+V((0,-.035,-.085)),Q((1,0,0),-.5+.12*breath))
 for leg,s in [('l',1),('r',-1)]:
  rear=leg==side
  ankle=p.r['foot_'+leg]['h'].copy();ankle.x=s*.115
  ankle.y+=.27 if rear else -.15
  ankle.z+=.055 if rear else 0
  p.leg(leg,ankle,foot_q=Q((1,0,0),-33 if rear else 0))
 for arm,s in [('l',1),('r',-1)]:
  p.arm(arm,(s*.15,-.43,1.04),hint=(s,0,0),hand_q=wall_hand(p,arm))

def quad(p, side, breath):
 sign=1 if side=='l' else -1
 support='r' if side=='l' else 'l';ss=-sign
 p.torso(p.origin+V((-sign*.055,0,-.012)),Q((1,0,0),.15*breath))
 p.leg(support,p.r['foot_'+support]['h'])
 # Fixed thigh, calf folded behind: keeps the knee close to the support knee.
 knee,ankle=_direct_leg(p,side,(sign*.04,.025,-1),(0,.34,.94),Q((1,0,0),150))
 wrist=ankle+V((sign*.018,-.03,.065))
 p.arm(side,wrist,hint=(sign,.3,0),hand_q=hand_direction(p,side,(0,.15,-1)))
 p.arm(support,(ss*.17,-.39,1.04),hint=(ss,0,0),hand_q=wall_hand(p,support))

def upper_back(p, breath):
 p.torso(p.origin,Q((1,0,0),2+.12*breath));p.standing_legs()
 for side,s in [('l',1),('r',-1)]:
  p.arm(side,(s*.045,-.41,1.13),hint=(s,-.1,-.1),hand_q=hand_direction(p,side,(0,-1,-.1)))

def glute(p, side, breath):
 _supine(p)
 other='r' if side=='l' else 'l';sign=1 if side=='l' else -1
 p.leg(other,(-sign*.13,-.31,.066),hint=(0,0,1),foot_q=Quaternion())
 knee,ankle=_direct_leg(p,side,(0,.67+.002*breath,.74),(0,-.96,-.28),Q((1,0,0),-20))
 thigh=p.joint('thigh_'+side)*.18+knee*.82
 for arm,s in [('l',1),('r',-1)]:
  wrist=thigh+V((s*.055,-.035,-.005))
  p.arm(arm,wrist,hint=(s,0,.1),hand_q=hand_direction(p,arm,(-s*.5,.4,.3)))

def pose(p,id,t):
 if id not in SPECS:return False
 breath=math.sin(2*math.pi*(t%1))
 side='l' if id.endswith('L') else 'r'
 if id.startswith('hamstring'):hamstring(p,side,breath)
 elif id.startswith('hipFlexor'):hip_flexor(p,side,breath)
 elif id.startswith('quad'):quad(p,side,breath)
 elif id.startswith('glute'):glute(p,side,breath)
 else:upper_back(p,breath)
 return True
