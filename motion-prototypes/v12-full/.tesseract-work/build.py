import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text()); doc['duration']=82
L=[]; A=[]; uid=3000
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; AMBER='#FFF4DC'; AI='#956515'; PURPLE='#EEE9FF'; PI='#6A4BC4'; RED='#FDEBEC'; RI='#B33A42'; DARK='#1C2738'; BORDER='#E5E8EE'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=82):
 global uid; uid+=1; return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
def rect(n,x,y,w,h,col,r=0,s=0,e=82):
 o=b('Rect',n,x,y,s,e); o['rect']=dict(size=[w,h],fillColor=c(col),roundness=r); return o
def txt(n,v,x,y,z=30,col=INK,w=800,s=0,e=82,bold=False):
 o=b('Text',n,x,y,s,e); o['sourceText']=dict(text=v,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=z,fillColor=c(col),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,300],leading=z*1.12); return o
def grp(n,ch,x=0,y=0,s=0,e=82):
 o=b('Group',n,x,y,s,e); o['layers']=ch[::-1]; return o
def card(n,x,y,w,h,col='#FFFFFF',r=22,s=0,e=82):
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
def chip(v,x,y,w,col,tc,s=0,e=82): return grp(v,[rect('bg',0,0,w,52,col,12,s,e),txt('t',v,17,11,22,tc,w-24,s,e,True)],x,y,s,e)
def scene(n,ch,s,e): L.append(grp(n,ch,s=s,e=e))
def title(a,e,s,en):
 g=grp('Headline',[txt('l',a,80,182,61,INK,900,s,en,True),txt('e',e,80,265,58,BLUE,900,s,en,True)],s=s,e=en); reveal(g); L.append(g)

proto=copy.deepcopy(doc)
L=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,BORDER),rect('Rule',80,1225,920,2,BORDER),rect('Rule',80,1730,920,2,BORDER)]

# S01
title('The shift is bigger than','better autocomplete.',0,8)
a=[]
editor=grp('Editor',[card('c',0,0,820,500,DARK),txt('lab','EDITOR',28,24,20,'#AAB6CE',150,bold=True),txt('file','profile.tsx',28,70,24,'#DCE3F3',230,bold=True),txt('code','const profile = await getProfile(user.id)\n\nreturn <ProfileCard profile={profile}',28,145,28,'#FFFFFF',730),txt('ghost',' />',650,211,28,'#7F8AA1',100),chip('TAB TO ACCEPT',28,408,220,'#2B3850','#DCE3F3',0,8)],130,525); reveal(editor,.1); a.append(editor)
a.append(chip('SUGGESTION',420,1080,240,SOFT,BLUE,0,8)); scene('S01',a,0,8)

# S02
title('Autocomplete suggests.','You still drive each step.',8,18)
a=[]
a.append(grp('Editor2',[card('c',0,0,850,460,DARK),txt('lab','EDITOR',30,26,20,'#AAB6CE',150,bold=True),txt('code','function saveProfile(data) {\n  return api.post("/profile", data)\n}',30,115,32,'#FFFFFF',760),txt('ghost','// add error handling',30,250,28,'#7F8AA1',500),chip('ACCEPT / REJECT',30,370,250,'#2B3850','#DCE3F3',8,18)],115,550))
a.append(grp('Human',[card('c',0,0,850,140,'#FFFFFF'),txt('t','You choose the next action every time.',30,45,32,INK,760,bold=True)],115,1050))
scene('S02',a,8,18)

# S03
title('An agent can inspect','the wider system.',18,28)
a=[]
repo=grp('Repo',[card('c',0,0,400,500,DARK),chip('REPOSITORY',25,24,190,'#2B3850','#DCE3F3',18,28),txt('tree','src/\n  auth/\n  profile/\n  billing/\n  tests/\n\npackage.json\nREADME.md',28,105,29,'#FFFFFF',300)],90,520); reveal(repo,.2); a.append(repo)
goal=grp('Goal',[card('c',0,0,430,260,SOFT),chip('GOAL',25,24,120,'#FFFFFF',BLUE,18,28),txt('t','“Fix profile save\nand verify the flow.”',25,96,35,INK,360,bold=True)],560,550); reveal(goal,.6); a.append(goal)
a.append(grp('Decision',[card('c',0,0,430,190,'#FFFFFF'),txt('l','AGENT DECIDES',25,24,20,MUT,200,bold=True),txt('t','Which files matter\nbefore editing.',25,72,31,INK,360,bold=True)],560,860))
scene('S03',a,18,28)

# S04
title('Then it can act,','not just suggest.',28,38)
a=[]
items=[('EDIT','profile/save.ts',90,545,GREEN,GI),('RUN','npm test',565,545,AMBER,AI),('TOOLS','browser / API',90,800,PURPLE,PI),('CHECK','result',565,800,SOFT,BLUE)]
for i,(n,sub,x,y,bg,tc) in enumerate(items):
 box=grp(n,[card('c',0,0,410,190,bg),txt('n',n,26,27,28,tc,170,bold=True),txt('s',sub,26,83,30,INK,340,bold=True),chip('ACTION',26,128,140,'#FFFFFF',tc,28,38)],x,y); reveal(box,.15+i*.2); a.append(box)
