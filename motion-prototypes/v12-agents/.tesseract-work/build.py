import copy,json
from pathlib import Path
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]
doc=json.loads((ROOT/'motion-prototypes/mcp-full-episode/.tesseract-work/approved-presenter.json').read_text()); doc['duration']=18
L=[]; A=[]; uid=2700
BG='#F7F8FA'; INK='#101724'; MUT='#687385'; BLUE='#5B6CFF'; SOFT='#EEF0FF'; GREEN='#E9F7EF'; GI='#167749'; AMBER='#FFF4DC'; AI='#956515'; PURPLE='#EEE9FF'; PI='#6A4BC4'; DARK='#1C2738'; BORDER='#E5E8EE'
def c(h): return [int(h[i:i+2],16)/255 for i in (1,3,5)]+[1]
def tr(x=0,y=0): return dict(anchorPoint=[0,0],position=[x,y],scale=[100,100],rotation=0,opacity=100)
def b(t,n,x=0,y=0,s=0,e=18):
 global uid; uid+=1; return dict(type=t,id=uid,name=n,blendMode='normal',activeRange={'start':int(s*1000),'duration':int((e-s)*1000)},transform=tr(x,y))
def rect(n,x,y,w,h,col,r=0,s=0,e=18):
 o=b('Rect',n,x,y,s,e); o['rect']=dict(size=[w,h],fillColor=c(col),roundness=r); return o
def txt(n,v,x,y,z=30,col=INK,w=800,s=0,e=18,bold=False):
 o=b('Text',n,x,y,s,e); o['sourceText']=dict(text=v,fontFamily='Geist',fontStyle='SemiBold' if bold else 'Regular',fontSize=z,fillColor=c(col),strokeWidth=0,justification='left',verticalAlign='top',boxText=True,boxPosition=[0,0],boxSize=[w,280],leading=z*1.12); return o
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

proto=copy.deepcopy(doc)
L=[rect('Canvas',0,0,1080,1920,BG),rect('Rule',80,430,920,2,BORDER),rect('Rule',80,1225,920,2,BORDER),rect('Rule',80,1730,920,2,BORDER)]

# 0-8 autocomplete
h1=grp('H1',[txt('l','AI coding used to feel like',80,182,61,INK,900,0,8,True),txt('e','better autocomplete.',80,265,59,BLUE,900,0,8,True)],s=0,e=8); reveal(h1); L.append(h1)
editor=grp('Editor',[card('c',0,0,820,520,DARK),txt('lab','EDITOR',28,24,20,'#AAB6CE',160,bold=True),txt('file','profile.tsx',28,68,24,'#DCE3F3',250,bold=True),txt('code','const profile = await getProfile(user.id)\n\nreturn <ProfileCard profile={profile}',28,132,28,'#FFFFFF',740),txt('ghost',' />',650,198,28,'#7F8AA1',100),chip('TAB TO ACCEPT',28,430,220,'#2B3850','#DCE3F3')],130,520)
keys(editor,'scale',[(0,[118,118]),(.8,[100,100]),(5,[100,100]),(7.2,[72,72])]); keys(editor,'position',[(0,[60,470]),(.8,[130,520]),(5,[130,520]),(7.2,[105,560])]); L.append(editor)
accepted=chip('SUGGESTION ACCEPTED',560,1050,300,GREEN,GI); keys(accepted,'opacity',[(0,0),(3.2,0),(3.6,100)]); L.append(accepted)

# 8-18 pull back into agent workspace
h2=grp('H2',[txt('l','Now the tool can',80,182,61,INK,900,8,18,True),txt('e','act across the workflow.',80,265,59,BLUE,900,8,18,True)],s=8,e=18); reveal(h2); L.append(h2)
workspace=grp('Workspace',[card('c',0,0,520,360,'#FFFFFF'),txt('lab','AGENT WORKSPACE',26,24,20,MUT,230,bold=True),txt('goal','Goal: update profile flow',26,72,34,INK,440,bold=True)],280,535,s=8,e=18); reveal(workspace,.1); L.append(workspace)
tools=[('REPO','Inspect files',85,545,GREEN,GI),('TERMINAL','Run commands',85,780,DARK,'#FFFFFF'),('BROWSER','Use tools',770,545,PURPLE,PI),('TESTS','Check result',770,780,AMBER,AI)]
for i,(name,sub,x,y,bg,tc) in enumerate(tools):
 box=grp(name,[card('c',0,0,220,160,bg),txt('n',name,22,24,24,tc,180,bold=True),txt('s',sub,22,76,23,INK if bg!=DARK else '#FFFFFF',180)],x,y,8,18); reveal(box,.35+i*.18); L.append(box)
steps=[('1','Inspect repo',370,680),('2','Edit files',370,755),('3','Run tests',370,830),('4','Review result',370,905)]
for i,(n,label,x,y) in enumerate(steps):
 row=grp('Step '+n,[rect('num',0,0,42,42,BLUE,10),txt('n',n,13,7,20,'#FFFFFF',24,bold=True),txt('label',label,62,6,25,INK,260,bold=True)],x,y,8,18); reveal(row,.5+i*.2); L.append(row)
role=grp('Role',[card('c',0,0,820,135,DARK),txt('t','Typing  →  Directing  →  Reviewing',35,46,34,'#FFFFFF',760,bold=True)],130,1085,8,18); keys(role,'opacity',[(0,0),(5.5,0),(6,100)]); L.append(role)

presenter=copy.deepcopy(next(l for l in proto['composition']['layers'] if l['name']=='Original Creator OS presenter'))
ids=set()
def ext(o):
 ids.add(o['id']); o['activeRange']={'start':0,'duration':18000}
 for ch in o.get('layers',[]): ext(ch)
ext(presenter); presenter['transform']['position']=[40,1390]; presenter['transform']['scale']=[84,84]; L.append(presenter)
dyn=[e for e in proto['composition']['dynamics']['entries'] if e['target']['layerId'] in ids and e['target']['layerId']!=presenter['id']]
arm=next(c for c in presenter['layers'] if c['name']=='Pointing arm'); dyn=[e for e in dyn if e['target']['layerId']!=arm['id']]
keys(presenter,'position',[(0,[40,1650]),(.7,[40,1390])]); keys(arm,'rotation',[(0,18),(.9,-8),(4,-18),(7,-5),(9,-18),(13,-8),(17,-15)])
n1=grp('n1',[txt('s','AUTOCOMPLETE',650,1460,22,BLUE,330,bold=True),txt('b','Predict the next line.\nYou drive every step.',650,1508,30,INK,330)],s=0,e=8); enter(n1); L.append(n1)
n2=grp('n2',[txt('s','AGENTIC WORKFLOW',650,1460,22,BLUE,330,bold=True),txt('b','Inspect, act, test\nand return for review.',650,1508,30,INK,330)],s=8,e=18); enter(n2); L.append(n2)

doc['composition']={'id':'main','name':'V12 Autocomplete to Agents / opening prototype','layers':L[::-1],'dynamics':{'entries':dyn}}
json.dump(doc,open(HERE.parent/'document.json','w'),indent=2); json.dump(A,open(HERE.parent/'animation.json','w'),indent=2)
print('V12',uid,len(A))
