import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text())
doc['duration']=18

layers=[]; actions=[]; uid=200
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
GREEN='#E9F7EF'; GREENINK='#167749'; BORDER='#E5E8EE'

def col(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def trans(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def base(t,n,x=0,y=0,start=0,end=18):
    global uid; uid+=1
    return dict(type=t,id=uid,name=n,blendMode='normal',
                activeRange={'start':int(start*1000),'duration':int((end-start)*1000)},
                transform=trans(x,y))
def rect(n,x,y,w,h,c,r=0,start=0,end=18):
    o=base('Rect',n,x,y,start,end)
    o['rect']=dict(size=[w,h],fillColor=col(c),roundness=r)
    return o
def text(n,s,x,y,size=40,c=INK,w=900,start=0,end=18,bold=False):
    o=base('Text',n,x,y,start,end)
    o['sourceText']=dict(text=s,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',
                         fontSize=size,fillColor=col(c),strokeWidth=0,justification='left',
                         verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,300],
                         leading=size*1.12)
    return o
def path(n,cmd,c=None,stroke=None,width=3,start=0,end=18):
    o=base('Shape',n,start=start,end=end)
    o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
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
    x,y=o['transform']['position']
    keys(o,'position',[(0,[x,y+dy]),(.55,[x,y])]); enter(o,delay)

proto=copy.deepcopy(doc)
layers.append(rect('Canvas',0,0,1080,1920,BG))
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# Headline — no top branding.
head=group('Opening headline',[
    text('Lead','A beautiful screen',80,185,69,INK,w=900,bold=True),
    text('Emphasis','is only the top layer.',80,270,64,BLUE,w=900,bold=True)
],start=0,end=8)
reveal(head,0,.0); layers.append(head)

# Polished login UI.
ui=[]
ui.append(card('App shell',0,0,740,610,'#FFFFFF',30))
ui.append(rect('Window rail',0,0,740,84,'#F1F3F6',30))
for i,x in enumerate([34,60,86]): ui.append(ellipse('Window dot',x,41,7,7,'#C9CED9'))
ui.append(text('Brand','Atlas',46,112,31,INK,w=170,bold=True))
ui.append(text('Title','Welcome back',46,172,48,INK,w=600,bold=True))
ui.append(text('Sub','Sign in to continue',46,235,27,MUT,w=600))
ui.append(text('Email label','EMAIL',46,303,19,MUT,w=300,bold=True))
ui.append(rect('Email input',46,338,648,74,'#F7F8FA',14))
ui.append(text('Email value','you@company.com',67,354,28,INK,w=550))
ui.append(text('Password label','PASSWORD',46,436,19,MUT,w=300,bold=True))
ui.append(rect('Password input',46,471,648,74,'#F7F8FA',14))
ui.append(text('Password value','••••••••••',67,487,28,INK,w=550))
ui.append(rect('Login button',46,560,648,76,BLUE,16))
ui.append(text('Button text','Log in',310,577,29,'#FFFFFF',w=150,bold=True))
app=group('Polished app interface',ui,170,505,start=0,end=8)
keys(app,'position',[(0,[170,545]),(.7,[170,505]),(3.8,[170,505]),(5.15,[72,548])])
keys(app,'scale',[(0,[100,100]),(3.8,[100,100]),(5.15,[54,54])])
keys(app,'opacity',[(0,100),(3.8,100),(5.15,76),(7.8,76)])
layers.append(app)

# Five hidden layers reveal beside the source UI. This avoids the compressed pile
# and keeps every label fully readable throughout the animation.
labels=[
 ('1','INTERFACE','#FFFFFF',INK),
 ('2','APPLICATION LOGIC','#EEF0FF',BLUE),
 ('3','API / BACKEND','#E7EBF6',INK),
 ('4','DATA + IDENTITY','#DDE2FF',INK),
 ('5','INFRASTRUCTURE','#D4DAEA',INK)
]
stack=[]
for i,(num,label,c,tc) in enumerate(labels):
    layer=group('Layer '+label,[
        card('Layer card',0,0,465,76,c,16),
        group('Index badge',[
            rect('Badge',0,0,46,46,BLUE if i==0 else '#FFFFFF',11),
            text('Number',num,14,7,22,'#FFFFFF' if i==0 else BLUE,w=30,bold=True)
        ],18,15),
        text('Layer label',label,82,18,24,tc,w=355,bold=True)
    ],535,505+i*102,start=4.25,end=18)
    enter(layer,.12+i*.10)
    stack.append(layer); layers.append(layer)

# Interface isolates in scene 2.
for i,layer in enumerate(stack):
    if i==0:
        keys(layer,'position',[(0,[145,645]),(5.4,[145,645]),(7,[145,560]),(12.8,[145,560])])
        keys(layer,'scale',[(0,[100,100]),(7,[106,106]),(12.8,[106,106])])
    else:
        keys(layer,'opacity',[(0,100),(5.4,100),(6.2,18),(9,18)])
        keys(layer,'position',[(0,[145,645+i*104]),(6.5,[145,770+i*28]),(9,[145,770+i*28])])

# scene 2 headline and mini interactive interface.
h2=group('Interface headline',[
    text('Lead','Layer one is',80,185,68,INK,w=900,bold=True),
    text('Emphasis','the interface.',80,270,64,BLUE,w=900,bold=True)
],start=8,end=18)
reveal(h2,0); layers.append(h2)

mini=[]
mini.append(card('Interaction card',0,0,650,330,'#FFFFFF',24))
mini.append(text('Interaction heading','What the user sees and touches',30,28,32,INK,w=590,bold=True))
mini.append(rect('Mini input',30,100,590,64,'#F4F6F9',12))
mini.append(text('Mini email','you@company.com',49,115,25,INK,w=520))
mini.append(rect('Mini button',30,188,590,68,BLUE,14))
mini.append(text('Mini button label','Log in',272,204,27,'#FFFFFF',w=140,bold=True))
mini.append(group('Success chip',[rect('Chip',0,0,205,48,GREEN,11),text('Chip text','SIGNED IN',20,10,22,GREENINK,w=170,bold=True)],30,273))
m=group('Interface interaction',mini,350,885,start=8,end=18)
reveal(m,.25); layers.append(m)
buttonFlash=rect('Button pulse',380,1073,590,68,'#FFFFFF',14,start=8,end=18)
keys(buttonFlash,'opacity',[(0,0),(2.1,0),(2.2,18),(2.35,0),(3,0)])
layers.append(buttonFlash)

# Presenter from approved V04 asset.
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
keys(arm,'rotation',[(0,18),(.9,-10),(4,-4),(6.1,-23),(8.5,-4),(11.5,-18),(16,-6)])

note1=group('Presenter note one',[
    text('Stage','LOOK BEHIND THE UI',640,1370,23,BLUE,w=350,bold=True),
    text('Body','The screen sits on\nfour hidden layers.',640,1420,32,INK,w=350)
],start=0,end=8); enter(note1); layers.append(note1)
note2=group('Presenter note two',[
    text('Stage','LAYER 1',640,1370,23,BLUE,w=350,bold=True),
    text('Body','Buttons, forms,\nscreens and feedback.',640,1420,32,INK,w=350)
],start=8,end=18); enter(note2); layers.append(note2)

doc['composition']={'id':'main','name':'V05 Layers / opening prototype','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V05 prototype layers',uid,'animation actions',len(actions))
