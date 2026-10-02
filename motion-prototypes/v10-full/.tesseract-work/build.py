import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text()); doc['duration']=80
L=[]; A=[]; uid=2100
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; PURPLE='#EEE9FF'; PI='#6A4BC4'; AMBER='#FFF4DC'; AI='#956515'; RED='#FDEBEC'; RI='#B33A42'; DARK='#1C2738'; BORDER='#E5E8EE'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=80):
 global uid; uid+=1; return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
def rect(n,x,y,w,h,col,r=0,s=0,e=80):
 o=b('Rect',n,x,y,s,e); o['rect']=dict(size=[w,h],fillColor=c(col),roundness=r); return o
def txt(n,v,x,y,z=30,col=INK,w=800,s=0,e=80,bold=False):
 o=b('Text',n,x,y,s,e); o['sourceText']=dict(text=v,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=z,fillColor=c(col),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,280],leading=z*1.12); return o
def path(n,cmd,col=None,stroke=None,width=3,s=0,e=80):
 o=b('Shape',n,s=s,e=e); o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
 if col:o['shape']['fills']=[dict(paint={'type':'solid','color':c(col)},fillRule='nonZeroWinding',blendMode='normal',opacity=100)]
 if stroke:o['shape']['strokes']=[dict(paint={'type':'solid','color':c(stroke)},width=width,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]
 return o
def M(x,y): return dict(type='moveTo',x=x,y=y)
def C(a,b,cx,d,x,y): return dict(type='cubicTo',c1x=a,c1y=b,c2x=cx,c2y=d,x=x,y=y)
def grp(n,ch,x=0,y=0,s=0,e=80):
 o=b('Group',n,x,y,s,e); o['layers']=ch[::-1]; return o
def card(n,x,y,w,h,col='#FFFFFF',r=22,s=0,e=80):
 o=rect(n,x,y,w,h,col,r,s,e); o['dropShadow']=dict(color=[.05,.08,.14,.12],blurRadius=24,spreadRadius=0,offset=[0,12],blendMode='normal'); return o
def anim(o,p,code): A.append(dict(type='setFxPropertyAnimator',compositionId='main',property={'layerId':o['id'],'propertyType':p},animator={'type':'jsScript','layerTimeJsCode':code},dependencies=[]))
def keys(o,p,vals):
 if p in ['position','scale']:
  for ax,ix in [('X',0),('Y',1)]: keys(o,p+ax,[(t,v[ix]) for t,v in vals])
  return
 typ='vector2' if isinstance(vals[0][1],list) else 'float'
 A.append(dict(type='setFxPropertyKeyframes',compositionId='main',property={'layerId':o['id'],'propertyType':p},keyframes=[dict(id=f'{o["id"]}-{p}-{i}',layerTime=int(t*1000),value={'type':typ,'value':v},easing={'type':'cubicBezier','x1':.22,'y1':1,'x2':.36,'y2':1}) for i,(t,v) in enumerate(vals)]))
def enter(o,d=0): anim(o,'opacity',f'return Math.min(100,Math.max(0,(input.time.seconds-{d})*400));')
def reveal(o,d=0,dy=28): x,y=o['transform']['position']; keys(o,'position',[(0,[x,y+dy]),(.55,[x,y])]); enter(o,d)
def chip(v,x,y,w,col,tc,s=0,e=80): return grp(v,[rect('bg',0,0,w,52,col,12,s,e),txt('t',v,17,11,22,tc,w-24,s,e,True)],x,y,s,e)
def conn(x1,y1,x2,y2,col=BLUE,w=4,s=0,e=80): return path('Connector',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=col,width=w,s=s,e=e)
def scene(n,ch,s,e): L.append(grp(n,ch,s=s,e=e))
def title(a,b,s,e):
 g=grp('Headline',[txt('l',a,80,182,64,INK,900,s,e,True),txt('e',b,80,265,59,BLUE,900,s,e,True)],s=s,e=e); reveal(g); L.append(g)
proto=copy.deepcopy(doc)
L=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,BORDER),rect('Rule',80,1225,920,2,BORDER),rect('Rule',80,1730,920,2,BORDER)]

# S01 one vs many
title('One task can use','one agent or several.',0,8)
a=[]
one=grp('One agent',[card('c',0,0,350,300,SOFT),chip('ONE AGENT',25,24,190,'#FFFFFF',BLUE,0,8),txt('t','Goal\n→ work\n→ review',25,105,36,INK,280,bold=True)],105,570); reveal(one,.2); a.append(one)
many=grp('Many agents',[card('c',0,0,450,300,'#FFFFFF'),chip('ORCHESTRATOR + SUBAGENTS',25,24,350,DARK,'#FFFFFF',0,8),txt('t','Goal → delegate\n→ parallel work\n→ integrate',25,105,34,INK,380,bold=True)],525,570); reveal(many,.5); a.append(many)
a.append(grp('rule',[card('c',0,0,820,135,DARK),txt('t','The architecture should follow the task — not a fixed number of agents.',28,46,29,'#FFFFFF',760,bold=True)],130,1010))
scene('S01 One vs many',a,0,8)

