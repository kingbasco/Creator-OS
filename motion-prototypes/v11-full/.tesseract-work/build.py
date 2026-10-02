import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text()); doc['duration']=78
L=[]; A=[]; uid=2500
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; AMBER='#FFF4DC'; AI='#956515'; RED='#FDEBEC'; RI='#B33A42'; PURPLE='#EEE9FF'; PI='#6A4BC4'; DARK='#1C2738'; BORDER='#E5E8EE'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=78):
 global uid; uid+=1; return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
def rect(n,x,y,w,h,col,r=0,s=0,e=78):
 o=b('Rect',n,x,y,s,e); o['rect']=dict(size=[w,h],fillColor=c(col),roundness=r); return o
def txt(n,v,x,y,z=30,col=INK,w=800,s=0,e=78,bold=False):
 o=b('Text',n,x,y,s,e); o['sourceText']=dict(text=v,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=z,fillColor=c(col),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=z*1.12); return o
def grp(n,ch,x=0,y=0,s=0,e=78):
 o=b('Group',n,x,y,s,e); o['layers']=ch[::-1]; return o
def card(n,x,y,w,h,col='#FFFFFF',r=22,s=0,e=78):
 o=rect(n,x,y,w,h,col,r,s,e); o['dropShadow']=dict(color=[.05,.08,.14,.12],blurRadius=24,spreadRadius=0,offset=[0,12],blendMode='normal'); return o
def anim(o,p,code): A.append(dict(type='setFxPropertyAnimator',compositionId='main',property={'layerId':o['id'],'propertyType':p},animator={'type':'jsScript','layerTimeJsCode':code},dependencies=[]))
def keys(o,p,vals):
 if p in ['position','scale']:
  for ax,ix in [('X',0),('Y',1)]: keys(o,p+ax,[(t,v[ix]) for t,v in vals])
  return
 typ='vector2' if isinstance(vals[0][1],list) else 'float'
 A.append(dict(type='setFxPropertyKeyframes',compositionId='main',property={'layerId':o['id'],'propertyType':p},keyframes=[dict(id=f'{o["id"]}-{p}-{i}',layerTime=int(t*1000),value={'type':typ,'value':v},easing={'type':'cubicBezier','x1':.22,'y1':1,'x2':.36,'y2':1}) for i,(t,v) in enumerate(vals)]))
def enter(o,d=0): anim(o,'opacity',f'return Math.min(100,Math.max(0,(input.time.seconds-{d})*400));')
def reveal(o,d=0,dy=28): x,y=o['transform']['position']; keys(o,'position',[(0,[x,y+dy]),(.55,[x,y])]); enter(o,d)
def chip(v,x,y,w,col,tc,s=0,e=78): return grp(v,[rect('bg',0,0,w,52,col,12,s,e),txt('t',v,17,11,22,tc,w-24,s,e,True)],x,y,s,e)
def scene(n,ch,s,e): L.append(grp(n,ch,s=s,e=e))
def title(a,e,s,en):
 g=grp('Headline',[txt('l',a,80,182,62,INK,900,s,en,True),txt('e',e,80,265,59,BLUE,900,s,en,True)],s=s,e=en); reveal(g); L.append(g)

proto=copy.deepcopy(doc)
L=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,BORDER),rect('Rule',80,1225,920,2,BORDER),rect('Rule',80,1730,920,2,BORDER)]

# S01 loop overview
title('A better build comes from','a better loop.',0,8)
a=[]
st=[('INSPECT','Repo scan',110,550,GREEN,GI),('PLAN','Change plan',690,550,SOFT,BLUE),('CODE','Focused diff',690,900,AMBER,AI),('TEST','Run checks',110,900,PURPLE,PI)]
for i,(n,sub,x,y,bg,tc) in enumerate(st):
 box=grp(n,[card('c',0,0,280,150,bg),txt('n',n,24,24,25,tc,220,bold=True),txt('s',sub,24,76,24,INK,220)],x,y); reveal(box,.15+i*.15); a.append(box)
center=grp('center',[card('c',0,0,360,200,DARK),txt('l','WORKFLOW',30,25,20,'#AAB6CE',180,bold=True),txt('t','Inspect → Plan\nCode → Test',30,76,36,'#FFFFFF',300,bold=True)],360,725); reveal(center,.65); a.append(center)
a.append(chip('REVIEW EVERY PASS',400,1110,280,GREEN,GI))
scene('S01',a,0,8)

