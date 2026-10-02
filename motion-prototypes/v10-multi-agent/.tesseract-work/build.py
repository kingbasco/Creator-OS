import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text()); doc['duration']=18
A=[]; acts=[]; uid=1900
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; PURPLE='#EEE9FF'; PI='#6A4BC4'; AMBER='#FFF4DC'; AI='#956515'; RED='#FDEBEC'; RI='#B33A42'; DARK='#1C2738'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=18):
 global uid; uid+=1; return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
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
def conn(x1,y1,x2,y2,col='#B9C2D3',w=4,s=0,e=18):
 o=b('Shape','Connector',s=s,e=e); o['shape']={'path':{'commands':[{'type':'moveTo','x':x1,'y':y1},{'type':'cubicTo','c1x':x1,'c1y':(y1+y2)/2,'c2x':x2,'c2y':(y1+y2)/2,'x':x2,'y':y2}]},'fills':[],'strokes':[dict(paint={'type':'solid','color':c(col)},width=w,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]}; return o

proto=copy.deepcopy(doc)
A=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,'#E5E8EE'),rect('Rule',80,1225,920,2,'#E5E8EE'),rect('Rule',80,1730,920,2,'#E5E8EE')]

h1=grp('H1',[txt('L','One agent can work alone.',80,182,62,INK,900,0,8,True),txt('E','Or it can delegate.',80,265,59,BLUE,900,0,8,True)],s=0,e=8); reveal(h1); A.append(h1)
root=grp('Root',[card('c',0,0,360,220,DARK),txt('lab','MAIN AGENT',28,25,20,'#AAB6CE',200,bold=True),txt('title','Keep the goal',28,72,38,'#FFFFFF',280,bold=True),chip('ORCHESTRATOR',28,145,220,'#2B3850','#DCE3F3')],360,555); reveal(root,.1); A.append(root)
roles=[('RESEARCH',80,870,GREEN,GI),('FRONTEND',315,930,SOFT,BLUE),('BACKEND',565,930,AMBER,AI),('TESTS',810,870,PURPLE,PI)]
for i,(name,x,y,bg,tc) in enumerate(roles):
 r=grp(name,[card('c',0,0,190,140,bg),txt('n',name,22,26,24,tc,150,bold=True),rect('track',22,86,146,12,'#FFFFFF',6),rect('fill',22,86,115 if i%2==0 else 90,12,tc if tc.startswith('#') else BLUE,6)],x,y); reveal(r,.35+i*.18); A.append(r); A.append(conn(540,775,x+95,y,BLUE,3))
lab=chip('PARALLEL WORK',430,1120,220,GREEN,GI); keys(lab,'opacity',[(0,0),(3.2,0),(3.6,100)]); A.append(lab)

h2=grp('H2',[txt('L','Then the results',80,182,62,INK,900,8,18,True),txt('E','come back together.',80,265,59,BLUE,900,8,18,True)],s=8,e=18); reveal(h2); A.append(h2)
for i,(name,x,y,bg,tc) in enumerate(roles):
 r=grp('Result '+name,[card('c',0,0,190,130,bg),txt('n',name,20,22,22,tc,150,bold=True),chip('DONE',20,72,120,'#FFFFFF',tc,8,18)],x,y-170,s=8,e=18); reveal(r,.15+i*.16); A.append(r)
 merge=grp('Merge'+name,[chip(name+' RESULT',0,0,175,bg,tc,8,18)],x,y+20,s=8,e=18); keys(merge,'position',[(0,[x,y+20]),(3.0+i*.2,[x,y+20]),(4.8+i*.2,[455,885+i*8])]); A.append(merge)

review=grp('Integration',[card('c',0,0,440,250,DARK),txt('lab','INTEGRATION + REVIEW',28,25,20,'#AAB6CE',290,bold=True),txt('title','Combine the work',28,75,38,'#FFFFFF',340,bold=True),txt('body','Resolve conflicts\nRun final checks',28,135,28,'#DCE3F3',330)],320,920,s=8,e=18); keys(review,'opacity',[(0,0),(4.5,0),(5,100)]); A.append(review)
conflict=grp('Conflict',[card('c',0,0,330,135,RED),txt('lab','SHARED FILE?',24,22,19,RI,180,bold=True),txt('body','Coordinate edits first.',24,66,28,INK,270,bold=True)],650,1110,s=8,e=18); keys(conflict,'opacity',[(0,0),(6.1,0),(6.5,100)]); A.append(conflict)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]; A.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])]); keys(arm,'rotation',[(0,18),(.9,-8),(4,-18),(7,-5),(9,-18),(13,-8),(17,-15)])
n1=grp('N1',[txt('s','DELEGATE',650,1380,22,BLUE,340,bold=True),txt('b','Independent tasks can\nrun in focused contexts.',650,1428,31,INK,340)],s=0,e=8); enter(n1); A.append(n1)
n2=grp('N2',[txt('s','INTEGRATE',650,1380,22,BLUE,340,bold=True),txt('b','The main agent brings\nresults back together.',650,1428,31,INK,340)],s=8,e=18); enter(n2); A.append(n2)

doc['composition']={'id':'main','name':'V10 Multi-agent / opening prototype','layers':A[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(acts,open(HERE.parent/'animation.json','w'),indent=2)
print('V10 layers',uid,'actions',len(acts))
