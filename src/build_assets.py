"""B52 / Northern Vietnam 1972: parametric Blender authoring, seed 19721218.
Run Blender --background --python src/build_assets.py -- --out .
Without bpy, produces the same compact declarative mesh recipe for the web build.
Blender creates actual meshes, a .blend library and GLB, plus measured bounds.
Y-up recipe -> Blender (x,-z,y). No aircraft serial or individual sortie is asserted.
"""
import math, random, json, sys, pathlib, argparse
P=argparse.ArgumentParser(); P.add_argument('--out',default='.')
args=P.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ([] if 'bpy' in sys.modules else sys.argv[1:]))
ROOT=pathlib.Path(args.out).resolve(); (ROOT/'assets').mkdir(parents=True,exist_ok=True)
R=random.Random(19721218)
M={
 'air':{'color':'#62684b','rough':0.53,'metal':0.38,'tex':'camo'},
 'black':{'color':'#181f21','rough':0.53,'metal':0.3},
 'steel':{'color':'#58656b','rough':0.59,'metal':0.68,'tex':'metal'},
 'wreckskin':{'color':'#74796c','rough':0.91,'metal':0.18,'tex':'metal'},
 'silver':{'color':'#a6b0ac','rough':0.45,'metal':0.72},
 'glass':{'color':'#163543','rough':0.17,'metal':0.58},
 'rubber':{'color':'#202323','rough':0.97},
 'cream':{'color':'#bdac86','rough':0.91,'tex':'plaster'},
 'ochre':{'color':'#ae986f','rough':0.94,'tex':'plaster'},
 'grey':{'color':'#93998f','rough':0.94,'tex':'plaster'},
 'brick':{'color':'#87624b','rough':0.97,'tex':'brick'},
 'tile':{'color':'#724b3c','rough':0.86,'tex':'tile'},
 'wood':{'color':'#484634','rough':0.93,'tex':'wood'},
 'greenwood':{'color':'#384e43','rough':0.86,'tex':'wood'},
 'dark':{'color':'#171d1c','rough':1},
 'stone':{'color':'#7b8177','rough':0.98,'tex':'plaster'},
 'rust':{'color':'#665441','rough':0.86,'metal':0.52,'tex':'metal'},
 'leaf':{'color':'#394c30','rough':0.95},
 'warm':{'color':'#ac8651','rough':0.77,'emissive':'#805529'},
 'ash':{'color':'#716f62','rough':1,'tex':'plaster'}
}
A={}; CURRENT=None
# Records are typed geometric operations, not opaque embedded files.
def asset(name):
 global CURRENT; CURRENT=[]; A[name]=CURRENT

def op(kind,mat,*data): CURRENT.append([kind,mat,*data])
def box(mat,p,s,rot=(0,0,0)): op('box',mat,list(p),list(s),list(rot))
def beam(mat,a,b,r=.08,r2=None,n=8): op('beam',mat,list(a),list(b),r,r if r2 is None else r2,n)
def ell(mat,p,s,n=12): op('ell',mat,list(p),list(s),n)
def tor(mat,p,r,t,rot=(0,0,0)): op('tor',mat,list(p),r,t,list(rot))
def poly(mat,points,faces): op('poly',mat,points,faces)
def lathe(mat,stations,n=40,x=0,y=0): op('lathe',mat,stations,n,x,y)
def quad(mat,a,b,c,d): poly(mat,[a,b,c,d],[[0,1,2,3]])

