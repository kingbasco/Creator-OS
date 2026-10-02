import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text())
doc['duration']=80
A=[]; acts=[]; uid=2300
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; PURPLE='#EEE9FF'; PI='#6A4BC4'; AMBER='#FFF4DC'; AI='#956515'; RED='#FDEBEC'; RI='#B33A42'; DARK='#1C2738'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=80):
 global uid; uid+=1
 return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
def rect(n,x,y,w,h,col,r=0,s=0,e=80):
 o=b('Rect',n,x,y,s,e); o['rect']=dict(size=[w,h],fillColor=c(col),roundness=r); return o
def txt(n,v,x,y,z=30,col=INK,w=800,s=0,e=80,bold=False):
 o=b('Text',n,x,y,s,e); o['sourceText']=dict(text=v,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=z,fillColor=c(col),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,260],leading=z*1.12); return o
def grp(n,ch,x=0,y=0,s=0,e=80):
 o=b('Group',n,x,y,s,e); o['layers']=ch[::-1]; return o
def card(n,x,y,w,h,col='#FFFFFF',r=22,s=0,e=80):
 o=rect(n,x,y,w,h,col,r,s,e); o['dropShadow']=dict(color=[.05,.08,.14,.12],blurRadius=24,spreadRadius=0,offset=[0,12],blendMode='normal'); return o
def anim(o,p,code): acts.append(dict(type='setFxPropertyAnimator',compositionId='main',property={'layerId':o['id'],'propertyType':p},animator={'type':'jsScript','layerTimeJsCode':code},dependencies=[]))
def keys(o,p,vals):
 if p in ['position','scale']:
  for ax,ix in [('X',0),('Y',1)]: keys(o,p+ax,[(t,v[ix]) for t,v in vals])
  return
 typ='vector2' if isinstance(vals[0][1],list) else 'float'
 acts.append(dict(type='setFxPropertyKeyframes',compositionId='main',property={'layerId':o['id'],'propertyType':p},keyframes=[dict(id=f'{o["id"]}-{p}-{i}',layerTime=int(t*1000),value={'type':typ,'value':v},easing={'type':'cubicBezier','x1':.22,'y1':1,'x2':.36,'y2':1}) for i,(t,v) in enumerate(vals)]))
def enter(o,d=0): anim(o,'opacity',f'return Math.min(100,Math.max(0,(input.time.seconds-{d})*400));')
def reveal(o,d=0,dy=28): x,y=o['transform']['position']; keys(o,'position',[(0,[x,y+dy]),(.55,[x,y])]); enter(o,d)
def chip(v,x,y,w,col,tc,s=0,e=80): return grp(v,[rect('bg',0,0,w,52,col,12,s,e),txt('t',v,17,11,22,tc,w-24,s,e,True)],x,y,s,e)
def connector(x1,y1,x2,y2,col='#B9C2D3',w=4,s=0,e=80):
 o=b('Shape','Connector',s=s,e=e)
 o['shape']={'path':{'commands':[{'type':'moveTo','x':x1,'y':y1},{'type':'cubicTo','c1x':x1,'c1y':(y1+y2)/2,'c2x':x2,'c2y':(y1+y2)/2,'x':x2,'y':y2}]},'fills':[],'strokes':[dict(paint={'type':'solid','color':c(col)},width=w,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]}
 return o
def title(a,e,s,en):
 g=grp('Headline',[txt('L',a,80,182,64,INK,900,s,en,True),txt('E',e,80,265,59,BLUE,900,s,en,True)],s=s,e=en); reveal(g); A.append(g)
def scene(n,ch,s,e): A.append(grp(n,ch,s=s,e=e))
proto=copy.deepcopy(doc)
A=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,'#E5E8EE'),rect('Rule',80,1225,920,2,'#E5E8EE'),rect('Rule',80,1730,920,2,'#E5E8EE')]

# S01
title('One agent can do','the whole task.',0,9)
a=[]
task=grp('Task',[card('c',0,0,760,250,'#FFFFFF'),txt('lab','PRODUCT TASK',30,27,20,MUT,220,bold=True),txt('t','Ship the participant workflow',30,76,39,INK,690,bold=True),txt('s','Research · UI · backend · tests · review',30,150,28,MUT,650)],160,560); reveal(task,.1); a.append(task)
agent=grp('Agent',[card('c',0,0,410,240,DARK),chip('MAIN AGENT',28,25,170,'#2B3850','#DCE3F3',0,9),txt('t','One context\nOne worker\nOne result',28,93,31,'#FFFFFF',330,bold=True)],335,900); reveal(agent,.6); a.append(agent)
scene('S01',a,0,9)

