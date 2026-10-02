import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text())
doc['duration']=80
A=[]; acts=[]; uid=1700
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; PURPLE='#EEE9FF'; PI='#6A4BC4'; RED='#FDEBEC'; RI='#B33A42'; AMBER='#FFF4DC'; AI='#956515'; DARK='#1C2738'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=80):
 global uid; uid+=1; return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
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
def scene(n,ch,s,e): A.append(grp(n,ch,s=s,e=e))
def title(a,e,s,en):
 g=grp('Headline',[txt('L',a,80,182,64,INK,900,s,en,True),txt('E',e,80,265,59,BLUE,900,s,en,True)],s=s,e=en); reveal(g); A.append(g)
def connector(x1,y1,x2,y2,col='#B9C2D3',w=4,s=0,e=80):
 return b('Shape','Connector',s=s,e=e)|{'shape':{'path':{'commands':[{'type':'moveTo','x':x1,'y':y1},{'type':'cubicTo','c1x':x1,'c1y':(y1+y2)/2,'c2x':x2,'c2y':(y1+y2)/2,'x':x2,'y':y2}]},'fills':[],'strokes':[dict(paint={'type':'solid','color':c(col)},width=w,cap='round',join='round',miterLimit=4,blendMode='normal',opacity=100)]}}
proto=copy.deepcopy(doc)
A=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,'#E5E8EE'),rect('Rule',80,1225,920,2,'#E5E8EE'),rect('Rule',80,1730,920,2,'#E5E8EE')]

# S01
title('Logged in does not mean','allowed to see every row.',0,8)
a=[]
for name,x,colr,tc,uidv in [('Alice',95,GREEN,GI,'user_42'),('Bob',740,PURPLE,PI,'user_57')]:
 u=grp(name,[card('User',0,0,245,175,colr),chip('AUTHENTICATED',20,20,195,'#FFFFFF',tc),txt('Name',name,22,88,32,INK,180,bold=True),txt('ID',uidv,22,132,22,MUT,170)],x,545); reveal(u,.1 if name=='Alice' else .25); a.append(u)
tbl=grp('Profiles',[card('Table',0,0,560,350),txt('title','profiles',26,24,31,INK,200,bold=True),rect('head',26,82,508,44,'#F1F3F6',8),txt('headt','owner_id       name       email',40,92,18,MUT,470,bold=True),rect('r1',26,145,508,70,GREEN,8),txt('r1t','user_42        Alice      alice@x.com',40,165,19,INK,470),rect('r2',26,230,508,70,PURPLE,8),txt('r2t','user_57        Bob        bob@x.com',40,250,19,INK,470)],260,790); reveal(tbl,.4); a.append(tbl)
a += [chip('Alice row',145,1100,180,GREEN,GI),chip('Bob row',145,1164,180,PURPLE,PI),chip('Alice row',755,1100,180,GREEN,GI),chip('Bob row',755,1164,180,PURPLE,PI)]
scene('S01',a,0,8)

# S02
title('Two users.','One shared table.',8,18)
a=[]
a.append(grp('Alice',[card('c',0,0,250,165,GREEN),txt('n','Alice',24,30,31,INK,180,bold=True),txt('id','user_42',24,83,22,MUT,170)],100,570))
a.append(grp('Bob',[card('c',0,0,250,165,PURPLE),txt('n','Bob',24,30,31,INK,180,bold=True),txt('id','user_57',24,83,22,MUT,170)],730,570))
a.append(grp('Table',[card('c',0,0,600,380),txt('t','profiles',28,24,32,INK,200,bold=True),rect('h',28,82,544,46,'#F1F3F6',8),txt('ht','owner_id       name       role',42,93,19,MUT,500,bold=True),rect('r1',28,150,544,74,GREEN,8),txt('r1t','user_42        Alice      member',42,170,21,INK,500),rect('r2',28,244,544,74,PURPLE,8),txt('r2t','user_57        Bob        member',42,264,21,INK,500)],240,800))
a.append(chip('ONE TABLE',430,1190,220,SOFT,BLUE,8,18))
scene('S02',a,8,18)

