"""Looping floor exercise poses for the approved isahhah character.

All dimensions use the shared rig's measured segment lengths. These are movement
illustrations for review, not clinical biomechanical certification.
"""
import math
from mathutils import Vector, Quaternion
from pose_api import Q, pulse, smooth
V=Vector

SPECS={
 'push':{'duration':5,'view':'floor'},'fullPush':{'duration':5,'view':'floor'},
 'pausePush':{'duration':6,'view':'floor'},'wallPush':{'duration':5,'view':'wall'},
 'bridge':{'duration':5,'view':'floor'},'bridgeHold':{'duration':6,'view':'floor'},
 'bridgeMarch':{'duration':8,'view':'floor'},
 'wRaise':{'duration':5,'view':'floor'},'wHold':{'duration':6,'view':'floor'},
 'wSupported':{'duration':5,'view':'floor'},'angel':{'duration':8,'view':'floor'},
 'deadbug':{'duration':10,'view':'floor'},'heelSlide':{'duration':8,'view':'floor'},
 'heelTap':{'duration':8,'view':'floor'},
 'sideL':{'duration':6,'view':'floor'},'sideR':{'duration':6,'view':'floor'},
 'sideFullL':{'duration':6,'view':'floor'},'sideFullR':{'duration':6,'view':'floor'},
 'bird':{'duration':10,'view':'floor'},'birdEasy':{'duration':12,'view':'floor'},
 'birdHold':{'duration':12,'view':'floor'},
 'plank':{'duration':6,'view':'floor'},'fullPlank':{'duration':6,'view':'floor'},
 'taps':{'duration':8,'view':'floor'},'weightShift':{'duration':6,'view':'floor'},
}

def _hold_pulse(t):
    u=t%1
    if u<.4:return smooth(u/.4)
    if u<.6:return 1.
    return 1-smooth((u-.6)/.4)

def _alternating(t,hold=False):
    u=(t%1)*2
    return ('l' if u<1 else 'r'), (_hold_pulse(u%1) if hold else pulse(u%1))

def _handq(p,side,direction):
    r=p.r['hand_'+side]
    return (r['t']-r['h']).rotation_difference(V(direction))

def _direct_leg(p,side,knee_direction,calf_direction,foot_q):
    thigh,calf,foot,ball=[n+'_'+side for n in ['thigh','calf','foot','ball']]
    hip=p.joint(thigh)
    knee=hip+V(knee_direction).normalized()*p.length(thigh)
    ankle=knee+V(calf_direction).normalized()*p.length(calf)
    p.bone(thigh,hip,knee);p.bone(calf,knee,ankle);p.bone(foot,ankle,q=foot_q)
    p.bone(ball,ankle+foot_q@(p.r[ball]['h']-p.r[foot]['h']),q=foot_q)
    return knee,ankle

def _head_flat(p,rotation):
    """Keep a bridge's supported neck/head near the mat as the hips rise."""
    n='neck_01';head=p.joint(n)
    # Neck starts at the upper chest; neck and head keep a neutral floor axis.
    p.bone(n,head,q=rotation)
    h=head+rotation@(p.r['head']['h']-p.r[n]['h'])
    p.bone('head',h,q=rotation)

def _supine(p,height=.135,tilt=-90,y=0):
    p.torso((0,y,height),Q((1,0,0),tilt))

def _supine_arms(p):
    for side,sign in [('l',1),('r',-1)]:
        shoulder=p.joint('upperarm_'+side)
        p.arm(side,(sign*.22,shoulder.y-.37,.075),hint=(sign,0,-.05),hand_q=_handq(p,side,(0,-1,0)))

def _bridge(p,id,t):
    a=.75 if id=='bridgeMarch' else (_hold_pulse(t) if id=='bridgeHold' else pulse(t))
    rise=.17*a
    theta=math.degrees(math.asin(rise/.44))
    _supine(p,.135+rise,-90-theta,.44-math.sqrt(.44*.44-rise*rise))
    _head_flat(p,Q((1,0,0),-90))
    active,amount=_alternating(t,True)
    for side,sign in [('l',1),('r',-1)]:
        lift=.055*amount if id=='bridgeMarch' and active==side else 0
        p.leg(side,(sign*.13,-.31,.066+lift),hint=(0,0,1),foot_q=Quaternion())
    _supine_arms(p)