asset('b52')
# Fuselage station z, horizontal radius, vertical radius, vertical center.
stations=[[-23.8506,.025,.04,-.20],[-23.35,.42,.40,-.14],[-22.4,.93,.85,0],[-21.1,1.37,1.3,.09],[-19.6,1.65,1.72,.16],[-17.4,1.79,1.95,.23],[-14,1.82,1.92,.16],[-10,1.83,1.88,.08],[-5,1.83,1.86,0],[0,1.78,1.83,0],[5,1.62,1.76,.05],[10,1.39,1.58,.15],[14,1.14,1.36,.25],[17,.86,1.10,.31],[20,.57,.77,.35],[22.1,.38,.47,.40],[23.0,.20,.24,.42]]
lathe('black',stations[:5],56); lathe('air',stations[4:],56)
# Airfoil skin: sections x, leading z, chord, center y, thickness fraction.
for s in [-1,1]:
 sections=[[s*1.48,-8.5,14.6,.94,.095],[s*5,-6.5,12.6,1.07,.090],[s*11,-2.5,9.9,1.04,.083],[s*18,2.4,6.7,.68,.074],[s*24,6.55,4.2,.12,.065],[s*28.194,9.52,2.85,-.33,.054]]
 # Calibrate total projected area (including extrapolated center section) to
 # the 4000 sq ft B-52 family reference, not merely length/span bounding boxes.
 # This remains an interpretive airfoil, not a recovered B-52D factory loft.
 chord_scale=371.61216/486.1637
 for sec in sections: sec[2]*=chord_scale
 op('airfoil','air',sections,32)
 # Flap seams and tip fairings, clean historical geometry, not modern winglets.
 for j in range(1,6):
  a=sections[j-1]; b=sections[j]
  beam('black',(a[0],a[3]+.12,a[1]+a[2]*.79),(b[0],b[3]+.08,b[1]+b[2]*.79),.014,n=5)
 for xx,zz in [(8.15,-4.5),(18.25,2.1)]:
  x=s*xx
  # Thin swept pylon, paired J57 nacelles: eight engines in four pods.
  poly('air',[[x-.22,-1.8,zz-2],[x+.22,-1.8,zz-2],[x+.22,.8,zz+3],[x-.22,.8,zz+3],[x-.22,-1.8,zz+3],[x+.22,-1.8,zz+3]],[[0,1,2,3],[0,4,5,1],[1,5,2],[0,3,4],[3,2,5,4]])
  box('air',(x,-1.78,zz+.1),(2.58,.52,5.3))
  for side in [-1,1]:
   ex=x+side*.67; ey=-2.21
   ns=[[zz-3.15,.52,.54,0],[zz-2.92,.62,.64,0],[zz-2.45,.66,.67,0],[zz+1.4,.61,.61,0],[zz+2.8,.47,.48,.03],[zz+3.1,.40,.41,.03]]
   lathe('air',ns,32,ex,ey)
   beam('silver',(ex,ey,zz-3.17),(ex,ey,zz-3.03),.525,n=32)
   beam('dark',(ex,ey,zz-3.20),(ex,ey,zz-3.17),.455,n=32)
   ell('steel',(ex,ey,zz-3.22),(.14,.14,.26),12)
   for k in range(14):
    th=k*math.tau/14; a=(ex+.16*math.cos(th),ey+.16*math.sin(th),zz-3.215); b=(ex+.42*math.cos(th+.20),ey+.42*math.sin(th+.20),zz-3.211)
    beam('steel',a,b,.017,n=4)
   beam('black',(ex,ey+.03,zz+3.0),(ex,ey+.03,zz+3.16),.36,n=28)
   beam('dark',(ex,ey+.03,zz+3.17),(ex,ey+.03,zz+3.20),.30,n=28)
 # Outboard streamlined fuel tank.
 lathe('black',[[6.3,.03,.03,0],[6.8,.48,.48,0],[7.8,.69,.70,0],[11.7,.64,.65,0],[13.4,.30,.31,0],[14.1,.02,.02,0]],28,s*25.6,-.30)
 op('airfoil','air',[[s*.7,13.6,8,1.0,.095],[s*4.3,15.8,5.8,1.3,.080],[s*8.65,19.3,2.0,1.55,.065]],24)
# Tall D vertical tail, with two-sided actual thickness.
poly('air',[[-.23,1.1,11.3],[.23,1.1,11.3],[-.15,11.55,18.4],[.15,11.55,18.4],[-.09,11.55,21.5],[.09,11.55,21.5],[-.24,1.0,23.0],[.24,1.0,23.0]],[[0,2,4,6],[1,7,5,3],[0,1,3,2],[2,3,5,4],[4,5,7,6],[6,7,1,0]])
for s in [-1,1]:
 beam('black',(s*.245,1.5,21.2),(s*.115,11.3,20.95),.019,n=5)
 # Faceted cockpit glazing stays near the fuselage skin.
 quad('glass',[s*.09,1.70,-20.1],[s*.79,1.59,-19.96],[s*.98,2.015,-18.52],[s*.11,2.15,-18.55])
 quad('glass',[s*.92,1.59,-19.86],[s*1.35,1.32,-19.40],[s*1.58,1.69,-17.82],[s*1.10,1.99,-18.48])
 quad('glass',[s*1.38,1.27,-19.25],[s*1.66,.91,-18.5],[s*1.78,1.03,-16.8],[s*1.61,1.63,-17.62])
 beam('silver',(s*.87,1.65,-19.90),(s*1.035,2.05,-18.49),.035,n=6)
 # Gear doors and aerials, not exposed wheels in flight.
 box('black',(s*.65,-1.785,-8.2),(1.12,.055,4.6))
 box('black',(s*.56,-1.70,7.0),(.95,.055,3.7))
 beam('steel',(s*1.73,.30,-18.5),(s*1.9,.28,-20.3),.023,n=6)