# S03
title('Without a row policy,','too much data can return.',18,28)
a=[]
req=grp('Request',[card('c',0,0,300,185,SOFT),txt('l','CURRENT USER',24,22,20,BLUE,180,bold=True),txt('u','Alice · user_42',24,65,29,INK,240,bold=True),chip('SELECT profiles',24,118,220,'#FFFFFF',BLUE,18,28)],90,580); reveal(req,.1); a.append(req)
raw=grp('Raw',[card('c',0,0,500,350,'#FFFFFF'),txt('l','DATABASE RESULT',26,24,20,MUT,230,bold=True),rect('r1',26,84,448,80,GREEN,8),txt('r1t','Alice row',42,109,27,INK,200,bold=True),rect('r2',26,184,448,80,PURPLE,8),txt('r2t','Bob row',42,209,27,INK,200,bold=True),chip('2 ROWS RETURNED',26,286,240,RED,RI,18,28)],490,520); reveal(raw,.7); a.append(raw)
a.append(connector(390,670,490,670,RI,5,18,28))
a.append(grp('Problem',[card('c',0,0,850,150,DARK),txt('l','PROBLEM',28,22,20,'#AAB6CE',180,bold=True),txt('b','The query returned data Alice should not receive.',28,64,31,'#FFFFFF',780,bold=True)],115,1040))
scene('S03',a,18,28)

# S04
title('RLS puts the rule','at the database.',28,38)
a=[]
shield=grp('Shield',[card('c',0,0,420,330,DARK),txt('l','ROW LEVEL SECURITY',28,27,20,'#AAB6CE',280,bold=True),txt('t','Check identity\nbefore each row',28,78,38,'#FFFFFF',340,bold=True),chip('owner_id = auth user',28,220,310,AMBER,AI,28,38)],330,540); reveal(shield,.2); a.append(shield)
a.append(grp('Identity',[card('c',0,0,260,180,GREEN),txt('l','CURRENT IDENTITY',22,23,19,GI,200,bold=True),txt('v','user_42',22,78,34,INK,200,bold=True)],75,640))
a.append(grp('Rows',[card('c',0,0,260,270,'#FFFFFF'),txt('l','ROWS',22,22,20,MUT,100,bold=True),chip('user_42 · Alice',22,72,210,GREEN,GI,28,38),chip('user_57 · Bob',22,144,210,PURPLE,PI,28,38)],745,600))
a.append(connector(335,730,330,705,BLUE,4,28,38)); a.append(connector(750,735,745,735,BLUE,4,28,38))
scene('S04',a,28,38)

# S05
title('Alice requests profiles.','Only Alice passes.',38,48)
a=[]
a.append(grp('Alice',[card('c',0,0,230,150,GREEN),txt('n','Alice',24,27,31,INK,170,bold=True),txt('id','user_42',24,80,22,MUT,160)],85,590))
a.append(grp('Policy',[card('c',0,0,330,220,DARK),txt('l','POLICY',24,24,19,'#AAB6CE',150,bold=True),txt('rule','owner_id = user_42',24,72,31,'#FFFFFF',270,bold=True),chip('MATCH',24,145,140,GREEN,GI,38,48)],370,555))
a.append(grp('Result',[card('c',0,0,280,220,GREEN),txt('l','RESULT',24,24,19,GI,140,bold=True),txt('row','Alice row',24,74,34,INK,220,bold=True),chip('ALLOW',24,145,120,'#FFFFFF',GI,38,48)],735,555))
a.append(grp('Filtered',[card('c',0,0,850,180,'#FFFFFF'),txt('l','FILTERED OUT',26,22,20,MUT,180,bold=True),txt('b','Bob row never leaves the database for Alice.',26,70,31,INK,780,bold=True)],115,980))
scene('S05',a,38,48)

