import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=82

layers=[]; actions=[]; uid=1300
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
GREEN='#E9F7EF'; GREENINK='#167749'; AMBER='#FFF4DC'; AMBERINK='#956515'
RED='#FDEBEC'; REDINK='#B33A42'; BORDER='#E5E8EE'; DARK='#1C2738'
PURPLE='#EEE9FF'; PURPLEINK='#6A4BC4'; CYAN='#E7F7FA'; CYANINK='#21728A'

def col(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def trans(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def base(t,n,x=0,y=0,start=0,end=82):
    global uid; uid+=1
    return dict(type=t,id=uid,name=n,blendMode='normal',
                activeRange={'start':int(start*1000),'duration':int((end-start)*1000)},
                transform=trans(x,y))
def rect(n,x,y,w,h,c,r=0,start=0,end=82):
    o=base('Rect',n,x,y,start,end); o['rect']=dict(size=[w,h],fillColor=col(c),roundness=r); return o
def text(n,s,x,y,size=40,c=INK,w=900,start=0,end=82,bold=False):
    o=base('Text',n,x,y,start,end)
    o['sourceText']=dict(text=s,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',
        fontSize=size,fillColor=col(c),strokeWidth=0,justification='left',verticalAlign='top',
        boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=size*1.12)
    return o
def path(n,cmd,c=None,stroke=None,width=3,start=0,end=82):
    o=base('Shape',n,start=start,end=end); o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
    if c:o['shape']['fills']=[dict(paint={'type':'solid','color':col(c)},fillRule='nonZeroWinding',blendMode='normal',opacity=100)]
    if stroke:o['shape']['strokes']=[dict(paint={'type':'solid','color':col(stroke)},width=width,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]
    return o
def M(x,y): return dict(type='moveTo',x=x,y=y)
def L(x,y): return dict(type='lineTo',x=x,y=y)
def C(a,b,c,d,x,y): return dict(type='cubicTo',c1x=a,c1y=b,c2x=c,c2y=d,x=x,y=y)
def Z(): return dict(type='close')
def ellipse(n,x,y,rx,ry,c,start=0,end=82):
    k=.55228475
    return path(n,[M(x+rx,y),C(x+rx,y+k*ry,x+k*rx,y+ry,x,y+ry),
                   C(x-k*rx,y+ry,x-rx,y+k*ry,x-rx,y),
                   C(x-rx,y-k*ry,x-k*rx,y-ry,x,y-ry),
                   C(x+k*rx,y-ry,x+rx,y-k*ry,x+rx,y),Z()],c,start=start,end=end)
def group(n,children,x=0,y=0,start=0,end=82):
    o=base('Group',n,x,y,start,end); o['layers']=children[::-1]; return o
def card(n,x,y,w,h,c='#FFFFFF',r=26,start=0,end=82):
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
def chip(label,x,y,w=250,c=SOFT,tc=BLUE,start=0,end=82):
    return group(label,[rect('Chip',0,0,w,54,c,12,start=start,end=end),text('Chip text',label,18,12,23,tc,w=w-28,start=start,end=end,bold=True)],x,y,start=start,end=end)
def connector(x1,y1,x2,y2,c='#B9C2D3',width=4,start=0,end=82):
    return path('Connector',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=c,width=width,start=start,end=end)
def packet(x,y,label='DATA',c=BLUE,start=0,end=82):
    return group('Packet',[rect('Packet body',-65,-23,130,46,c,23,start=start,end=end),text('Packet text',label,-44,-14,18,'#FFFFFF',w=100,start=start,end=end,bold=True)],x,y,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# S01 frontend vs backend
title('A frontend still','needs a backend.',0,9)
a=[]
app=group('Frontend app',[card('App',0,0,360,330,'#FFFFFF',26),text('App label','FRONTEND',28,26,20,MUT,w=180,bold=True),text('App title','Profile screen',28,72,40,INK,w=300,bold=True),rect('Avatar',28,145,76,76,PURPLE,18),text('Avatar label','IMG',47,165,20,PURPLEINK,w=50,bold=True),text('Name','Ada',135,162,30,INK,w=170,bold=True),chip('Save profile',28,254,220,BLUE,'#FFFFFF',start=0,end=9)],360,595); reveal(app,.1); a.append(app)
for i,(label,sub,x,y,w,bg,tc) in enumerate([
 ('AUTH','Users + sessions',95,515,245,GREEN,GREENINK),
 ('POSTGRES','Structured data',740,515,250,SOFT,BLUE),
 ('STORAGE','Files + uploads',95,930,245,PURPLE,PURPLEINK),
 ('FUNCTIONS/API','Backend logic',740,930,250,AMBER,AMBERINK),
 ('REALTIME','Live changes',415,1085,250,RED,REDINK)
]):
    b=group('Block '+label,[card('Block',0,0,w,150,bg,20),text('Label',label,24,27,27,tc,w=w-48,bold=True),text('Sub',sub,24,78,23,INK,w=w-48)],x,y); reveal(b,.25+i*.16); a.append(b); a.append(connector(540,760,x+w/2,y+75,BLUE,3,start=0,end=9))
scene('S01 Frontend backend',a,0,9)

# S02 platform overview
title('One platform.','Several backend jobs.',9,19)
a=[]
center=group('Supabase concept',[card('Center',0,0,340,190,DARK,24),text('Center label','BACKEND PLATFORM',30,26,20,'#AAB6CE',w=250,bold=True),text('Center title','One project',30,73,39,'#FFFFFF',w=270,bold=True)],370,650); reveal(center,.2); a.append(center)
blocks=[('AUTH','Identity',90,525,GREEN,GREENINK),('POSTGRES','Data',720,525,SOFT,BLUE),('STORAGE','Files',90,890,PURPLE,PURPLEINK),('FUNCTIONS/API','Logic',680,890,AMBER,AMBERINK),('REALTIME','Updates',415,1070,CYAN,CYANINK)]
for i,(label,sub,x,y,bg,tc) in enumerate(blocks):
    w=270 if label!='FUNCTIONS/API' else 310
    b=group(label,[card('Card',0,0,w,135,bg,20),text('Label',label,22,24,25,tc,w=w-44,bold=True),text('Sub',sub,22,72,24,INK,w=w-44)],x,y); reveal(b,.4+i*.18); a.append(b); a.append(connector(540,745,x+w/2,y+67,BLUE,3,start=9,end=19))
scene('S02 Platform overview',a,9,19)

# S03 Auth
title('Auth answers','who is this user?',19,29)
a=[]
form=group('Login form',[card('Form',0,0,360,410,'#FFFFFF',24),text('Title','Sign in',28,28,38,INK,w=290,bold=True),text('Email label','EMAIL',28,104,18,MUT,w=100,bold=True),rect('Email',28,136,304,60,'#F4F6F9',10),text('Email value','ada@example.com',43,150,22,INK,w=260),text('Password label','PASSWORD',28,222,18,MUT,w=120,bold=True),rect('Password',28,254,304,60,'#F4F6F9',10),text('Password value','••••••••',43,269,22,INK,w=250),chip('SIGN IN',28,332,150,BLUE,'#FFFFFF',start=19,end=29)],105,535); reveal(form,.15); a.append(form)
auth=group('Auth service',[card('Auth',0,0,390,330,GREEN,24),chip('AUTH',26,24,120,'#FFFFFF',GREENINK,start=19,end=29),text('Question','Who is this user?',26,100,36,INK,w=330,bold=True),text('List','• verify credentials\n• create session\n• identify user\n• return user ID',26,166,27,INK,w=320)],580,585); reveal(auth,.7); a.append(auth)
a.append(connector(465,730,580,730,BLUE,5,start=19,end=29))
p=packet(520,730,'LOGIN',BLUE,start=19,end=29); keys(p,'position',[(0,[465,730]),(2,[465,730]),(3.2,[580,730])]); a.append(p)
a.append(chip('USER 42',650,995,170,GREEN,GREENINK,start=19,end=29))
scene('S03 Auth',a,19,29)

# S04 Postgres
title('Postgres stores','structured app data.',29,39)
a=[]
db=group('Database',[card('DB',0,0,880,520,'#FFFFFF',24),chip('POSTGRES',28,24,185,SOFT,BLUE,start=29,end=39),text('Table title','profiles',28,100,35,INK,w=250,bold=True),rect('Header',28,160,824,46,'#F1F3F6',8),text('Header text','id      user_id      name      plan',42,171,21,MUT,w=780,bold=True)],100,515)
rows=[('1','42','Ada','Pro'),('2','57','Maya','Free'),('3','61','Tariq','Pro')]
for i,row in enumerate(rows):
    y=218+i*72
    db['layers'].append(rect('Row bg',28,y,824,58,SOFT if i==0 else '#FFFFFF',8))
    db['layers'].append(text('Row text','      '.join(row),42,y+15,22,INK,w=780))
reveal(db,.2); a.append(db)
rel=group('Relations',[card('Rel',0,0,700,150,DARK,20),text('Rel label','RELATIONSHIPS',26,22,20,'#AAB6CE',w=220,bold=True),text('Rel text','users.id  →  profiles.user_id  →  projects.owner_id',26,66,27,'#FFFFFF',w=650,bold=True)],190,1080); reveal(rel,1.2); a.append(rel)
scene('S04 Postgres',a,29,39)

# S05 Storage
title('Storage handles','files and uploads.',39,49)
a=[]
upload=group('Upload UI',[card('Upload',0,0,360,320,'#FFFFFF',24),chip('PROFILE IMAGE',28,24,220,PURPLE,PURPLEINK,start=39,end=49),rect('Dropzone',28,105,304,125,PURPLE,16),text('Drop text','ada.png\n1.8 MB',107,135,28,PURPLEINK,w=150,bold=True),chip('UPLOAD',28,252,145,BLUE,'#FFFFFF',start=39,end=49)],100,565); reveal(upload,.2); a.append(upload)
bucket=group('Bucket',[card('Bucket',0,0,380,360,PURPLE,24),text('Bucket label','STORAGE BUCKET',26,26,20,PURPLEINK,w=230,bold=True),text('Bucket title','avatars/',26,76,36,INK,w=280,bold=True),text('Files','ada.png\nmaya.jpg\ntariq.webp',26,145,28,INK,w=260),chip('PUBLIC URL',26,284,180,'#FFFFFF',PURPLEINK,start=39,end=49)],600,545); reveal(bucket,.8); a.append(bucket)
a.append(connector(460,720,600,720,PURPLEINK,5,start=39,end=49))
pk=packet(520,720,'FILE',PURPLEINK,start=39,end=49); keys(pk,'position',[(0,[460,720]),(2,[460,720]),(3.5,[600,720])]); a.append(pk)
scene('S05 Storage',a,39,49)

# S06 Functions/API
title('Functions and APIs','run backend logic.',49,59)
a=[]
browser=group('Browser request',[card('Browser',0,0,330,245,'#FFFFFF',22),text('Label','BROWSER',24,24,20,MUT,w=140,bold=True),text('Title','Buy plan',24,70,34,INK,w=250,bold=True),chip('POST /checkout',24,145,230,SOFT,BLUE,start=49,end=59)],90,615); reveal(browser,.2); a.append(browser)
fn=group('Function',[card('Function',0,0,390,360,AMBER,24),chip('FUNCTION / API',26,24,250,'#FFFFFF',AMBERINK,start=49,end=59),text('Logic','1. verify user\n2. read plan\n3. call payment service\n4. save result',26,105,29,INK,w=330)],590,565); reveal(fn,.7); a.append(fn)
a.append(connector(420,735,590,735,BLUE,5,start=49,end=59))
pk=packet(510,735,'POST',BLUE,start=49,end=59); keys(pk,'position',[(0,[420,735]),(1.8,[420,735]),(3.2,[590,735])]); a.append(pk)
a.append(group('Protected note',[card('Note',0,0,780,140,DARK,20),text('Note label','WHY BACKEND?',26,22,20,'#AAB6CE',w=200,bold=True),text('Note body','Secrets and protected service calls stay out of the browser.',26,63,29,'#FFFFFF',w=720,bold=True)],150,1050))
scene('S06 Functions',a,49,59)

# S07 Realtime
title('Realtime reacts','when data changes.',59,70)
a=[]
source=group('Source row',[card('Source',0,0,700,150,'#FFFFFF',20),text('Label','profiles · user 42',28,22,22,MUT,w=300,bold=True),text('Value','status: online',28,66,34,INK,w=300,bold=True),chip('UPDATE',500,48,160,BLUE,'#FFFFFF',start=59,end=70)],190,540); reveal(source,.15); a.append(source)
clients=[('Web app',90,830),('Admin',390,930),('Mobile',690,830)]
for i,(label,x,y) in enumerate(clients):
    c=group('Client '+label,[card('Client',0,0,250,170,CYAN,20),text('Client label',label,24,30,29,INK,w=200,bold=True),chip('online',24,93,140,GREEN,GREENINK,start=59,end=70)],x,y); reveal(c,.5+i*.25); a.append(c); a.append(connector(540,690,x+125,y,CYANINK,4,start=59,end=70))
pulse=ellipse('Pulse',540,690,14,14,CYANINK,start=59,end=70); keys(pulse,'scale',[(0,[60,60]),(2,[60,60]),(3.5,[180,180]),(5,[60,60]),(7,[180,180]),(9,[60,60])]); a.append(pulse)
scene('S07 Realtime',a,59,70)

# S08 full user flow
title('Frontend + backend','make the product real.',70,82)
a=[]
steps=[
 ('1','SIGN UP',70,560,210,GREEN,GREENINK),
 ('2','AUTH',300,560,170,GREEN,GREENINK),
 ('3','UPLOAD',490,560,180,PURPLE,PURPLEINK),
 ('4','SAVE ROW',690,560,200,SOFT,BLUE),
 ('5','RETURN',910,560,150,CYAN,CYANINK)
]
for i,(num,label,x,y,w,bg,tc) in enumerate(steps):
    s=group('Step '+num,[card('Step',0,0,w,115,bg,18),group('Num',[rect('Num bg',0,0,42,42,'#FFFFFF',10),text('N',num,13,7,20,tc,w=25,bold=True)],18,18),text('Label',label,68,31,23,INK,w=w-85,bold=True)],x,y); reveal(s,.2+i*.15); a.append(s)
for i in range(len(steps)-1):
    x1=steps[i][2]+steps[i][4]; x2=steps[i+1][2]
    a.append(connector(x1,617,x2,617,BLUE,4,start=70,end=82))
summary=group('Summary',[card('Summary',0,0,850,360,DARK,24),text('Summary label','ONE WORKING FLOW',30,26,20,'#AAB6CE',w=250,bold=True),text('Summary text','Frontend: what the user touches.\n\nBackend: identity, data, files, logic\nand live updates that make it work.',30,78,36,'#FFFFFF',w=780,bold=True)],115,790); reveal(summary,1.1); a.append(summary)
scene('S08 Flow',a,70,82)

# presenter
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
    ids.add(o['id']); o['activeRange']={'start':0,'duration':82000}
    for ch in o.get('layers',[]): extend(ch)
extend(presenter)
presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]
layers.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])])
keys(arm,'rotation',[(0,18),(.9,-8),(5,-18),(10,-7),(15,-18),(20,-8),(25,-17),(30,-8),(35,-17),(40,-8),(45,-17),(50,-8),(55,-18),(60,-8),(65,-18),(71,-8),(77,-17)])
notes=[
 (0,9,'FRONTEND ≠ BACKEND','The screen still needs\nbackend responsibilities.'),
 (9,19,'ONE PLATFORM','Several jobs sit\nbehind the interface.'),
 (19,29,'AUTH','Identity and sessions.'),
 (29,39,'POSTGRES','Structured application data.'),
 (39,49,'STORAGE','Files and uploads.'),
 (49,59,'FUNCTIONS / API','Protected backend logic.'),
 (59,70,'REALTIME','Clients react to changes.'),
 (70,82,'FULL FLOW','Identity, file and data\ncome back to the app.')
]
for st,en,label,body in notes:
    g=group('Presenter note',[text('Stage',label,640,1380,22,BLUE,w=345,bold=True),text('Body',body,640,1428,31,INK,w=345)],start=st,end=en); enter(g); layers.append(g)

doc['composition']={'id':'main','name':'V08 Supabase / full visual draft','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V08 full visual layers',uid,'animation actions',len(actions))
