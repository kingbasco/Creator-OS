import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text()); doc['duration']=80
L=[]; A=[]; uid=1700
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; PURPLE='#EEE9FF'; PI='#6A4BC4'; RED='#FDEBEC'; RI='#B33A42'; AMBER='#FFF4DC'; AI='#956515'; DARK='#1C2738'; BORDER='#E5E8EE'
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
 g=grp('Headline',[txt('l',a,80,182,65,INK,900,s,e,True),txt('e',b,80,265,59,BLUE,900,s,e,True)],s=s,e=e); reveal(g); L.append(g)
proto=copy.deepcopy(doc)
L=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,BORDER),rect('Rule',80,1225,920,2,BORDER),rect('Rule',80,1730,920,2,BORDER)]

# S01
title('Login can work','while data access is wrong.',0,8)
a=[]
a.append(grp('Auth ok',[card('c',0,0,840,180,GREEN),chip('AUTHENTICATION',25,25,240,'#FFFFFF',GI),txt('q','Who are you?',25,91,35,INK,300,bold=True),chip('Alice = user_42',490,60,280,'#FFFFFF',GI)],120,560))
a.append(grp('Access bad',[card('c',0,0,840,230,RED),chip('AUTHORIZATION',25,24,230,'#FFFFFF',RI),txt('q','Which rows may you access?',25,92,34,INK,460,bold=True),chip('Not enforced yet',540,112,240,'#FFFFFF',RI)],120,820))
a.append(chip('LOGGED IN',180,1090,220,GREEN,GI))
a.append(chip('DATA STILL EXPOSED',645,1090,290,RED,RI))
scene('S01 Auth vs access',a,0,8)

# S02
title('Two users.','One profiles table.',8,18)
a=[]
for name,uidv,x,col,tc in [('Alice','user_42',95,GREEN,GI),('Bob','user_57',735,PURPLE,PI)]:
 u=grp(name,[card('c',0,0,250,180,col),txt('name',name,24,28,33,INK,190,bold=True),txt('id',uidv,24,78,23,MUT,180),chip('AUTHENTICATED',24,120,190,'#FFFFFF',tc,8,18)],x,545); reveal(u,.2); a.append(u)
table=grp('table',[card('c',0,0,600,355),txt('title','profiles',28,24,31,INK,200,bold=True),rect('h',28,82,544,44,'#F1F3F6',8),txt('ht','owner_id       name       email',42,92,19,MUT,500,bold=True),rect('r1',28,145,544,70,GREEN,8),txt('r1t','user_42        Alice      alice@x.com',42,165,20,INK,500),rect('r2',28,230,544,70,PURPLE,8),txt('r2t','user_57        Bob        bob@x.com',42,250,20,INK,500)],240,805); reveal(table,.5); a.append(table)
scene('S02 Users and table',a,8,18)

# S03
title('Without a row policy,','too much can come back.',18,28)
a=[]
table=grp('table',[card('c',0,0,600,355),txt('title','profiles',28,24,31,INK,200,bold=True),rect('h',28,82,544,44,'#F1F3F6',8),txt('ht','owner_id       name       email',42,92,19,MUT,500,bold=True),rect('r1',28,145,544,70,GREEN,8),txt('r1t','user_42        Alice      alice@x.com',42,165,20,INK,500),rect('r2',28,230,544,70,PURPLE,8),txt('r2t','user_57        Bob        bob@x.com',42,250,20,INK,500)],240,600); reveal(table,.2); a.append(table)
a.append(chip('REQUEST AS ALICE',110,1010,250,SOFT,BLUE,18,28))
a.append(chip('RETURNS 2 ROWS',410,1010,250,RED,RI,18,28))
a.append(chip('INCLUDES BOB',710,1010,250,RED,RI,18,28))
bad=grp('warning',[card('c',0,0,840,130,DARK),txt('t','The request succeeded — but the access rule was wrong.',30,42,30,'#FFFFFF',780,bold=True)],120,1110); reveal(bad,1); a.append(bad)
scene('S03 No policy',a,18,28)