for xx in [-.16,.16]:
 for yy in [.29,.55]: beam('black',(xx,yy,22.86),(xx,yy,23.8506),.055,n=10)
for z in [-12,-4,8]:
 poly('black',[[-.04,1.85,z],[.04,1.85,z],[.02,2.4,z+.65],[-.02,2.4,z+.65]],[[0,1,2,3]])
asset('baydoor'); box('black',(0,0,0),(1.38,.08,8.5))
asset('bomb')
lathe('steel',[[-1.15,.01,.01,0],[-.9,.17,.17,0],[-.65,.24,.24,0],[.65,.24,.24,0],[.92,.13,.13,0],[1.1,.08,.08,0]],16)
for a in [0,math.pi/2]: box('steel',(0,0,.93),(.68,.045,.60),(0,0,a))

# Vernacular tiled buildings; every visible member is an authored mesh.
def roof(w,d,h,mat='tile'):
 rise=w*.25
 for z in [-d/2,d/2]: poly('cream',[[-w/2,h,z],[w/2,h,z],[0,h+rise,z]],[[0,1,2]])
 for s in [-1,1]:
  quad(mat,[0,h+rise,-d/2-.35],[s*(w/2+.35),h,-d/2-.35],[s*(w/2+.35),h,d/2+.35],[0,h+rise,d/2+.35])
  for j in range(8):
   f=j/8; beam('tile',(s*(w/2+.35)*f,h+rise*(1-f)+.015,-d/2-.35),(s*(w/2+.35)*f,h+rise*(1-f)+.015,d/2+.35),.032,n=5)
 beam('tile',(0,h+rise+.09,-d/2-.4),(0,h+rise+.09,d/2+.4),.14,n=10)
 for x in [-w/2,w/2]: beam('wood',(x,h,-d/2-.4),(x,h,d/2+.4),.07,n=6)

def window(x,y,z,w=1.12,h=1.65,mat='greenwood'):
 box('dark',(x,y,z),(w+.14,h+.14,.09)); box('cream',(x,y-h/2-.13,z+.12),(w+.32,.14,.30))
 for s in [-1,1]:
  box(mat,(x+s*w*.27,y,z+.095),(w*.45,h,.09))
  for k in range(7): box('wood',(x+s*w*.27,y-h*.39+k*h*.13,z+.151),(w*.39,.065,.035))
 beam('cream',(x-w*.53,y+h*.55,z+.08),(x+w*.53,y+h*.55,z+.08),.065,n=4)