scene('S04',a,28,38)

# S05
title('Tests turn assistance','into an execution loop.',38,48)
a=[]
term=grp('Terminal',[card('c',0,0,850,500,DARK),chip('TEST RUN',28,25,180,'#2B3850','#DCE3F3',38,48),txt('t1','✓ typecheck',28,125,28,'#FFFFFF',500),txt('t2','✗ profile save test',28,190,28,'#FFFFFF',500),txt('err','Expected 200 · received 500',58,245,24,'#F3B8BD',650),txt('fix','Agent edits error handling…',28,325,28,'#FFFFFF',650),txt('pass','✓ profile save test',28,390,28,'#BFE8CD',650)],115,520); reveal(term,.2); a.append(term)
a.append(chip('RUN → FIX → RUN AGAIN',330,1080,420,GREEN,GI,38,48)); scene('S05',a,38,48)

# S06
title('The developer shifts from','typing → directing.',48,58)
a=[]
left=grp('Typing',[card('c',0,0,360,350,'#FFFFFF'),chip('TYPING',25,24,150,SOFT,BLUE,48,58),txt('t','Write every line\nchoose every step\nrun every command',25,110,29,INK,300)],100,560); reveal(left,.2); a.append(left)
right=grp('Directing',[card('c',0,0,460,410,DARK),chip('DIRECTING',25,24,190,'#2B3850','#DCE3F3',48,58),txt('h','Define:',25,100,28,'#AAB6CE',180,bold=True),txt('t','Goal\nConstraints\nArchitecture\nAcceptance criteria',25,150,32,'#FFFFFF',360,bold=True)],520,530); reveal(right,.6); a.append(right)
scene('S06',a,48,58)

# S07
title('Then the job becomes','reviewing the result.',58,68)
a=[]
items=[('DIFF','What changed?',90,550,GREEN,GI),('TESTS','Did it pass?',565,550,PURPLE,PI),('PERMISSIONS','What access was used?',90,815,AMBER,AI),('INTENT','Does it match the goal?',565,815,SOFT,BLUE)]
for i,(n,sub,x,y,bg,tc) in enumerate(items):
 box=grp(n,[card('c',0,0,410,200,bg),txt('n',n,26,28,27,tc,250,bold=True),txt('s',sub,26,90,29,INK,340,bold=True)],x,y); reveal(box,.15+i*.18); a.append(box)
a.append(chip('HUMAN JUDGMENT',385,1090,310,DARK,'#FFFFFF',58,68)); scene('S07',a,58,68)

# S08
title('The new workflow is','specify → execute → review.',68,82)
a=[]
steps=[('1','SPECIFY','Goal + boundaries',90,555,GREEN,GI),('2','EXECUTE','Agent acts in scope',380,555,SOFT,BLUE),('3','REVIEW','Human checks result',700,555,AMBER,AI)]
for i,(num,n,sub,x,y,bg,tc) in enumerate(steps):
 box=grp(n,[card('c',0,0,280,220,bg),grp('num',[rect('bg',0,0,44,44,'#FFFFFF',10),txt('n',num,14,7,21,tc,25,bold=True)],22,22),txt('n',n,80,30,25,tc,170,bold=True),txt('s',sub,24,100,28,INK,225,bold=True)],x,y); reveal(box,.15+i*.25); a.append(box)
summary=grp('Summary',[card('c',0,0,850,300,DARK),txt('l','THE SHIFT',30,25,20,'#AAB6CE',180,bold=True),txt('t','Agents expand execution.\nHumans keep judgment.',30,82,41,'#FFFFFF',760,bold=True),chip('AUTOCOMPLETE → AGENTS',30,205,330,'#2B3850','#DCE3F3',68,82)],115,860); reveal(summary,1); a.append(summary)
scene('S08',a,68,82)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':82000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1390]; presenter['transform']['scale']=[84,84]; L.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1650]),(.7,[40,1390])]); keys(arm,'rotation',[(0,18),(.9,-8),(5,-18),(10,-7),(15,-18),(20,-7),(25,-18),(30,-7),(35,-18),(40,-7),(45,-18),(50,-7),(55,-18),(60,-7),(65,-18),(70,-7),(77,-16)])
notes=[(0,8,'AUTOCOMPLETE','Suggestion inside\nthe editor.'),(8,18,'HUMAN DRIVES','You choose every\nnext step.'),(18,28,'AGENT CONTEXT','Inspect the repo\nbefore editing.'),(28,38,'AGENT ACTIONS','Edit, run, use tools\nand check.'),(38,48,'ITERATION','Tests create a loop.'),(48,58,'DIRECTING','Specify goals and\nboundaries.'),(58,68,'REVIEWING','Check diff, tests,\npermissions and intent.'),(68,82,'THE NEW LOOP','Specify → Execute → Review.')]
for s,e,l,body in notes:
 n=grp('note',[txt('s',l,650,1460,22,BLUE,330,s,e,True),txt('b',body,650,1508,30,INK,330,s,e)],s=s,e=e); enter(n); L.append(n)

doc['composition']={'id':'main','name':'V12 Autocomplete to Agents / full visual draft','layers':L[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(A,open(HERE.parent/'animation.json','w'),indent=2)
print('V12 full',uid,len(A))
