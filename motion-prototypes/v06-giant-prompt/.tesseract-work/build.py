import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=18

layers=[]; actions=[]; uid=500
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
BORDER='#E5E8EE'; DARK='#1C2738'; RED='#FDEBEC'; REDINK='#B33A42'
GREEN='#E9F7EF'; GREENINK='#167749'; AMBER='#FFF4DC'; AMBERINK='#956515'

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
        boxText=True,boxPosition=[0,0],boxSize=[w,400],leading=size*1.12)
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
def chip(label,x,y,w=260,c=SOFT,tc=BLUE,start=0,end=18):
    return group(label,[rect('Chip',0,0,w,54,c,12,start=start,end=end),
        text('Chip text',label,18,12,23,tc,w=w-26,start=start,end=end,bold=True)],x,y,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# S01: giant prompt overwhelms the frame.
h1=group('Headline',[text('Lead','One giant prompt',80,184,70,INK,w=900,bold=True),
                    text('Emphasis','creates too many guesses.',80,270,62,BLUE,w=900,bold=True)],start=0,end=8)
reveal(h1,0,18); layers.append(h1)

prompt=[]
prompt.append(card('Prompt shell',0,0,820,540,'#FFFFFF',28))
prompt.append(text('Prompt label','PROMPT',34,30,21,MUT,w=200,bold=True))
prompt.append(text('Prompt body',
    'Build the whole app.\nAdd auth, payments, dashboards,\nroles, emails, reports and deployment.\nMake it production-ready.',
    34,82,34,INK,w=750,bold=True))
prompt.append(rect('Send button',590,446,190,60,BLUE,14))
prompt.append(text('Send text','Run it',654,462,25,'#FFFFFF',w=100,bold=True))
big=group('Giant prompt card',prompt,130,510,start=0,end=8)
keys(big,'scale',[(0,[88,88]),(.8,[100,100]),(3.6,[100,100]),(5.8,[113,113])])
keys(big,'position',[(0,[130,550]),(.8,[130,510]),(3.6,[130,510]),(5.8,[75,475])])
layers.append(big)

# Hidden assumption tags orbit the expanding prompt.
tags=[
 ('SCOPE?',95,1090,230,RED,REDINK),
 ('CONSTRAINTS?',720,1040,255,AMBER,AMBERINK),
 ('EXISTING CODE?',80,820,290,SOFT,BLUE),
 ('EDGE CASES?',730,760,250,RED,REDINK),
 ('WHAT IS DONE?',390,1160,300,AMBER,AMBERINK)
]
for i,(label,x,y,w,bg,tc) in enumerate(tags):
    g=chip(label,x,y,w,bg,tc,start=2.1,end=8)
    reveal(g,.25+i*.15,18)
    keys(g,'rotation',[(0,(-4 if i%2==0 else 5)),(3.5,(3 if i%2==0 else -3))])
    layers.append(g)

# S02: prompt breaks into a clear structure.
h2=group('Headline',[text('Lead','Break the instruction',80,184,68,INK,w=900,bold=True),
                    text('Emphasis','into a clear execution loop.',80,270,60,BLUE,w=900,bold=True)],start=8,end=18)
reveal(h2,0,18); layers.append(h2)

steps=[
 ('1','GOAL','Define the outcome.'),
 ('2','CONSTRAINTS','Protect what must stay intact.'),
 ('3','INSPECT','Read the current state first.'),
 ('4','SMALL TASK','Change one focused thing.'),
 ('5','CRITERIA','Describe what done means.'),
 ('6','TEST','Verify the result.')
]
for i,(num,label,desc) in enumerate(steps):
    colx=95 if i<3 else 555
    row=i if i<3 else i-3
    y=520+row*195
    tile=group('Structured step '+label,[
        card('Step card',0,0,430,158,'#FFFFFF',20),
        group('Number badge',[rect('Badge',0,0,52,52,BLUE,12),
            text('Num',num,16,8,24,'#FFFFFF',w=28,bold=True)],22,22),
        text('Step label',label,94,23,28,INK,w=300,bold=True),
        text('Step detail',desc,94,70,23,MUT,w=300)
    ],colx,y,start=8,end=18)
    reveal(tile,.2+i*.18,24)
    layers.append(tile)

flow=path('Execution lane',[M(300,1115),C(430,1195,650,1195,780,1115)],stroke=BLUE,width=5,start=8,end=18)
layers.append(flow)
arrow=group('Flow label',[chip('LESS ROOM TO GUESS',0,0,315,GREEN,GREENINK,start=8,end=18)],390,1160,start=8,end=18)
reveal(arrow,2.2,12); layers.append(arrow)

# Presenter from V04.
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
    ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
    for ch in o.get('layers',[]): extend(ch)
extend(presenter)
presenter['transform']['position']=[30,1285]
layers.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[30,1630]),(.7,[30,1285])])
keys(arm,'rotation',[(0,18),(.9,-10),(4.2,-20),(7,-7),(9,-18),(13,-7),(16,-16)])

note1=group('Presenter note 1',[text('Stage','TOO MUCH AT ONCE',640,1372,22,BLUE,w=340,bold=True),
                               text('Body','The agent has to\nfill in the blanks.',640,1420,31,INK,w=340)],start=0,end=8)
enter(note1); layers.append(note1)
note2=group('Presenter note 2',[text('Stage','STRUCTURE THE TASK',640,1372,22,BLUE,w=340,bold=True),
                               text('Body','Clear steps reduce\nambiguity and rework.',640,1420,31,INK,w=340)],start=8,end=18)
enter(note2); layers.append(note2)

doc['composition']={'id':'main','name':'V06 Giant Prompt / opening prototype','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V06 prototype layers',uid,'animation actions',len(actions))