def house(v):
 w=6.0+v*.6; d=9.0+v*.55; h=5.8+v*.45; ma=['cream','ochre','grey','cream'][v]
 asset('house'+str(v)); box('stone',(0,.18,0),(w+.2,.36,d+.2)); box(ma,(0,h/2,0),(w,h,d))
 box('brick',(0,.66,d/2+.025),(w,.9,.12))
 box('cream',(0,3.1,d/2+.14),(w+.18,.2,.30)); box('cream',(0,h-.12,d/2+.15),(w+.25,.22,.36))
 for x in [-w/2+.19,w/2-.19]: box('cream',(x,h/2,d/2+.14),(.24,h,.22))
 box('dark',(0,1.36,d/2+.05),(1.62,2.45,.12));
 for j in range(6): box('wood',(-.67+j*.27,1.30,d/2+.13),(.24,2.37,.10))
 for xx in [-w*.30,w*.30]: window(xx,1.65,d/2+.08,1.08,1.65); window(xx,4.38,d/2+.08,1.18,1.64)
 if v%2==0:
  box('stone',(0,3.26,d/2+.78),(w*.73,.18,1.6));
  for xx in [-w*.35,w*.35]: beam('steel',(xx,3.35,d/2+1.52),(xx,4.23,d/2+1.52),.038,n=5)
  beam('steel',(-w*.35,4.23,d/2+1.52),(w*.35,4.23,d/2+1.52),.048,n=6)
  for j in range(13): beam('steel',(-w*.35+j*w*.7/12,3.35,d/2+1.52),(-w*.35+j*w*.7/12,4.23,d/2+1.52),.025,n=4)
 roof(w,d,h)
 # Side windows, rain pipe, a small period masonry chimney.
 for side in [-1,1]:
  for zz in [-2.7,1.1]: box('greenwood',(side*(w/2+.03),4.1,zz),(.08,1.4,1.0))
 beam('steel',(w/2-.25,.2,d/2+.30),(w/2-.25,h,d/2+.30),.055,n=8)
 box('brick',(-w*.26,h+.62,-d*.25),(.55,1.4,.58)); box('stone',(-w*.26,h+1.35,-d*.25),(.72,.15,.75))
 # Separate, rewindable wreck state; jagged masonry not a flattened intact box.
 asset('ruin'+str(v)); box('ash',(0,.12,0),(w+.2,.24,d+.2))
 rr=random.Random(72+v)
 for side in [-1,1]:
  for j in range(5):
   hh=rr.uniform(.55,3.5); box('brick',(side*w/2,hh/2,-d/2+j*d/5),(.35,hh,d/5*.88))
 for j in range(5):
  hh=rr.uniform(.3,2.2); box('cream',(-w/2+j*w/5,hh/2,-d/2),(w/5*.87,hh,.33))
 for j in range(60):
  p=(rr.uniform(-w*.7,w*.7),rr.uniform(.1,.75),rr.uniform(-d*.62,d*.65)); sc=(rr.uniform(.18,.8),rr.uniform(.1,.4),rr.uniform(.14,.85))
  box(['brick','ash','tile'][j%3],p,sc,(rr.random(),rr.random()*3,rr.random()))
 for j in range(9): beam('wood',(rr.uniform(-w*.5,w*.5),.3,rr.uniform(-d*.45,d*.45)),(rr.uniform(-w*.6,w*.6),rr.uniform(.5,2),rr.uniform(-d*.4,d*.4)),.085,n=5)
for v in range(4): house(v)

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


asset('hospital')
# Interpretive central facade, based on archive photographs, not survey drawings.
box('stone',(0,.2,0),(16,.4,8)); box('cream',(0,4.5,0),(14,9,6))
box('cream',(0,7.92,3.48),(16,.5,1)); box('stone',(0,9.02,0),(14.6,.24,6.6))
for x in [-6.5,-3.7,3.7,6.5]: box('cream',(x,4.4,3.17),(.42,8.8,.48))
for x in [-2,2]:
 box('dark',(x,2.3,3.05),(2.5,4.35,.18))
 for j in range(7): box('greenwood',(x-1.04+j*.34,2.22,3.2),(.28,4.15,.12))
for x in [-5.1,0,5.1]:
 box('dark',(x,8.45,3.10),(1.65,.62,.1))
 for j in range(5): box('stone',(x-.66+j*.33,8.45,3.22),(.095,.64,.17))
for x in [-7.4,7.4]:
 box('stone',(x,1.0,6.8),(.8,2,1.0)); box('cream',(x,2.05,6.8),(1,.14,1.2))
for step in range(4): box('stone',(0,.10+step*.13,4.6-step*.34),(10,.2+step*.26,1.55))
asset('ward')
box('cream',(0,3.1,0),(28,6.2,9)); box('brick',(0,.43,4.54),(28,.75,.12))
for x in [-12,-8,-4,0,4,8,12]: window(x,1.9,4.54,1.65,2); window(x,4.74,4.54,1.6,1.7)
box('cream',(0,3.27,4.64),(28,.17,.3))
for sg in [-1,1]:
 quad('tile',[-14.4,8.5,0],[14.4,8.5,0],[14.4,6.2,sg*4.85],[-14.4,6.2,sg*4.85])
 for j in range(7):
  t=j/7; beam('tile',(-14.4,8.5-2.3*t,sg*4.85*t),(14.4,8.5-2.3*t,sg*4.85*t),.035,n=5)
for x in [-14,14]: poly('cream',[[x,6.2,-4.5],[x,6.2,4.5],[x,8.5,0]],[[0,1,2]])
beam('tile',(-14.5,8.59,0),(14.5,8.59,0),.13,n=10)