# S02 orchestrator
title('The orchestrator','keeps the whole goal.',8,18)
a=[]
orch=grp('Orchestrator',[card('c',0,0,760,330,DARK),chip('ORCHESTRATOR',30,28,240,'#2B3850','#DCE3F3',8,18),txt('goal','GOAL',30,110,20,'#AAB6CE',150,bold=True),txt('g','Ship participant email editing safely',30,150,36,'#FFFFFF',680,bold=True),txt('owns','Owns scope · delegation · integration',30,236,27,'#DCE3F3',680)],160,545); reveal(orch,.2); a.append(orch)
for i,(lab,x) in enumerate([('SCOPE',165),('DELEGATE',400),('TRACK',630),('INTEGRATE',815)]):
 a.append(chip(lab,x,970,180,SOFT,BLUE,8,18))
scene('S02 Orchestrator',a,8,18)

# S03 delegate
title('Delegate','focused subtasks.',18,28)
a=[]
orch=grp('Orch',[card('c',0,0,360,190,DARK),txt('l','ORCHESTRATOR',26,24,20,'#AAB6CE',220,bold=True),txt('t','One shared goal',26,73,35,'#FFFFFF',270,bold=True)],360,520); reveal(orch,.2); a.append(orch)
agents=[('RESEARCH','Current behavior',80,850,GREEN,GI),('FRONTEND','Edit UI',310,850,SOFT,BLUE),('BACKEND','Update API',555,850,AMBER,AI),('TESTS','Verify flow',805,850,PURPLE,PI)]
for i,(name,sub,x,y,bg,tc) in enumerate(agents):
 w=195
 ag=grp(name,[card('c',0,0,w,160,bg),txt('n',name,20,22,22,tc,w-40,bold=True),txt('s',sub,20,67,21,INK,w-40)],x,y); reveal(ag,.4+i*.16); a.append(ag); a.append(conn(540,710,x+w/2,y,BLUE,3,18,28))
a.append(chip('SMALLER CONTEXTS',390,1080,300,GREEN,GI,18,28))
scene('S03 Delegate',a,18,28)

# S04 parallel work
title('Independent work','can run in parallel.',28,38)
a=[]
names=['Research','Frontend','Backend','Tests']; cols=[GREEN,SOFT,AMBER,PURPLE]; tcs=[GI,BLUE,AI,PI]
for i,(name,bg,tc) in enumerate(zip(names,cols,tcs)):
 y=530+i*145
 row=grp('row'+name,[card('c',0,0,820,105,'#FFFFFF'),txt('n',name,25,28,27,INK,180,bold=True),rect('track',220,40,430,22,'#E6E9EF',11),chip('RUNNING',675,26,120,bg,tc,28,38)],130,y); reveal(row,.15+i*.12); a.append(row)
 fill=rect('fill'+name,350,y+40,430,22,bg,11,28,38); keys(fill,'scale',[(0,[0,100]),(1.2+i*.2,[0,100]),(5.2+i*.2,[100,100])]); a.append(fill)
done=grp('done',[card('c',0,0,820,135,GREEN),txt('t','4 focused tasks finished in the same working window.',28,44,30,INK,760,bold=True)],130,1120); keys(done,'opacity',[(0,0),(6.4,0),(6.8,100)]); a.append(done)
scene('S04 Parallel',a,28,38)

# S05 coordination conflict
title('Parallel work creates','coordination problems.',38,48)
a=[]
front=grp('Frontend output',[card('c',0,0,380,310,SOFT),chip('FRONTEND',25,24,170,'#FFFFFF',BLUE,38,48),txt('l','Expects',25,100,20,MUT,120,bold=True),txt('t','PATCH /participants/:id\n{ email }',25,142,29,INK,320,bold=True)],100,555); reveal(front,.2); a.append(front)
back=grp('Backend output',[card('c',0,0,380,310,AMBER),chip('BACKEND',25,24,170,'#FFFFFF',AI,38,48),txt('l','Implements',25,100,20,MUT,120,bold=True),txt('t','PUT /participants/:id\n{ newEmail }',25,142,29,INK,320,bold=True)],600,555); reveal(back,.5); a.append(back)
conf=grp('Conflict',[card('c',0,0,180,115,RED),txt('t','CONFLICT',26,40,26,RI,130,bold=True)],450,850); keys(conf,'opacity',[(0,0),(2.5,0),(2.9,100)]); a.append(conf)
a.append(grp('why',[card('c',0,0,820,160,DARK),txt('t','Both agents “finished” — but their assumptions do not match.',30,52,30,'#FFFFFF',760,bold=True)],130,1045))
scene('S05 Conflict',a,38,48)