# S02 inspect
title('First, inspect','what already exists.',8,18)
a=[]
repo=grp('repo',[card('c',0,0,420,500,DARK),chip('1  INSPECT',26,24,190,'#2B3850','#DCE3F3',8,18),txt('tree','src/\n  auth/\n    login.ts\n  participants/\n    edit-email.ts\n  mail/\n    send.ts\n  db/\n    users.sql',28,106,27,'#FFFFFF',330)],95,535); reveal(repo,.2); a.append(repo)
current=grp('current',[card('c',0,0,430,360,'#FFFFFF'),txt('l','CURRENT BEHAVIOR',26,25,20,MUT,240,bold=True),txt('t','Admin edits email\n→ DB changes\n→ login identity stays old',26,86,32,INK,360,bold=True),chip('SMALLEST SURFACE',26,268,250,SOFT,BLUE,8,18)],555,590); reveal(current,.7); a.append(current)
scene('S02',a,8,18)

# S03 plan
title('Then make','a short plan.',18,28)
a=[]
plan=grp('plan',[card('c',0,0,850,520,'#FFFFFF'),chip('2  PLAN',28,25,160,SOFT,BLUE,18,28),txt('h','Change participant email safely',28,100,38,INK,760,bold=True)],115,520)
items=['Goal: update email everywhere','Files: participants + auth + mail','Constraint: keep participant ID','Done: login + email both work']
for i,it in enumerate(items):
 plan['layers'].append(grp('i'+str(i),[rect('dot',0,0,36,36,GREEN,9),txt('tick','✓',9,2,24,GI,22,bold=True),txt('it',it,54,2,27,INK,690)],28,180+i*72))
reveal(plan,.2); a.append(plan)
scene('S03',a,18,28)

# S04 code
title('Code one','small slice.',28,38)
a=[]
diff=grp('diff',[card('c',0,0,850,500,DARK),chip('3  CODE',28,25,160,'#2B3850','#DCE3F3',28,38),txt('file','participants/edit-email.ts',28,96,24,'#AAB6CE',500,bold=True),txt('code','- updateParticipant(email)\n+ updateParticipant(email)\n+ syncAuthIdentity(email)\n+ writeAuditEvent(email)',28,152,29,'#FFFFFF',760)],115,530); reveal(diff,.2); a.append(diff)
a.append(chip('FOCUSED DIFF',390,1080,300,AMBER,AI,28,38))
scene('S04',a,28,38)

# S05 test
title('Test immediately','while the change is small.',38,48)
a=[]
term=grp('term',[card('c',0,0,850,500,DARK),chip('4  TEST',28,25,160,'#2B3850','#DCE3F3',38,48),txt('h','CHECKS',28,98,21,'#AAB6CE',150,bold=True)],115,520)
tests=[('typecheck','PASS',GREEN,GI),('email updates DB','PASS',GREEN,GI),('login accepts new email','FAIL',RED,RI),('old email rejected','WAIT',AMBER,AI)]
for i,(name,state,bg,tc) in enumerate(tests):
 term['layers'].append(grp('t'+str(i),[txt('n',name,0,0,27,'#FFFFFF',520),chip(state,620,-8,130,bg,tc,38,48)],28,170+i*70))
reveal(term,.2); a.append(term)
a.append(chip('FAILURE IS CLOSE TO THE CHANGE',300,1085,480,RED,RI,38,48))
scene('S05',a,38,48)

# S06 review
title('Now review','the diff and the result.',48,58)
a=[]
left=grp('plan summary',[card('c',0,0,380,390,SOFT),chip('PLAN',24,24,120,'#FFFFFF',BLUE,48,58),txt('b','• update DB\n• sync auth identity\n• preserve participant ID\n• record audit event',24,105,28,INK,320)],95,550); reveal(left,.2); a.append(left)
right=grp('result summary',[card('c',0,0,380,390,'#FFFFFF'),chip('RESULT',24,24,135,GREEN,GI,48,58),txt('b','DB updated\nAuth updated\nID unchanged\nAudit event created',24,105,28,INK,320)],605,550); reveal(right,.55); a.append(right)
a.append(grp('review',[card('c',0,0,850,150,DARK),txt('l','REVIEW',28,22,20,'#AAB6CE',150,bold=True),txt('t','Does the result match the plan?',28,64,32,'#FFFFFF',750,bold=True)],115,1010))
scene('S06',a,48,58)