asset('bridge')
box('wood',(0,7.4,0),(40,.35,8.0))
for z in [-.75,.75]: box('steel',(0,7.64,z),(40,.15,.10))
for j in range(40): box('wood',(-19.5+j,7.63,0),(.23,.14,3.1))
for z in [-3.5,3.5]:
 points=[(-20,16,z),(-12,13,z),(-4,11,z),(4,11,z),(12,13,z),(20,16,z)]
 for j in range(5):
  a=points[j]; b=points[j+1]; beam('rust',a,b,.19,n=6); beam('rust',(a[0],7.7,z),(b[0],7.7,z),.19,n=6)
  beam('rust',(a[0],7.7,z),b,.14,n=6); beam('rust',a,(b[0],7.7,z),.11,n=6)
 for x,y,_ in points: beam('rust',(x,7.7,z),(x,y,z),.16,n=6)
for x in [-20,-12,-4,4,12,20]:
 y=16 if abs(x)==20 else 13 if abs(x)==12 else 11
 beam('rust',(x,y,-3.5),(x,y,3.5),.16,n=6); beam('rust',(x,y,-3.5),(x+6,y-1,3.5),.09,n=6)
for x in [-20,20]: box('stone',(x,2.8,0),(2.8,9.1,6.4))

asset('warehouse'); box('brick',(0,3,0),(18,6,35)); roof(18,35,6,'steel')
for z in [-17.53,17.53]:
 for x in [-6,0,6]: box('wood',(x,2.1,z),(3,4.0,.10))
asset('crane')
for x in [-2.7,2.7]:
 for z in [-2.7,2.7]: beam('rust',(x,0,z),(x*.5,13,z*.5),.18,n=8)
for y in [2,5,8,11]:
 for z in [-2.3,2.3]: beam('rust',(-2.3,y,z),(2.3,y+2,z),.10,n=5)
box('steel',(0,13,0),(4.3,2.5,3.5)); box('glass',(0,13.4,1.8),(3,.9,.12))
beam('rust',(0,14,0),(0,23,21),.28,n=8); beam('rust',(0,12,0),(0,21,21),.22,n=8)
for i in range(10): beam('rust',(0,14+i*.9,i*2.1),(0,12+(i+1)*.9,(i+1)*2.1),.10,n=6)
beam('steel',(0,23,21),(0,4,21),.037,n=6)
asset('boat')
poly('black',[[-5,0,-20],[5,0,-20],[5,0,13],[0,0,23],[-5,0,13],[-4,-3,-16],[4,-3,-16],[4,-3,12],[0,-2,20],[-4,-3,12]],[[0,1,2,3,4],[0,5,6,1],[1,6,7,2],[2,7,8,3],[3,8,9,4],[4,9,5,0],[5,9,8,7,6]])
box('rust',(0,.5,-2),(8,1,29)); box('cream',(0,3.4,-13),(7,5.8,8)); box('black',(0,6.4,-13),(7.7,.35,8.6))
for x in [-2,0,2]: box('glass',(x,4.8,-8.93),(1.4,1,.1))
beam('rust',(0,0,9),(0,14,9),.16,n=10)

for side in [-1,1]:
 for z in [-17,-12,-7,-2,3,8,13]:
  beam('steel',(side*4.65,.25,z),(side*4.65,1.20,z),.055,n=8)
  if z<13:beam('steel',(side*4.65,1.17,z),(side*4.65,1.17,z+5),.045,n=8)
 for z in [-14,-4,6,12]:tor('rubber',(side*5.0,.02,z),.63,.15,(0,math.pi/2,0))
 for z in [-15,-12,-10]:box('glass',(side*3.53,4.8,z),(.08,1.15,1.55))
for z in range(-7,13):box('wood',(0,1.045,z),(7.9,.055,.05))
for z in [-3,6]:
 box('steel',(0,1.22,z),(5.6,.36,6.1))
 for k in [-2,-1,0,1,2]:box('rust',(k,1.45,z),(.10,.09,6.2))
for z in [-18,15]:
 for x in [-3,3]:beam('steel',(x,.2,z),(x,1.0,z),.22,n=12);beam('steel',(x-.4,.9,z),(x+.4,.9,z),.12,n=10)
beam('steel',(0,13.8,9),(-4.3,1,16),.026,n=6);beam('steel',(0,13.8,9),(4.3,1,16),.026,n=6);beam('steel',(0,13.8,9),(0,6.6,-10),.026,n=6)
beam('black',(1.6,6.4,-14),(1.6,9.,-14),.35,n=14)
asset('chimney'); beam('brick',(0,0,0),(0,30,0),2.1,1.4,n=20); beam('black',(0,29.9,0),(0,30.12,0),1.12,n=20)

