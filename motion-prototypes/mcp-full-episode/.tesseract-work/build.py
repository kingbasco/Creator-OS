import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
doc=json.load(open(ROOT/'.tesseract-work/approved-presenter.json')); doc['duration']=78
layers=[]; actions=[]; uid=100
BG='#F7F8FA';INK='#101724';MUT='#687385';BLUE='#5B6CFF';SOFT='#EEF0FF';SKIN='#A96543';LIGHT='#C8845C';HAIR='#192330'
def col(h):return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def trans(x=0,y=0):return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def base(t,n,x=0,y=0,start=0,end=78):
 global uid;uid+=1
 return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(start*1000),'duration':int((end-start)*1000)},transform=trans(x,y))
def rect(n,x,y,w,h,c,r=0,start=0,end=78):
 o=base('Rect',n,x,y,start,end);o['rect']=dict(size=[w,h],fillColor=col(c),roundness=r);return o

def text(n,s,x,y,size=40,c=INK,w=900,start=0,end=78,bold=False):
 o=base('Text',n,x,y,start,end);o['sourceText']=dict(text=s,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=size,fillColor=col(c),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=size*1.12);return o

def path(n,cmd,c=None,stroke=None,width=3,start=0,end=78):
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
def group(n,children,x=0,y=0,start=0,end=78):
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
# Full episode: scene clocks follow the existing 78-second V04 script.
import copy
proto=copy.deepcopy(doc)
layers=[rect('Canvas',0,0,1080,1920,BG)]
for y in [430,1240,1730]:layers.append(rect('Editorial rule',80,y,920,2,'#E5E8EE'))

def reveal(o,t=.2,dy=35):
 x,y=o['transform']['position'];keys(o,'position',[(0,[x,y+dy]),(t+.5,[x,y])]);enter(o,t)
def scene(n,children,start,end):
 g=group(n,children,start=start,end=end);layers.append(g);return g

def title(a,b,st,en):
 g=group('Headline',[text('Lead',a,80,180,68,INK,bold=True),text('Emphasis',b,80,267,65,BLUE,bold=True)],start=st,end=en);reveal(g,0,18);layers.append(g)
def chip(label,x,y,w=230,c=SOFT,tc=BLUE):
 return group(label,[rect('Chip',0,0,w,56,c,12),text('Chip label',label,18,12,25,tc,w=w-20,bold=True)],x,y)
def fileicon(x,y,scale=1):
 g=group('Document icon',[rect('Paper',0,0,62,80,'#DDE2FF',8),rect('Line one',13,21,36,5,BLUE,2),rect('Line two',13,34,27,5,BLUE,2),rect('Line three',13,47,33,5,BLUE,2)],x,y);g['transform']['scale']=[scale*100]*2;return g

def connector(x1,y1,x2,y2,c='#B9C2D3',width=4):
 return path('Connection',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=c,width=width)
def dot(x,y,c=BLUE):return ellipse('Signal',x,y,9,9,c)
# 01: hub assembles from tools, then a common connector takes focus.
title('Your AI. Your tools.','One connection pattern.',0,8)
a=[]
a.append(card('Central AI app',312,680,455,220,INK))
a.append(text('AI app heading','AI application',350,718,43,'#FFFFFF',w=410,bold=True))
a.append(text('AI app subheading','Connect to useful context',350,785,27,'#ADB9D0',w=410))
for i,(x,y,label) in enumerate([(90,492,'Files'),(720,495,'Database'),(725,1015,'Services')]):
 a.append(connector(x+110,y+85,540,680 if y<700 else 900))
 tile=group(label,[card('Tool surface',0,0,225,143),text('Tool title',label,25,79,30,INK,w=200,bold=True),fileicon(27,15,.53)],x,y);reveal(tile,.45+i*.3);a.append(tile)
 sig=dot(0,0);keys(sig,'position',[(0,[x+110,y+85]),(2+i*.3,[x+110,y+85]),(3.5+i*.3,[540,680 if y<700 else 900]),(7,[540,680 if y<700 else 900])]);a.append(sig)
