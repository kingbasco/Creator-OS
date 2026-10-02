import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=78

layers=[]; actions=[]; uid=600
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
GREEN='#E9F7EF'; GREENINK='#167749'; RED='#FDEBEC'; REDINK='#B33A42'
AMBER='#FFF4DC'; AMBERINK='#956515'; BORDER='#E5E8EE'; DARK='#1C2738'

def col(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def trans(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def base(t,n,x=0,y=0,start=0,end=78):
    global uid; uid+=1
    return dict(type=t,id=uid,name=n,blendMode='normal',
                activeRange={'start':int(start*1000),'duration':int((end-start)*1000)},
                transform=trans(x,y))
def rect(n,x,y,w,h,c,r=0,start=0,end=78):
    o=base('Rect',n,x,y,start,end); o['rect']=dict(size=[w,h],fillColor=col(c),roundness=r); return o
def text(n,s,x,y,size=40,c=INK,w=900,start=0,end=78,bold=False):
    o=base('Text',n,x,y,start,end)
    o['sourceText']=dict(text=s,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',
        fontSize=size,fillColor=col(c),strokeWidth=0,justification='left',verticalAlign='top',
        boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=size*1.12)
    return o
def path(n,cmd,c=None,stroke=None,width=3,start=0,end=78):
    o=base('Shape',n,start=start,end=end); o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
    if c:o['shape']['fills']=[dict(paint={'type':'solid','color':col(c)},fillRule='nonZeroWinding',blendMode='normal',opacity=100)]
    if stroke:o['shape']['strokes']=[dict(paint={'type':'solid','color':col(stroke)},width=width,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]
    return o
def M(x,y): return dict(type='moveTo',x=x,y=y)
def L(x,y): return dict(type='lineTo',x=x,y=y)
def C(a,b,c,d,x,y): return dict(type='cubicTo',c1x=a,c1y=b,c2x=c,c2y=d,x=x,y=y)
def Z(): return dict(type='close')
def ellipse(n,x,y,rx,ry,c,start=0,end=78):
    k=.55228475
    return path(n,[M(x+rx,y),C(x+rx,y+k*ry,x+k*rx,y+ry,x,y+ry),
                   C(x-k*rx,y+ry,x-rx,y+k*ry,x-rx,y),
                   C(x-rx,y-k*ry,x-k*rx,y-ry,x,y-ry),
                   C(x+k*rx,y-ry,x+rx,y-k*ry,x+rx,y),Z()],c,start=start,end=end)
def group(n,children,x=0,y=0,start=0,end=78):
    o=base('Group',n,x,y,start,end); o['layers']=children[::-1]; return o
def card(n,x,y,w,h,c='#FFFFFF',r=26,start=0,end=78):
    o=rect(n,x,y,w,h,c,r,start,end)
    o['dropShadow']=dict(color=[.05,.08,.14,.12],blurRadius=28,spreadRadius=0,offset=[0,14],blendMode='normal')
    return o
def anim(o,prop,expr):
    actions.append(dict(type='setFxPropertyAnimator',compositionId='main',
        property={'layerId':o['id'],'propertyType':prop},
        animator={'type':'jsScript','layerTimeJsCode':expr},dependencies=[]))
def keys(o,prop,values):
    if prop in ['position','scale']:
        for axis,ix in [('X',0),('Y',1)]: keys(o,prop+axis,[(t,v[ix]) for t,v in values])
        return
    typ='vector2' if isinstance(values[0][1],list) else 'float'
    actions.append(dict(type='setFxPropertyKeyframes',compositionId='main',
        property={'layerId':o['id'],'propertyType':prop},
        keyframes=[dict(id=f'{o["id"]}-{prop}-{i}',layerTime=int(t*1000),
            value={'type':typ,'value':v},
            easing={'type':'cubicBezier','x1':.22,'y1':1,'x2':.36,'y2':1})
            for i,(t,v) in enumerate(values)]))
def enter(o,delay=0):
    anim(o,'opacity',f'return Math.min(100,Math.max(0,(input.time.seconds-{delay})*400));')
def reveal(o,delay=0,dy=34):
    x,y=o['transform']['position']; keys(o,'position',[(0,[x,y+dy]),(.55,[x,y])]); enter(o,delay)
def scene(n,children,start,end):
    g=group(n,children,start=start,end=end); layers.append(g); return g
def title(a,b,st,en):
    g=group('Headline',[text('Lead',a,80,182,68,INK,w=900,bold=True),text('Emphasis',b,80,266,62,BLUE,w=900,bold=True)],start=st,end=en)
    reveal(g,0,18); layers.append(g)
def chip(label,x,y,w=250,c=SOFT,tc=BLUE,start=0,end=78):
    return group(label,[rect('Chip',0,0,w,54,c,12,start=start,end=end),text('Chip text',label,18,12,23,tc,w=w-28,start=start,end=end,bold=True)],x,y,start=start,end=end)
def connector(x1,y1,x2,y2,c='#B9C2D3',width=4,start=0,end=78):
    return path('Connector',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=c,width=width,start=start,end=end)
def packet(x,y,label='TASK',c=BLUE,start=0,end=78):
    return group('Packet',[rect('Packet body',-72,-24,144,48,c,24,start=start,end=end),text('Packet label',label,-48,-15,18,'#FFFFFF',w=110,start=start,end=end,bold=True)],x,y,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# S01 Giant prompt.
title('One giant prompt','creates too many guesses.',0,8)
prompt=[]
prompt.append(card('Prompt shell',0,0,820,525,'#FFFFFF',28))
prompt.append(text('Prompt label','PROMPT',32,28,20,MUT,w=180,bold=True))
prompt.append(text('Prompt body',
    'Build the entire app. Add auth, payments, dashboards,\n'
    'roles, emails, reports and deployment.\n'
    'Make it production-ready and do not break anything.',
    32,80,34,INK,w=750))
prompt.append(chip('Run it',615,420,165,BLUE,'#FFFFFF'))
gprompt=group('Giant prompt',prompt,130,520,start=0,end=8)
keys(gprompt,'scale',[(0,[86,86]),(.7,[100,100]),(4,[100,100]),(6.2,[110,110])])
keys(gprompt,'position',[(0,[130,575]),(.7,[130,520]),(4,[130,520]),(6.2,[95,495])])
layers.append(gprompt)
for i,(label,x,y,w,bg,tc) in enumerate([
 ('SCOPE?',90,1050,180,RED,REDINK),('EXISTING CODE?',300,1110,250,AMBER,AMBERINK),
 ('EDGE CASES?',595,1050,220,RED,REDINK),('WHAT IS DONE?',755,1140,235,AMBER,AMBERINK),
 ('CONSTRAINTS?',120,1200,225,SOFT,BLUE),('SUCCESS?',420,1240,190,SOFT,BLUE)
]):
    t=chip(label,x,y,w,bg,tc,start=2.2,end=8); enter(t,.18+i*.09); layers.append(t)

# S02 Hidden assumptions as a cloud around the request.
title('The problem is','hidden assumptions.',8,18)
a=[]
center=group('Prompt fragment',[card('Prompt fragment',0,0,570,180,'#FFFFFF',22),text('Fragment label','“Build the app”',31,31,41,INK,w=500,bold=True),text('Fragment note','What exactly should the agent assume?',31,96,26,MUT,w=500)],255,580); reveal(center,.1); a.append(center)
tags=[
 ('SCOPE',110,520,220,SOFT,BLUE),('CONSTRAINTS',745,520,230,AMBER,AMBERINK),
 ('CURRENT CODE',85,820,260,SOFT,BLUE),('EDGE CASES',735,820,230,RED,REDINK),
 ('SUCCESS',160,1050,200,SOFT,BLUE),('OWNERSHIP',700,1050,220,AMBER,AMBERINK)
]
for i,(label,x,y,w,bg,tc) in enumerate(tags):
    t=chip(label,x,y,w,bg,tc,start=8,end=18); reveal(t,.35+i*.18,22); a.append(t)
a.append(connector(540,760,220,820,'#CBD2DF',3,start=8,end=18))
a.append(connector(540,760,860,820,'#CBD2DF',3,start=8,end=18))
scene('S02 Assumptions',a,8,18)

# S03 One goal.
title('Start with','one clear goal.',18,28)
a=[]
goal=group('Goal card',[card('Goal',0,0,820,290,'#FFFFFF',26),chip('1  GOAL',30,25,190,SOFT,BLUE,start=18,end=28),text('Question','What are we changing?',30,103,43,INK,w=740,bold=True),text('Answer','Add participant email editing without breaking login.',30,174,31,MUT,w=740)],130,560)
reveal(goal,.1); a.append(goal)
before=group('Before state',[card('Before',0,0,360,185,RED,20),text('Before label','BEFORE',24,22,20,REDINK,w=140,bold=True),text('Before copy','Admin cannot correct\na mistyped email.',24,66,28,INK,w=310)],130,930); reveal(before,1); a.append(before)
after=group('After state',[card('After',0,0,360,185,GREEN,20),text('After label','AFTER',24,22,20,GREENINK,w=140,bold=True),text('After copy','Admin edits once.\nLogin + email stay aligned.',24,66,28,INK,w=310)],590,930); reveal(after,1.4); a.append(after)
a.append(connector(490,1023,590,1023,BLUE,5,start=18,end=28))
scene('S03 Goal',a,18,28)

# S04 Constraints + inspect current state.
title('Protect what works,','then inspect.',28,38)
a=[]
constraints=group('Constraints',[card('Constraints card',0,0,370,345,'#FFFFFF',22),chip('2  CONSTRAINTS',25,24,250,AMBER,AMBERINK,start=28,end=38),text('Keep heading','MUST STAY INTACT',25,105,20,MUT,w=300,bold=True),text('Keep list','• existing login\n• participant ID\n• current permissions\n• audit trail',25,151,28,INK,w=315)],95,550); reveal(constraints,.2); a.append(constraints)
repo=group('Repo inspect',[card('Repo card',0,0,470,450,DARK,22),chip('3  INSPECT',25,24,190,'#2B3850','#DCE3F3',start=28,end=38),text('Repo title','CURRENT STATE',25,104,20,'#AAB6CE',w=300,bold=True),text('Tree','src/\n  auth/\n    login.ts\n  participants/\n    edit-email.ts\n  mail/\n    send.ts\n  db/\n    users.sql',25,149,27,'#FFFFFF',w=380)],515,500); reveal(repo,.6); a.append(repo)
cursor=rect('Inspect highlight',542,677,390,42,'#44506B',8,start=28,end=38)
keys(cursor,'position',[(0,[542,677]),(2,[542,677]),(3.2,[542,726]),(4.5,[542,775]),(6,[542,824])]); a.append(cursor)
scene('S04 Constraints inspect',a,28,38)

# S05 One small task.
title('Now give it','one small task.',38,48)
a=[]
backlog=group('Backlog',[card('Backlog card',0,0,890,520,'#FFFFFF',24),text('Backlog heading','Instead of “finish the product”',30,28,36,INK,w=820,bold=True)],95,525)
for i,(label,state) in enumerate([
 ('Fix participant email edit','ACTIVE'),('Rebuild settings page','LATER'),('Add analytics','LATER'),('Change auth provider','LATER')
]):
    y=98+i*92
    bg=SOFT if i==0 else '#F3F4F6'
    tc=BLUE if i==0 else MUT
    backlog['layers'].append(group('Task '+str(i),[rect('Task row',0,0,830,72,bg,14),text('Task text',label,22,19,27,INK,w=620,bold=i==0),chip(state,650,10,150,SOFT if i==0 else '#ECEEF2',tc,start=38,end=48)],30,y))
reveal(backlog,.2); a.append(backlog)
focus=group('Focus card',[card('Focus',0,0,680,165,DARK,22),text('Focus label','CURRENT TASK',25,20,20,'#AAB6CE',w=240,bold=True),text('Focus copy','Edit one participant email safely.',25,66,34,'#FFFFFF',w=610,bold=True)],200,1100); reveal(focus,2); a.append(focus)
scene('S05 Small task',a,38,48)

# S06 Acceptance criteria checklist.
title('Define what','done looks like.',48,58)
a=[]
criteria=group('Criteria card',[card('Criteria',0,0,850,560,'#FFFFFF',24),chip('5  ACCEPTANCE CRITERIA',28,25,390,SOFT,BLUE,start=48,end=58),text('Criteria heading','The edit is complete when:',28,110,37,INK,w=760,bold=True)],115,520)
items=[
 'Admin can edit the email',
 'New email updates the login identity',
 'Old email stops authenticating',
 'Mail sends to the corrected address',
 'Change is recorded in the audit log'
]
for i,item in enumerate(items):
    y=176+i*70
    criteria['layers'].append(group('Check '+str(i),[
        rect('Check box',0,0,38,38,GREEN,9),
        text('Tick','✓',10,3,25,GREENINK,w=25,bold=True),
        text('Criterion',item,58,4,27,INK,w=690)
    ],28,y))
reveal(criteria,.2); a.append(criteria)
scene('S06 Criteria',a,48,58)

# S07 Tests flip from pending to passed.
title('Make testing','part of the task.',58,68)
a=[]
terminal=group('Test terminal',[card('Terminal',0,0,870,520,DARK,24),text('Terminal title','TEST RUN',30,28,21,'#AAB6CE',w=240,bold=True)],105,525)
test_labels=['email edit updates DB','login accepts corrected email','old email is rejected','mail uses corrected address','audit event is created']
for i,label in enumerate(test_labels):
    y=95+i*72
    row=group('Test '+str(i),[ellipse('Dot',19,19,10,10,'#7B879B'),text('Test label',label,48,3,27,'#FFFFFF',w=680),text('Pending','pending',690,4,24,'#AAB6CE',w=120)],32,y)
    terminal['layers'].append(row)
reveal(terminal,.2); a.append(terminal)
for i,y in enumerate([620,692,764,836,908]):
    passchip=chip('PASS',805,y,115,GREEN,GREENINK,start=58,end=68)
    keys(passchip,'opacity',[(0,0),(2.2+i*.65,0),(2.5+i*.65,100)]); a.append(passchip)
summary=group('Verified summary',[card('Verified',0,0,500,130,GREEN,20),text('Verified label','TASK VERIFIED',25,22,20,GREENINK,w=240,bold=True),text('Verified copy','5 / 5 checks passed',25,61,31,INK,w=430,bold=True)],290,1100); keys(summary,'opacity',[(0,0),(6.4,0),(6.8,100)]); a.append(summary)
scene('S07 Tests',a,58,68)

# S08 Clean loop.
title('Give structure.','Reduce guessing.',68,78)
a=[]
steps=[('GOAL',185,560),('CONSTRAINTS',590,560),('INSPECT',755,805),('TASK',590,1045),('CRITERIA',185,1045),('TEST',20,805)]
centers=[]
for i,(label,x,y) in enumerate(steps):
    w=305
    item=group('Loop '+label,[card('Loop card',0,0,w,115,'#FFFFFF',20),group('Num',[rect('Num bg',0,0,42,42,BLUE,10),text('N',str(i+1),13,7,20,'#FFFFFF',w=25,bold=True)],20,20),text('Loop label',label,78,29,24,INK,w=190,bold=True)],x,y)
    reveal(item,.15+i*.14,18); a.append(item); centers.append((x+w/2,y+57))
for i in range(len(centers)):
    x1,y1=centers[i]; x2,y2=centers[(i+1)%len(centers)]
    a.append(connector(x1,y1,x2,y2,BLUE,4,start=68,end=78))
center=group('Loop center',[card('Center',0,0,360,170,DARK,22),text('Center label','LESS ROOM\nTO GUESS',50,36,36,'#FFFFFF',w=280,bold=True)],360,770); reveal(center,1); a.append(center)
scene('S08 Loop',a,68,78)

# Presenter.
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
    ids.add(o['id']); o['activeRange']={'start':0,'duration':78000}
    for ch in o.get('layers',[]): extend(ch)
extend(presenter)
presenter['transform']['position']=[36,1290]; presenter['transform']['scale']=[92,92]
layers.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[36,1620]),(.7,[36,1290])])
keys(arm,'rotation',[(0,18),(.9,-8),(5,-21),(9,-9),(14,-18),(19,-8),(24,-20),(29,-8),(34,-18),(39,-7),(44,-17),(49,-8),(54,-18),(59,-8),(64,-21),(69,-8),(74,-17)])
notes=[
 (0,8,'TOO MUCH AT ONCE','The agent has to\nfill in the blanks.'),
 (8,18,'ASSUMPTIONS','Ambiguity hides\ninside the request.'),
 (18,28,'1. GOAL','Define the outcome\nbefore the code.'),
 (28,38,'2–3. PROTECT + INSPECT','Keep working parts safe\nand read the repo first.'),
 (38,48,'4. SMALL TASK','Shrink the surface\nof the change.'),
 (48,58,'5. CRITERIA','Describe the exact\nfinished behavior.'),
 (58,68,'6. TEST','Verification is part\nof the task.'),
 (68,78,'REPEAT THE LOOP','Structure gives the\nagent less room to guess.')
]
for st,en,label,body in notes:
    g=group('Presenter note',[text('Stage',label,640,1380,22,BLUE,w=345,bold=True),text('Body',body,640,1428,31,INK,w=345)],start=st,end=en); enter(g); layers.append(g)

doc['composition']={'id':'main','name':'V06 Structured Prompt / full visual draft','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V06 full visual layers',uid,'animation actions',len(actions))