asset('wreck')
rr=random.Random(272)
for j in range(4):
 z=-1.6+j*1.;beam('rust',(-5.3,.2,z),(-1.5,2.8,z+.3),.17,n=9);beam('rust',(-1.5,2.8,z+.3),(3.9,.6,z+.5),.15,n=9)
# One connected, dented shell: shared vertices give coherent smooth metal normals.
vs=[];fs=[];nx=21;na=17
for i in range(nx):
 for j in range(na):
  a=-.17+j*math.pi/(na-1);u=i/(nx-1);rad=1.8+.18*math.sin(i*.8+j*.6)+.13*math.cos(j*1.2-i*.2)
  vs.append([-5.3+u*8.2+.10*math.sin(j*1.6+i),.45+math.sin(a)*rad+.08*math.sin(i*1.9+j),math.cos(a)*rad+.11*math.sin(i*.7+j*1.6)])
for i in range(nx-1):
 for j in range(na-1):
  if (i<2 and j%5<2) or (i>17 and j%4==0) or (7<i<11 and 4<j<8):continue
  fs.append([i*na+j,(i+1)*na+j,(i+1)*na+j+1,i*na+j+1])
op('poly','wreckskin',vs,fs,True)
# Broken wing skin follows a shallow bent surface rather than a flat triangle.
vs=[];fs=[]
for i in range(12):
 for j in range(8):
  u=i/11;v=j/7;vs.append([-5.8+u*4.8,.30+(1-v)*4.0+math.sin(u*3+v*4)*.18,-1.6+v*3.1+u*.15])
for i in range(11):
 for j in range(7):
  if i>8 and j==0:continue
  fs.append([i*8+j,(i+1)*8+j,(i+1)*8+j+1,i*8+j+1])
op('poly','wreckskin',vs,fs,True)
for j in range(10):
 u=j/10;beam('steel',(-5.8+u*4.8,4.3+math.sin(u*3)*.18,-1.6+u*.15),(-5.8+u*4.8,.3,1.5+u*.15),.065,n=8)
for j in range(5):
 x=rr.uniform(-5,2);z=rr.uniform(-2.3,1.8);y=rr.uniform(.2,.8)
 op('poly','wreckskin',[[x,y,z],[x+1.,y+.2,z-.3],[x+1.6,y+.65,z+.6],[x+.4,y+1.0,z+1.1]],[[0,1,2],[0,2,3]],True)
beam('steel',(1,.6,-1),(3,2.,1.5),.30,n=16)
for x in [2.4,3.65]:
 for z in [-.85,1.55]:tor('rubber',(x,1.15,z),.89,.29,(0,math.pi/2,0));beam('steel',(x-.12,1.15,z),(x+.12,1.15,z),.50,n=24)
for j in range(32):ell('rust',(-4.8+j*.24,1.36+j*.014,-1.78),(.055,.055,.055),8)
asset('pole'); beam('wood',(0,0,0),(0,9,0),.12,.08,n=10); box('wood',(0,8.3,0),(2.5,.14,.18))
for x in [-1,0,1]: beam('stone',(x,8.4,0),(x,8.75,0),.085,n=8)
asset('tree')
beam('wood',(0,0,0),(.17,5.4,.18),.34,.15,n=10)
for j in range(12):
 a=j*2.4; y=2.4+j*.22; b=(math.cos(a)*2.4,y+2.5,math.sin(a)*2.4)
 beam('wood',(.10,y,0),b,.10,.025,n=7)
asset('bicycle')
for z in [-.9,.9]: tor('rubber',(0,.70,z),.67,.036,(0,math.pi/2,0)); tor('steel',(0,.70,z),.62,.012,(0,math.pi/2,0))
for a,b in [((0,.7,-.9),(0,.8,.0)),((0,.8,0),(0,.7,.9)),((0,.7,-.9),(0,1.55,-.35)),((0,1.55,-.35),(0,.8,0)),((0,1.55,-.35),(0,1.55,.65)),((0,1.55,.65),(0,.8,0)),((0,1.55,.65),(0,.7,.9))]: beam('greenwood',a,b,.028,n=6)
box('black',(0,1.6,-.35),(.28,.08,.38)); beam('steel',(-.32,1.82,.62),(.32,1.82,.62),.025,n=6)