# S06
title('Bob runs the same query.','He gets a different row.',48,58)
a=[]
a.append(grp('Bob',[card('c',0,0,230,150,PURPLE),txt('n','Bob',24,27,31,INK,170,bold=True),txt('id','user_57',24,80,22,MUT,160)],85,590))
a.append(grp('Query',[card('c',0,0,330,220,SOFT),txt('l','SAME QUERY',24,24,19,BLUE,160,bold=True),txt('q','SELECT profiles',24,75,31,INK,270,bold=True),chip('user_57',24,145,140,'#FFFFFF',BLUE,48,58)],370,555))
a.append(grp('Result',[card('c',0,0,280,220,PURPLE),txt('l','RESULT',24,24,19,PI,140,bold=True),txt('row','Bob row',24,74,34,INK,220,bold=True),chip('ALLOW',24,145,120,'#FFFFFF',PI,48,58)],735,555))
a.append(grp('Note',[card('c',0,0,850,180,DARK),txt('l','KEY IDEA',26,22,20,'#AAB6CE',180,bold=True),txt('b','Same query · different identity · different allowed rows.',26,70,31,'#FFFFFF',780,bold=True)],115,980))
scene('S06',a,48,58)

# S07
title('Authentication and authorization','answer different questions.',58,68)
a=[]
auth=grp('Auth',[card('c',0,0,390,360,GREEN),chip('AUTHENTICATION',26,24,250,'#FFFFFF',GI,58,68),txt('q','Who are you?',26,103,38,INK,330,bold=True),txt('b','Login\nSession\nUser identity',26,174,29,INK,300)],95,550); reveal(auth,.2); a.append(auth)
authz=grp('Authz',[card('c',0,0,390,360,AMBER),chip('AUTHORIZATION',26,24,250,'#FFFFFF',AI,58,68),txt('q','What may you access?',26,103,35,INK,330,bold=True),txt('b','Rows\nActions\nPermissions',26,174,29,INK,300)],595,550); reveal(authz,.6); a.append(authz)
a.append(chip('AUTH  ≠  AUTHORIZATION',315,1010,450,DARK,'#FFFFFF',58,68))
scene('S07',a,58,68)

# S08
title('Before you ship,','review every exposed table.',68,80)
a=[]
tables=[('profiles',GREEN,GI,'RLS ON'),('projects',GREEN,GI,'RLS ON'),('orders',AMBER,AI,'REVIEW'),('messages',GREEN,GI,'RLS ON')]
for i,(name,bg,tc,state) in enumerate(tables):
 y=535+i*140
 row=grp('Table '+name,[card('c',0,0,850,110,'#FFFFFF'),txt('n',name,28,33,30,INK,300,bold=True),chip(state,610,28,190,bg,tc,68,80)],115,y); reveal(row,.15+i*.25); a.append(row)
a.append(grp('Rule',[card('c',0,0,850,190,DARK),txt('l','SHIP CHECK',28,23,20,'#AAB6CE',180,bold=True),txt('b','Login protects identity.\nPolicies protect data access.',28,69,35,'#FFFFFF',780,bold=True)],115,1120))
scene('S08',a,68,80)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':80000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]; A.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])]); keys(arm,'rotation',[(0,18),(.9,-8),(5,-18),(9,-7),(14,-18),(19,-7),(24,-18),(29,-7),(34,-18),(39,-7),(44,-18),(49,-7),(54,-17),(59,-7),(64,-17),(69,-7),(75,-16)])
notes=[(0,8,'LOGIN IS NOT ACCESS','Identity alone does not\nprotect every row.'),(8,18,'TWO USERS','One shared data table.'),(18,28,'NO ROW POLICY','Too much data can return.'),(28,38,'DATABASE GATE','Check identity per row.'),(38,48,'ALICE','Only Alice row passes.'),(48,58,'BOB','Same query, different row.'),(58,68,'AUTH ≠ AUTHZ','Identity and access\nare separate decisions.'),(68,80,'BEFORE SHIPPING','Review policies on\nevery exposed table.')]
for s,e,l,body in notes:
 n=grp('Note',[txt('s',l,640,1380,22,BLUE,345,s,e,True),txt('b',body,640,1428,31,INK,345,s,e)],s=s,e=e); enter(n); A.append(n)

doc['composition']={'id':'main','name':'V09 RLS / full visual draft','layers':A[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(acts,open(HERE.parent/'animation.json','w'),indent=2)
print('V09 full layers',uid,'actions',len(acts))
