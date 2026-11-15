import math
from pose_api import V,Q,pulse,smooth
IDS=['squat','chairSquat','shallowSquat','pauseSquat','slowSquat','calf','slowCalf','splitL','splitR','splitSwitch','reverse','lateral','sideSquat','hinge','staggerHinge','sumoSquat','narrowSquat','wallSit','calfSingle']
SPECS={id:{'duration':6 if id not in ['reverse','lateral','sideSquat','splitSwitch','staggerHinge','calfSingle'] else 12,'view':'standing'}for id in IDS}
SPECS['chairSquat']['prop']='chair';SPECS['wallSit']['prop']='backWall'
for id in ['splitL','splitR','splitSwitch','calf','slowCalf','calfSingle']:SPECS[id]['prop']='support'
def squat_amount(t,id):
 if id=='slowSquat':return smooth(t/.70) if t<.70 else 1-smooth((t-.70)/.30)
 if id=='pauseSquat':return smooth(t/.4) if t<.4 else 1 if t<.6 else 1-smooth((t-.6)/.4)
 return pulse(t)
def pose(p,id,t):
 if id not in SPECS:return False
 a=squat_amount(t,id);base=p.origin.copy()
 if id in ['squat','chairSquat','shallowSquat','pauseSquat','slowSquat','sumoSquat','narrowSquat','wallSit']:
  depth=.29 if id!='shallowSquat' else .14
  if id=='chairSquat':depth=.31
  if id=='wallSit':a=1;depth=.23
  if id=='sumoSquat':base.z-=.025
  p.torso(base+V((0,.21*a,-depth*a)),Q((1,0,0),24*a if id!='wallSit' else -4))
  for side,sign in [('l',1),('r',-1)]:
   ankle=p.r['foot_'+side]['h'].copy()
   if id=='sumoSquat':ankle.x=sign*.27
   if id=='narrowSquat':ankle.x=sign*.10
   if id=='wallSit':ankle.y-=.16
   p.leg(side,ankle,(sign*.20,-1,0),Q((0,0,1),sign*12 if id=='sumoSquat' else 0))
   p.arm_dirs(side,(sign*.12,-(.13+.84*a),-(.98-.82*a)),(-sign*.10,-(.3+.67*a),-(.95-.8*a)))
 elif id in ['calf','slowCalf','calfSingle']:
  if id=='slowCalf':a=smooth(t/.3) if t<.3 else 1-smooth((t-.3)/.7)
  if id=='calfSingle':a=pulse(t*2%1)
  angle=Q((1,0,0),22*a)
  lift=0
  for side in ['l','r']:
   foot=p.r['foot_'+side]['h'];ball=p.r['ball_'+side]['h'];lift=max(lift,(ball+angle@(foot-ball)).z-foot.z)
  phase=pulse(t*2%1);shift=.075*phase if id=='calfSingle' else 0;sign=1 if t<.5 else -1
  p.torso(base+V((shift*sign,0,lift)));
  for side,s in [('l',1),('r',-1)]:
   foot=p.r['foot_'+side]['h'];ball=p.r['ball_'+side]['h'];ankle=ball+angle@(foot-ball)
   if id=='calfSingle' and s!=sign:ankle+=V((0,.04*phase,.11*phase))
   p.leg(side,ankle,foot_q=angle)
   if id!='calfSingle' or s==sign:p.bone('ball_'+side,ball,q=Q((1,0,0),0))
  p.relaxed_arms();p.arm('l',(.40,-.04,.98),(1,0,0),hand_q=(p.r['hand_l']['t']-p.r['hand_l']['h']).rotation_difference(V((0,0,1))))
 elif id in ['hinge','staggerHinge']:
  cycle=t if id=='hinge' else (t*2)%1;a=pulse(cycle)
  p.torso(base+V((0,.14*a,-.07*a)),Q((1,0,0),45*a))
  for side,sign in [('l',1),('r',-1)]:
   ankle=p.r['foot_'+side]['h'].copy()
   if id=='staggerHinge':ankle.y+=.10*sign*(1 if t<.5 else -1)*math.sin(math.pi*cycle)**2
   p.leg(side,ankle)
  for side,sign in [('l',1),('r',-1)]:p.arm_dirs(side,(sign*.12,0,-1),(0,0,-1))
 elif id in ['splitL','splitR','splitSwitch','reverse']:
  cyc=t if id in ['splitL','splitR'] else t*2%1
  sidefront='l' if id=='splitL' or (id in ['splitSwitch','reverse'] and t<.5) else 'r'
  a=pulse(cyc);stance=1 if id in ['splitL','splitR'] else math.sin(math.pi*cyc)**2
  p.torso(base+V((0,0,-.12*stance-.16*a)),Q((1,0,0),8*a))
  for side,sign in [('l',1),('r',-1)]:
   front=side==sidefront;ankle=p.r['foot_'+side]['h'].copy();ankle.x=sign*.12
   ankle.y+=(-.22 if front else .29)*stance
   fq=Q((1,0,0),0 if front else -36*stance)
   if not front:ankle.z+=.06*stance
   p.leg(side,ankle,(0,-1,0),fq)
  p.relaxed_arms()
  if id!='reverse':p.arm('l',(.40,-.04,.98),(1,0,0),hand_q=(p.r['hand_l']['t']-p.r['hand_l']['h']).rotation_difference(V((0,0,1))))
 elif id in ['lateral','sideSquat']:
  cyc=t*2%1;sign=1 if t<.5 else -1;a=pulse(cyc)
  p.torso(base+V((sign*.12*a,.08*a,-.14*a)),Q((1,0,0),14*a))
  for side,s in [('l',1),('r',-1)]:
   ankle=p.r['foot_'+side]['h'].copy()
   if s==sign:ankle.x+=sign*(.18 if id=='lateral' else .12)*a;ankle.z+=.025*math.sin(2*math.pi*cyc)**2
   p.leg(side,ankle,(s*.25,-1,0))
   p.arm_dirs(side,(s*.12,-.55*a,-1),(-s*.1,-.6*a,-1))
 return True