DATA={'format':'B52-parametric-v1','seed':19721218,'units':'metres','up':'Y','authoring':'Blender 5.1 + src/build_assets.py','materials':M,'assets':A,'expected_aircraft':{'span_m':56.388,'length_m':47.7012,'engine_count':8,'variant':'B-52D','note':'Representative exterior, not serial-specific; height in flight is not ground height.'}}
(ROOT/'assets'/'recipe.json').write_text(json.dumps(DATA,separators=(',',':')),encoding='utf-8')
print('RECIPE',len(json.dumps(DATA)),len(A),'assets',sum(len(x) for x in A.values()),'operations',flush=True)
try: import bpy
except ImportError: print('Recipe generated; Blender authoring is skipped outside Blender.'); sys.exit(0)
from mathutils import Vector, Matrix, Euler
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
matlib={}
for name,d in M.items():
 m=bpy.data.materials.new(name); m.use_nodes=True; nd=m.node_tree.nodes; nd.clear(); bs=nd.new('ShaderNodeBsdfPrincipled'); out=nd.new('ShaderNodeOutputMaterial'); m.node_tree.links.new(bs.outputs['BSDF'],out.inputs['Surface']); h=d['color'].lstrip('#'); rgb=[int(h[i:i+2],16)/255 for i in [0,2,4]]
 # Blender node values are linear; convert authored sRGB colors.
 rgb=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
 bs.inputs['Base Color'].default_value=(*rgb,1); bs.inputs['Roughness'].default_value=d.get('rough',.8); bs.inputs['Metallic'].default_value=d.get('metal',0)
 if name=='air':
  tex=nd.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=.18; tex.inputs['Detail'].default_value=1.3
  ramp=nd.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation='CONSTANT'; e=ramp.color_ramp.elements; e[0].position=.30; e[0].color=(.035,.055,.035,1); e[1].position=.58; e[1].color=(.24,.21,.12,1); e.new(.44).color=(.12,.15,.07,1)
  m.node_tree.links.new(tex.outputs['Fac'],ramp.inputs['Fac']); m.node_tree.links.new(ramp.outputs['Color'],bs.inputs['Base Color'])
 matlib[name]=m

def cv(p): return (p[0],-p[2],p[1])
def rawmesh(n,vs,fs,ma,smooth=False):
 me=bpy.data.meshes.new(n); me.from_pydata([cv(p) for p in vs],[],fs); me.update(); ob=bpy.data.objects.new(n,me); bpy.context.collection.objects.link(ob); ob.data.materials.append(matlib[ma]);
 for f in me.polygons: f.use_smooth=smooth
 return ob

def localmat(rot):
 # Recipe rotation order XYZ, matrix used by both renderers.
 return Euler(rot,'XYZ').to_matrix()
def transform(v,p,s,rot):
 q=localmat(rot)@Vector((v[0]*s[0],v[1]*s[1],v[2]*s[2])); return [q[i]+p[i] for i in range(3)]
