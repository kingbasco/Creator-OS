import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text()); doc['duration']=18
L=[]; A=[]; uid=2300
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; AMBER='#FFF4DC'; AI='#956515'; RED='#FDEBEC'; RI='#B33A42'; PURPLE='#EEE9FF'; PI='#6A4BC4'; DARK='#1C2738'; BORDER='#E5E8EE'
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

h1=grp('H1',[txt('l','A better build comes from',80,182,62,INK,900,0,8,True),txt('e','a better loop.',80,265,60,BLUE,900,0,8,True)],s=0,e=8); enter(h1); L.append(h1)

stages=[
 ('INSPECT','Repo scan',110,545,250,GREEN,GI),
 ('PLAN','Change plan',720,545,250,SOFT,BLUE),
 ('CODE','Focused diff',720,890,250,AMBER,AI),
 ('TEST','Run checks',110,890,250,PURPLE,PI),
]
for i,(name,sub,x,y,w,bg,tc) in enumerate(stages):
 box=grp(name,[card('c',0,0,w,150,bg),txt('n',name,24,24,25,tc,w-48,bold=True),txt('s',sub,24,76,24,INK,w-48)],x,y,0,8); reveal(box,.15+i*.16); L.append(box)
L += [conn(360,620,720,620,BLUE,4,0,8),conn(845,695,845,890,BLUE,4,0,8),conn(720,965,360,965,BLUE,4,0,8),conn(235,890,235,695,BLUE,4,0,8)]
center=grp('Center',[card('c',0,0,360,190,DARK),txt('l','WORKFLOW',30,26,20,'#AAB6CE',180,bold=True),txt('t','Inspect → Plan\nCode → Test',30,78,36,'#FFFFFF',300,bold=True)],360,720,0,8); reveal(center,.6); L.append(center)
L.append(chip('REVIEW EVERY PASS',400,1095,280,GREEN,GI,0,8))

h2=grp('H2',[txt('l','A failed test should',80,182,62,INK,900,8,18,True),txt('e','send you back one step.',80,265,60,BLUE,900,8,18,True)],s=8,e=18); enter(h2); L.append(h2)

code=grp('Code stage',[card('c',0,0,420,300,AMBER),chip('CODE',25,24,130,'#FFFFFF',AI,8,18),txt('d','+ update email field\n+ sync auth identity\n+ add audit event',25,105,28,INK,350)],95,560,8,18); reveal(code,.2); L.append(code)
test=grp('Test stage',[card('c',0,0,420,300,'#FFFFFF'),chip('TEST',25,24,130,PURPLE,PI,8,18),txt('d','email edit updates DB\nlogin accepts new email\nold email is rejected',25,105,26,INK,350)],565,560,8,18); reveal(test,.5); L.append(test)

fail=chip('1 FAILED',695,790,170,RED,RI,8,18); keys(fail,'opacity',[(0,0),(2.5,0),(2.9,100),(5.5,100),(5.8,0)]); L.append(fail)
back=chip('BACK TO CODE',385,920,235,RED,RI,8,18); keys(back,'opacity',[(0,0),(3.2,0),(3.6,100),(5.8,100),(6.1,0)]); L.append(back)
patch=chip('PATCH APPLIED',190,920,210,GREEN,GI,8,18); keys(patch,'opacity',[(0,0),(5.8,0),(6.2,100)]); L.append(patch)
passed=chip('3 PASSED',690,920,185,GREEN,GI,8,18); keys(passed,'opacity',[(0,0),(6.4,0),(6.8,100)]); L.append(passed)
review=grp('Review',[card('c',0,0,760,140,DARK),txt('l','REVIEW',28,22,20,'#AAB6CE',150,bold=True),txt('t','Diff matches plan → continue the loop',28,63,30,'#FFFFFF',700,bold=True)],160,1070,8,18); keys(review,'opacity',[(0,0),(7.2,0),(7.6,100)]); L.append(review)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1390]; presenter['transform']['scale']=[84,84]; L.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1650]),(.7,[40,1390])]); keys(arm,'rotation',[(0,18),(.9,-8),(4,-18),(7,-5),(9,-18),(13,-8),(17,-15)])
n1=grp('n1',[txt('s','USE THE LOOP',650,1460,22,BLUE,330,bold=True),txt('b','Keep every step\nsmall and reviewable.',650,1508,30,INK,330)],s=0,e=8); enter(n1); L.append(n1)
n2=grp('n2',[txt('s','FAIL CLOSE TO CHANGE',650,1460,22,BLUE,330,bold=True),txt('b','Fix the last step\nbefore adding more.',650,1508,30,INK,330)],s=8,e=18); enter(n2); L.append(n2)

doc['composition']={'id':'main','name':'V11 Coding Loop / opening prototype','layers':L[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(A,open(HERE.parent/'animation.json','w'),indent=2)
print('V11',uid,len(A))