def _deadbug(p,id,t):
    _supine(p)
    active,a=_alternating(t)
    if id=='heelSlide':
        for side,sign in [('l',1),('r',-1)]:
            amount=a if side==active else 0
            p.leg(side,(sign*.13,-.31-.34*amount,.066),hint=(0,0,1),foot_q=Quaternion())
        _supine_arms(p);return
    for side,sign in [('l',1),('r',-1)]:
        amount=a if side==active else 0
        # Start in tabletop: knees over hips, lower leg parallel to the floor.
        if id=='heelTap':target=(sign*.12,-.32-.04*amount,.48-.39*amount)
        else:target=(sign*.12,-.32-.34*amount,.48-.30*amount)
        p.leg(side,target,hint=(0,0,1),foot_q=Q((1,0,0),-25*(1-amount)))
        if id=='heelTap':continue
        # Opposite arm reaches overhead while the other remains vertical.
        arm_amount=a if side!=active else 0
        shoulder=p.joint('upperarm_'+side)
        upper=V((sign*.025,math.sin(arm_amount*1.35),math.cos(arm_amount*1.35)))
        p.arm_dirs(side,upper,upper,hand_q=_handq(p,side,upper))
    if id=='heelTap':_supine_arms(p)

def _push(p,id,t):
    a=_hold_pulse(t) if id=='pausePush' else pulse(t)
    if id=='wallPush':
        # Wall face is Y=-0.53. Hands stay on it throughout the repetition.
        angle=10+10*a
        q=Q((1,0,0),angle)
        pelvis=p.origin+V((0,-.13*a,-.014*a))
        p.torso(pelvis,q)
        for side,sign in [('l',1),('r',-1)]:
            p.leg(side,p.r['foot_'+side]['h'],hint=(0,-1,0))
            p.arm(side,(sign*.22,-.50,1.16),hint=(sign,.5,0),hand_q=_handq(p,side,(0,0,1)))
        return
    full=id=='fullPush'
    if full:
        angle=70+12*a;theta=math.radians(angle);q=Q((1,0,0),angle)
        leglen=(p.length('thigh_l')+p.length('calf_l'))*.995
        # Hips move around fixed toe/ankle supports; trunk stays in line.
        offset=q@(p.r['thigh_l']['h']-p.origin)
        pelvis=(0,.65-leglen*math.sin(theta)-offset.y,.11+leglen*math.cos(theta)-offset.z)
        p.torso(pelvis,q)
        for side,sign in [('l',1),('r',-1)]:p.leg(side,(sign*.11,.65,.11),hint=(0,0,-1),foot_q=Q((1,0,0),30))
    else:
        angle=65+18*a;q=Q((1,0,0),angle)
        thigh_theta=math.radians(45+22*a)
        knee_y=.25;knee_z=.055
        length=p.length('thigh_l')
        offset=q@(p.r['thigh_l']['h']-p.origin)
        p.torso((0,knee_y-length*math.sin(thigh_theta)-offset.y,knee_z+length*math.cos(thigh_theta)-offset.z),q)
        for side in ['l','r']:_direct_leg(p,side,(0,math.sin(thigh_theta),-math.cos(thigh_theta)),(0,.985,.17),Q((1,0,0),75))
    for side,sign in [('l',1),('r',-1)]:
        p.arm(side,(sign*.215,-.40,.085),hint=(sign*.7,.8,0),hand_q=_handq(p,side,(0,-1,0)))

def _prone(p,id,t):
    a=_hold_pulse(t) if id=='wHold' else pulse(t)
    p.torso((0,0,.155),Q((1,0,0),90))
    for side,sign in [('l',1),('r',-1)]:
        p.leg(side,(sign*.13,.735,.08),hint=(0,0,.2),foot_q=Q((1,0,0),108))
        if id=='angel':
            # Sweep in the floor plane from beside hips to a comfortable V.
            ang=math.radians(-50+195*a)
            d=V((sign*math.cos(ang),math.sin(ang),.06))
            # positive Y is hips; overhead is negative Y
            d.y=-d.y
            p.arm_dirs(side,d,d,hand_q=_handq(p,side,d))
        else:
            lift=.0 if id=='wSupported' else .13*a
            p.arm_dirs(side,(sign*.90,.20+(.045*a if id=='wSupported' else 0),lift),(-sign*.20,-.95,lift),hand_q=_handq(p,side,(-sign*.20,-.95,.05)))

