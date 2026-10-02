import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=18

layers=[]; actions=[]; uid=800
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
GREEN='#E9F7EF'; GREENINK='#167749'; AMBER='#FFF4DC'; AMBERINK='#956515'
RED='#FDEBEC'; REDINK='#B33A42'; BORDER='#E5E8EE'; DARK='#1C2738'

def col(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def trans(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def base(t,n,x=0,y=0,start=0,end=18):
    global uid; uid+=1
    return dict(type=t,id=uid,name=n,blendMode='normal',
                activeRange={'start':int(start*1000),'duration':int((end-start)*1000)},
                transform=trans(x,y))
def rect(n,x,y,w,h,c,r=0,start=0,end=18):
    o=base('Rect',n,x,y,start,end); o['rect']=dict(size=[w,h],fillColor=col(c),roundness=r); return o
def text(n,s,x,y,size=40,c=INK,w=900,start=0,end=18,bold=False):
    o=base('Text',n,x,y,start,end)
    o['sourceText']=dict(text=s,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',
        fontSize=size,fillColor=col(c),strokeWidth=0,justification='left',verticalAlign='top',
        boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=size*1.12)
    return o
def path(n,cmd,c=None,stroke=None,width=3,start=0,end=18):
    o=base('Shape',n,start=start,end=end); o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
    if c:o['shape']['fills']=[dict(paint={'type':'solid','color':col(c)},fillRule='nonZeroWinding',blendMode='normal',opacity=100)]
    if stroke:o['shape']['strokes']=[dict(paint={'type':'solid','color':col(stroke)},width=width,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]
    return o
def M(x,y): return dict(type='moveTo',x=x,y=y)
def L(x,y): return dict(type='lineTo',x=x,y=y)
def C(a,b,c,d,x,y): return dict(type='cubicTo',c1x=a,c1y=b,c2x=c,c2y=d,x=x,y=y)
def Z(): return dict(type='close')
def ellipse(n,x,y,rx,ry,c,start=0,end=18):
    k=.55228475
    return path(n,[M(x+rx,y),C(x+rx,y+k*ry,x+k*rx,y+ry,x,y+ry),
                   C(x-k*rx,y+ry,x-rx,y+k*ry,x-rx,y),
                   C(x-rx,y-k*ry,x-k*rx,y-ry,x,y-ry),
                   C(x+k*rx,y-ry,x+rx,y-k*ry,x+rx,y),Z()],c,start=start,end=end)
def group(n,children,x=0,y=0,start=0,end=18):
    o=base('Group',n,x,y,start,end); o['layers']=children[::-1]; return o
def card(n,x,y,w,h,c='#FFFFFF',r=26,start=0,end=18):
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
def chip(label,x,y,w=250,c=SOFT,tc=BLUE,start=0,end=18):
    return group(label,[rect('Chip',0,0,w,54,c,12,start=start,end=end),text('Chip text',label,18,12,23,tc,w=w-28,start=start,end=end,bold=True)],x,y,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# Scene 1: autonomy scale.
h1=group('Headline',[
    text('Lead','More autonomy',80,182,68,INK,w=900,bold=True),
    text('Emphasis','needs the right guardrails.',80,266,62,BLUE,w=900,bold=True)
],start=0,end=8); reveal(h1,0,18); layers.append(h1)

scale=group('Autonomy scale',[
    rect('Scale track',0,0,850,18,'#D8DDE8',9),
    rect('Safe zone',0,0,330,18,'#BFE8CD',9),
    rect('Review zone',330,0,280,18,'#F4D98C',0),
    rect('Sensitive zone',610,0,240,18,'#F3B8BD',9),
    text('Safe label','REVERSIBLE / EASY TO REVIEW',0,-55,20,GREENINK,w=320,bold=True),
    text('Sensitive label','SENSITIVE / HARD TO UNDO',590,-55,20,REDINK,w=280,bold=True)
],115,695); reveal(scale,.1); layers.append(scale)

tasks=[
 ('Draft UI',120,560,210,GREEN,GREENINK),
 ('Write tests',250,820,210,GREEN,GREENINK),
 ('Refactor',365,575,190,GREEN,GREENINK),
 ('Shared API',520,825,210,AMBER,AMBERINK),
 ('Auth',645,570,165,AMBER,AMBERINK),
 ('Permissions',705,845,210,AMBER,AMBERINK),
 ('Delete data',820,585,190,RED,REDINK),
 ('Deploy prod',825,970,190,RED,REDINK)
]
for i,(label,x,y,w,bg,tc) in enumerate(tasks):
    t=chip(label,x,y,w,bg,tc,start=0,end=8)
    keys(t,'position',[(0,[540,615]),(.65+i*.12,[x,y])]); enter(t,.08+i*.07)
    layers.append(t)

# Small marker labels under the scale.
layers.append(text('Left rule','More autonomy',115,755,24,GREENINK,w=230,bold=True,start=0,end=8))
layers.append(text('Right rule','More human review',760,755,24,REDINK,w=260,bold=True,start=0,end=8))

# Scene 2: approval gate stops a sensitive action.
h2=group('Gate headline',[
    text('Lead','Sensitive actions',80,182,68,INK,w=900,bold=True),
    text('Emphasis','stop at an approval gate.',80,266,62,BLUE,w=900,bold=True)
],start=8,end=18); reveal(h2,0,18); layers.append(h2)

migration=group('Migration card',[
    card('Migration',0,0,365,250,RED,22),
    text('Migration label','DATABASE CHANGE',26,24,20,REDINK,w=260,bold=True),
    text('Migration title','DROP old_orders',26,72,35,INK,w=315,bold=True),
    text('Migration note','Destructive migration\nremoves 18k rows.',26,132,27,MUT,w=315)
],90,615,start=8,end=18); reveal(migration,.1); layers.append(migration)

# Gate.
gate=group('Human approval gate',[
    rect('Gate bar left',0,0,24,300,DARK,8),
    rect('Gate bar right',126,0,24,300,DARK,8),
    rect('Gate top',0,0,150,24,DARK,8),
    rect('Lock body',46,120,60,54,AMBER,12),
    path('Lock loop',[M(58,120),C(58,82,94,82,94,120)],stroke=AMBERINK,width=7,start=8,end=18)
],470,575,start=8,end=18); reveal(gate,.5,12); layers.append(gate)

packet=chip('EXECUTE',355,718,150,RED,REDINK,start=8,end=18)
keys(packet,'position',[(0,[355,718]),(2,[355,718]),(3.4,[430,718]),(7.4,[430,718]),(8.6,[610,718])])
layers.append(packet)

diff=group('Diff panel',[
    card('Diff',0,0,350,250,'#FFFFFF',22),
    text('Diff label','CHANGE PREVIEW',24,22,20,MUT,w=230,bold=True),
    text('Diff body','- drop table old_orders\n- remove legacy index\n- delete archived rows',24,72,26,INK,w=300),
    chip('18,204 rows affected',24,180,250,RED,REDINK,start=8,end=18)
],630,545,start=8,end=18)
keys(diff,'opacity',[(0,0),(3.2,0),(3.6,100)]); layers.append(diff)

approve=group('Approval card',[
    card('Approval',0,0,350,220,DARK,22),
    text('Approval label','HUMAN APPROVAL',24,22,20,'#AAB6CE',w=250,bold=True),
    text('Approval title','Review impact',24,69,34,'#FFFFFF',w=300,bold=True),
    chip('APPROVE',24,138,145,GREEN,GREENINK,start=8,end=18),
    chip('HOLD',185,138,120,'#2B3850','#DCE3F3',start=8,end=18)
],630,835,start=8,end=18)
keys(approve,'opacity',[(0,0),(4.8,0),(5.2,100)]); layers.append(approve)

unlock=chip('APPROVED',635,1080,180,GREEN,GREENINK,start=8,end=18)
keys(unlock,'opacity',[(0,0),(7.4,0),(7.8,100)]); layers.append(unlock)

# Presenter.
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
    ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
    for ch in o.get('layers',[]): extend(ch)
extend(presenter)
presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]
layers.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])])
keys(arm,'rotation',[(0,18),(.9,-8),(4,-18),(7,-5),(9,-20),(13,-8),(17,-16)])

n1=group('Presenter note one',[
    text('Stage','AUTONOMY SCALE',650,1380,22,BLUE,w=340,bold=True),
    text('Body','Give more freedom\nwhere work is reversible.',650,1428,31,INK,w=340)
],start=0,end=8); enter(n1); layers.append(n1)
n2=group('Presenter note two',[
    text('Stage','APPROVAL GATE',650,1380,22,BLUE,w=340,bold=True),
    text('Body','Sensitive actions\nwait for a human.',650,1428,31,INK,w=340)
],start=8,end=18); enter(n2); layers.append(n2)

doc['composition']={'id':'main','name':'V07 Autonomy / opening prototype','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V07 prototype layers',uid,'animation actions',len(actions))