# S02
title('For larger jobs,','the agent can delegate.',9,19)
a=[]
orch=grp('Orch',[card('c',0,0,360,170,DARK),chip('ORCHESTRATOR',25,22,220,'#2B3850','#DCE3F3',9,19),txt('t','Keeps the goal',25,90,31,'#FFFFFF',300,bold=True)],360,540); reveal(orch,.2); a.append(orch)
roles=[('RESEARCH','Find answers',80,850,GREEN,GI),('FRONTEND','Build UI',310,850,SOFT,BLUE),('BACKEND','Data + API',540,850,AMBER,AI),('TESTS','Verify',770,850,PURPLE,PI)]
for i,(lab,sub,x,y,bg,tc) in enumerate(roles):
 g=grp(lab,[card('c',0,0,210,165,bg),txt('l',lab,20,24,22,tc,170,bold=True),txt('s',sub,20,74,23,INK,170),chip('TASK',20,111,105,'#FFFFFF',tc,9,19)],x,y); reveal(g,.45+i*.15); a.append(g); a.append(connector(540,710,x+105,y,BLUE,3,9,19))
scene('S02',a,9,19)

# S03
title('Each subagent gets','a narrower context.',19,29)
a=[]
roles2=[('RESEARCH','Docs + decisions','Search only what matters',80,540,GREEN,GI),('FRONTEND','Components + states','Own the UI slice',555,540,SOFT,BLUE),('BACKEND','Schema + endpoints','Own data/API changes',80,820,AMBER,AI),('TESTS','Acceptance criteria','Own verification',555,820,PURPLE,PI)]
for i,(lab,scope,sub,x,y,bg,tc) in enumerate(roles2):
 g=grp(lab,[card('c',0,0,405,220,bg),txt('l',lab,24,22,21,tc,340,bold=True),txt('scope',scope,24,72,30,INK,350,bold=True),txt('sub',sub,24,132,23,MUT,340)],x,y); reveal(g,.15+i*.2); a.append(g)
a.append(grp('Rule',[card('c',0,0,850,145,DARK),txt('r','Smaller responsibility → less unrelated context',28,46,31,'#FFFFFF',790,bold=True)],115,1090))
scene('S03',a,19,29)

# S04
title('Independent work can','run in parallel.',29,39)
a=[]
for i,(lab,x,bg,tc) in enumerate([('RESEARCH',80,GREEN,GI),('FRONTEND',310,SOFT,BLUE),('BACKEND',540,AMBER,AI),('TESTS',770,PURPLE,PI)]):
 g=grp(lab,[card('c',0,0,210,260,bg),txt('l',lab,20,24,21,tc,170,bold=True),rect('track',20,96,170,14,'#FFFFFF',7),rect('fill',20,96,145 if i!=2 else 125,14,tc,7),txt('s','working independently',20,140,22,INK,170),chip('PARALLEL',20,195,145,'#FFFFFF',tc,29,39)],x,600); reveal(g,.15+i*.18); a.append(g)
a.append(chip('CLEAR DEPENDENCIES',340,1010,400,DARK,'#FFFFFF',29,39))
scene('S04',a,29,39)

# S05
title('More agents also mean','more coordination.',39,49)
a=[]
left=grp('A',[card('c',0,0,360,270,SOFT),txt('l','FRONTEND AGENT',26,24,20,BLUE,260,bold=True),txt('t','edits\nparticipants.tsx',26,77,34,INK,280,bold=True),chip('CHANGE A',26,198,150,'#FFFFFF',BLUE,39,49)],100,570); reveal(left,.2); a.append(left)
right=grp('B',[card('c',0,0,360,270,AMBER),txt('l','BACKEND AGENT',26,24,20,AI,260,bold=True),txt('t','also edits\nparticipants.tsx',26,77,34,INK,280,bold=True),chip('CHANGE B',26,198,150,'#FFFFFF',AI,39,49)],620,570); reveal(right,.5); a.append(right)
conf=grp('Conflict',[card('c',0,0,560,190,RED),txt('l','COORDINATION CONFLICT',28,25,20,RI,330,bold=True),txt('t','Same file · different assumptions',28,78,34,INK,500,bold=True)],260,950); reveal(conf,1.1); a.append(conf)
scene('S05',a,39,49)