a.append(chip('MCP',430,940,220));scene('01 / One pattern',a,0,8)
# 02: opening the host makes the embedded client visible, server stays outside.
title('Three parts.','Clear roles.',8,18)
a=[card('Host application',85,500,545,610),text('Host title','AI application',120,542,43,INK,w=460,bold=True),text('Host explainer','The host',122,606,29,MUT,w=440)]
client=group('Client inside host',[rect('Client panel',0,0,440,230,SOFT,24),text('Client title','MCP client',33,35,42,BLUE,w=390,bold=True),text('Client subtitle','Manages the connection',33,104,29,MUT,w=380)],138,762);reveal(client,1);a.append(client)
a.append(connector(575,870,721,870,BLUE,5))
server=group('External server',[card('Server panel',0,0,285,265,INK),text('Server title','MCP\nserver',30,37,43,'#FFFFFF',w=240,bold=True),text('Server subtitle','Exposes tools',30,169,26,'#ADB9D0',w=240)],715,742);reveal(server,2);a.append(server)
a.append(text('Boundary note','Inside your AI app',125,1047,27,MUT,w=475))
a.append(text('Server note','Connected system',715,1047,23,MUT,w=295))
scene('02 / Host client server',a,8,18)
# 03: discover list -> select tool -> input schema.
title('Before it calls a tool,','it discovers the options.',18,28)
a=[card('Tool catalog',85,505,910,660,INK),text('Catalog title','Available tools',120,541,44,'#FFFFFF',w=740,bold=True)]
for i,(label,desc) in enumerate([('files.search','Find documents in your workspace'),('files.read','Read a selected document'),('calendar.list','List upcoming events')]):
 row=group('Tool row '+label,[rect('Row',0,0,835,105,'#202C40',16),text('Name',label,23,15,34,'#FFFFFF',w=680,bold=True),text('Description',desc,23,61,23,'#B6C0D3',w=750)],123,627+i*126);reveal(row,.4+i*.3);a.append(row)
 # lower rows make room for the selected schema
 if i>0:keys(row,'opacity',[(0,0),(.8+i*.3,100),(4,100),(4.5,0)])
selected=group('Selected tool input',[rect('Input schema',0,0,835,263,'#EDF0FF',18),text('Schema heading','files.search',25,20,36,BLUE,w=700,bold=True),text('Schema description','Input required',25,80,27,MUT,w=700),rect('Input field',24,133,784,76,'#FFFFFF',12),text('Input definition','query  :  string',44,151,30,INK,w=735)],123,778,start=4.5,end=10);reveal(selected,0);a.append(selected)
scene('03 / Discover capabilities',a,18,28)
# 04: exact user query becomes named tool call; outbound packet crosses line.
title('You ask a question.','A tool call goes out.',28,38)
a=[card('Prompt composer',85,505,910,265),text('Composer label','YOUR REQUEST',121,538,24,MUT,w=700),rect('Composer input',120,598,842,100,SOFT,16)]
t=text('Typed prompt','',143,625,38,INK,w=790);anim(t,'textContent',"return 'Find the latest project brief.'.slice(0,Math.floor(Math.max(0,input.time.seconds-.5)*20));");a.append(t)
request=group('Tool call packet',[card('Tool call surface',0,0,610,232,INK),text('Call label','TOOL CALL',27,25,23,'#AAB6CE',w=500),text('Call name','files.search',27,68,42,'#FFFFFF',w=550,bold=True),text('Query parameter','query: “project brief”',27,141,30,'#CDD4E4',w=550)],85,867,start=2.8,end=10);reveal(request,0);a.append(request)
a.append(connector(696,984,827,984,BLUE,5))
a.append(group('Destination',[rect('Server tile',0,0,165,160,SOFT,24),text('Server label','MCP\nserver',25,31,31,BLUE,w=130,bold=True)],828,903))
signal=dot(0,0);keys(signal,'position',[(0,[698,984]),(4,[698,984]),(5.5,[830,984]),(9,[830,984])]);enter(signal,4);a.append(signal)
scene('04 / Send request',a,28,38)
# 05: connected system returns brief, expanding into grounded answer.
title('The tool finds the file.','The result comes back.',38,48)
a=[card('Result app',85,505,910,663),text('Result heading','Assistant',123,540,37,INK,w=790,bold=True)]
for i,(name,date) in enumerate([('Meeting notes','Yesterday'),('Project brief','Today'),('Brand assets','Last week')]):
 row=group('Search match '+name,[rect('Document row',0,0,834,109,SOFT if i==1 else '#F2F4F7',16),fileicon(18,14,.8),text('Document title',name,91,19,33,BLUE if i==1 else INK,w=590,bold=True),text('Updated',date,92,66,22,MUT,w=590)],123,627+i*132)
 keys(row,'opacity',[(0,0),(.5+i*.25,100),(3,100),(3.5,0)]);a.append(row)
answer=group('Answer with citation',[rect('Answer panel',0,0,834,447,'#FFFFFF',14),chip('DOCUMENT FOUND',0,4,278,'#E9F7EF','#167749'),text('Answer','Here’s your project brief.',0,94,43,INK,w=810,bold=True),text('Answer detail','Launch scope, milestones\nand owners — ready to reference.',0,180,35,MUT,w=810),chip('[1] Project brief',0,322,340)],123,635,start=3.5,end=10);reveal(answer,0);a.append(answer)
scene('05 / Return and use',a,38,48)
# 06: same center protocol routes to three specific implementations.
title('One shared protocol.','Different capabilities.',48,58)
a=[]
center=group('Protocol hub',[card('Hub',0,0,418,208,INK),text('Hub title','MCP',134,41,68,'#FFFFFF',w=330,bold=True),text('Hub subtitle','The exchange format',49,135,26,'#AAB6CE',w=380)],331,505);a.append(center)
for i,(x,label,tool) in enumerate([(85,'Files','search / read'),(400,'Database','query'),(715,'Services','specific actions')]):
 a.append(connector(540,714,x+140,890,BLUE,4))
 tile=group(label,[card('System panel',0,0,280,268),fileicon(106,29,.8),text('System name',label,26,133,35,INK,w=250,bold=True),text('Specific capability',tool,26,193,24,MUT,w=245)],x,884);reveal(tile,.5+i*.35);a.append(tile)
 signal=dot(0,0);keys(signal,'position',[(0,[540,714]),(1+i*.5,[540,714]),(2.5+i*.5,[x+140,890]),(8,[x+140,890])]);a.append(signal)