# S07 repeat / failed test sends back
title('If it fails,','go back one step.',58,68)
a=[]
code=grp('code',[card('c',0,0,380,280,AMBER),chip('CODE',25,24,130,'#FFFFFF',AI,58,68),txt('b','Fix auth identity sync\nwithout touching more files.',25,105,29,INK,320)],110,570); reveal(code,.2); a.append(code)
test=grp('test',[card('c',0,0,380,280,'#FFFFFF'),chip('TEST',25,24,130,PURPLE,PI,58,68),txt('b','login accepts new email\nold email rejected',25,105,28,INK,320)],590,570); reveal(test,.55); a.append(test)
fail=chip('1 FAILED',700,805,170,RED,RI,58,68); keys(fail,'opacity',[(0,0),(2,0),(2.4,100),(4.8,100),(5.2,0)]); a.append(fail)
patch=chip('PATCH APPLIED',190,885,210,GREEN,GI,58,68); keys(patch,'opacity',[(0,0),(4.8,0),(5.2,100)]); a.append(patch)
passed=chip('2 PASSED',700,885,180,GREEN,GI,58,68); keys(passed,'opacity',[(0,0),(5.5,0),(5.9,100)]); a.append(passed)
a.append(grp('note',[card('c',0,0,820,145,DARK),txt('t','Fix the last step before adding more work.',30,50,31,'#FFFFFF',760,bold=True)],130,1040))
scene('S07',a,58,68)

# S08 final loop
title('Inspect → Plan → Code → Test','→ Review → Repeat.',68,78)
a=[]
steps=[('INSPECT',120,590,GREEN,GI),('PLAN',330,500,SOFT,BLUE),('CODE',610,500,AMBER,AI),('TEST',820,590,PURPLE,PI),('REVIEW',610,820,GREEN,GI),('REPEAT',330,820,SOFT,BLUE)]
for i,(name,x,y,bg,tc) in enumerate(steps):
 w=180
 item=grp(name,[card('c',0,0,w,110,bg),txt('n',name,22,34,23,tc,135,bold=True)],x,y); reveal(item,.12+i*.12); a.append(item)
a.append(grp('center',[card('c',0,0,360,180,DARK),txt('l','THE LOOP',30,25,20,'#AAB6CE',170,bold=True),txt('t','Direction + checkpoints',30,76,33,'#FFFFFF',300,bold=True)],360,665))
a.append(chip('SCREENSHOT THIS',390,1055,300,BLUE,'#FFFFFF',68,78))
scene('S08',a,68,78)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':78000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1390]; presenter['transform']['scale']=[84,84]; L.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1650]),(.7,[40,1390])]); keys(arm,'rotation',[(0,18),(.9,-8),(5,-18),(10,-7),(15,-18),(20,-7),(25,-18),(30,-7),(35,-18),(40,-7),(45,-18),(50,-7),(55,-18),(60,-7),(65,-18),(70,-7),(75,-16)])
notes=[(0,8,'USE THE LOOP','Quality comes from\na repeatable process.'),(8,18,'1. INSPECT','Understand the current\nsystem first.'),(18,28,'2. PLAN','Define the change\nbefore editing.'),(28,38,'3. CODE','Keep the diff small.'),(38,48,'4. TEST','Catch failure close\nto the change.'),(48,58,'5. REVIEW','Compare plan and result.'),(58,68,'CORRECT + REPEAT','Go back one step\nwhen a check fails.'),(68,78,'COPY THIS WORKFLOW','Give the agent direction\nand yourself checkpoints.')]
for s,e,l,body in notes:
 n=grp('note',[txt('s',l,650,1460,22,BLUE,330,s,e,True),txt('b',body,650,1508,30,INK,330,s,e)],s=s,e=e); enter(n); L.append(n)

doc['composition']={'id':'main','name':'V11 Coding Loop / full visual draft','layers':L[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(A,open(HERE.parent/'animation.json','w'),indent=2)
print('V11 full',uid,len(A))
