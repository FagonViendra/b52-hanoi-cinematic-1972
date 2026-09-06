import pathlib
P=pathlib.Path.cwd();f=P/'src/build_assets.py';s=f.read_text(encoding='utf-8-sig')
insert=r'''
# RefinementV2: distinct vernacular facades and irregular continuous fracture edges.
def fracture(ma,a,b,ha,hb,th=.28):
 dx=b[0]-a[0]; dz=b[1]-a[1]; le=max(.001,math.hypot(dx,dz)); ox=-dz/le*th/2; oz=dx/le*th/2
 vs=[]
 for side in [-1,1]:
  vs.extend([[a[0]+side*ox,.02,a[1]+side*oz],[b[0]+side*ox,.02,b[1]+side*oz],[b[0]+side*ox,hb,b[1]+side*oz],[a[0]+side*ox,ha,a[1]+side*oz]])
 poly(ma,vs,[[0,1,2,3],[4,7,6,5],[0,4,5,1],[3,2,6,7],[1,5,6,2],[0,3,7,4]])
for vi in range(4):
 w=6+vi*.6; d=9+vi*.55; rr=random.Random(902+vi); asset('ruin'+str(vi))
 quad('ash',[-w*.6,.014,-d*.57],[w*.6,.014,-d*.57],[w*.6,.014,d*.57],[-w*.6,.014,d*.57])
 for side in [-1,1]:
  heights=[rr.uniform(.3,3.7) for j in range(10)]
  if vi==2 and side==-1: heights[1]=5.7;heights[2]=5.25
  for j in range(9):
   if rr.random()<.12: continue
   fracture('brick',(side*w/2,-d/2+j*d/9),(side*w/2,-d/2+(j+1)*d/9),heights[j],heights[j+1],.32)
 for j in range(5):fracture('cream',(-w/2+j*w/5,-d/2),(-w/2+(j+1)*w/5,-d/2),rr.uniform(.3,2.8),rr.uniform(.3,2.8),.30)
 vs=[[0,1.35,0]]
 for j in range(15):
  a=j*math.tau/15;vs.append([math.cos(a)*w*.49,rr.uniform(.12,.45),math.sin(a)*d*.43])
 poly('ash',vs,[[0,j+1,(j+1)%15+1] for j in range(15)])
 for j in range(100):
  x=rr.uniform(-w*.64,w*.64);z=rr.uniform(-d*.57,d*.57);y=max(.07,1.1*(1-(x/(w*.55))**2-(z/(d*.49))**2))+rr.uniform(0,.3)
  box(['brick','ash','tile','cream'][j%4],(x,y,z),(rr.uniform(.18,.7),rr.uniform(.12,.4),rr.uniform(.20,.7)),(rr.random()*2,rr.random()*4,rr.random()*2))
 for j in range(10):beam('dark',(rr.uniform(-w*.5,w*.5),.3,rr.uniform(-d*.48,d*.48)),(rr.uniform(-w*.6,w*.6),rr.uniform(.6,2),rr.uniform(-d*.5,d*.5)),.10,n=6)
 quad('tile',[-w*.5,.25,-d*.1],[-.3,1.7,-d*.2],[.5,1.8,d*.17],[-w*.44,.4,d*.3])
 quad('tile',[.4,.4,-d*.4],[w*.46,.25,-d*.25],[w*.4,1.2,.5],[.2,1.4,.0])
 if vi%2==0:
  for x in [-1.1,1.1]:beam('greenwood',(x,.3,d*.23),(x,2.0,d*.08),.07,n=4)
  for y,z in [(.3,d*.23),(2.0,d*.08)]:beam('greenwood',(-1.1,y,z),(1.1,y,z),.07,n=4)
for vi in range(4,8):
 w=6.25+(vi-4)*.35;d=9.2;h=[3.4,6.65,6.1,3.75][vi-4];ma=['ochre','cream','grey','brick'][vi-4];asset('house'+str(vi))
 box('stone',(0,.16,0),(w+.2,.32,d+.2));box(ma,(0,h/2,0),(w,h,d));box('brick',(0,.45,d/2+.02),(w,.64,.10))
 for x in [-w/2+.18,w/2-.18]:box('cream',(x,h/2,d/2+.1),(.22,h,.22))
 box('dark',(0,1.35,d/2+.05),(1.7,2.5,.1))
 for j in range(6):box('wood',(-.7+j*.28,1.3,d/2+.14),(.25,2.4,.10))
 for x in [-w*.30,w*.30]:window(x,1.65,d/2+.05,1.05,1.55)
 if h>5:
  for x in [-w*.31,0,w*.31]:window(x,4.9,d/2+.05,1.25,1.5)
  box('cream',(0,3.4,d/2+.12),(w+.2,.19,.28))
 if vi==5:
  box('stone',(0,h+.1,0),(w+.4,.20,d+.3));box('cream',(0,h+.55,d/2),(w,.8,.22))
  for x in [-w*.43,0,w*.43]:box('cream',(x,h+.98,d/2),(.35,.2,.4))
 elif vi==6:
  a=[-w/2-.3,h,-d/2-.3];b=[w/2+.3,h,-d/2-.3];c=[w/2+.3,h,d/2+.3];dd=[-w/2-.3,h,d/2+.3];p=[0,h+1.7,-2.4];q=[0,h+1.7,2.4]
  poly('tile',[a,b,c,dd,p,q],[[0,1,4],[1,2,5,4],[2,3,5],[3,0,4,5]]);beam('tile',p,q,.14,n=10)
 else:
  for sg in [-1,1]:quad('tile',[-w/2-.35,h+1.8,0],[w/2+.35,h+1.8,0],[w/2+.35,h,sg*(d/2+.35)],[-w/2-.35,h,sg*(d/2+.35)])
  for x in [-w/2,w/2]:poly(ma,[[x,h,-d/2],[x,h,d/2],[x,h+1.8,0]],[[0,1,2]])
  beam('tile',(-w/2-.4,h+1.86,0),(w/2+.4,h+1.86,0),.14,n=10)
  # Timber shop awning, not a modern sign or steel roller door.
  quad('wood',[-w/2,2.75,d/2],[w/2,2.75,d/2],[w/2,2.45,d/2+1.25],[-w/2,2.45,d/2+1.25])
  for x in [-w/2+.15,w/2-.15]:beam('wood',(x,.15,d/2+1.12),(x,2.55,d/2+1.12),.06,n=6)
 import copy
 A['ruin'+str(vi)]=copy.deepcopy(A['ruin'+str(vi%4)])
'''
if '# RefinementV2:' not in s:s=s.replace("for v in range(4): house(v)\n", "for v in range(4): house(v)\n"+insert+'\n')
a=s.index("asset('wreck')");b=s.index("asset('pole')",a)
s=s[:a]+r'''asset('wreck')
# Irregular torn skin, wing spars and gear, not an intact tubular airframe.
rr=random.Random(272)
for j in range(4):
 z=-1.6+j*1.0;beam('rust',(-5.3,.2,z),(-1.5,2.8,z+.3),.17,n=7);beam('rust',(-1.5,2.8,z+.3),(3.9,.6,z+.5),.15,n=7)
vs=[]
for i in range(7):
 for j in range(7):
  a=-.2+j*.5;rad=2.0+rr.uniform(-.45,.4);vs.append([-5.3+i*1.4+rr.uniform(-.22,.22),.45+math.sin(a)*rad+rr.uniform(-.25,.3),math.cos(a)*rad+rr.uniform(-.3,.3)])
for i in range(6):
 for j in range(6):
  if rr.random()<.16:continue
  ids=[i*7+j,(i+1)*7+j,(i+1)*7+j+1,i*7+j+1]
  poly(['silver','steel','rust'][int(rr.random()*3)],[vs[k] for k in ids],[[0,1,2],[0,2,3]])
poly('air',[[-6,.2,-.3],[-4.7,4.8,-2.0],[-1.8,4.1,-2.1],[1.1,.3,.2],[-2.4,.1,2.2]],[[0,1,2],[0,2,4],[2,3,4]])
for j in range(8):
 t=j/8;beam('silver',(-4.7+2.9*t,4.8-.7*t,-2.0-.1*t),(-5+5.8*t,.3,.8),.065,n=6)
for j in range(10):
 x=rr.uniform(-5,3.5);z=rr.uniform(-2.5,2.3);y=rr.uniform(.2,1.4)
 poly(['rust','silver','steel'][j%3],[[x,y,z],[x+1.4,y+.3,z-.5],[x+2.2,y+.9,z+.7],[x+.5,y+1.8,z+1.5]],[[0,1,2],[0,2,3]])
beam('steel',(1,.6,-1),(3,2.0,1.5),.30,n=12)
for x in [2.4,3.65]:
 for z in [-.85,1.55]:tor('rubber',(x,1.15,z),.89,.29,(0,math.pi/2,0));beam('silver',(x-.12,1.15,z),(x+.12,1.15,z),.50,n=16)
for j in range(22):ell('rust',(-4.6+j*.3,1.5+j*.035,-1.8),(.055,.055,.055),8)
''' + s[b:]
f.write_text(s,encoding='utf-8');print('Refinement V2 saved',len(s))
