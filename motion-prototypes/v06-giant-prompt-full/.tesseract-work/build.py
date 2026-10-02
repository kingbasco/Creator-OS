import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=78

layers=[]; actions=[]; uid=700
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
BORDER='#E5E8EE'; DARK='#1C2738'; RED='#FDEBEC'; REDINK='#B33A42'
GREEN='#E9F7EF'; GREENINK='#167749'; AMBER='#FFF4DC'; AMBERINK='#956515'
CODE='#111827'; CODEMUT='#AAB6CE'

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
        boxText=True,boxPosition=[0,0],boxSize=[w,400],leading=size*1.12)
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
def reveal(o,delay=0,dy=30):
    x,y=o['transform']['position']; keys(o,'position',[(0,[x,y+dy]),(.55,[x,y])]); enter(o,delay)
def scene(n,children,start,end):
    g=group(n,children,start=start,end=end); layers.append(g); return g
def title(a,b,st,en):
    g=group('Headline',[text('Lead',a,80,184,68,INK,w=900,bold=True),
        text('Emphasis',b,80,270,61,BLUE,w=900,bold=True)],start=st,end=en)
    reveal(g,0,18); layers.append(g)
def chip(label,x,y,w=260,c=SOFT,tc=BLUE,start=0,end=78):
    return group(label,[rect('Chip',0,0,w,54,c,12,start=start,end=end),
        text('Chip text',label,18,12,23,tc,w=w-26,start=start,end=end,bold=True)],x,y,start=start,end=end)
def connector(x1,y1,x2,y2,c='#B9C2D3',width=4,start=0,end=78):
    return path('Connector',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=c,width=width,start=start,end=end)
