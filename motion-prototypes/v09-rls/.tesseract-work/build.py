import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text())
doc['duration']=18
A=[]; acts=[]; uid=1500
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; PURPLE='#EEE9FF'; PI='#6A4BC4'; RED='#FDEBEC'; RI='#B33A42'; DARK='#1C2738'
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
def reveal(o,d=0): x,y=o['transform']['position']; keys(o,'position',[(0,[x,y+28]),(.55,[x,y])]); enter(o,d)
def chip(v,x,y,w,col,tc,s=0,e=18): return grp(v,[rect('bg',0,0,w,52,col,12,s,e),txt('t',v,17,11,22,tc,w-24,s,e,True)],x,y,s,e)

proto=copy.deepcopy(doc)
A=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,'#E5E8EE'),rect('Rule',80,1225,920,2,'#E5E8EE'),rect('Rule',80,1730,920,2,'#E5E8EE')]

h1=grp('H1',[txt('L','Logged in does not mean',80,182,63,INK,900,0,8,True),txt('E','allowed to see every row.',80,265,59,BLUE,900,0,8,True)],s=0,e=8); enter(h1); A.append(h1)
alice=grp('Alice',[card('c',0,0,245,175,GREEN),chip('AUTHENTICATED',20,20,195,'#FFFFFF',GI),txt('n','Alice',22,88,32,INK,180,bold=True),txt('id','user_42',22,132,22,MUT,170)],90,545,s=0,e=8); reveal(alice,.1); A.append(alice)
bob=grp('Bob',[card('c',0,0,245,175,PURPLE),chip('AUTHENTICATED',20,20,195,'#FFFFFF',PI),txt('n','Bob',22,88,32,INK,180,bold=True),txt('id','user_57',22,132,22,MUT,170)],745,545,s=0,e=8); reveal(bob,.2); A.append(bob)
table=grp('Table',[card('c',0,0,560,350),txt('title','profiles',26,24,31,INK,200,bold=True),rect('head',26,82,508,44,'#F1F3F6',8),txt('headt','owner_id       name       email',40,92,18,MUT,470,bold=True),rect('r1',26,145,508,70,GREEN,8),txt('r1t','user_42        Alice      alice@x.com',40,165,19,INK,470),rect('r2',26,230,508,70,PURPLE,8),txt('r2t','user_57        Bob        bob@x.com',40,250,19,INK,470)],260,785,s=0,e=8); reveal(table,.4); A.append(table)
leak=grp('Leak',[chip('Alice row',0,0,180,GREEN,GI),chip('Bob row',0,64,180,PURPLE,PI)],145,1010,s=0,e=8); keys(leak,'opacity',[(0,0),(3.2,0),(3.6,100)]); A.append(leak)
leak2=grp('Leak2',[chip('Alice row',0,0,180,GREEN,GI),chip('Bob row',0,64,180,PURPLE,PI)],755,1010,s=0,e=8); keys(leak2,'opacity',[(0,0),(3.5,0),(3.9,100)]); A.append(leak2)
warn=chip('TOO MUCH DATA',420,1150,240,RED,RI,0,8); keys(warn,'opacity',[(0,0),(4.6,0),(5,100)]); A.append(warn)

h2=grp('H2',[txt('L','RLS moves the rule',80,182,63,INK,900,8,18,True),txt('E','into the database.',80,265,59,BLUE,900,8,18,True)],s=8,e=18); enter(h2); A.append(h2)
a2=grp('Alice2',[card('c',0,0,220,145,GREEN),txt('n','Alice',24,28,31,INK,170,bold=True),txt('id','user_42',24,80,22,MUT,160)],75,575,s=8,e=18); reveal(a2,.1); A.append(a2)
b2=grp('Bob2',[card('c',0,0,220,145,PURPLE),txt('n','Bob',24,28,31,INK,170,bold=True),txt('id','user_57',24,80,22,MUT,160)],785,575,s=8,e=18); reveal(b2,.2); A.append(b2)
shield=grp('Shield',[card('c',0,0,330,230,DARK),txt('lab','ROW LEVEL SECURITY',25,25,19,'#AAB6CE',270,bold=True),txt('title','Policy gate',25,72,34,'#FFFFFF',270,bold=True),chip('owner_id = user.id',25,145,270,'#FFF4DC','#956515',8,18)],375,535,s=8,e=18); reveal(shield,.45); A.append(shield)
ft=grp('Filtered',[card('c',0,0,680,335),txt('title','profiles',26,22,30,INK,180,bold=True),rect('head',26,78,628,42,'#F1F3F6',8),txt('ht','owner_id       name       policy',40,88,18,MUT,590,bold=True),rect('r1',26,140,628,68,GREEN,8),txt('r1t','user_42        Alice      ALLOW',40,158,20,INK,580),rect('r2',26,225,628,68,PURPLE,8),txt('r2t','user_57        Bob        ALLOW',40,243,20,INK,580)],200,850,s=8,e=18); reveal(ft,.8); A.append(ft)
out1=chip('Alice → Alice row',120,1110,285,GREEN,GI,8,18); keys(out1,'opacity',[(0,0),(4,0),(4.4,100)]); A.append(out1)
out2=chip('Bob → Bob row',680,1110,260,PURPLE,PI,8,18); keys(out2,'opacity',[(0,0),(4.3,0),(4.7,100)]); A.append(out2)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]; A.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])]); keys(arm,'rotation',[(0,18),(.9,-8),(4,-18),(7,-5),(9,-18),(13,-8),(17,-15)])
n1=grp('N1',[txt('s','AUTHENTICATED',650,1380,22,BLUE,340,bold=True),txt('b','Both users are known.\nAccess is still too broad.',650,1428,31,INK,340)],s=0,e=8); enter(n1); A.append(n1)
n2=grp('N2',[txt('s','AUTHORIZED BY ROW',650,1380,22,BLUE,340,bold=True),txt('b','The database filters\nwhat each user can access.',650,1428,31,INK,340)],s=8,e=18); enter(n2); A.append(n2)

doc['composition']={'id':'main','name':'V09 RLS / opening prototype','layers':A[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2)
json.dump(acts,open(HERE.parent/'animation.json','w'),indent=2)
print('V09 layers',uid,'actions',len(acts))
