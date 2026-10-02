import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=18

layers=[]; actions=[]; uid=500
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
RED='#FDEBEC'; REDINK='#B33A42'; AMBER='#FFF4DC'; AMBERINK='#956515'; BORDER='#E5E8EE'; DARK='#1C2738'

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
def chip(label,x,y,w=250,c=SOFT,tc=BLUE,start=0,end=18):
    return group(label,[rect('Chip',0,0,w,54,c,12,start=start,end=end),text('Chip text',label,18,12,23,tc,w=w-28,start=start,end=end,bold=True)],x,y,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# Scene 1: giant prompt that grows beyond comfort.
headline=group('Headline',[
    text('Lead','One giant prompt',80,182,68,INK,w=900,bold=True),
    text('Emphasis','creates too many guesses.',80,266,62,BLUE,w=900,bold=True)
],start=0,end=8); reveal(headline,0,18); layers.append(headline)

prompt=[]
prompt.append(card('Prompt shell',0,0,820,525,'#FFFFFF',28))
prompt.append(text('Prompt label','PROMPT',32,28,20,MUT,w=180,bold=True))
prompt.append(text('Prompt body',
    'Build the entire app. Add auth, dashboard, settings,\n'
    'billing, notifications, responsive mobile layouts,\n'
    'permissions, analytics, error handling, tests,\n'
    'and make sure nothing already working breaks.',
    32,78,34,INK,w=750,bold=False))
prompt.append(chip('Run',32,420,150,BLUE,'#FFFFFF'))
gprompt=group('Giant prompt',prompt,130,525,start=0,end=8)
keys(gprompt,'scale',[(0,[86,86]),(.7,[100,100]),(3.8,[100,100]),(6.2,[110,110])])
keys(gprompt,'position',[(0,[130,575]),(.7,[130,525]),(3.8,[130,525]),(6.2,[95,500])])
layers.append(gprompt)

# Hidden assumptions orbit the prompt, with safe spacing.
assumptions=[
 ('SCOPE?',95,1045,180,RED,REDINK),
 ('EXISTING CODE?',300,1115,250,AMBER,AMBERINK),
 ('EDGE CASES?',585,1045,220,RED,REDINK),
 ('WHAT IS DONE?',760,1145,235,AMBER,AMBERINK),
 ('CONSTRAINTS?',125,1205,225,SOFT,BLUE),
 ('SUCCESS?',415,1240,190,SOFT,BLUE),
]
for i,(label,x,y,w,bg,tc) in enumerate(assumptions):
    tag=chip(label,x,y,w,bg,tc,start=2.2,end=8)
    keys(tag,'position',[(0,[x,y+28]),(.45+i*.08,[x,y])])
    enter(tag,.18+i*.09)
    layers.append(tag)

# Scene 2: prompt collapses and clean structure replaces noise.
h2=group('Structured headline',[
    text('Lead','Break the instruction',80,182,68,INK,w=900,bold=True),
    text('Emphasis','into a clear workflow.',80,266,62,BLUE,w=900,bold=True)
],start=8,end=18); reveal(h2,0,18); layers.append(h2)

cards=[
 ('1','GOAL','What are we changing?'),
 ('2','CONSTRAINTS','What must stay intact?'),
 ('3','INSPECT','Read the current state.'),
 ('4','SMALL TASK','Change one thing.'),
 ('5','CRITERIA','Define “done”.'),
 ('6','TEST','Verify the result.')
]
positions=[(120,525),(555,525),(120,705),(555,705),(120,885),(555,885)]
for i,((num,label,sub),(x,y)) in enumerate(zip(cards,positions)):
    item=group('Structured card '+label,[
        card('Card',0,0,405,145,'#FFFFFF',20),
        group('Number badge',[
            rect('Badge',0,0,48,48,BLUE,11),
            text('Number',num,15,8,22,'#FFFFFF',w=28,bold=True)
        ],20,20),
        text('Label',label,88,23,26,INK,w=280,bold=True),
        text('Sub',sub,88,67,23,MUT,w=285)
    ],x,y,start=8,end=18)
    # fan in from a shared center, then settle into a 2-column grid.
    keys(item,'position',[(0,[405,760]),(.55+i*.11,[x,y])]); enter(item,.08+i*.08)
    layers.append(item)

# one clean execution lane appears below.
lane=group('Execution lane',[
    card('Lane',0,0,840,105,DARK,20),
    text('Lane text','Goal  →  Constraints  →  Inspect  →  Task  →  Criteria  →  Test',28,35,24,'#FFFFFF',w=790,bold=True)
],120,1110,start=12.5,end=18)
reveal(lane,.15,20); layers.append(lane)

# Approved presenter: smaller and kept out of core diagrams.
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
    ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
    for ch in o.get('layers',[]): extend(ch)
extend(presenter)
presenter['transform']['position']=[42,1290]
presenter['transform']['scale']=[92,92]
layers.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[42,1620]),(.7,[42,1290])])
keys(arm,'rotation',[(0,18),(.9,-8),(4,-21),(7,-4),(9,-18),(13,-6),(17,-15)])

note1=group('Presenter note one',[
    text('Stage','TOO MUCH AT ONCE',650,1380,22,BLUE,w=340,bold=True),
    text('Body','The agent has to\nfill in the blanks.',650,1426,31,INK,w=340)
],start=0,end=8); enter(note1); layers.append(note1)
note2=group('Presenter note two',[
    text('Stage','ADD STRUCTURE',650,1380,22,BLUE,w=340,bold=True),
    text('Body','Reduce ambiguity\nbefore asking for code.',650,1426,31,INK,w=340)
],start=8,end=18); enter(note2); layers.append(note2)

doc['composition']={'id':'main','name':'V06 Giant Prompt / opening prototype','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V06 prototype layers',uid,'animation actions',len(actions))