# S06
title('The orchestrator','collects and integrates.',49,59)
a=[]
outs=[('Research','Decision notes',90,560,GREEN,GI),('Frontend','UI patch',90,760,SOFT,BLUE),('Backend','API patch',700,560,AMBER,AI),('Tests','Test report',700,760,PURPLE,PI)]
for i,(lab,sub,x,y,bg,tc) in enumerate(outs):
 g=grp(lab,[card('c',0,0,290,145,bg),txt('l',lab.upper(),22,22,20,tc,230,bold=True),txt('s',sub,22,69,27,INK,240,bold=True)],x,y); reveal(g,.15+i*.15); a.append(g)
merge=grp('Merge',[card('c',0,0,380,250,DARK),txt('l','ORCHESTRATOR',27,25,20,'#AAB6CE',240,bold=True),txt('t','Compare\nResolve\nIntegrate',27,76,35,'#FFFFFF',300,bold=True)],350,900); reveal(merge,1.0); a.append(merge)
for x,y in [(235,705),(235,905),(845,705),(845,905)]: a.append(connector(x,y,540,900,BLUE,3,49,59))
scene('S06',a,49,59)

# S07
title('Many outputs still need','one verification step.',59,69)
a=[]
combined=grp('Combined',[card('c',0,0,720,180,'#FFFFFF'),txt('l','COMBINED CHANGE',28,25,20,MUT,230,bold=True),txt('t','Research + UI + API + tests',28,74,34,INK,640,bold=True)],180,540); reveal(combined,.15); a.append(combined)
checks=[('TYPECHECK',GREEN,GI),('TESTS',GREEN,GI),('REVIEW',SOFT,BLUE),('FINAL CHECK',AMBER,AI)]
for i,(lab,bg,tc) in enumerate(checks):
 g=grp(lab,[card('c',0,0,185,145,bg),txt('l',lab,20,24,20,tc,145,bold=True),chip('PASS',20,80,105,'#FFFFFF',tc,59,69)],95+i*230,810); reveal(g,.45+i*.2); a.append(g)
a.append(chip('ONE VERIFIED RESULT',340,1040,400,DARK,'#FFFFFF',59,69))
scene('S07',a,59,69)

# S08
title('Split only when','the work can be split.',69,80)
a=[]
one=grp('One agent',[card('c',0,0,390,360,GREEN),chip('ONE AGENT',28,25,170,'#FFFFFF',GI,69,80),txt('t','Best fit',28,99,35,INK,300,bold=True),txt('b','Small task\nTightly connected\nShared context',28,166,28,INK,300)],95,540); reveal(one,.2); a.append(one)
many=grp('Many agents',[card('c',0,0,390,360,SOFT),chip('MULTI-AGENT',28,25,210,'#FFFFFF',BLUE,69,80),txt('t','Best fit',28,99,35,INK,300,bold=True),txt('b','Clear subtasks\nIndependent work\nStrong coordination',28,166,28,INK,300)],595,540); reveal(many,.5); a.append(many)
a.append(grp('Rule',[card('c',0,0,850,210,DARK),txt('l','THE REAL IDEA',28,25,20,'#AAB6CE',220,bold=True),txt('t','Task decomposition\n+ coordination',28,76,42,'#FFFFFF',760,bold=True)],115,1025))
scene('S08',a,69,80)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':80000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]; A.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])]); keys(arm,'rotation',[(0,18),(.9,-8),(5,-18),(10,-7),(15,-18),(20,-8),(25,-17),(30,-8),(35,-17),(40,-8),(45,-17),(50,-8),(55,-17),(60,-8),(65,-17),(70,-8),(76,-16)])
notes=[(0,9,'ONE AGENT','A single worker can\nown the whole task.'),(9,19,'DELEGATE','Split clear responsibilities.'),(19,29,'NARROW CONTEXT','Each subagent gets\na focused slice.'),(29,39,'PARALLEL','Independent work can\nmove at the same time.'),(39,49,'COORDINATION','More workers create\nmerge and conflict work.'),(49,59,'INTEGRATE','One agent collects\nand resolves outputs.'),(59,69,'VERIFY','Several outputs still\nneed one final check.'),(69,80,'CHOOSE DELIBERATELY','Split only when the\nwork can be split.')]
for s,e,l,body in notes:
 n=grp('Note',[txt('s',l,640,1380,22,BLUE,345,s,e,True),txt('b',body,640,1428,31,INK,345,s,e)],s=s,e=e); enter(n); A.append(n)

doc['composition']={'id':'main','name':'V10 Multi-agent / full visual draft','layers':A[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(acts,open(HERE.parent/'animation.json','w'),indent=2)
print('V10 full layers',uid,'actions',len(acts))
