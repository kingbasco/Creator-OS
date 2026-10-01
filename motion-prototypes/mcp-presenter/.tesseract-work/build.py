import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
doc=json.load(open(ROOT/'.tesseract-work/base.json')); doc['duration']=15
layers=[]; actions=[]; uid=0
BG='#F7F8FA';INK='#101724';MUT='#687385';BLUE='#5B6CFF';SOFT='#EEF0FF';SKIN='#A96543';LIGHT='#C8845C';HAIR='#192330'
def col(h):return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def trans(x=0,y=0):return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def base(t,n,x=0,y=0,start=0,end=15):
 global uid;uid+=1
 return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(start*1000),'duration':int((end-start)*1000)},transform=trans(x,y))
def rect(n,x,y,w,h,c,r=0,start=0,end=15):
 o=base('Rect',n,x,y,start,end);o['rect']=dict(size=[w,h],fillColor=col(c),roundness=r);return o

def text(n,s,x,y,size=40,c=INK,w=900,start=0,end=15,bold=False):
 o=base('Text',n,x,y,start,end);o['sourceText']=dict(text=s,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=size,fillColor=col(c),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=size*1.12);return o

def path(n,cmd,c=None,stroke=None,width=3,start=0,end=15):
 o=base('Shape',n,start=start,end=end);o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
 if c:o['shape']['fills']=[dict(paint={'type':'solid','color':col(c)},fillRule='nonZeroWinding',blendMode='normal',opacity=100)]
 if stroke:o['shape']['strokes']=[dict(paint={'type':'solid','color':col(stroke)},width=width,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]
 return o

def M(x,y):return dict(type='moveTo',x=x,y=y)
def L(x,y):return dict(type='lineTo',x=x,y=y)
def C(a,b,c,d,x,y):return dict(type='cubicTo',c1x=a,c1y=b,c2x=c,c2y=d,x=x,y=y)
def Z():return dict(type='close')
def ellipse(n,x,y,rx,ry,c):
 k=.55228475
 return path(n,[M(x+rx,y),C(x+rx,y+k*ry,x+k*rx,y+ry,x,y+ry),C(x-k*rx,y+ry,x-rx,y+k*ry,x-rx,y),C(x-rx,y-k*ry,x-k*rx,y-ry,x,y-ry),C(x+k*rx,y-ry,x+rx,y-k*ry,x+rx,y),Z()],c)
def group(n,children,x=0,y=0,start=0,end=15):
 o=base('Group',n,x,y,start,end);o['layers']=children[::-1];return o

def anim(o,prop,expr):
 actions.append(dict(type='setFxPropertyAnimator',compositionId='main',property={'layerId':o['id'],'propertyType':prop},animator={'type':'jsScript','layerTimeJsCode':expr},dependencies=[]))
def keys(o,prop,values):
 if prop in ['position','scale']:
  for axis,ix in [('X',0),('Y',1)]:keys(o,prop+axis,[(t,v[ix]) for t,v in values])
  return
 typ='vector2' if isinstance(values[0][1],list) else 'float'
 actions.append(dict(type='setFxPropertyKeyframes',compositionId='main',property={'layerId':o['id'],'propertyType':prop},keyframes=[dict(id=f'{o["id"]}-{prop}-{i}',layerTime=int(t*1000),value={'type':typ,'value':v},easing={'type':'cubicBezier','x1':.22,'y1':1,'x2':.36,'y2':1}) for i,(t,v) in enumerate(values)]))
def enter(o,delay=0):
 anim(o,'opacity',f'return Math.min(100,Math.max(0,(input.time.seconds-{delay})*400));')

def card(n,x,y,w,h,c='#FFFFFF',r=26):
 o=rect(n,x,y,w,h,c,r);o['dropShadow']=dict(color=[.05,.08,.14,.12],blurRadius=28,spreadRadius=0,offset=[0,14],blendMode='normal');return o
# Environment
layers.append(rect('Canvas',0,0,1080,1920,BG))
for y in [440,1210,1730]:layers.append(rect('Editorial rule',80,y,920,2,'#E5E8EE'))
layers.append(text('Brand','creator os',80,82,28,INK,bold=True))
layers.append(text('Topic','MCP / A VISUAL EXPLAINER',570,88,22,MUT,w=450))
for start,end,a,b in [(0,4.4,'Your AI needs','more than a prompt.'),(4.4,9.8,'A shared way','to reach your tools.'),(9.8,15,'The right context.','Back in the answer.')]:
 h=group('Editorial headline',[text('Headline',a,80,190,70,INK,bold=True),text('Emphasis',b,80,274,66,BLUE,bold=True)],start=start,end=end)
 enter(h);layers.append(h)
# Chat UI, stays same object and reframes
chat=[]
chat.append(card('AI app surface',0,0,880,620))
chat.append(rect('Header rule',0,92,880,2,'#EBEDF2'))
chat.append(ellipse('AI app emblem',48,47,14,14,BLUE))
chat.append(text('App title','Assistant',78,26,29,INK,bold=True))
chat.append(text('App status','Workspace connected',526,31,23,MUT,w=330))
chat.append(rect('Prompt bubble',40,140,800,115,SOFT,20))
prompt=text('Typed request','',65,169,35,INK,w=740);chat.append(prompt)
anim(prompt,'textContent',"const s='Find the latest project brief.';return s.slice(0,Math.floor(Math.max(0,input.time.seconds-.65)*22));")
chat.append(text('Tool label','AVAILABLE TOOL',44,297,21,MUT))
chat.append(rect('Tool chip',40,339,445,67,'#F1F3F6',12))
chat.append(text('Tool name','files.search',62,351,30,INK,bold=True))
chat.append(text('Tool description','Search connected project documents',45,435,29,MUT,w=780))
chat.append(text('Tool access','Uses the access you have granted.',45,494,24,MUT,w=780))
gchat=group('AI application',chat,100,510);layers.append(gchat)
keys(gchat,'scale',[(0,[100,100]),(4,[100,100]),(4.8,[53,53]),(9.2,[53,53]),(10,[100,100])])
keys(gchat,'position',[(0,[100,555]),(.55,[100,510]),(4,[100,510]),(4.8,[80,520]),(9.2,[80,520]),(10,[100,510])])
# Server service right, slide in
service=[]
service.append(card('Connected service',0,0,350,328,INK))
service.append(text('Service heading','PROJECT FILES',29,28,22,'#A7B1C4',w=300))
service.append(rect('File symbol',32,94,60,76,'#DDE2FF',9))
for y,w in [(112,33),(126,24),(140,31)]:service.append(rect('File line',45,y,w,4,BLUE,2))
service.append(text('File title','Project brief',113,95,28,'#FFFFFF',w=230,bold=True))
service.append(text('File version','Updated today',113,140,21,'#A7B1C4',w=240))
service.append(rect('Server badge',28,233,294,55,'#283349',10))
service.append(text('MCP server label','MCP server',78,243,26,'#DDE2FF',w=250))
gservice=group('MCP file server',service,650,520,start=4.5,end=10);enter(gservice);layers.append(gservice)
keys(gservice,'position',[(0,[1120,520]),(.55,[650,520]),(4.6,[650,520]),(5.4,[1120,520])])
# route loops drawn as native strokes
route=path('Request and return route',[M(315,863),L(315,1010),C(315,1050,360,1050,405,1050),L(755,1050),C(800,1050,825,1030,825,990),L(825,860)],stroke='#CED4E2',width=5,start=4.8,end=9.8)
layers.append(route)
label=text('Connection label','MCP',476,1074,29,BLUE,start=4.8,end=9.8,bold=True);enter(label);layers.append(label)
# request pill crosses route in 1.2 seconds
packet=group('Tool request',[rect('Request body',-80,-25,160,50,BLUE,25),text('Request text','search',-48,-17,25,'#FFFFFF',w=130)],start=5.5,end=7.5)
keys(packet,'position',[(0,[315,850]),(.35,[315,1050]),(1.05,[825,1050]),(1.5,[825,840])]);layers.append(packet)
# returned document card follows opposite direction
returned=group('Returned document',[card('Document card',-94,-63,188,126),rect('File accent',-76,-43,8,86,BLUE,4),text('Document name','Brief',-50,-43,26,INK,w=130,bold=True),rect('Document rule',-50,4,110,5,'#CDD3DF',2),rect('Document rule short',-50,21,79,5,'#CDD3DF',2)],start=7.5,end=9.9)
keys(returned,'position',[(0,[825,790]),(.45,[825,1050]),(1.45,[315,1050]),(2.3,[315,735])]);layers.append(returned)
# returned result overlays existing lower portion of chat after reframe
result=[]
result.append(rect('Answer background',34,276,812,309,'#FFFFFF',14))
result.append(rect('Result chip',43,294,248,51,'#E9F7EF',10))
result.append(text('Result status','DOCUMENT FOUND',59,306,20,'#167749',w=245,bold=True))
result.append(text('Answer heading','Here’s your project brief.',43,369,38,INK,w=790,bold=True))
result.append(text('Answer description','Launch scope, milestones and\nowners — ready to reference.',43,432,30,MUT,w=770))
result.append(text('Citation','[1] Project brief · connected files',43,541,22,BLUE,w=780))
gresult=group('Answer with source',result,100,510,start=10.05,end=15);enter(gresult);layers.append(gresult)
# human presenter, original vector illustration
p=[]
p.append(ellipse('Ground shadow',250,491,207,22,'#E1E5EE'))
p.append(path('Overshirt',[M(105,494),L(119,300),C(125,245,177,225,231,225),L(287,225),C(350,234,380,260,391,319),L(410,494),Z()],'#334769'))
p.append(path('T shirt',[M(217,243),L(281,243),L(310,493),L(190,493),Z()],'#F7F2E9'))
p.append(rect('Shirt seam',321,330,3,160,'#526686',1))
p.append(rect('Pocket',330,344,43,40,'#263B5D',5))
p.append(rect('Neck',220,183,61,91,SKIN,20))
p.append(path('Neck shade',[M(219,203),L(281,203),L(281,233),C(250,251,228,240,219,230),Z()],'#854C35'))
# head group with pivot under chin
head=[]
head.append(ellipse('Left ear',165,137,21,32,SKIN));head.append(ellipse('Right ear',329,137,21,32,SKIN))
head.append(rect('Face silhouette',172,53,151,180,LIGHT,60))
head.append(path('Face side shade',[M(292,78),C(333,120,326,194,285,218),C(312,178,309,106,292,78),Z()],SKIN))
head.append(path('Hair',[M(169,121),C(135,28,174,12,213,18),C(247,-3,320,17,330,55),L(323,132),L(305,113),L(301,73),C(253,88,216,79,194,65),L(188,119),Z()],HAIR))
head.append(path('Hair light',[M(180,48),C(203,15,267,13,304,44),C(262,34,221,40,180,48),Z()],'#2C384A'))
for x in [205,277]:
 head.append(path('Eyebrow',[M(x-10,117),C(x,111,x+11,111,x+19,116)],stroke=HAIR,width=7))
 eye=ellipse('Eye',x+3,139,7,10,HAIR);head.append(eye)
 anim(eye,'opacity',"return (input.time.seconds%3.7>3.58)?0:100;")
head.append(path('Nose',[M(245,134),L(239,163),C(242,168,251,167,256,163)],stroke='#8F5038',width=4))
head.append(path('Smile',[M(221,187),C(235,200,260,203,277,182),C(252,189,239,189,221,187),Z()],'#FFFFFF'))
head.append(path('Jaw detail',[M(203,204),C(224,228,271,233,296,204)],stroke='#633E32',width=5))
ghead=group('Head / tilt and expression',head);ghead['transform']['anchorPoint']=[249,228];ghead['transform']['position']=[249,228];p.append(ghead)
anim(ghead,'rotation','return -3+Math.sin(input.time.seconds*1.2)*2;')
# resting arm left
p.append(path('Resting sleeve',[M(125,280),C(88,308,91,391,98,441),L(142,446),L(173,313),Z()],'#405779'))
p.append(path('Resting hand',[M(99,428),L(145,433),L(168,476),C(167,495,137,503,120,479),Z()],LIGHT))
# pointing arm right pivots at shoulder
arm=[]
arm.append(path('Raised sleeve',[M(345,274),C(364,280,392,307,405,321),L(466,282),L(495,321),L(414,379),C(391,390,367,372,344,350),Z()],'#405779'))
arm.append(path('Forearm',[M(465,284),L(492,242),L(520,256),L(497,321),Z()],LIGHT))
arm.append(path('Pointing hand',[M(490,250),L(494,214),L(484,183),C(482,169,496,165,502,178),L(516,211),C(546,195,558,214,548,235),L(522,260),Z()],LIGHT))
arm.append(path('Finger detail',[M(516,211),L(524,232)],stroke=SKIN,width=4))
garm=group('Pointing arm',arm);garm['transform']['anchorPoint']=[348,291];garm['transform']['position']=[348,291];p.append(garm)
keys(garm,'rotation',[(0,23),(.9,-8),(3,0),(4.6,-22),(7,2),(10,-16),(12,-5),(14.5,-5)])
presenter=group('Original Creator OS presenter',p,56,1240);layers.append(presenter)
keys(presenter,'position',[(0,[56,1610]),(.7,[56,1240]),(4,[56,1240]),(4.8,[56,1280]),(10,[56,1280]),(10.7,[56,1240])])
# concise explanation next to presenter
for st,en,title,body in [(0,4.4,'ASK','“Find my project brief.”'),(4.4,9.8,'CONNECT','A tool request goes out.\nA document comes back.'),(9.8,15,'USE THE RESULT','The assistant can now\nanswer with context.')]:
 g=group('Presenter side annotation',[text('Stage title',title,655,1360,23,BLUE,w=350,bold=True),text('Stage explanation',body,655,1415,34,INK,w=350)],start=st,end=en);enter(g);layers.append(g)
layers.append(text('End note','A connection protocol. Not another AI model.',80,1786,28,MUT,w=940,start=11.6,end=15))
doc['composition']['name']='MCP — ask, connect, return';doc['composition']['layers']=layers[::-1]
json.dump(doc,open(ROOT/'.tesseract-work/document.json','w'),indent=2)
json.dump(actions,open(ROOT/'.tesseract-work/animation.json','w'),indent=2)
print('Native layers:',uid,'Animation tracks:',len(actions))
