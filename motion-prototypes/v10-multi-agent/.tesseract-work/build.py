import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text())
doc['duration']=18
A=[]; acts=[]; uid=2000
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; PURPLE='#EEE9FF'; PI='#6A4BC4'; AMBER='#FFF4DC'; AI='#956515'; RED='#FDEBEC'; RI='#B33A42'; DARK='#1C2738'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=18):
 global uid; uid+=1
 return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
def rect(n,x,y,w,h,col,r=0,s=0,e=18):
 o=b('Rect',n,x,y,s,e); o['rect']=dict(size=[w,h],fillColor=c(col),roundness=r); return o
def txt(n,v,x,y,z=30,col=INK,w=800,s=0,e=18,bold=False):
 o=b('Text',n,x,y,s,e); o['sourceText']=dict(text=v,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=z,fillColor=c(col),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,260],leading=z*1.12); return o
def grp(n,ch,x=0,y=0,s=0,e=18):
 o=b('Group',n,x,y,s,e); o['layers']=ch[::-1]; return o
def card(n,x,y,w,h,col='#FFFFFF',r=22,s=0,e=18):
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
def chip(v,x,y,w,col,tc,s=0,e=18): return grp(v,[rect('bg',0,0,w,52,col,12,s,e),txt('t',v,17,11,22,tc,w-24,s,e,True)],x,y,s,e)
def connector(x1,y1,x2,y2,col='#B9C2D3',w=4,s=0,e=18):
 o=b('Shape','Connector',s=s,e=e)
 o['shape']={'path':{'commands':[{'type':'moveTo','x':x1,'y':y1},{'type':'cubicTo','c1x':x1,'c1y':(y1+y2)/2,'c2x':x2,'c2y':(y1+y2)/2,'x':x2,'y':y2}]},'fills':[],'strokes':[dict(paint={'type':'solid','color':c(col)},width=w,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]}
 return o

proto=copy.deepcopy(doc)
A=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,'#E5E8EE'),rect('Rule',80,1225,920,2,'#E5E8EE'),rect('Rule',80,1730,920,2,'#E5E8EE')]

# Scene 1: big task splits.
h1=grp('H1',[txt('L','One agent can hold',80,182,63,INK,900,0,9,True),txt('E','the goal — then delegate.',80,265,59,BLUE,900,0,9,True)],s=0,e=9); enter(h1); A.append(h1)
task=grp('Big task',[card('c',0,0,720,220,'#FFFFFF'),txt('lab','PRODUCT TASK',28,25,20,MUT,200,bold=True),txt('title','Ship the new participant workflow',28,72,38,INK,650,bold=True),txt('sub','Research · UI · data · tests',28,140,27,MUT,600)],180,520,s=0,e=9)
reveal(task,.1); A.append(task)
orch=grp('Orchestrator',[card('c',0,0,360,180,DARK),chip('ORCHESTRATOR',24,22,220,'#2B3850','#DCE3F3',0,9),txt('body','Keeps the overall goal',24,90,31,'#FFFFFF',300,bold=True)],360,795,s=0,e=9); reveal(orch,.6); A.append(orch)

agents=[
 ('RESEARCH','Find answers',80,1040,GREEN,GI),
 ('FRONTEND','Build UI',310,1040,SOFT,BLUE),
 ('BACKEND','Data + API',540,1040,AMBER,AI),
 ('TESTS','Verify',770,1040,PURPLE,PI)
]
for i,(label,sub,x,y,bg,tc) in enumerate(agents):
 w=210
 g=grp(label,[card('c',0,0,w,150,bg),txt('lab',label,20,24,23,tc,w-40,bold=True),txt('sub',sub,20,72,22,INK,w-40)],x,y,s=0,e=9)
 keys(g,'position',[(0,[435,860]),(.65+i*.14,[x,y])]); enter(g,.08+i*.08); A.append(g)
 A.append(connector(540,975,x+w/2,y,BLUE,3,0,9))

# Scene 2: parallel progress and merge.
h2=grp('H2',[txt('L','Focused agents can work',80,182,63,INK,900,9,18,True),txt('E','in parallel — then merge.',80,265,59,BLUE,900,9,18,True)],s=9,e=18); enter(h2); A.append(h2)
branches=[
 ('RESEARCH','Docs checked',80,535,GREEN,GI),
 ('FRONTEND','UI ready',310,535,SOFT,BLUE),
 ('BACKEND','API ready',540,535,AMBER,AI),
 ('TESTS','5 checks',770,535,PURPLE,PI)
]
for i,(label,status,x,y,bg,tc) in enumerate(branches):
 g=grp('Branch '+label,[card('c',0,0,210,230,bg),txt('lab',label,20,22,22,tc,170,bold=True),rect('track',20,84,170,14,'#FFFFFF',7),rect('fill',20,84,150 if i!=2 else 135,14,tc,7),txt('status',status,20,125,24,INK,170,bold=True),chip('DONE',20,174,115,'#FFFFFF',tc,9,18)],x,y,s=9,e=18)
 reveal(g,.15+i*.15); A.append(g)

merge=grp('Merge',[card('c',0,0,420,220,DARK),txt('lab','MERGE + REVIEW',28,27,20,'#AAB6CE',240,bold=True),txt('body','Collect outputs\nResolve conflicts\nRun final review',28,76,31,'#FFFFFF',340,bold=True)],330,900,s=9,e=18)
reveal(merge,1.1); A.append(merge)
for i,(label,status,x,y,bg,tc) in enumerate(branches):
 A.append(connector(x+105,y+230,540,900,BLUE,3,9,18))
conf=chip('shared file conflict',425,1140,230,RED,RI,9,18); keys(conf,'opacity',[(0,0),(4.5,0),(4.9,100),(6.4,100),(6.8,0)]); A.append(conf)
final=chip('FINAL REVIEW',430,1188,220,GREEN,GI,9,18); keys(final,'opacity',[(0,0),(6.8,0),(7.2,100)]); A.append(final)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]; A.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])]); keys(arm,'rotation',[(0,18),(.9,-8),(4,-18),(8,-6),(10,-18),(14,-8),(17,-15)])
n1=grp('N1',[txt('s','DELEGATE CLEARLY',650,1380,22,BLUE,340,bold=True),txt('b','The main agent keeps\nthe overall goal.',650,1428,31,INK,340)],s=0,e=9); enter(n1); A.append(n1)
n2=grp('N2',[txt('s','PARALLEL + MERGE',650,1380,22,BLUE,340,bold=True),txt('b','Focused outputs still\nneed one integration step.',650,1428,31,INK,340)],s=9,e=18); enter(n2); A.append(n2)

doc['composition']={'id':'main','name':'V10 Multi-agent / opening prototype','layers':A[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(acts,open(HERE.parent/'animation.json','w'),indent=2)
print('V10 prototype layers',uid,'actions',len(acts))