def makeop(rec,n):
 k,ma,*d=rec; vs=[]; fs=[]; smooth=False
 if k=='box':
  p,s,rot=d; vs=[transform(v,p,s,rot) for v in [(-.5,-.5,-.5),(.5,-.5,-.5),(.5,.5,-.5),(-.5,.5,-.5),(-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5)]]; fs=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[3,7,6,2],[1,2,6,5],[0,4,7,3]]
 elif k=='poly': vs,fs=d[:2]; smooth=bool(d[2]) if len(d)>2 else False
 elif k=='lathe':
  stations,seg,xx,yy=d; smooth=True
  for z,rx,ry,cy in stations:
   for j in range(seg): a=j*math.tau/seg; vs.append([xx+rx*math.cos(a),yy+cy+ry*math.sin(a),z])
  for i in range(len(stations)-1):
   for j in range(seg): fs.append([i*seg+j,i*seg+(j+1)%seg,(i+1)*seg+(j+1)%seg,(i+1)*seg+j])
 elif k=='airfoil':
  secs,steps=d; smooth=True
  for x,lead,chord,cy,thick in secs:
   for j in range(steps*2):
    a=j*math.tau/(steps*2); f=(1-math.cos(a))*.5
    t=5*thick*chord*(.2969*math.sqrt(max(f,0))-.126*f-.3516*f*f+.2843*f**3-.1015*f**4)
    vs.append([x,cy+(t if j<=steps else -t),lead+f*chord])
  ns=steps*2
  for i in range(len(secs)-1):
   for j in range(ns): fs.append([i*ns+j,i*ns+(j+1)%ns,(i+1)*ns+(j+1)%ns,(i+1)*ns+j])
 elif k=='beam':
  a,b,r1,r2,seg=d; smooth=True; va=Vector(a); vb=Vector(b); axis=(vb-va).normalized(); u=axis.cross(Vector((0,1,0)))
  if u.length<.001: u=axis.cross(Vector((1,0,0)))
  u.normalize(); v=axis.cross(u)
  for cen,r in [(va,r1),(vb,r2)]:
   for j in range(seg): q=cen+r*(u*math.cos(j*math.tau/seg)+v*math.sin(j*math.tau/seg)); vs.append(list(q))
  for j in range(seg): fs.append([j,(j+1)%seg,(j+1)%seg+seg,j+seg])
  fs.extend([list(reversed(range(seg))),list(range(seg,seg*2))])
 elif k in ['ell','tor']:
  p=d[0]; smooth=True
  if k=='ell':
   s,seg=d[1:]; rows=max(6,seg//2)
   for i in range(rows+1):
    th=i*math.pi/rows
    for j in range(seg): a=j*math.tau/seg; vs.append([p[0]+s[0]*math.sin(th)*math.cos(a),p[1]+s[1]*math.cos(th),p[2]+s[2]*math.sin(th)*math.sin(a)])
  else:
   r,t,rot=d[1:]; rows=10; seg=24
   for i in range(rows+1):
    b=i*math.tau/rows
    for j in range(seg): a=j*math.tau/seg; v=[(r+t*math.cos(b))*math.cos(a),(r+t*math.cos(b))*math.sin(a),t*math.sin(b)]; vs.append(transform(v,p,(1,1,1),rot))
  for i in range(rows):
   for j in range(seg): fs.append([i*seg+j,i*seg+(j+1)%seg,(i+1)*seg+(j+1)%seg,(i+1)*seg+j])
 return rawmesh(n,vs,fs,ma,smooth)
measure={}
for name,recs in A.items():
 col=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(col); objs=[]
 for i,rec in enumerate(recs):
  ob=makeop(rec,name+'_'+str(i));
  for c in list(ob.users_collection): c.objects.unlink(ob)
  col.objects.link(ob); objs.append(ob)
 bpy.context.view_layer.update()
 pts=[ob.matrix_world@Vector(p) for ob in objs for p in ob.bound_box]
 mi=[min(p[i] for p in pts) for i in range(3)]; mx=[max(p[i] for p in pts) for i in range(3)]
 measure[name]={'objects':len(objs),'blender_min':mi,'blender_max':mx,'dimensions':[mx[i]-mi[i] for i in range(3)],'polygons':sum(len(o.data.polygons) for o in objs)}
 # Space assets for inspectable authoring contact sheet; runtime uses local origins.
 index=list(A).index(name); offset=Vector(((index%5)*65,(index//5)*65,0))
 for ob in objs: ob.location+=offset
bpy.context.scene.unit_settings.system='METRIC'
world=bpy.context.scene.world or bpy.data.worlds.new('World'); bpy.context.scene.world=world; world.use_nodes=True; next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs[0].default_value=(.19,.22,.24,1); next(n for n in world.node_tree.nodes if n.type=='BACKGROUND').inputs[1].default_value=.8
bpy.ops.object.light_add(type='AREA',location=(10,-25,55)); key=bpy.context.object; key.name='Inspection key'; key.data.energy=25000; key.data.shape='DISK'; key.data.size=40
bpy.ops.object.camera_add(location=(65,-70,46)); cam=bpy.context.object; direction=Vector((0,0,2))-cam.location; cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler(); cam.data.lens=46; bpy.context.scene.camera=cam
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=24; scene.render.resolution_x=1280; scene.render.resolution_y=800; scene.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets'/'Northern_Vietnam_1972.blend'))
# GLB library is supplementary; compact exported recipe is the browser delivery.
bpy.ops.export_scene.gltf(filepath=str(ROOT/'assets'/'library.glb'),export_format='GLB',export_cameras=False,export_lights=False)
(ROOT/'assets'/'blender_measurements.json').write_text(json.dumps({'blender':bpy.app.version_string,'assets':measure},indent=2))
print('BLENDER_SAVED',bpy.app.version_string,json.dumps(measure['b52']),flush=True)
