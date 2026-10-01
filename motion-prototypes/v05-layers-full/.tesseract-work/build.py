import copy, json
from pathlib import Path

HERE=Path(__file__).resolve()
ROOT=HERE.parents[3]
SOURCE=ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json'
doc=json.loads(SOURCE.read_text()); doc['duration']=76

layers=[]; actions=[]; uid=300
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'
GREEN='#E9F7EF'; GREENINK='#167749'; RED='#FDEBEC'; REDINK='#B33A42'
AMBER='#FFF4DC'; AMBERINK='#956515'; BORDER='#E5E8EE'; DARK='#1C2738'

def col(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def trans(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def base(t,n,x=0,y=0,start=0,end=76):
    global uid; uid+=1
    return dict(type=t,id=uid,name=n,blendMode='normal',
                activeRange={'start':int(start*1000),'duration':int((end-start)*1000)},
                transform=trans(x,y))
def rect(n,x,y,w,h,c,r=0,start=0,end=76):
    o=base('Rect',n,x,y,start,end); o['rect']=dict(size=[w,h],fillColor=col(c),roundness=r); return o
def text(n,s,x,y,size=40,c=INK,w=900,start=0,end=76,bold=False):
    o=base('Text',n,x,y,start,end)
    o['sourceText']=dict(text=s,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',
        fontSize=size,fillColor=col(c),strokeWidth=0,justification='left',verticalAlign='top',
        boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=size*1.12)
    return o
def path(n,cmd,c=None,stroke=None,width=3,start=0,end=76):
    o=base('Shape',n,start=start,end=end); o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
    if c:o['shape']['fills']=[dict(paint={'type':'solid','color':col(c)},fillRule='nonZeroWinding',blendMode='normal',opacity=100)]
    if stroke:o['shape']['strokes']=[dict(paint={'type':'solid','color':col(stroke)},width=width,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]
    return o
def M(x,y): return dict(type='moveTo',x=x,y=y)
def L(x,y): return dict(type='lineTo',x=x,y=y)
def C(a,b,c,d,x,y): return dict(type='cubicTo',c1x=a,c1y=b,c2x=c,c2y=d,x=x,y=y)
def Z(): return dict(type='close')
def ellipse(n,x,y,rx,ry,c,start=0,end=76):
    k=.55228475
    return path(n,[M(x+rx,y),C(x+rx,y+k*ry,x+k*rx,y+ry,x,y+ry),
                   C(x-k*rx,y+ry,x-rx,y+k*ry,x-rx,y),
                   C(x-rx,y-k*ry,x-k*rx,y-ry,x,y-ry),
                   C(x+k*rx,y-ry,x+rx,y-k*ry,x+rx,y),Z()],c,start=start,end=end)
def group(n,children,x=0,y=0,start=0,end=76):
    o=base('Group',n,x,y,start,end); o['layers']=children[::-1]; return o
def card(n,x,y,w,h,c='#FFFFFF',r=26,start=0,end=76):
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
    g=group('Headline',[text('Lead',a,80,180,68,INK,w=900,bold=True),text('Emphasis',b,80,266,64,BLUE,w=900,bold=True)],start=st,end=en)
    reveal(g,0,18); layers.append(g)
def chip(label,x,y,w=260,c=SOFT,tc=BLUE,start=0,end=76):
    return group(label,[rect('Chip',0,0,w,54,c,12,start=start,end=end),text('Chip text',label,18,12,23,tc,w=w-28,start=start,end=end,bold=True)],x,y,start=start,end=end)
def connector(x1,y1,x2,y2,c='#B9C2D3',width=4,start=0,end=76):
    return path('Connector',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=c,width=width,start=start,end=end)
def packet(x,y,label='REQUEST',c=BLUE,start=0,end=76):
    return group('Packet',[rect('Packet body',-72,-24,144,48,c,24,start=start,end=end),text('Packet label',label,-52,-15,18,'#FFFFFF',w=115,start=start,end=end,bold=True)],x,y,start=start,end=end)

proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1225,1730]: layers.append(rect('Editorial rule',80,y,920,2,BORDER))

# S01 — polished interface lifts and reveals four more layers.
title('A beautiful screen','is only the top layer.',0,8)
ui=[]
ui.append(card('App shell',0,0,740,610,'#FFFFFF',30))
ui.append(rect('Window rail',0,0,740,84,'#F1F3F6',30))
for x in [34,60,86]: ui.append(ellipse('Window dot',x,41,7,7,'#C9CED9'))
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

# Clean side-by-side reveal: the source UI steps back while all five layers become
# independently readable. No layer card sits over form copy or another label.
labels=[('1','INTERFACE','#FFFFFF',INK),('2','APPLICATION LOGIC','#EEF0FF',BLUE),('3','API / BACKEND','#E7EBF6',INK),('4','DATA + IDENTITY','#DDE2FF',INK),('5','INFRASTRUCTURE','#D4DAEA',INK)]
for i,(num,label,c,tc) in enumerate(labels):
    layer=group('Layer '+label,[
        card('Layer card',0,0,465,76,c,16),
        group('Index badge',[
            rect('Badge',0,0,46,46,BLUE if i==0 else '#FFFFFF',11),
            text('Number',num,14,7,22,'#FFFFFF' if i==0 else BLUE,w=30,bold=True)
        ],18,15),
        text('Layer label',label,82,18,24,tc,w=355,bold=True)
    ],535,505+i*102,start=4.25,end=8)
    enter(layer,.12+i*.10)
    layers.append(layer)

# A subtle bridge keeps the "screen becomes the stack" idea without collisions.
layers.append(connector(455,730,535,730,BLUE,4,start=4.25,end=8))
bridge=packet(488,730,'UI',BLUE,start=4.25,end=8)
keys(bridge,'position',[(0,[455,730]),(.7,[455,730]),(1.45,[530,730])])
keys(bridge,'scale',[(0,[78,78]),(1.45,[78,78])])
layers.append(bridge)

# S02 — isolate interface and show real feedback.
title('Layer one is','the interface.',8,18)
a=[]
a.append(group('Interface badge',[card('Badge card',0,0,790,82),chip('1  INTERFACE',20,14,250)],145,530))
surface=[]
surface.append(card('Interaction card',0,0,780,430,'#FFFFFF',24))
surface.append(text('Interaction heading','What the user sees and touches',34,31,34,INK,w=700,bold=True))
surface.append(text('Email label','EMAIL',34,99,18,MUT,w=200,bold=True))
surface.append(rect('Email input',34,132,712,67,'#F4F6F9',12))
surface.append(text('Email','you@company.com',55,146,25,INK,w=650))
surface.append(text('Password label','PASSWORD',34,222,18,MUT,w=200,bold=True))
surface.append(rect('Password input',34,255,712,67,'#F4F6F9',12))
surface.append(text('Password','••••••••••',55,269,25,INK,w=650))
surface.append(rect('Button',34,344,712,65,BLUE,14))
surface.append(text('Login','Log in',327,359,27,'#FFFFFF',w=140,bold=True))
a.append(group('Working UI',surface,150,650))
success=chip('SIGNED IN',184,1091,215,GREEN,GREENINK,start=8,end=18); keys(success,'opacity',[(0,0),(4.3,0),(4.7,100)]); a.append(success)
flash=rect('Tap flash',184,994,712,65,'#FFFFFF',14,start=8,end=18); keys(flash,'opacity',[(0,0),(2.9,0),(3,20),(3.22,0)]); a.append(flash)
scene('S02 Interface',a,8,18)

# S03 — button click becomes logic decision tree.
title('Layer two decides','what should happen next.',18,28)
a=[]
a.append(chip('2  APPLICATION LOGIC',145,525,410,start=18,end=28))
root=group('Click event',[card('Click node',0,0,280,94,INK,20),text('Click text','Log in clicked',28,27,31,'#FFFFFF',w=240,bold=True)],400,650); reveal(root,.2); a.append(root)
a.append(connector(540,744,540,830,BLUE,5,start=18,end=28))
check=group('Decision',[card('Decision node',0,0,430,105,SOFT,20),text('Decision title','Are fields valid?',32,31,33,BLUE,w=370,bold=True)],325,830); reveal(check,1); a.append(check)
a.append(connector(430,936,265,1022,'#B9C2D3',4,start=18,end=28)); a.append(connector(650,936,815,1022,'#B9C2D3',4,start=18,end=28))
bad=group('Invalid branch',[card('Error branch',0,0,310,120,RED,18),text('Branch label','NO',24,19,20,REDINK,w=80,bold=True),text('Branch text','Show an error',24,56,29,REDINK,w=250,bold=True)],110,1022); reveal(bad,2); a.append(bad)
good=group('Valid branch',[card('Success branch',0,0,310,120,GREEN,18),text('Branch label','YES',24,19,20,GREENINK,w=80,bold=True),text('Branch text','Send request',24,56,29,GREENINK,w=250,bold=True)],660,1022); reveal(good,2.3); a.append(good)
sig=packet(540,697,'CLICK',BLUE,start=18,end=28); keys(sig,'position',[(0,[540,697]),(1.2,[540,697]),(2.1,[540,858]),(3.4,[540,880]),(4.9,[815,1081])]); a.append(sig)
scene('S03 Logic',a,18,28)

# S04 — request transforms into backend call.
title('Layer three handles','the request.',28,38)
a=[]
a.append(chip('3  API / BACKEND',145,525,330,start=28,end=38))
client=group('App request',[card('App card',0,0,315,200,'#FFFFFF',22),text('App label','APP',25,22,20,MUT,w=120,bold=True),text('App title','Login form',25,66,36,INK,w=260,bold=True),chip('POST /login',25,126,225,SOFT,BLUE,start=28,end=38)],110,690); reveal(client,.2); a.append(client)
server=group('Backend',[card('Backend card',0,0,370,330,DARK,24),text('Backend label','BACKEND',30,25,21,'#AAB6CE',w=220,bold=True),text('Backend title','API service',30,71,39,'#FFFFFF',w=300,bold=True),chip('Validate input',30,141,285,'#2B3850','#DCE3F3',start=28,end=38),chip('Check identity',30,208,285,'#2B3850','#DCE3F3',start=28,end=38),chip('Return response',30,275,285,'#2B3850','#DCE3F3',start=28,end=38)],600,630); reveal(server,1); a.append(server)
a.append(connector(425,790,600,790,BLUE,5,start=28,end=38))
req=packet(448,790,'POST',BLUE,start=28,end=38); keys(req,'position',[(0,[448,790]),(2,[448,790]),(3.1,[575,790]),(5,[720,790])]); a.append(req)
a.append(text('Backend note','The UI does not talk directly\nto every system.',145,1040,31,MUT,w=790))
scene('S04 Backend',a,28,38)

# S05 — auth, permissions and database live in data/identity.
title('Layer four is','data + identity.',38,48)
a=[]
a.append(chip('4  DATA + IDENTITY',145,525,365,start=38,end=48))
auth=group('Authentication',[card('Auth',0,0,330,220,SOFT,22),text('Auth label','AUTHENTICATION',27,26,21,BLUE,w=270,bold=True),text('Auth title','Who are you?',27,75,34,INK,w=270,bold=True),chip('Password verified',27,141,260,GREEN,GREENINK,start=38,end=48)],100,675); reveal(auth,.3); a.append(auth)
perm=group('Permissions',[card('Permissions',0,0,330,220,AMBER,22),text('Perm label','PERMISSIONS',27,26,21,AMBERINK,w=270,bold=True),text('Perm title','What may you do?',27,75,31,INK,w=280,bold=True),chip('member role',27,141,220,'#FFFFFF',AMBERINK,start=38,end=48)],650,675); reveal(perm,.8); a.append(perm)
db=group('Database',[card('Database',0,0,880,220,'#FFFFFF',22),text('DB label','DATABASE',27,25,21,MUT,w=200,bold=True),text('DB table','users',27,68,33,INK,w=180,bold=True),rect('Table head',27,118,826,44,'#F1F3F6',8),text('Header','id        email                  role',43,126,21,MUT,w=780,bold=True),rect('Selected row',27,169,826,42,GREEN,8),text('Row','42        you@company.com      member',43,177,21,GREENINK,w=780,bold=True)],100,960); reveal(db,1.5); a.append(db)
a.append(connector(265,895,380,960,BLUE,4,start=38,end=48)); a.append(connector(815,895,700,960,BLUE,4,start=38,end=48))
scene('S05 Data identity',a,38,48)

# S06 — zoom out to infrastructure runtime.
title('Layer five keeps','the app running.',48,58)
a=[]
a.append(chip('5  INFRASTRUCTURE',145,525,345,start=48,end=58))
runtime=group('Runtime',[card('Runtime frame',0,0,900,525,DARK,28),text('Runtime title','Production environment',38,30,40,'#FFFFFF',w=760,bold=True),
    chip('DEPLOYMENT',38,103,250,'#2B3850','#DCE3F3',start=48,end=58),
    chip('ENV VARS',325,103,220,'#2B3850','#DCE3F3',start=48,end=58),
    chip('LOGS',583,103,160,'#2B3850','#DCE3F3',start=48,end=58),
    group('App instance',[rect('Instance',0,0,300,210,'#263349',20),text('Instance title','app-web-01',26,27,31,'#FFFFFF',w=250,bold=True),chip('HEALTHY',26,84,190,GREEN,GREENINK,start=48,end=58),text('Uptime','Running · 99.9%',26,151,24,'#AAB6CE',w=240)],40,185),
    group('Logs',[rect('Log panel',0,0,455,260,'#151E2C',18),text('Logs title','LIVE LOGS',25,22,20,'#AAB6CE',w=200,bold=True),text('Logs body','19:22  POST /login  200\n19:22  auth verified\n19:22  user loaded\n19:23  GET /profile  200',25,65,24,'#DDE4F1',w=395)],405,185)
],90,650); reveal(runtime,.2); a.append(runtime)
scene('S06 Infrastructure',a,48,58)

# S07 — full stack login travels down and back up.
title('One login touches','all five layers.',58,68)
a=[]
stack_labels=[('1','INTERFACE','#FFFFFF'),('2','APPLICATION LOGIC','#EEF0FF'),('3','API / BACKEND','#E7EBF6'),('4','DATA + IDENTITY','#DDE2FF'),('5','INFRASTRUCTURE','#D4DAEA')]
ys=[]
for i,(num,label,c) in enumerate(stack_labels):
    y=545+i*122; ys.append(y)
    tile=group('Stack '+label,[card('Layer',0,0,760,93,c,18),group('Badge',[rect('Badge bg',0,0,50,50,BLUE,11),text('N',num,16,8,23,'#FFFFFF',w=30,bold=True)],22,21),text('Layer name',label,94,24,28,INK,w=590,bold=True)],160,y); reveal(tile,.15+i*.13); a.append(tile)
down=packet(850,592,'LOGIN',BLUE,start=58,end=68)
keys(down,'position',[(0,[850,592]),(1.2,[850,592]),(4.6,[850,1080]),(5.0,[850,1080]),(8.2,[850,592])])
keys(down,'scale',[(0,[100,100]),(4.6,[92,92]),(5,[92,92]),(8.2,[100,100])]); a.append(down)
status=chip('SIGNED IN',430,1174,220,GREEN,GREENINK,start=58,end=68); keys(status,'opacity',[(0,0),(8.2,0),(8.6,100)]); a.append(status)
a.append(text('Flow hint','request ↓                       response ↑',250,1208,24,MUT,w=600))
scene('S07 Full stack flow',a,58,68)

# S08 — debug the layer, not "the app".
title('When something breaks,','find the owning layer.',68,76)
a=[]
examples=[
 ('Button does nothing','INTERFACE / LOGIC',BLUE,SOFT),
 ('401 after login','AUTH / PERMISSIONS',AMBERINK,AMBER),
 ('App is unreachable','INFRASTRUCTURE',REDINK,RED),
]
for i,(bug,owner,tc,bg) in enumerate(examples):
    row=group('Bug row '+str(i),[card('Bug row',0,0,870,140,'#FFFFFF',20),text('Bug text',bug,26,24,33,INK,w=470,bold=True),chip(owner,520,42,315,bg,tc,start=68,end=76)],105,560+i*170); reveal(row,.3+i*.55); a.append(row)
question=group('Debug rule',[card('Rule card',0,0,870,180,DARK,22),text('Rule label','DEBUGGING QUESTION',28,23,20,'#AAB6CE',w=420,bold=True),text('Rule text','Which layer owns this problem?',28,69,38,'#FFFFFF',w=800,bold=True)],105,1095); reveal(question,2.2); a.append(question)
scene('S08 Debug right layer',a,68,76)

# Approved presenter remains a supporting guide.
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
    ids.add(o['id']); o['activeRange']={'start':0,'duration':76000}
    for ch in o.get('layers',[]): extend(ch)
extend(presenter)
presenter['transform']['position']=[32,1280]
layers.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[32,1625]),(.7,[32,1280])])
keys(arm,'rotation',[(0,18),(.9,-10),(6,-22),(9,-8),(14,-18),(19,-8),(24,-20),(29,-6),(34,-17),(39,-8),(44,-20),(49,-9),(54,-19),(59,-7),(64,-22),(69,-7),(74,-18)])
notes=[
 (0,8,'LOOK BEHIND THE UI','The screen sits on\nfour hidden layers.'),
 (8,18,'LAYER 1','Buttons, forms,\nscreens and feedback.'),
 (18,28,'LAYER 2','Rules decide what\nhappens next.'),
 (28,38,'LAYER 3','Requests are validated\nand coordinated.'),
 (38,48,'LAYER 4','Identity, permissions\nand data live here.'),
 (48,58,'LAYER 5','Deployment, config\nand runtime health.'),
 (58,68,'FOLLOW THE REQUEST','One action travels\nthrough the stack.'),
 (68,76,'DEBUG SMARTER','Find the layer that\nowns the failure.')
]
for st,en,label,body in notes:
    g=group('Presenter note',[text('Stage',label,640,1372,22,BLUE,w=350,bold=True),text('Body',body,640,1420,31,INK,w=350)],start=st,end=en); enter(g); layers.append(g)

doc['composition']={'id':'main','name':'V05 Five Layers / full visual draft','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(actions,open(HERE.parent/'animation.json','w'),indent=2)
print('V05 full visual layers',uid,'animation actions',len(actions))