def _quadruped(p,id,t):
    active,a=_alternating(t,id=='birdHold')
    shift=.018*math.sin(2*math.pi*t) if id=='weightShift' else 0
    p.torso((shift,0,.405),Q((1,0,0),90))
    arm_active=active;leg_active='r' if active=='l' else 'l'
    if id=='birdEasy':
        phase=int((t%1)*4);a=pulse((t%1)*4%1)
        arm_active=['l','r',None,None][phase];leg_active=[None,None,'l','r'][phase]
    for side,sign in [('l',1),('r',-1)]:
        bird=id in ['bird','birdHold','birdEasy']
        reach=a if bird and side==leg_active else 0
        # Neutral support uses a knee under the hip; reach unfolds the leg.
        thigh_dir=V((0,.19*(1-reach)+reach,-.982*(1-reach)))
        calf_dir=V((0,.985,.17*(1-reach)))
        if reach>0:
            qfoot=Q((1,0,0),75+105*reach)
        else:qfoot=Q((1,0,0),75)
        _direct_leg(p,side,thigh_dir,calf_dir,qfoot)
        shoulder=p.joint('upperarm_'+side)
        neutral=V((sign*.20,-.43,.065))
        if bird and side==arm_active:
            target=V((sign*.15,-.80,.42));wrist=neutral.lerp(target,a)
        elif id=='taps' and side==active:
            other=p.joint('upperarm_'+('r' if side=='l' else 'l'))
            wrist=neutral.lerp(other+V((0,.015,-.05)),a)
        else:wrist=neutral
        hand_direction=V((0,-1,0)).lerp(V((-sign,0,0)),a) if id=='taps' and side==active else V((0,-1,0))
        p.arm(side,wrist,hint=(sign*.35,.7,0),hand_q=_handq(p,side,hand_direction))

def _forearm(p,id,t):
    # Tiny breathing variation makes the isometric hold visibly alive.
    breath=.002*math.sin(2*math.pi*t)
    if id=='fullPlank':
        angle=82.65;theta=math.radians(angle);q=Q((1,0,0),angle)
        length=(p.length('thigh_l')+p.length('calf_l'))*.995
        offset=q@(p.r['thigh_l']['h']-p.origin)
        p.torso((0,.65-length*math.sin(theta)-offset.y,.11+length*math.cos(theta)-offset.z+breath),q)
        for side,sign in [('l',1),('r',-1)]:p.leg(side,(sign*.11,.65,.11),hint=(0,0,-1),foot_q=Q((1,0,0),30))
    else:
        p.torso((0,-.05,.19+breath),Q((1,0,0),80))
        for side in ['l','r']:_direct_leg(p,side,(0,.92,-.39),(0,.985,.17),Q((1,0,0),75))
    for side,sign in [('l',1),('r',-1)]:
        p.arm_dirs(side,(sign*.03,0,-1),(0,-1,0),hand_q=_handq(p,side,(0,-1,0)))

def _side(p,id,t):
    left=id.endswith('L');sign=1 if left else -1
    full='Full' in id
    q=Q((1,0,0),-14)@Q((0,1,0),90*sign)@Q((1,0,0),90)
    p.torso((0,0,.30+.0015*math.sin(2*math.pi*t)),q)
    bottom='l' if left else 'r'
    for side in ['l','r']:
        lower=side==bottom
        if full:
            hip=p.joint('thigh_'+side)
            ankle_z=.065 if lower else .145
            reach=(p.length('thigh_'+side)+p.length('calf_'+side))*.995
            ankle_y=hip.y+math.sqrt(max(.001,reach*reach-(ankle_z-hip.z)**2-hip.x**2))
            p.leg(side,(0,ankle_y,ankle_z),hint=(0,0,-1),foot_q=q)
        else:
            hip=p.joint('thigh_'+side)
            dz=(.055 if lower else .14)-hip.z
            dy=math.sqrt(max(.001,p.length('thigh_'+side)**2-dz*dz))
            _direct_leg(p,side,(0,dy,dz),(sign*.90,-.38,.10),q)
        shoulder=p.joint('upperarm_'+side)
        if lower:
            p.arm_dirs(side,(0,0,-1),(-sign,0,0),hand_q=_handq(p,side,(-sign,0,0)))
        else:
            # Free hand rests close to the hip, with elbow slightly open.
            wrist=p.pelvis+V((-sign*.10,.04,.10))
            p.arm(side,wrist,hint=(-sign,0,.4),hand_q=_handq(p,side,(0,1,0)))

def pose(p,id,t):
    if id not in SPECS:return False
    if id in ['push','fullPush','pausePush','wallPush']:_push(p,id,t)
    elif id in ['bridge','bridgeHold','bridgeMarch']:_bridge(p,id,t)
    elif id in ['deadbug','heelSlide','heelTap']:_deadbug(p,id,t)
    elif id in ['wRaise','wHold','wSupported','angel']:_prone(p,id,t)
    elif id in ['bird','birdEasy','birdHold','taps','weightShift']:_quadruped(p,id,t)
    elif id in ['plank','fullPlank']:_forearm(p,id,t)
    else:_side(p,id,t)
    return True