# S04
title('RLS checks identity','before a row is allowed.',28,38)
a=[]
shield=grp('shield',[card('c',0,0,360,310,DARK),txt('l','ROW LEVEL SECURITY',28,26,20,'#AAB6CE',290,bold=True),txt('t','Policy gate',28,76,38,'#FFFFFF',280,bold=True),chip('owner_id = user.id',28,160,275,AMBER,AI,28,38),txt('sub','Check every candidate row',28,232,25,'#DCE3F3',280)],360,555); reveal(shield,.2); a.append(shield)
a.append(grp('identity',[card('c',0,0,240,150,GREEN),txt('t','Current identity',24,24,22,GI,180,bold=True),txt('u','user_42',24,70,31,INK,180,bold=True)],90,650))
a.append(grp('rows',[card('c',0,0,240,215,'#FFFFFF'),txt('l','Candidate rows',24,22,22,MUT,180,bold=True),chip('user_42',24,78,170,GREEN,GI,28,38),chip('user_57',24,140,170,PURPLE,PI,28,38)],750,615))
a.append(conn(330,725,360,710)); a.append(conn(720,710,750,725))
a.append(chip('ALLOW',350,980,160,GREEN,GI,28,38)); a.append(chip('FILTER',575,980,170,RED,RI,28,38))
scene('S04 Policy check',a,28,38)

# S05
title('Alice requests profiles.','Only Alice passes.',38,48)
a=[]
alice=grp('Alice',[card('c',0,0,250,170,GREEN),txt('n','Alice',24,28,32,INK,180,bold=True),txt('id','user_42',24,78,22,MUT,170),chip('REQUEST',24,115,145,'#FFFFFF',GI,38,48)],85,585); reveal(alice,.15); a.append(alice)
gate=grp('gate',[card('c',0,0,300,250,DARK),txt('l','RLS POLICY',25,24,20,'#AAB6CE',200,bold=True),txt('rule','owner_id\n= user_42',25,75,34,'#FFFFFF',240,bold=True),chip('CHECK ROWS',25,170,210,AMBER,AI,38,48)],390,545); reveal(gate,.5); a.append(gate)
rows=grp('rows',[card('c',0,0,300,280,'#FFFFFF'),chip('Alice row',24,35,220,GREEN,GI,38,48),chip('Bob row',24,105,220,PURPLE,PI,38,48),chip('FILTER BOB',24,190,220,RED,RI,38,48)],710,530); reveal(rows,.8); a.append(rows)
a.append(conn(335,670,390,670)); a.append(conn(690,670,710,670))
a.append(grp('result',[card('c',0,0,700,140,GREEN),txt('t','RESULT: Alice receives only Alice\'s row.',28,46,31,INK,640,bold=True)],190,1020))
scene('S05 Alice',a,38,48)

# S06
title('Bob runs the same query.','The result changes.',48,58)
a=[]
bob=grp('Bob',[card('c',0,0,250,170,PURPLE),txt('n','Bob',24,28,32,INK,180,bold=True),txt('id','user_57',24,78,22,MUT,170),chip('SAME QUERY',24,115,170,'#FFFFFF',PI,48,58)],85,585); reveal(bob,.15); a.append(bob)
gate=grp('gate',[card('c',0,0,300,250,DARK),txt('l','RLS POLICY',25,24,20,'#AAB6CE',200,bold=True),txt('rule','owner_id\n= user_57',25,75,34,'#FFFFFF',240,bold=True),chip('CHECK ROWS',25,170,210,AMBER,AI,48,58)],390,545); reveal(gate,.5); a.append(gate)
rows=grp('rows',[card('c',0,0,300,280,'#FFFFFF'),chip('Alice row',24,35,220,GREEN,GI,48,58),chip('Bob row',24,105,220,PURPLE,PI,48,58),chip('FILTER ALICE',24,190,220,RED,RI,48,58)],710,530); reveal(rows,.8); a.append(rows)
a.append(conn(335,670,390,670)); a.append(conn(690,670,710,670))
a.append(grp('result',[card('c',0,0,700,140,PURPLE),txt('t','RESULT: Bob receives only Bob\'s row.',28,46,31,INK,640,bold=True)],190,1020))
scene('S06 Bob',a,48,58)