def packet(x,y,label='TASK',c=BLUE,start=0,end=78):
    return group('Packet',[rect('Body',-72,-24,144,48,c,24,start=start,end=end),
        text('Label',label,-48,-14,18,'#FFFFFF',w=110,start=start,end=end,bold=True)],x,y,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# S01 — giant prompt overload.
title('One giant prompt','creates too many guesses.',0,8)
prompt=[]
prompt.append(card('Prompt shell',0,0,820,540,'#FFFFFF',28))
prompt.append(text('Prompt label','PROMPT',34,30,21,MUT,w=200,bold=True))
prompt.append(text('Prompt body','Build the whole app.\nAdd auth, payments, dashboards,\nroles, emails, reports and deployment.\nMake it production-ready.',34,82,34,INK,w=750,bold=True))
prompt.append(rect('Send button',590,446,190,60,BLUE,14))
prompt.append(text('Send text','Run it',654,462,25,'#FFFFFF',w=100,bold=True))
big=group('Giant prompt card',prompt,130,510,start=0,end=8)
keys(big,'scale',[(0,[88,88]),(.8,[100,100]),(3.6,[100,100]),(5.8,[113,113])])
keys(big,'position',[(0,[130,550]),(.8,[130,510]),(3.6,[130,510]),(5.8,[75,475])]); layers.append(big)
for i,(label,x,y,w,bg,tc) in enumerate([
    ('SCOPE?',95,1090,230,RED,REDINK),('CONSTRAINTS?',720,1040,255,AMBER,AMBERINK),
    ('EXISTING CODE?',80,820,290,SOFT,BLUE),('EDGE CASES?',730,760,250,RED,REDINK),
    ('WHAT IS DONE?',390,1160,300,AMBER,AMBERINK)]):
    g=chip(label,x,y,w,bg,tc,start=2.1,end=8); reveal(g,.25+i*.15,18); layers.append(g)

# S02 — hidden assumptions become a tangled dependency map.
title('The real problem is','hidden assumptions.',8,18)
a=[]
center=group('Unclear task',[card('Task card',0,0,390,150,DARK,22),text('Task label','GIANT TASK',28,27,21,'#AAB6CE',w=250,bold=True),text('Task text','“Build the app”',28,69,37,'#FFFFFF',w=320,bold=True)],345,580); reveal(center,.2); a.append(center)
assumptions=[
 ('Scope',100,805,SOFT,BLUE),('Constraints',700,805,AMBER,AMBERINK),
 ('Existing code',95,1025,SOFT,BLUE),('Edge cases',705,1025,RED,REDINK),
 ('Success',390,1135,GREEN,GREENINK)]
for i,(label,x,y,bg,tc) in enumerate(assumptions):
    a.append(connector(540,730,x+125,y,tc,4))
    g=chip(label,x,y,250,bg,tc); reveal(g,.5+i*.25); a.append(g)
scene('S02 Assumptions',a,8,18)

# S03 — clear goal.
title('Start with','one clear goal.',18,28)
a=[]
before=group('Before prompt',[card('Before',0,0,770,165,'#FFFFFF',20),text('Before label','VAGUE',28,23,20,REDINK,w=180,bold=True),text('Before text','“Improve the dashboard.”',28,66,35,INK,w=680,bold=True)],155,555); reveal(before,.2); a.append(before)
after=group('After goal',[card('After',0,0,770,240,SOFT,22),text('After label','GOAL',28,25,20,BLUE,w=180,bold=True),text('After text','Add monthly revenue to the dashboard.',28,68,35,INK,w=690,bold=True),chip('DONE = chart shows last 12 months',28,155,520,GREEN,GREENINK)],155,805); reveal(after,1.1); a.append(after)
arrow=path('Transform arrow',[M(540,728),C(540,754,540,765,540,795)],stroke=BLUE,width=6); a.append(arrow)
scene('S03 Goal',a,18,28)

# S04 — constraints plus repository inspection.
title('Protect what works,','then inspect first.',28,38)
a=[]
constraints=group('Constraints panel',[card('Panel',0,0,385,385,SOFT,22),text('Label','CONSTRAINTS',28,25,20,BLUE,w=260,bold=True),
    chip('Keep existing auth',28,82,300,'#FFFFFF',INK),
    chip('No schema changes',28,153,300,'#FFFFFF',INK),
    chip('Mobile stays intact',28,224,300,'#FFFFFF',INK),
    chip('Use current API',28,295,300,'#FFFFFF',INK)],90,575); reveal(constraints,.2); a.append(constraints)
repo=[]
repo.append(card('Repo',0,0,475,510,DARK,22))
repo.append(text('Repo label','CURRENT REPO',28,24,20,'#AAB6CE',w=250,bold=True))
repo.append(text('Repo title','Inspect before edit',28,66,34,'#FFFFFF',w=380,bold=True))
for i,(name,indent,tc) in enumerate([
 ('src/',0,'#FFFFFF'),('components/',1,'#DDE4F1'),('Dashboard.tsx',2,'#FFFFFF'),
 ('lib/',1,'#DDE4F1'),('auth.ts',2,'#FFFFFF'),('api.ts',2,'#FFFFFF'),('schema.sql',0,'#DDE4F1')]):
    repo.append(text('Tree '+name,name,31+indent*28,135+i*45,23,tc,w=360,bold=(indent==0)))
inspect=group('Repository inspection',repo,520,535); reveal(inspect,.8); a.append(inspect)
cursor=rect('Scan highlight',548,746,390,44,'#2B3850',8)
keys(cursor,'position',[(0,[548,746]),(2,[548,746]),(4,[548,836]),(6,[548,881])]); a.append(cursor)
scene('S04 Constraints inspect',a,28,38)

# S05 — shrink to one focused task.
title('Give it','one small task.',38,48)
a=[]
backlog=group('Large backlog',[card('Backlog',0,0,820,140,'#FFFFFF',22),text('Backlog label','WHOLE PRODUCT',28,23,20,MUT,w=250,bold=True),
    text('Backlog body','Auth  •  Billing  •  Reports  •  Emails  •  Dashboard  •  Roles',28,67,27,INK,w=760,bold=True)],130,545); reveal(backlog,.2); a.append(backlog)
focus=group('Focused task',[card('Focus',0,0,610,225,SOFT,22),text('Focus label','SMALL TASK',28,24,20,BLUE,w=220,bold=True),
    text('Focus body','Add monthly revenue\nto the dashboard.',28,72,39,INK,w=520,bold=True),chip('1 file area · 1 behavior',28,160,325,GREEN,GREENINK)],235,795); reveal(focus,1.1); a.append(focus)
for i,label in enumerate(['Auth','Billing','Reports','Emails','Roles']):
    ghost=chip(label,120+i*170,1090,145,'#F1F3F6',MUT); keys(ghost,'opacity',[(0,100),(3,100),(4.5,22)]); a.append(ghost)
scene('S05 Small task',a,38,48)

# S06 — acceptance criteria.
title('Define','what done means.',48,58)
a=[]
criteria=group('Acceptance criteria',[card('Criteria panel',0,0,850,560,'#FFFFFF',24),text('Criteria label','ACCEPTANCE CRITERIA',32,28,21,BLUE,w=500,bold=True),
    text('Criteria title','Monthly revenue chart',32,72,39,INK,w=700,bold=True)],115,545); reveal(criteria,.2); a.append(criteria)
items=[
 'Shows the last 12 months',
 'Uses the existing revenue API',
 'Handles an empty month as zero',
 'Keeps the mobile layout intact'
]
for i,item in enumerate(items):
    y=690+i*95
    box=group('Criterion '+str(i),[rect('Check box',0,0,52,52,'#FFFFFF',12),text('Check', '✓',13,5,31,GREENINK,w=30,bold=True),
        text('Criterion',item,78,8,27,INK,w=680,bold=True)],150,y)
    reveal(box,.7+i*.45,15); a.append(box)
scene('S06 Acceptance',a,48,58)

# S07 — tests run before "done".
title('Do not stop at code.','Test the result.',58,68)
a=[]
runner=group('Test runner',[card('Runner',0,0,850,525,DARK,24),text('Runner label','TEST RUN',32,26,20,'#AAB6CE',w=240,bold=True),
    text('Runner title','dashboard-revenue.spec',32,70,36,'#FFFFFF',w=700,bold=True)],115,540); reveal(runner,.2); a.append(runner)
tests=[
 ('renders 12 months',685),('handles empty month',775),('uses current API',865),('mobile layout unchanged',955)
]
for i,(label,y) in enumerate(tests):
    a.append(text('Test name',label,170,y,28,'#FFFFFF',w=570,bold=True))
    badge=chip('PENDING',730,y-7,190,AMBER,AMBERINK)
    keys(badge,'opacity',[(0,100),(3.0+i*.6,100),(3.25+i*.6,0)])
    a.append(badge)
    passed=chip('PASSED',730,y-7,190,GREEN,GREENINK)
    keys(passed,'opacity',[(0,0),(3.0+i*.6,0),(3.25+i*.6,100)])
    a.append(passed)
summary=chip('4 / 4 VERIFIED',380,1085,320,GREEN,GREENINK)
keys(summary,'opacity',[(0,0),(6.2,0),(6.7,100)]); a.append(summary)
scene('S07 Test',a,58,68)

# S08 — clean reusable loop.
title('Give structure.','Reduce guessing.',68,78)
a=[]
loop_steps=[
 ('GOAL',540,555),('CONSTRAINTS',765,690),('INSPECT',765,945),
 ('SMALL TASK',540,1080),('CRITERIA',315,945),('TEST',315,690)
]
for i,(label,x,y) in enumerate(loop_steps):
    g=group('Loop '+label,[ellipse('Node',0,0,88,88,SOFT),text('Node label',label,-70,-13,25,BLUE,w=145,bold=True)],x,y)
    reveal(g,.2+i*.2,15); a.append(g)
# ring connectors
pairs=[(540,643,765,690),(853,778,853,945),(765,1033,540,1080),(452,1080,315,1033),(227,945,227,778),(315,690,452,643)]
for x1,y1,x2,y2 in pairs: a.append(connector(x1,y1,x2,y2,BLUE,5))
center=group('Loop center',[card('Center',0,0,320,180,DARK,22),text('Center title','LESS ROOM\nTO GUESS',46,39,39,'#FFFFFF',w=250,bold=True)],380,790); reveal(center,2); a.append(center)
scene('S08 Loop',a,68,78)

# Presenter.
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
    ids.add(o['id']); o['activeRange']={'start':0,'duration':78000}
    for ch in o.get('layers',[]): extend(ch)
extend(presenter)
presenter['transform']['position']=[30,1285]; layers.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[30,1630]),(.7,[30,1285])])
keys(arm,'rotation',[(0,18),(.9,-10),(6,-21),(9,-8),(15,-17),(19,-7),(25,-19),(29,-7),(35,-18),(39,-8),(45,-18),(49,-7),(55,-20),(59,-8),(65,-19),(69,-7),(75,-18)])
notes=[
(0,8,'TOO MUCH AT ONCE','The agent has to\nfill in the blanks.'),
(8,18,'HIDDEN ASSUMPTIONS','Ambiguity compounds\nacross the task.'),
(18,28,'1 · GOAL','Define the exact\noutcome first.'),
(28,38,'2 · CONSTRAINTS','Protect what works.\nInspect before editing.'),
(38,48,'3 · SMALL TASK','Shrink the change\nsurface.'),
(48,58,'4 · CRITERIA','Make done\nmeasurable.'),
(58,68,'5 · TEST','Verification is part\nof the task.'),
(68,78,'REPEAT THE LOOP','Clear structure gives\nless room to guess.')
]
for st,en,label,body in notes:
    g=group('Presenter note',[text('Stage',label,640,1372,22,BLUE,w=340,bold=True),text('Body',body,640,1420,31,INK,w=340)],start=st,end=en); enter(g); layers.append(g)

doc['composition']={'id':'main','name':'V06 Giant Prompt / full visual draft','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V06 full visual layers',uid,'animation actions',len(actions))
