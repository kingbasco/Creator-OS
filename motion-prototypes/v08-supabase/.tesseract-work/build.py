import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=18

layers=[]; actions=[]; uid=1100
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
GREEN='#E9F7EF'; GREENINK='#167749'; AMBER='#FFF4DC'; AMBERINK='#956515'
RED='#FDEBEC'; REDINK='#B33A42'; BORDER='#E5E8EE'; DARK='#1C2738'
PURPLE='#EEE9FF'; PURPLEINK='#6A4BC4'

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
def connector(x1,y1,x2,y2,c='#B9C2D3',width=4,start=0,end=18):
    return path('Connector',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=c,width=width,start=start,end=end)
def packet(x,y,label='DATA',c=BLUE,start=0,end=18):
    return group('Packet',[rect('Packet body',-65,-23,130,46,c,23,start=start,end=end),text('Packet text',label,-44,-14,18,'#FFFFFF',w=100,start=start,end=end,bold=True)],x,y,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# Scene 1 architecture fan.
h1=group('Headline',[
    text('Lead','Your frontend still',80,182,68,INK,w=900,bold=True),
    text('Emphasis','needs a backend.',80,266,62,BLUE,w=900,bold=True)
],start=0,end=8); reveal(h1,0,18); layers.append(h1)

app=group('App card',[
    card('App',0,0,330,300,'#FFFFFF',26),
    text('App label','YOUR APP',28,26,20,MUT,w=170,bold=True),
    text('App title','Profile screen',28,72,39,INK,w=280,bold=True),
    rect('Avatar',28,140,72,72,PURPLE,18),
    text('Avatar mark','IMG',45,160,20,PURPLEINK,w=50,bold=True),
    text('Name label','Name',125,142,20,MUT,w=130),
    text('Name value','Ada',125,171,28,INK,w=160,bold=True),
    chip('Save profile',28,232,210,BLUE,'#FFFFFF')
],375,610); reveal(app,.1); layers.append(app)

blocks=[
 ('AUTH','Users + sessions',95,520,245,GREEN,GREENINK),
 ('POSTGRES','Structured data',740,520,250,SOFT,BLUE),
 ('STORAGE','Files + uploads',95,930,245,PURPLE,PURPLEINK),
 ('FUNCTIONS/API','Backend logic',740,930,250,AMBER,AMBERINK),
 ('REALTIME','Live changes',415,1070,250,RED,REDINK)
]
centers=[]
for i,(label,sub,x,y,w,bg,tc) in enumerate(blocks):
    b=group('Block '+label,[card('Backend block',0,0,w,150,bg,20),text('Block label',label,24,27,27,tc,w=w-48,bold=True),text('Block sub',sub,24,78,23,INK,w=w-48)],x,y)
    reveal(b,.25+i*.18); layers.append(b); centers.append((x+w/2,y+75))
for x,y in centers:
    layers.append(connector(540,760,x,y,BLUE,3,start=0,end=8))

# Scene 2 signup → storage → row.
h2=group('Flow headline',[
    text('Lead','One signup touches',80,182,68,INK,w=900,bold=True),
    text('Emphasis','several backend jobs.',80,266,62,BLUE,w=900,bold=True)
],start=8,end=18); reveal(h2,0,18); layers.append(h2)

form=group('Signup form',[
    card('Signup',0,0,300,360,'#FFFFFF',24),
    text('Form title','Create account',24,27,33,INK,w=250,bold=True),
    text('Email label','EMAIL',24,94,18,MUT,w=100,bold=True),
    rect('Email field',24,126,252,58,'#F4F6F9',10),
    text('Email','ada@example.com',39,139,21,INK,w=215),
    text('Photo label','PROFILE IMAGE',24,205,18,MUT,w=170,bold=True),
    rect('Photo field',24,237,252,58,PURPLE,10),
    text('Photo','ada.png',39,250,21,PURPLEINK,w=210,bold=True),
    chip('SIGN UP',24,312,150,BLUE,'#FFFFFF',start=8,end=18)
],70,560,start=8,end=18); reveal(form,.1); layers.append(form)

# The flow is intentionally arranged as a left-to-right pipeline so no result card
# covers the signup form, central route, or database table.
auth=group('Auth result',[
    card('Auth card',0,0,250,145,GREEN,20),
    text('Auth label','AUTH',22,20,20,GREENINK,w=105,bold=True),
    text('Auth result','Identity created',22,60,27,INK,w=205,bold=True)
],415,555,start=8,end=18); keys(auth,'opacity',[(0,0),(2.0,0),(2.4,100)]); layers.append(auth)

storage=group('Storage result',[
    card('Storage card',0,0,250,145,PURPLE,20),
    text('Storage label','STORAGE',22,20,20,PURPLEINK,w=130,bold=True),
    text('Storage result','ada.png uploaded',22,60,26,INK,w=205,bold=True)
],415,755,start=8,end=18); keys(storage,'opacity',[(0,0),(3.8,0),(4.2,100)]); layers.append(storage)

db=group('Database row',[
    card('DB card',0,0,330,300,'#FFFFFF',22),
    text('DB label','POSTGRES · profiles',22,22,19,BLUE,w=260,bold=True),
    text('DB note','Profile record',22,62,28,INK,w=250,bold=True),
    rect('Head',22,112,286,42,'#F1F3F6',8),
    text('Header','id   name   avatar_url',34,121,18,MUT,w=260,bold=True),
    rect('Row',22,164,286,65,SOFT,8),
    text('Row text','42   Ada\n/avatars/ada.png',34,174,19,INK,w=255),
    chip('ROW SAVED',22,242,165,GREEN,GREENINK,start=8,end=18)
],700,630,start=8,end=18); keys(db,'opacity',[(0,0),(5.8,0),(6.2,100)]); layers.append(db)

# Connectors reinforce the order without crossing through text.
layers.append(connector(370,650,415,625,BLUE,4,start=8,end=18))
layers.append(connector(370,825,415,825,PURPLEINK,4,start=8,end=18))
layers.append(connector(665,625,700,690,BLUE,4,start=8,end=18))
layers.append(connector(665,825,700,820,PURPLEINK,4,start=8,end=18))

p1=packet(390,638,'SIGNUP',BLUE,start=8,end=18)
keys(p1,'position',[(0,[390,638]),(1.3,[390,638]),(2.3,[420,625])]); layers.append(p1)
p2=packet(390,825,'IMAGE',PURPLEINK,start=8,end=18)
keys(p2,'position',[(0,[390,825]),(3.0,[390,825]),(4.1,[420,825])]); layers.append(p2)
p3=packet(680,735,'PROFILE',BLUE,start=8,end=18)
keys(p3,'position',[(0,[680,735]),(5.0,[680,735]),(6.2,[705,735])]); layers.append(p3)

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
keys(arm,'rotation',[(0,18),(.9,-8),(4,-18),(7,-5),(9,-20),(13,-8),(17,-15)])

n1=group('Presenter note one',[
    text('Stage','BACKEND RESPONSIBILITIES',650,1380,22,BLUE,w=340,bold=True),
    text('Body','The UI connects to\nseveral backend jobs.',650,1428,31,INK,w=340)
],start=0,end=8); enter(n1); layers.append(n1)
n2=group('Presenter note two',[
    text('Stage','ONE USER FLOW',650,1380,22,BLUE,w=340,bold=True),
    text('Body','Identity, file and\ndata move separately.',650,1428,31,INK,w=340)
],start=8,end=18); enter(n2); layers.append(n2)

doc['composition']={'id':'main','name':'V08 Supabase / opening prototype','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V08 prototype layers',uid,'animation actions',len(actions))
