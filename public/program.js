export const LEVELS = {beginner:30, regular:40, advanced:50};
export const LEVEL_NAMES = {beginner:'Beginner / returning',regular:'Regular',advanced:'Advanced'};
export const CAP = 900;
const ex = (name, family, cue, easier, harder, zone='Full body', media=null) => ({name,family,cue,easier,harder,zone,media});
export const EXERCISES = {
 upperBackStretch:{...ex("Gentle upper-back reach",'stretch',"Stand tall with knees soft. Bring your hands together in front at chest height and gently reach forwards. Let your shoulder blades move apart while keeping your neck relaxed. Hold a mild stretch across the upper back without forcing a rounded spine.","Reach less, keeping your back comfortable",'Keep the stretch mild','Cooldown'),target:"Upper back"},

 gluteStretchR:{...ex("Supine knee-to-chest stretch · right",'stretch',"Lie on your back with knees bent and both feet grounded. Hold behind your right thigh and gently bring that knee toward your chest. Keep your head and other foot supported. Hold a comfortable stretch around the back of your hip; do not pull hard.","Bring the knee only a little toward you",'Keep the stretch mild','Cooldown'),target:"Glutes and lower back"},

 quadStretchR:{...ex("Supported thigh stretch · right",'stretch',"Hold a wall with one hand. Bend your right knee and gently hold that ankle with the same-side hand. Keep knees close and your trunk upright. Hold a mild stretch at the front of the thigh. If you cannot comfortably reach your ankle, release and rest.","Release the ankle and rest if reaching is uncomfortable",'Keep the stretch mild','Cooldown'),target:"Quadriceps"},

 hipFlexorStretchR:{...ex("Standing hip-flexor stretch · right",'stretch',"Put your right foot behind you in a short split stance with the rear heel raised. Use wall support. Keep your trunk upright, gently tuck your pelvis and soften the front knee. Hold a mild stretch at the front of the rear hip without arching your back.","Shorter stance and less bend",'Keep the stretch mild','Cooldown'),target:"Hip flexors"},

 hamstringStretchR:{...ex("Standing hamstring stretch · right",'stretch',"Place your right heel a little forward with toes raised and knee soft. Bend the other knee and hinge gently at the hips, hands resting lightly on the upper thigh. Keep your back long. Hold a mild stretch behind the thigh; do not bounce.","Shorter stance and smaller hip hinge",'Keep the stretch mild','Cooldown'),target:"Hamstrings"},

 gluteStretchL:{...ex("Supine knee-to-chest stretch · left",'stretch',"Lie on your back with knees bent and both feet grounded. Hold behind your left thigh and gently bring that knee toward your chest. Keep your head and other foot supported. Hold a comfortable stretch around the back of your hip; do not pull hard.","Bring the knee only a little toward you",'Keep the stretch mild','Cooldown'),target:"Glutes and lower back"},

 quadStretchL:{...ex("Supported thigh stretch · left",'stretch',"Hold a wall with one hand. Bend your left knee and gently hold that ankle with the same-side hand. Keep knees close and your trunk upright. Hold a mild stretch at the front of the thigh. If you cannot comfortably reach your ankle, release and rest.","Release the ankle and rest if reaching is uncomfortable",'Keep the stretch mild','Cooldown'),target:"Quadriceps"},

 hipFlexorStretchL:{...ex("Standing hip-flexor stretch · left",'stretch',"Put your left foot behind you in a short split stance with the rear heel raised. Use wall support. Keep your trunk upright, gently tuck your pelvis and soften the front knee. Hold a mild stretch at the front of the rear hip without arching your back.","Shorter stance and less bend",'Keep the stretch mild','Cooldown'),target:"Hip flexors"},

 hamstringStretchL:{...ex("Standing hamstring stretch · left",'stretch',"Place your left heel a little forward with toes raised and knee soft. Bend the other knee and hinge gently at the hips, hands resting lightly on the upper thigh. Keep your back long. Hold a mild stretch behind the thigh; do not bounce.","Shorter stance and smaller hip hinge",'Keep the stretch mild','Cooldown'),target:"Hamstrings"},

 sumoSquat:ex('Wide-stance squat','squat','Use a comfortably wider stance with toes turned slightly out. Bend knees in line with toes, keep whole feet grounded, and stand smoothly.','Ordinary shallow squat','Slower lowering','Legs'),
 narrowSquat:ex('Close-stance squat','squat','Bring feet a little closer than your usual stance. Lower only through a comfortable range, keep heels grounded and stand with control.','Ordinary squat','Brief comfortable pause','Legs'),
 wallSit:ex('Shallow wall sit','squat','Rest your back against a stable wall. Walk feet forward a little and bend knees to a comfortable shallow angle. Breathe throughout; stand to rest before form fades.','Higher position and shorter hold','Slightly lower comfortable hold','Legs'),
 calfSingle:ex('Supported single-leg calf raise','calf','Hold a stable wall. Lift one foot a little and rise gently onto the other forefoot. Lower slowly. Change legs halfway; take support and rest whenever needed.','Two-leg calf raise','Slower lowering','Lower legs'),
 standingCrunch:ex('Standing cross-body knee lift','knee','Lift one knee and bring the opposite elbow gently toward it. Keep the range small, lower with control and alternate. Avoid pulling on your neck.','Ordinary low knee march with support','Brief balanced pause','Conditioning'),
 sideLegRaise:ex('Standing side leg raise','balance','Stand tall near a wall for balance. Lift one leg a little sideways without leaning, lower slowly and alternate. Keep toes facing forward.','Side toe tap with stable support','Slower lowering','Balance'),
 backLegRaise:ex('Standing hip extension','balance','Stand tall near stable support. Move one leg a little behind you without arching your back, return and alternate. Keep the movement small.','Small backward toe tap with support','Brief controlled pause','Balance'),
 frontKick:ex('Low controlled front kick','knee','Lift one knee a little, extend the lower leg forward without locking the knee, then lower and change sides. Keep kicks low and unhurried.','Alternating heel dig with support','A short balance pause','Conditioning'),
 boxerStep:ex('Boxer weight shift','boxing','Keep both feet grounded and knees soft. Shift your weight gently side to side while adding relaxed alternating punches. Keep elbows soft and use no weights.','Weight shift without punches','Steady alternating rhythm','Conditioning'),
 stepReach:ex('Diagonal step and reach','step','Take a small step diagonally forward with a comfortable opposite-arm reach. Return to the centre and change sides. Keep one foot grounded.','Small diagonal toe tap, arms low','Slightly larger controlled step','Conditioning'),
 squat:ex('Squat','squat','Keep your whole foot grounded. Sit your hips back and bend your knees in a comfortable range. Breathe out as you stand.','Shallow supported squat','Three-second lowering','Legs','squat'),
 chairSquat:ex('Chair sit-to-stand','squat','Place a sturdy, non-wheeled chair against a wall. Sit down gently, then press through your whole feet to stand.','Use your hands lightly for support','Stand with arms reaching forward','Legs'),
 shallowSquat:ex('Shallow squat','squat','Stand near a wall for balance. Bend your knees and hips a little, then stand tall. Keep the movement comfortable.','Smaller range','Slightly deeper squat','Legs'),
 pauseSquat:ex('Pause squat','squat','Lower in control. Pause briefly at a comfortable depth, then stand. Keep breathing.','Ordinary shallow squat','Three-second lowering','Legs'),
 slowSquat:ex('Slow-lowering squat','squat','Take three seconds to lower, then stand smoothly. Keep your whole foot on the floor.','Ordinary squat','Brief bottom pause','Legs'),
 push:ex('Kneeling push-up','push','Knees on the mat, hands just wider than shoulders. Keep a steady line from head to knees. Lower your chest, then press away.','Wall push-up','Full push-up','Upper body'),
 wallPush:ex('Wall push-up','push','Hands on a wall at chest height. Keep your body straight as you bend your elbows and bring your chest toward the wall. Press back.','Stand closer to the wall','Move feet slightly farther back','Upper body','wall-push'),
 fullPush:ex('Full push-up','push','Hands just wider than shoulders. Keep your trunk steady from head to heels. Lower with elbows angled back, then press up.','Kneeling push-up','Slower lowering or brief pause','Upper body'),
 pausePush:ex('Push-up with a pause','push','Use your comfortable push-up position. Pause briefly near the bottom, then press away. Stop before your form breaks.','Remove the pause','Controlled full push-up','Upper body'),
 bridge:ex('Glute bridge','bridge','Lie on your back, knees bent and feet grounded. Squeeze your glutes to lift your hips without arching your back. Lower slowly.','Smaller lift','Brief hold at the top','Posterior chain'),
 bridgeHold:ex('Glute bridge with hold','bridge','Lift your hips using your glutes. Hold briefly with ribs relaxed, then lower gently. Keep your pelvis level.','Ordinary bridge','Bridge march','Posterior chain'),
 bridgeMarch:ex('Bridge march','bridge','Lift into a low bridge. Keep your pelvis level while lifting one foot a little, then set it down and change sides.','Ordinary bridge','Slower alternating steps','Posterior chain'),
 wRaise:ex('Prone W raise','shoulders','Lie face down, forehead comfortably supported. Bend elbows into a W. Gently lift the arms without shrugging or lifting your head.','Arms supported: squeeze shoulder blades gently','Brief hold','Upper back'),
 wHold:ex('W raise with hold','shoulders','Face down with arms in a W. Gently lift, pause briefly, then lower. Keep the neck relaxed.','Gentle shoulder-blade squeeze','Slightly longer controlled hold','Upper back'),
 wSupported:ex('Supported shoulder-blade squeeze','shoulders','Lie face down with arms supported in a W. Gently draw shoulder blades toward each other without lifting your head.','Use less effort','Small W raise','Upper back'),
 angel:ex('Reverse snow angel','shoulders','Lie face down. Sweep your arms slowly from near your hips toward overhead, only through comfortable shoulder range. Keep neck neutral.','Prone W raise','Slower sweep','Upper back'),
 deadbug:ex('Dead bug','core','Lie on your back, knees bent above hips. Slowly reach one arm and the opposite leg away. Return and change sides. Keep your lower back steady.','Alternating heel slide','Longer comfortable reach','Core'),
 heelSlide:ex('Alternating heel slide','core','Lie on your back with both feet supported. Slide one heel away, then return and change legs. Keep your trunk still.','Shorter slide','Longer controlled slide','Core'),
 heelTap:ex('Supine heel tap','core','Lie on your back with knees bent above hips. Lower one heel toward the mat, return, then change legs. Avoid arching your back.','Heel slide with other foot supported','Slower lowering','Core'),
 calf:ex('Standing calf raise','calf','Hold a wall or sturdy chair lightly. Rise onto your forefeet, then lower slowly. Keep your weight balanced.','Smaller rise with support','Single leg, switching halfway','Lower legs'),
 slowCalf:ex('Slow calf raise','calf','Rise onto your forefeet, then take three seconds to lower. Hold stable support for balance.','Ordinary two-leg raise','One leg, switching halfway','Lower legs'),
 splitL:ex('Supported split squat · left','split','Left foot forward, right foot back. Hold a wall or a sturdy chair placed against a wall. Bend both knees to lower vertically, then stand.','Shallower bend','Slow descent','Legs'),
 splitR:ex('Supported split squat · right','split','Right foot forward, left foot back. Hold a wall or a sturdy chair placed against a wall. Bend both knees to lower vertically, then stand.','Shallower bend','Slow descent','Legs'),
 splitSwitch:ex('Supported split squat · change halfway','split','Use a fixed staggered stance with wall or chair support. Lower gently and rise. Switch the front leg halfway through.','Smaller range','Slow descent','Legs'),
 reverse:ex('Alternating reverse lunge','split','Step one foot back and lower comfortably. Push through your front foot to return. Alternate evenly; use support if needed.','Supported split squat, switch halfway','Slow descent','Legs'),
 lateral:ex('Shallow lateral lunge','lateral','Step to one side, bend that knee and send hips back. Return to the centre and change sides. Keep the range comfortable.','Small side step and shallow squat','Slightly greater comfortable range','Legs'),
 sideSquat:ex('Side step with shallow squat','lateral','Take a small side step, bend knees gently, then stand and move back. Change direction evenly.','Step-touch only','Comfortable arm reach','Legs'),
 hinge:ex('Standing hip hinge','hinge','Soften your knees. Send hips backwards while keeping a long neutral spine. Squeeze your glutes to stand tall.','Hands on hips, short range','Staggered stance','Posterior chain'),
 staggerHinge:ex('Staggered hip hinge · change halfway','hinge','Place one foot a little behind the other. Hinge your hips back with a long spine. Switch the front foot halfway.','Even-stance hinge','Slower lowering','Posterior chain'),
 sideL:ex('Side plank · left','side','Left elbow under shoulder, knees bent. Lift hips gently and keep a steady line from shoulders to knees. Breathe.','Short hold; lower whenever needed','Straight legs','Core'),
 sideR:ex('Side plank · right','side','Right elbow under shoulder, knees bent. Lift hips gently and keep a steady line from shoulders to knees. Breathe.','Short hold; lower whenever needed','Straight legs','Core'),
 sideFullL:ex('Straight-leg side plank · left','side','Left elbow under shoulder, legs extended. Lift hips and hold a steady line. Keep breathing.','Bent-knee side plank','Maintain a steady hold','Core'),
 sideFullR:ex('Straight-leg side plank · right','side','Right elbow under shoulder, legs extended. Lift hips and hold a steady line. Keep breathing.','Bent-knee side plank','Maintain a steady hold','Core'),
 sideRound:ex('Side plank · alternate rounds','side','Left side in round one, right side in round two. Elbow under shoulder; knees bent. Lift hips and breathe steadily.','Shorter hold','Straight legs','Core'),
 bird:ex('Bird dog','bird','On hands and knees, reach opposite arm and leg away. Keep your hips level. Return slowly and change sides.','Move one limb at a time','Brief hold','Core'),
 birdEasy:ex('Bird dog · one limb at a time','bird','On hands and knees, reach one arm or one leg away at a time. Keep your hips still. Change sides evenly.','Shorter reach','Opposite arm and leg together','Core'),
 birdHold:ex('Bird dog with hold','bird','Reach opposite arm and leg away. Hold briefly without rotating your hips, then return and switch sides.','One limb at a time','Longer comfortable reach','Core'),
 plank:ex('Kneeling forearm plank','plank','Elbows under shoulders, knees on the mat. Hold your trunk steady and breathe normally. Rest before form breaks.','Shorter hold','Full forearm plank','Core'),
 fullPlank:ex('Forearm plank','plank','Elbows under shoulders, legs extended. Keep a steady line from head to heels without sagging. Breathe.','Knees down','Slightly longer lever','Core'),
 taps:ex('Kneeling shoulder tap','taps','Hands under shoulders, knees on the mat. Lift one hand to the opposite shoulder, replace it, then alternate without rocking.','Gentle weight shift, hands stay down','Full plank with wide feet','Core'),
 weightShift:ex('Kneeling weight shift','taps','Hands and knees on the mat. Gently shift weight from one hand to the other while both hands stay down. Keep your trunk still.','Smaller shift','Kneeling shoulder tap','Core'),
 march:ex('Brisk march','march','March on the spot with relaxed shoulders and comfortable arm swing. Keep a pace where you can still speak.','Lower knees, slower pace','Brisker controlled rhythm','Conditioning'),
 crossMarch:ex('Opposite-hand knee march','march','March with each hand moving toward the opposite knee. Stay tall and move in a comfortable rhythm.','Ordinary march','Slightly higher knees','Conditioning'),
 driveMarch:ex('March with arm drive','march','March steadily and swing opposite arms with purpose. Keep your shoulders relaxed and steps controlled.','Easy march','Brisker rhythm','Conditioning'),
 jack:ex('Low-impact step jack','jack','Step one foot out as your arms rise comfortably. Return and alternate feet. Keep one foot on the floor.','Smaller steps, arms low','Wider controlled steps','Conditioning'),
 knee:ex('Alternating knee drive','knee','Stand tall and lift one knee comfortably. Lower and change legs. Use a wall or chair for balance if needed.','Lower lift','Brisker controlled rhythm','Conditioning'),
 sideStep:ex('Side step with reach','step','Step sideways, bring the other foot in and reach comfortably. Change direction. Keep steps soft.','Small step-touch without reach','Larger comfortable reach','Conditioning'),
 doubleStep:ex('Double side step','step','Take two small steps to one side, then two back. Stay upright and add an easy arm reach if comfortable.','One step each way','Add a comfortable arm reach','Conditioning'),
 punch:ex('Straight-punch shadow boxing','boxing','Use light straight punches with relaxed shoulders. Keep elbows soft at the end of each punch. No weights.','Slower punches','Controlled alternating rhythm','Conditioning'),
 uppercut:ex('Light uppercut shadow boxing','boxing','With elbows bent, make small upward punches in front of you. Keep shoulders relaxed and avoid forceful twisting.','Slow straight punches','Steady alternating rhythm','Conditioning'),
 heelDig:ex('Heel dig with arm swing','heel','Place one heel lightly in front, bring it back, then alternate. Add a relaxed arm swing.','Smaller reach, arms relaxed','Comfortable overhead reach','Conditioning'),
 heelReach:ex('Heel dig with reach','heel','Alternate heel digs in front as your arms reach comfortably upward. Keep shoulders relaxed and arms below painful range.','No arm reach','Coordinated steady rhythm','Conditioning'),
 toeTap:ex('Side-to-side toe tap','heel','Tap one toe lightly to the side, bring it back, then alternate. Keep your weight centred.','Small taps with support','Add relaxed arm swing','Conditioning'),
 curl:ex('Standing hamstring curl','curl','Bend one knee to bring your heel back toward your buttock. Lower and alternate; keep knees near each other.','Small bend with support','Comfortable arm swing','Conditioning'),
 forwardMarch:ex('Forward-and-back march','march','Take small marching steps forward and back in clear space. Stay balanced and face the same direction.','March on the spot','Slightly larger controlled steps','Conditioning'),
 easyMarch:ex('Easy march','march','March gently on the spot. Relax your shoulders and let your breathing settle.','Slow small steps','Comfortable arm swing','Warm-up'),
 circles:ex('Shoulder circles and arm swings','mobility','Roll your shoulders gently and swing your arms through a comfortable range. Avoid forcing any movement.','Smaller circles','Relaxed arm swings','Warm-up'),
 ankle:ex('Ankle rocks','mobility','Hold stable support. Gently shift weight from heels toward forefeet and back, keeping the movement small.','Smaller movement','Comfortable controlled range','Warm-up'),
 reach:ex('Gentle arm reaches','mobility','Reach one arm, then the other, comfortably upward and forward. Keep your ribs relaxed.','Arms below shoulder height','Comfortable higher reach','Warm-up'),
 stretchL:{...ex('Supported calf stretch · left','stretch','Left leg behind with heel grounded, front knee slightly bent. Hold a wall. Feel a mild stretch; never force it.','Shorter stance','Mild comfortable hold','Cooldown'),target:'Calves'},
 stretchR:{...ex('Supported calf stretch · right','stretch','Right leg behind with heel grounded, front knee slightly bent. Hold a wall. Feel a mild stretch; never force it.','Shorter stance','Mild comfortable hold','Cooldown'),target:'Calves'},
 breathe:ex('Standing breathing and shoulder release','mobility','Stand comfortably. Breathe slowly and let your shoulders soften. Make small gentle shoulder movements.','Still relaxed breathing','Gentle shoulder movement','Cooldown'),
 chest:{...ex('Comfortable chest opening','mobility','Stand tall with arms low. Gently draw shoulders back to open the chest without arching. Breathe naturally.','Smaller movement','Mild comfortable hold','Cooldown'),target:'Chest and front shoulders'}
};
const S = (day,name,kind,moves,focus) => ({day,name,kind,moves,focus,week:Math.ceil(day/7)});
export const SESSIONS = [
 S(1,'Foundation','strength',['squat','push','bridge','wRaise','deadbug','calf'],'Learn your six essentials.'),
 S(2,'March & move','conditioning',['march','jack','knee','sideStep','punch','heelDig'],'Find your rhythm, keep it conversational.'),
 S(3,'Stability','strength',['splitL','splitR','push','hinge','wRaise','sideRound'],'Build a steady base.'),
 S(5,'Full-body control','strength',['sumoSquat','push','bridge','wRaise','bird','plank'],'Move with purpose from head to toe.'),
 S(6,'Coordination','conditioning',['crossMarch','sideSquat','stepReach','knee','boxerStep','march'],'A little rhythm. A little coordination.'),
 S(8,'Pause & control','strength',['pauseSquat','push','bridgeMarch','angel','heelTap','slowCalf'],'Slow down to build control.'),
 S(9,'Footwork','conditioning',['forwardMarch','curl','frontKick','toeTap','punch','heelReach'],'Stay light on your feet.'),
 S(10,'Step-back strength','strength',['reverse','push','hinge','wRaise','sideL','sideR'],'Train both sides with care.'),
 S(12,'Lateral control','strength',['lateral','push','bridgeHold','angel','birdHold','taps'],'Explore a different direction.'),
 S(13,'Rhythm','conditioning',['standingCrunch','doubleStep','sideLegRaise','uppercut','curl','jack'],'Easy energy, flowing movement.'),
 S(15,'Controlled strength','strength',['slowSquat','push','bridgeMarch','wHold','deadbug','sideRound'],'Choose control over speed.'),
 S(16,'Athletic movement','conditioning',['driveMarch','sideSquat','backLegRaise','forwardMarch','boxerStep','stepReach'],'Move confidently in your space.'),
 S(17,'Unilateral control','strength',['splitL','splitR','pausePush','staggerHinge','angel','taps'],'Build balance, one side at a time.'),
 S(19,'Foundation check-in','strength',['squat','push','bridge','wRaise','deadbug','calf'],'Repeat day one. Notice what feels different.'),
 S(20,'Conditioning mix','conditioning',['doubleStep','frontKick','uppercut','standingCrunch','crossMarch','jack'],'Finish your foundation with a fresh mix.')
];
// Four 30-second movements per phase. Repeat day 1 on day 19 for a fair check-in.
export const SESSION_PREPARATION = {
 1: {"warmup": ["easyMarch", "circles", "hinge", "shallowSquat"], "cooldown": ["easyMarch", "chest", "stretchL", "stretchR"], "focus": "Squats, pushing, bridges and calf work", "warmupNote": "Hips and shoulders, then a shallow squat rehearsal.", "cooldownNote": "Calves after calf raises, plus chest after push-ups."},
 2: {"warmup": ["sideStep", "ankle", "circles", "knee"], "cooldown": ["heelDig", "upperBackStretch", "stretchL", "stretchR"], "focus": "Marching, step jacks and light punches", "warmupNote": "Ankles, shoulders and gentle knee lifts for marching and step jacks.", "cooldownNote": "Calves after repeated steps, plus upper back after punching."},
 3: {"warmup": ["heelDig", "hinge", "splitSwitch", "wallPush"], "cooldown": ["easyMarch", "upperBackStretch", "hipFlexorStretchL", "hipFlexorStretchR"], "focus": "Split squats, hinges, pushing and trunk stability", "warmupNote": "Hips, split stance and an easy push-up pattern.", "cooldownNote": "Front of the hips after split squats, plus upper back after W raises."},
 5: {"warmup": ["easyMarch", "sideSquat", "wallPush", "birdEasy"], "cooldown": ["easyMarch", "chest", "gluteStretchL", "gluteStretchR"], "focus": "Wide squats, bridges, pushing and core control", "warmupNote": "Side-to-side leg movement, gentle pushing and supported trunk control.", "cooldownNote": "Glutes after squats and bridges, plus chest after pushing."},
 6: {"warmup": ["sideStep", "reach", "toeTap", "knee"], "cooldown": ["heelDig", "upperBackStretch", "hipFlexorStretchL", "hipFlexorStretchR"], "focus": "Knee lifts, diagonal steps and boxing", "warmupNote": "Shoulders, lateral steps and low knee lifts for coordination.", "cooldownNote": "Hip flexors after repeated knee lifts, plus upper back after boxing."},
 8: {"warmup": ["heelDig", "ankle", "wallPush", "hinge"], "cooldown": ["easyMarch", "chest", "hamstringStretchL", "hamstringStretchR"], "focus": "Paused squats, bridges, pushing and calf control", "warmupNote": "Ankles, gentle pushing and hip movement before controlled strength.", "cooldownNote": "Hamstrings after bridges and squats, plus chest after push-ups."},
 9: {"warmup": ["easyMarch", "ankle", "curl", "heelDig"], "cooldown": ["sideStep", "upperBackStretch", "hamstringStretchL", "hamstringStretchR"], "focus": "Footwork, hamstring curls, low kicks and punches", "warmupNote": "Ankles and easy knee bends before curls and low kicks.", "cooldownNote": "Hamstrings after curls and kicks, plus upper back after punching."},
 10: {"warmup": ["sideStep", "splitSwitch", "hinge", "wallPush"], "cooldown": ["easyMarch", "upperBackStretch", "quadStretchL", "quadStretchR"], "focus": "Reverse lunges, hinges, pushing and side planks", "warmupNote": "A shallow split stance, gentle hip hinge and easy pushing.", "cooldownNote": "Quadriceps after lunges, plus upper back after W raises."},
 12: {"warmup": ["easyMarch", "sideSquat", "wallPush", "weightShift"], "cooldown": ["easyMarch", "upperBackStretch", "gluteStretchL", "gluteStretchR"], "focus": "Lateral lunges, bridges, pushing and shoulder taps", "warmupNote": "Side-to-side leg loading and gentle hand support before taps.", "cooldownNote": "Glutes after lateral lunges and bridges, plus upper back after arm sweeps."},
 13: {"warmup": ["heelDig", "toeTap", "circles", "curl"], "cooldown": ["sideStep", "chest", "quadStretchL", "quadStretchR"], "focus": "Knee lifts, side steps, curls and uppercuts", "warmupNote": "Lateral steps, relaxed shoulders and easy knee bends.", "cooldownNote": "Quadriceps after repeated leg work, plus chest after uppercuts and arm reaches."},
 15: {"warmup": ["sideStep", "shallowSquat", "wallPush", "heelSlide"], "cooldown": ["easyMarch", "upperBackStretch", "hamstringStretchL", "hamstringStretchR"], "focus": "Slow squats, bridges, upper-back and core work", "warmupNote": "Gentle squats and pushing, then controlled trunk movement.", "cooldownNote": "Hamstrings after bridges and squats, plus upper back after W holds."},
 16: {"warmup": ["heelDig", "hinge", "circles", "sideSquat"], "cooldown": ["heelDig", "upperBackStretch", "gluteStretchL", "gluteStretchR"], "focus": "Hip extension, side squats, marching and boxing", "warmupNote": "Hip hinges, shoulder movement and shallow side squats.", "cooldownNote": "Glutes after hip extension and side squats, plus upper back after boxing."},
 17: {"warmup": ["easyMarch", "splitSwitch", "wallPush", "weightShift"], "cooldown": ["easyMarch", "chest", "hipFlexorStretchL", "hipFlexorStretchR"], "focus": "Split squats, staggered hinges, pushing and taps", "warmupNote": "Split stance and gentle arm support before unilateral work.", "cooldownNote": "Front of the hips after split squats, plus chest after paused push-ups."},
 19: {"warmup": ["easyMarch", "circles", "hinge", "shallowSquat"], "cooldown": ["easyMarch", "chest", "stretchL", "stretchR"], "focus": "Repeat the foundation session", "warmupNote": "The same warm-up as day one keeps the comparison consistent.", "cooldownNote": "The same calf and chest cooldown as day one."},
 20: {"warmup": ["sideStep", "knee", "circles", "heelDig"], "cooldown": ["sideStep", "chest", "hipFlexorStretchL", "hipFlexorStretchR"], "focus": "Low kicks, knee lifts, uppercuts and step jacks", "warmupNote": "Low knee lifts and relaxed shoulders before kicks and uppercuts.", "cooldownNote": "Hip flexors after kicks and knee lifts, plus chest after uppercuts."},
};
export function included(session,days){return session.kind==='strength'||(session.day%7===2&&Number(days)>=4)||(session.day%7===6&&Number(days)>=5);}
export function safetyReasons(p){const reasons=[];if(p.age==='under18')reasons.push('This programme is designed for adults.');if(p.pain!=='none')reasons.push('Current pain, injury or an exercise restriction needs individual guidance before we assign this routine.');if(p.floor!=='yes')reasons.push('This programme includes floor exercises. A reviewed standing programme is needed for your floor or balance limitation.');if(p.goal==='test')reasons.push('Military test preparation needs your actual test requirements and a separately calibrated plan.');return reasons;}
export function variation(id,p,round=0){
 if(id==='sideRound')id=round===0?'sideL':'sideR';
 const family=EXERCISES[id].family;
 const choice=p.variations?.[family]??(p.level==='beginner'?'easier':'standard');
 if(family==='push')return choice==='easier'?'wallPush':choice==='harder'?'fullPush':id==='pausePush'?'pausePush':'push';
 if(choice==='easier'){
  if(family==='squat')return p.equipment?.includes('chair')?'chairSquat':'shallowSquat';
  const map={bridgeMarch:'bridge',bridgeHold:'bridge',angel:'wRaise',wRaise:'wSupported',wHold:'wSupported',deadbug:'heelSlide',heelTap:'heelSlide',reverse:'splitSwitch',lateral:'sideSquat',staggerHinge:'hinge',bird:'birdEasy',birdHold:'birdEasy',taps:'weightShift',standingCrunch:'knee',frontKick:'heelDig',sideLegRaise:'toeTap',backLegRaise:'toeTap',stepReach:'sideStep',calfSingle:'calf'};
  return map[id]??id;
 }
 if(choice==='harder'){
  const map={squat:'slowSquat',bridge:'bridgeHold',wRaise:'wHold',calf:'slowCalf',sideL:'sideFullL',sideR:'sideFullR',bird:'birdHold',plank:'fullPlank'};
  return map[id]??id;
 }
 return id;
}
export function buildTimeline(session,profile,baseline=null){
 const p=session.day===19&&baseline?{...profile,level:baseline.level,variations:baseline.variations}:profile;
 const seconds=LEVELS[p.level];if(!seconds)throw new Error('Unknown level');
 const order=session.week===2&&session.kind==='strength'?[0,1,0,1,2,3,2,3,4,5,4,5]:[0,1,2,3,4,5,0,1,2,3,4,5];
 const preparation=SESSION_PREPARATION[session.day];
 const timeline=preparation.warmup.map(id=>({id,kind:'warmup',seconds:30}));
 const seen={};
 order.forEach((station,i)=>{
  const original=session.moves[station];const round=seen[station]??0;seen[station]=round+1;
  const id=variation(original,p,round);
  timeline.push({id,original,kind:'work',seconds,station:station+1,interval:i+1,round:round+1});
  if(i<11)timeline.push({kind:'rest',seconds:i===5?60:30,nextId:variation(session.moves[order[i+1]],p,seen[order[i+1]]??0)});
 });
 timeline.push(...preparation.cooldown.map(id=>({id,kind:'cooldown',seconds:30})));
 if(activeSeconds(timeline)>CAP)throw new Error('Active time cap exceeded');
 return timeline;
}
export const activeSeconds=timeline=>timeline.reduce((total,x)=>total+(x.kind==='rest'?0:x.seconds),0);
export const totalSeconds=timeline=>timeline.reduce((total,x)=>total+x.seconds,0);
export const formatTime=s=>`${Math.floor(Math.max(0,s)/60)}:${String(Math.ceil(Math.max(0,s)%60)).padStart(2,'0')}`;
export const dayDate=(start,day)=>{const d=new Date(`${start}T12:00:00`);d.setDate(d.getDate()+day-1);return d;};
