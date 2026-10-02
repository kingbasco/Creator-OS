import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text()); doc['duration']=18
L=[]; A=[]; uid=1900
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; PURPLE='#EEE9FF'; PI='#6A4BC4'; AMBER='#FFF4DC'; AI='#956515'; DARK='#1C2738'; RED='#FDEBEC'; RI='#B33A42'; BORDER='#E5E8EE'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=18):
 global uid; uid+=1; return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
def rect(n,x,y,w,h,col,r=0,s=0,e=18):
 o=b('Rect',n,x,y,s,e); o['rect']=dict(size=[w,h],fillColor=c(col),roundness=r); return o
def txt(n,v,x,y,z=30,col=INK,w=800,s=0,e=18,bold=False):
 o=b('Text',n,x,y,s,e); o['sourceText']=dict(text=v,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=z,fillColor=c(col),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,260],leading=z*1.12); return o
def path(n,cmd,col=None,stroke=None,width=3,s=0,e=18):
 o=b('Shape',n,s=s,e=e); o['shape']={'path':{'commands':cmd},'fills':[],'strokes':[]}
 if col:o['shape']['fills']=[dict(paint={'type':'solid','color':c(col)},fillRule='nonZeroWinding',blendMode='normal',opacity=100)]
 if stroke:o['shape']['strokes']=[dict(paint={'type':'solid','color':c(stroke)},width=width,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]
 return o
def M(x,y): return dict(type='moveTo',x=x,y=y)
def C(a,b,cx,d,x,y): return dict(type='cubicTo',c1x=a,c1y=b,c2x=cx,c2y=d,x=x,y=y)
def grp(n,ch,x=0,y=0,s=0,e=18):
 o=b('Group',n,x,y,s,e); o['layers']=ch[::-1]; return o
def card(n,x,y,w,h,col='#FFFFFF',r=22,s=0,e=18):
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
def chip(v,x,y,w,col,tc,s=0,e=18): return grp(v,[rect('bg',0,0,w,52,col,12,s,e),txt('t',v,17,11,22,tc,w-24,s,e,True)],x,y,s,e)
def conn(x1,y1,x2,y2,col=BLUE,w=4,s=0,e=18): return path('Connector',[M(x1,y1),C(x1,(y1+y2)/2,x2,(y1+y2)/2,x2,y2)],stroke=col,width=w,s=s,e=e)

proto=copy.deepcopy(doc)
L=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,BORDER),rect('Rule',80,1225,920,2,BORDER),rect('Rule',80,1730,920,2,BORDER)]

h1=grp('H1',[txt('l','One goal can become',80,182,64,INK,900,0,8,True),txt('e','four focused subtasks.',80,265,59,BLUE,900,0,8,True)],s=0,e=8); enter(h1); L.append(h1)
orch=grp('Orchestrator',[card('c',0,0,420,220,DARK,22,0,8),txt('lab','ORCHESTRATOR',28,24,20,'#AAB6CE',250,0,8,True),txt('title','Build the feature',28,70,37,'#FFFFFF',330,0,8,True),txt('sub','Keeps the goal + scope',28,132,25,'#DCE3F3',330,0,8)],330,520,0,8); reveal(orch,.1); L.append(orch)

agents=[
 ('RESEARCH','Find current behavior',75,865,GREEN,GI),
 ('FRONTEND','Update the UI',300,865,SOFT,BLUE),
 ('BACKEND','Change the API',555,865,AMBER,AI),
 ('TESTS','Verify the result',805,865,PURPLE,PI)
]
for i,(name,sub,x,y,bg,tc) in enumerate(agents):
 w=200
 a=grp(name,[card('c',0,0,w,165,bg,22,0,8),txt('n',name,20,23,23,tc,w-40,0,8,True),txt('s',sub,20,68,21,INK,w-40,0,8)],x,y,0,8); reveal(a,.25+i*.16); L.append(a); L.append(conn(540,740,x+w/2,y,BLUE,3,0,8))
note=grp('Note',[card('c',0,0,760,120,'#FFFFFF',22,0,8),txt('t','Same project · smaller contexts · clear responsibilities',30,39,28,INK,700,0,8,True)],160,1095,0,8); reveal(note,1); L.append(note)

h2=grp('H2',[txt('l','Independent work can',80,182,64,INK,900,8,18,True),txt('e','run in parallel.',80,265,59,BLUE,900,8,18,True)],s=8,e=18); enter(h2); L.append(h2)
orch2=grp('Orch2',[card('c',0,0,330,170,DARK),txt('lab','ORCHESTRATOR',24,22,19,'#AAB6CE',220,bold=True),txt('t','Track + integrate',24,67,33,'#FFFFFF',260,bold=True)],375,505,s=8,e=18); reveal(orch2,.1); L.append(orch2)
ys=[720,860,1000,1140]
cols=[GREEN,SOFT,AMBER,PURPLE]; tcs=[GI,BLUE,AI,PI]; names=['Research','Frontend','Backend','Tests']
for i,(name,y,bg,tc) in enumerate(zip(names,ys,cols,tcs)):
 row=grp('row'+name,[card('c',0,0,760,100,'#FFFFFF'),txt('n',name,24,25,26,INK,180,bold=True),rect('track',220,37,430,22,'#E6E9EF',11),rect('fill',220,37,0,22,bg,11)],160,y,s=8,e=18)
 reveal(row,.15+i*.12); L.append(row)
 fill=rect('progress '+name,380,y+37,0,22,bg,11,s=8,e=18)
 keys(fill,'scale',[(0,[0,100]),(1.5+i*.2,[0,100]),(5.0+i*.25,[100,100])]); fill['rect']['size']=[430,22]; L.append(fill)
 done=chip('DONE',820,y+24,105,bg,tc,8,18); keys(done,'opacity',[(0,0),(5.2+i*.25,0),(5.5+i*.25,100)]); L.append(done)
merge=grp('Merge',[card('c',0,0,650,130,DARK),txt('l','INTEGRATION / REVIEW',30,22,20,'#AAB6CE',300,bold=True),txt('t','Compare outputs → resolve conflicts → merge',30,63,28,'#FFFFFF',590,bold=True)],215,1290,s=8,e=18); keys(merge,'opacity',[(0,0),(6.8,0),(7.2,100)]); L.append(merge)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1430]; presenter['transform']['scale']=[80,80]; L.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1650]),(.7,[40,1430])]); keys(arm,'rotation',[(0,18),(.9,-8),(4,-18),(7,-6),(9,-18),(13,-8),(17,-15)])
n1=grp('n1',[txt('s','DELEGATE',650,1480,22,BLUE,330,bold=True),txt('b','Keep one goal.\nSplit focused work.',650,1528,30,INK,330)],s=0,e=8); enter(n1); L.append(n1)
n2=grp('n2',[txt('s','PARALLEL + INTEGRATE',650,1480,22,BLUE,330,bold=True),txt('b','Speed comes from\ncoordination, not chaos.',650,1528,30,INK,330)],s=8,e=18); enter(n2); L.append(n2)

doc['composition']={'id':'main','name':'V10 Multi-agent / opening prototype','layers':L[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(A,open(HERE.parent/'animation.json','w'),indent=2)
print('V10',uid,len(A))