scene('06 / Connected systems',a,48,58)
# 07: metadata is explicit, access boundary independently gates the action.
title('A common protocol.','Real access controls.',58,68)
a=[card('Request envelope',85,495,910,330),text('Envelope title','Each request carries metadata',120,528,37,INK,w=850,bold=True),chip('Protocol version',120,610,378),chip('Request details',521,610,378),text('Specification note','July 2026 core: stateless requests',121,730,27,MUT,w=840)]
gate=group('Permissions gate',[card('Access controls',0,0,910,304,INK),text('Access question','What may this tool do?',35,28,39,'#FFFFFF',w=840,bold=True),chip('Read approved files',35,105,532,'#E6F6EC','#177548'),chip('Sensitive action',35,185,430,'#3D3140','#F3CDA7'),text('Control outcome','Needs controls',510,205,27,'#F3CDA7',w=360)],85,858);reveal(gate,2);a.append(gate)
scene('07 / Permissions remain',a,58,68)
# 08: model and server are distinct; transition to next episode's app layers.
title('Tools around your AI.','That’s the connection.',68,78)
a=[card('Model tile',85,506,390,240),text('Model title','AI model',119,550,48,INK,w=350,bold=True),text('Model role','Reasons with context',119,631,28,MUT,w=330),card('Server tile',605,506,390,240,INK),text('Server title','MCP server',639,550,44,'#FFFFFF',w=350,bold=True),text('Server role','Exposes capabilities',639,631,27,'#B4BFD4',w=335),connector(477,629,605,629,BLUE,5)]
nextlabel=text('Next episode','NEXT: BEHIND THE SCREEN',85,829,26,BLUE,w=875,bold=True);a.append(nextlabel)
for i,(name,c) in enumerate([('Interface','#FFFFFF'),('Application logic',SOFT),('Data + services','#DDE2FF')]):
 tile=group('App layer '+name,[card('Layer',0,0,760,88,c,16),text('Layer name',name,25,22,32,INK,w=700,bold=True)],130,906+i*97)
 keys(tile,'position',[(0,[130,1010]),(3,[130,1010]),(4+i*.2,[130,906+i*97])]);enter(tile,3+i*.2);a.append(tile)
scene('08 / Tools around AI',a,68,78)
# Same approved presenter, preserved identity and layer IDs.
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def extend(o):
 ids.add(o['id']);o['activeRange']={'start':0,'duration':78000}
 for ch in o.get('layers',[]):extend(ch)
extend(presenter)
presenter['transform']['position']=[56,1250]
layers.append(presenter)
# Preserve eye/head behaviors, replace only long-form gesture/entrance timing.
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm')
dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[56,1620]),(.7,[56,1250])])
keys(arm,'rotation',[(0,20),(.9,-8),(6,0),(8.5,-22),(12,4),(17,-4),(20,-18),(25,4),(29,-15),(33,0),(39,-20),(44,0),(49,-19),(54,4),(60,-24),(65,2),(69,-12),(74,0),(77,0)])
# Presenter explains one concise supporting point at a time.
notes=[(0,8,'CONNECT','AI applications,\ntools and data.'),(8,18,'THREE ROLES','The host manages\nits MCP client.'),(18,28,'DISCOVER','Read descriptions\nand required inputs.'),(28,38,'CALL','Send a named tool\nand its search query.'),(38,48,'USE CONTEXT','Use the returned\nfile in the answer.'),(48,58,'IMPLEMENT','Each server provides\nits own capabilities.'),(58,68,'LIMIT ACCESS','MCP does not grant\nunlimited access.'),(68,78,'REMEMBER','A server is a program\nexposing capabilities.')]
for st,en,label,body in notes:
 g=group('Presenter annotation',[text('Stage',label,650,1380,24,BLUE,w=355,bold=True),text('Explanation',body,650,1433,32,INK,w=355)],start=st,end=en);enter(g);layers.append(g)
doc['composition']={'id':'main','name':'V04 MCP / full visual draft','layers':layers[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(ROOT/'.tesseract-work/document.json','w'),indent=2)
json.dump(actions,open(ROOT/'.tesseract-work/animation.json','w'),indent=2)
print('Created full episode; new highest layer ID',uid,'animation actions',len(actions))
