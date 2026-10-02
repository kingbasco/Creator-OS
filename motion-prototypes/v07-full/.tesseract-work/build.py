import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=80

layers=[]; actions=[]; uid=900
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
GREEN='#E9F7EF'; GREENINK='#167749'; AMBER='#FFF4DC'; AMBERINK='#956515'
RED='#FDEBEC'; REDINK='#B33A42'; BORDER='#E5E8EE'; DARK='#1C2738'

def col(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def trans(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def base(t,n,x=0,y=0,start=0,end=80):
    global uid; uid+=1
    return dict(type=t,id=uid,name=n,blendMode='normal',
                activeRange={'start':int(start*1000),'duration':int((end-start)*1000)},
                transform=trans(x,y))
def rect(n,x,y,w,h,c,r=0,start=0,end=80):
    o=base('Rect',n,x,y,start,end); o['rect']=dict(size=[w,h],fillColor=col(c),roundness=r); return o
def text(n,s,x,y,size=40,c=INK,w=900,start=0,end=80,bold=False):
    o=base('Text',n,x,y,start,end)
    o['sourceText']=dict(text=s,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',
        fontSize=size,fillColor=col(c),strokeWidth=0,justification='left',verticalAlign='top',
        boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=size*1.12)
    return o
def path(n,cmd,c=None,stroke=None,width=3,start=0,end=80):
    o=base('Shape',n,start=start,end=end); o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
    if c:o['shape']['fills']=[dict(paint={'type':'solid','color':col(c)},fillRule='nonZeroWinding',blendMode='normal',opacity=100)]
    if stroke:o['shape']['strokes']=[dict(paint={'type':'solid','color':col(stroke)},width=width,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]
    return o
def M(x,y): return dict(type='moveTo',x=x,y=y)
def L(x,y): return dict(type='lineTo',x=x,y=y)
def C(a,b,c,d,x,y): return dict(type='cubicTo',c1x=a,c1y=b,c2x=c,c2y=d,x=x,y=y)
def Z(): return dict(type='close')
def ellipse(n,x,y,rx,ry,c,start=0,end=80):
    k=.55228475
    return path(n,[M(x+rx,y),C(x+rx,y+k*ry,x+k*rx,y+ry,x,y+ry),
                   C(x-k*rx,y+ry,x-rx,y+k*ry,x-rx,y),
                   C(x-rx,y-k*ry,x-k*rx,y-ry,x,y-ry),
                   C(x+k*rx,y-ry,x+rx,y-k*ry,x+rx,y),Z()],c,start=start,end=end)
def group(n,children,x=0,y=0,start=0,end=80):
    o=base('Group',n,x,y,start,end); o['layers']=children[::-1]; return o
def card(n,x,y,w,h,c='#FFFFFF',r=26,start=0,end=80):
    o=rect(n,x,y,w,h,c,r,start,end)
    o['dropShadow']=dict(color=[.05,.08,.14,.12],blurRadius=26,spreadRadius=0,offset=[0,12],blendMode='normal')
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
def reveal(o,delay=0,dy=32):
    x,y=o['transform']['position']; keys(o,'position',[(0,[x,y+dy]),(.55,[x,y])]); enter(o,delay)
def scene(n,children,start,end):
    g=group(n,children,start=start,end=end); layers.append(g); return g
def title(a,b,st,en):
    g=group('Headline',[text('Lead',a,80,182,68,INK,w=900,bold=True),text('Emphasis',b,80,266,62,BLUE,w=900,bold=True)],start=st,end=en)
    reveal(g,0,18); layers.append(g)
def chip(label,x,y,w=250,c=SOFT,tc=BLUE,start=0,end=80):
    return group(label,[rect('Chip',0,0,w,54,c,12,start=start,end=end),text('Chip text',label,18,12,23,tc,w=w-28,start=start,end=end,bold=True)],x,y,start=start,end=end)
def connector(x1,y1,x2,y2,c='#B9C2D3',width=4,start=0,end=80):
    return path('Connector',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=c,width=width,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# S01 overview scale.
title('More autonomy','needs the right guardrails.',0,8)
a=[]
a.append(group('Scale',[
    rect('Track',0,0,850,18,'#D8DDE8',9),
    rect('Safe zone',0,0,330,18,'#BFE8CD',9),
    rect('Review zone',330,0,280,18,'#F4D98C',0),
    rect('Sensitive zone',610,0,240,18,'#F3B8BD',9),
    text('Left label','REVERSIBLE / EASY TO REVIEW',0,-55,20,GREENINK,w=320,bold=True),
    text('Right label','SENSITIVE / HARD TO UNDO',590,-55,20,REDINK,w=280,bold=True)
],115,690))
for i,(label,x,y,w,bg,tc) in enumerate([
 ('Draft UI',120,545,190,GREEN,GREENINK),('Write tests',245,840,210,GREEN,GREENINK),
 ('Refactor',360,560,180,GREEN,GREENINK),('Shared API',505,840,210,AMBER,AMBERINK),
 ('Auth',650,560,150,AMBER,AMBERINK),('Permissions',690,850,210,AMBER,AMBERINK),
 ('Delete data',820,575,190,RED,REDINK),('Deploy prod',825,980,190,RED,REDINK)
]):
    t=chip(label,x,y,w,bg,tc,start=0,end=8); keys(t,'position',[(0,[540,610]),(.6+i*.12,[x,y])]); enter(t,.05+i*.07); a.append(t)
a.append(text('Autonomy rule','More autonomy',115,755,24,GREENINK,w=240,bold=True))
a.append(text('Review rule','More human review',755,755,24,REDINK,w=270,bold=True))
scene('S01 Scale',a,0,8)

# S02 low-risk tasks.
title('Low-risk work','can move quickly.',8,18)
a=[]
for i,(label,sub,x,y) in enumerate([
 ('Draft component','Easy to inspect',110,555),
 ('Small refactor','Easy to undo',555,555),
 ('Write tests','Adds verification',110,770),
 ('Investigate error','Read-only analysis',555,770)
]):
    item=group('Low risk '+label,[card('Card',0,0,405,165,GREEN,20),text('Task',label,26,26,31,INK,w=345,bold=True),text('Sub',sub,26,83,24,GREENINK,w=340),chip('HIGH AUTONOMY',26,112,220,'#FFFFFF',GREENINK,start=8,end=18)],x,y)
    reveal(item,.2+i*.25); a.append(item)
a.append(group('Reason',[card('Reason card',0,0,850,160,DARK,22),text('Reason label','WHY?',28,22,20,'#AAB6CE',w=120,bold=True),text('Reason copy','Small blast radius · visible diff · easy rollback',28,68,32,'#FFFFFF',w=790,bold=True)],115,1010))
scene('S02 Low risk',a,8,18)

# S03 blast radius.
title('As impact grows,','review gets stronger.',18,28)
a=[]
center=group('Shared system',[card('Center',0,0,360,200,DARK,24),text('Label','SHARED API',32,28,22,'#AAB6CE',w=230,bold=True),text('Title','/participants',32,78,40,'#FFFFFF',w=290,bold=True)],360,615); reveal(center,.2); a.append(center)
for i,(label,x,y,c) in enumerate([
 ('Dashboard',90,540,SOFT),('Attendance',670,540,SOFT),('Assignments',90,860,SOFT),('Email',670,860,SOFT)
]):
    tile=group('Feature '+label,[card('Feature',0,0,320,140,c,20),text('Feature name',label,25,44,30,INK,w=270,bold=True)],x,y); reveal(tile,.5+i*.18); a.append(tile)
    a.append(connector(540,715,x+160,y+70,BLUE,4,start=18,end=28))
a.append(chip('BIGGER BLAST RADIUS',365,1015,350,AMBER,AMBERINK,start=18,end=28))
scene('S03 Blast radius',a,18,28)

# S04 auth and permissions.
title('Access control','deserves closer review.',28,38)
a=[]
auth=group('Auth panel',[card('Auth',0,0,390,420,'#FFFFFF',24),chip('AUTHENTICATION',25,24,245,SOFT,BLUE,start=28,end=38),text('Auth title','Who are you?',25,105,38,INK,w=330,bold=True),text('Auth body','Login provider\nsession creation\npassword reset\nMFA checks',25,172,28,MUT,w=320)],100,555); reveal(auth,.2); a.append(auth)
perm=group('Permissions panel',[card('Perm',0,0,390,420,AMBER,24),chip('PERMISSIONS',25,24,210,'#FFFFFF',AMBERINK,start=28,end=38),text('Perm title','What may you do?',25,105,35,INK,w=330,bold=True),text('Perm body','admin → full access\nstaff → assigned users\nparticipant → self only',25,172,27,INK,w=330)],590,555); reveal(perm,.6); a.append(perm)
a.append(group('Review note',[card('Review',0,0,880,150,DARK,20),text('Review copy','A small mistake here can change who is allowed to do what.',30,47,31,'#FFFFFF',w=820,bold=True)],100,1035))
scene('S04 Access control',a,28,38)

# S05 sensitive actions.
title('Some actions are','expensive or irreversible.',38,48)
a=[]
for i,(label,icon,bg,tc,x,y) in enumerate([
 ('DELETE DATA','DB',RED,REDINK,90,540),('SECRET ACCESS','KEY',RED,REDINK,560,540),
 ('BILLING CHANGE','$',AMBER,AMBERINK,90,785),('DEPLOY PROD','UP',AMBER,AMBERINK,560,785)
]):
    item=group('Sensitive '+label,[card('Card',0,0,410,190,bg,22),group('Icon',[rect('Icon bg',0,0,66,66,'#FFFFFF',15),text('Icon text',icon,15,17,24,tc,w=50,bold=True)],25,24),text('Label',label,112,36,28,INK,w=270,bold=True),chip('APPROVAL GATE',112,102,240,'#FFFFFF',tc,start=38,end=48)],x,y)
    reveal(item,.2+i*.25); a.append(item)
scene('S05 Sensitive actions',a,38,48)

# S06 approval gate.
title('Let the agent prepare.','Keep execution gated.',48,58)
a=[]
change=group('Prepared change',[card('Change',0,0,340,250,RED,22),text('Label','DATABASE CHANGE',25,24,20,REDINK,w=230,bold=True),text('Title','DROP old_orders',25,72,34,INK,w=290,bold=True),text('Body','Prepared, but not\nexecuted yet.',25,137,27,MUT,w=280)],85,590); reveal(change,.1); a.append(change)
gate=group('Gate',[rect('Left',0,0,24,330,DARK,8),rect('Right',126,0,24,330,DARK,8),rect('Top',0,0,150,24,DARK,8),rect('Lock',46,132,60,54,AMBER,12),path('Loop',[M(58,132),C(58,94,94,94,94,132)],stroke=AMBERINK,width=7,start=48,end=58)],465,545); reveal(gate,.4,10); a.append(gate)
diff=group('Diff',[card('Diff card',0,0,370,250,'#FFFFFF',22),text('Diff label','CHANGE PREVIEW',24,22,20,MUT,w=230,bold=True),text('Diff body','- drop table old_orders\n- remove legacy index\n- delete 18,204 rows',24,72,26,INK,w=315),chip('Impact: destructive',24,180,250,RED,REDINK,start=48,end=58)],625,520); keys(diff,'opacity',[(0,0),(2.4,0),(2.8,100)]); a.append(diff)
approval=group('Approval',[card('Approval',0,0,370,230,DARK,22),text('Approval label','HUMAN APPROVAL',24,22,20,'#AAB6CE',w=240,bold=True),text('Approval title','Review impact',24,67,34,'#FFFFFF',w=300,bold=True),chip('APPROVE',24,145,145,GREEN,GREENINK,start=48,end=58),chip('HOLD',190,145,120,'#2B3850','#DCE3F3',start=48,end=58)],625,825); keys(approval,'opacity',[(0,0),(4.2,0),(4.6,100)]); a.append(approval)
approved=chip('APPROVED',425,1080,190,GREEN,GREENINK,start=48,end=58); keys(approved,'opacity',[(0,0),(7.0,0),(7.4,100)]); a.append(approved)
scene('S06 Approval gate',a,48,58)

# S07 three questions.
title('Before execution,','ask three questions.',58,68)
a=[]
questions=[
 ('1','REVERSIBLE?','Can I undo this?',GREEN,GREENINK),
 ('2','BLAST RADIUS?','How much can it affect?',AMBER,AMBERINK),
 ('3','PRIVILEGED?','Does it use elevated access?',RED,REDINK)
]
for i,(num,label,sub,bg,tc) in enumerate(questions):
    item=group('Question '+num,[card('Question card',0,0,840,155,'#FFFFFF',22),group('Num',[rect('Num bg',0,0,54,54,bg,13),text('Num text',num,18,10,24,tc,w=30,bold=True)],26,23),text('Label',label,105,25,31,INK,w=340,bold=True),text('Sub',sub,105,76,27,MUT,w=650)],120,535+i*195)
    reveal(item,.2+i*.45); a.append(item)
a.append(group('Decision',[card('Decision',0,0,840,130,DARK,20),text('Decision text','More “no” answers → stronger human review',30,44,31,'#FFFFFF',w=780,bold=True)],120,1130))
scene('S07 Questions',a,58,68)

# S08 final policy.
title('Fast where reversible.','Gate what matters.',68,80)
a=[]
scale=group('Final scale',[
    rect('Track',0,0,850,20,'#D8DDE8',10),
    rect('Safe zone',0,0,330,20,'#BFE8CD',10),
    rect('Review zone',330,0,280,20,'#F4D98C',0),
    rect('Sensitive zone',610,0,240,20,'#F3B8BD',10),
    text('Left','MORE AUTONOMY',0,-52,20,GREENINK,w=250,bold=True),
    text('Right','MORE REVIEW',650,-52,20,REDINK,w=200,bold=True)
],115,650); reveal(scale,.1); a.append(scale)
for i,(label,x,bg,tc) in enumerate([
 ('Draft',130,GREEN,GREENINK),('Test',280,GREEN,GREENINK),('API',480,AMBER,AMBERINK),
 ('Auth',620,AMBER,AMBERINK),('Secrets',760,RED,REDINK),('Deploy',860,RED,REDINK)
]):
    w=130 if label not in ('Secrets','Deploy') else 145
    t=chip(label,x,560,w,bg,tc,start=68,end=80); reveal(t,.2+i*.16,20); a.append(t)
a.append(group('Rule card',[card('Rule',0,0,850,260,DARK,24),text('Rule label','WORKFLOW POLICY',30,25,20,'#AAB6CE',w=230,bold=True),text('Rule','Autonomy for reversible work.\nApproval gates for sensitive actions.',30,77,39,'#FFFFFF',w=780,bold=True)],115,820))
a.append(chip('BUILD FASTER',155,1115,220,GREEN,GREENINK,start=68,end=80))
a.append(chip('KEEP GUARDRAILS',705,1115,250,RED,REDINK,start=68,end=80))
scene('S08 Final',a,68,80)

# Presenter.
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
    ids.add(o['id']); o['activeRange']={'start':0,'duration':80000}
    for ch in o.get('layers',[]): extend(ch)
extend(presenter)
presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]
layers.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])])
keys(arm,'rotation',[(0,18),(.9,-8),(5,-18),(9,-7),(14,-16),(19,-7),(24,-18),(29,-8),(34,-18),(39,-7),(44,-17),(49,-8),(54,-19),(59,-8),(64,-17),(69,-8),(75,-16)])
notes=[
 (0,8,'AUTONOMY WITH GUARDRAILS','More freedom where\nwork is reversible.'),
 (8,18,'LOW RISK','Easy to review.\nEasy to undo.'),
 (18,28,'BLAST RADIUS','More impact means\nstronger review.'),
 (28,38,'ACCESS CONTROL','Auth and permissions\ndeserve closer review.'),
 (38,48,'SENSITIVE ACTIONS','Some changes are\nexpensive to reverse.'),
 (48,58,'APPROVAL GATE','Prepare the change.\nWait before execution.'),
 (58,68,'THREE QUESTIONS','Reversible? Blast radius?\nPrivileged access?'),
 (68,80,'BALANCED POLICY','Build faster while\nkeeping the right gates.')
]
for st,en,label,body in notes:
    g=group('Presenter note',[text('Stage',label,640,1380,22,BLUE,w=345,bold=True),text('Body',body,640,1428,31,INK,w=345)],start=st,end=en); enter(g); layers.append(g)

doc['composition']={'id':'main','name':'V07 Autonomy / full visual draft','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V07 full visual layers',uid,'animation actions',len(actions))