# S06 integration
title('Outputs return','to an integration step.',48,58)
a=[]
inputs=[('Research','behavior.md',80,GREEN,GI),('Frontend','ui.diff',300,SOFT,BLUE),('Backend','api.diff',550,AMBER,AI),('Tests','results.json',800,PURPLE,PI)]
for i,(name,file,x,bg,tc) in enumerate(inputs):
 box=grp(name,[card('c',0,0,190,145,bg),txt('n',name,20,22,21,tc,150,bold=True),txt('f',file,20,68,20,INK,150)],x,555); reveal(box,.2+i*.15); a.append(box); a.append(conn(x+95,700,540,850,BLUE,3,48,58))
integ=grp('Integration',[card('c',0,0,500,300,DARK),txt('l','INTEGRATION / REVIEW',30,26,20,'#AAB6CE',280,bold=True),txt('t','Compare outputs\nResolve conflicts\nRun final checks\nMerge one result',30,82,32,'#FFFFFF',420,bold=True)],290,850); reveal(integ,1); a.append(integ)
scene('S06 Integrate',a,48,58)

# S07 one agent better
title('Not every task','needs multiple agents.',58,68)
a=[]
small=grp('Small task',[card('c',0,0,780,220,GREEN),chip('SMALL + TIGHTLY CONNECTED',28,24,330,'#FFFFFF',GI,58,68),txt('t','Fix one button state and its nearby test.',28,95,35,INK,700,bold=True)],150,560); reveal(small,.2); a.append(small)
a.append(chip('ONE AGENT',175,860,230,GREEN,GI,58,68))
a.append(chip('LESS COORDINATION',640,860,280,SOFT,BLUE,58,68))
a.append(grp('rule',[card('c',0,0,820,170,DARK),txt('t','Split work only when the task actually separates cleanly.',30,57,31,'#FFFFFF',760,bold=True)],130,1015))
scene('S07 One agent',a,58,68)

# S08 final rubric
title('Ask whether the task','can be divided cleanly.',68,80)
a=[]
qs=[('1','Can subtasks work independently?',GREEN,GI),('2','Can their interfaces be defined?',AMBER,AI),('3','Can one step integrate the outputs?',SOFT,BLUE)]
for i,(num,q,bg,tc) in enumerate(qs):
 row=grp('q'+num,[card('c',0,0,840,145,'#FFFFFF'),chip(num,22,22,62,bg,tc,68,80),txt('q',q,112,42,30,INK,690,bold=True)],120,520+i*180); reveal(row,.2+i*.35); a.append(row)
a.append(grp('final',[card('c',0,0,840,210,DARK),txt('l','USE MULTI-AGENT WHEN',28,24,20,'#AAB6CE',300,bold=True),txt('t','Split cleanly.\nCoordinate well.\nReview together.',28,71,38,'#FFFFFF',720,bold=True)],120,1080))
scene('S08 Rubric',a,68,80)

# presenter
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':80000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]; L.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])]); keys(arm,'rotation',[(0,18),(.9,-8),(5,-18),(10,-8),(15,-17),(20,-8),(25,-17),(30,-8),(35,-17),(40,-8),(45,-17),(50,-8),(55,-17),(60,-8),(65,-17),(70,-8),(76,-16)])
notes=[(0,8,'ONE OR MANY','Architecture follows\nthe task.'),(8,18,'ORCHESTRATOR','Keep the goal and\nown integration.'),(18,28,'DELEGATE','Give focused work\nsmaller contexts.'),(28,38,'PARALLEL','Independent tasks can\nrun at the same time.'),(38,48,'COORDINATE','Parallel work can\ncreate conflicts.'),(48,58,'INTEGRATE','Compare and merge\none consistent result.'),(58,68,'DON\'T OVERSPLIT','Small connected tasks\nmay need one agent.'),(68,80,'USE THE TASK','Split cleanly.\nReview together.')]
for s,e,lab,body in notes:
 g=grp('note',[txt('s',lab,640,1380,22,BLUE,345,s,e,True),txt('b',body,640,1428,31,INK,345,s,e)],s=s,e=e); enter(g); L.append(g)

doc['composition']={'id':'main','name':'V10 Multi-agent / full visual draft','layers':L[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(A,open(HERE.parent/'animation.json','w'),indent=2)
print('V10 full',uid,len(A))