# S07
title('Authentication proves identity.','Authorization limits access.',58,68)
a=[]
auth=grp('auth',[card('c',0,0,390,370,GREEN),chip('AUTHENTICATION',25,24,245,'#FFFFFF',GI,58,68),txt('q','Who are you?',25,106,36,INK,330,bold=True),txt('b','• login\n• session\n• user ID',25,175,30,INK,300)],100,550); reveal(auth,.2); a.append(auth)
authz=grp('authz',[card('c',0,0,390,370,AMBER),chip('AUTHORIZATION',25,24,235,'#FFFFFF',AI,58,68),txt('q','What may you access?',25,106,34,INK,330,bold=True),txt('b','• rows\n• actions\n• permissions',25,175,30,INK,300)],590,550); reveal(authz,.5); a.append(authz)
a.append(grp('neq',[card('c',0,0,620,150,DARK),txt('t','AUTH  ≠  AUTHORIZATION',65,50,40,'#FFFFFF',510,bold=True)],230,1020))
scene('S07 Auth vs authz',a,58,68)

# S08
title('Before you ship,','review every exposed table.',68,80)
a=[]
tables=[('profiles','RLS ON',GREEN,GI),('projects','RLS ON',GREEN,GI),('orders','CHECK POLICY',AMBER,AI),('admin_notes','CLIENT BLOCKED',RED,RI)]
for i,(name,status,bg,tc) in enumerate(tables):
 y=530+i*145
 row=grp('row',[card('c',0,0,840,115,'#FFFFFF'),txt('n',name,28,34,31,INK,300,bold=True),chip(status,520,30,270,bg,tc,68,80)],120,y); reveal(row,.15+i*.25); a.append(row)
a.append(grp('final',[card('c',0,0,840,190,DARK),txt('l','SHIP CHECK',28,25,20,'#AAB6CE',180,bold=True),txt('t','Login protects identity.\nPolicies protect data access.',28,70,35,'#FFFFFF',760,bold=True)],120,1110))
scene('S08 Review',a,68,80)

# Presenter
presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':80000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1292]; presenter['transform']['scale']=[92,92]; L.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1620]),(.7,[40,1292])]); keys(arm,'rotation',[(0,18),(.9,-8),(5,-18),(10,-8),(15,-17),(20,-8),(25,-18),(30,-8),(35,-17),(40,-8),(45,-17),(50,-8),(55,-17),(60,-8),(65,-17),(70,-8),(76,-16)])
notes=[(0,8,'LOGIN ≠ DATA ACCESS','Identity can be correct\nwhile access is wrong.'),(8,18,'TWO USERS','Both are authenticated.'),(18,28,'NO POLICY','Too many rows can return.'),(28,38,'RLS','The database checks\nidentity per row.'),(38,48,'ALICE','Only Alice\'s row passes.'),(48,58,'BOB','Same query,\ndifferent allowed row.'),(58,68,'AUTH VS AUTHZ','Identity first.\nAccess rules second.'),(68,80,'SHIP CHECK','Review policies on\nevery exposed table.')]
for s,e,lab,body in notes:
 g=grp('note',[txt('s',lab,640,1380,22,BLUE,345,s,e,True),txt('b',body,640,1428,31,INK,345,s,e)],s=s,e=e); enter(g); L.append(g)

doc['composition']={'id':'main','name':'V09 RLS / full visual draft','layers':L[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(A,open(HERE.parent/'animation.json','w'),indent=2)
print('V09 full',uid,len(A))
