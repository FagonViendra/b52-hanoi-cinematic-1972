"""Reference-led asset rebuild. Callable from build_assets.py; idempotent replacement.
Units metres, Y up, aircraft nose -Z. Shared Blender/web geometry, no opaque imports.
References and uncertainties: references/v2 and HISTORY_V2.md.
"""
import math,random,json,pathlib
TAU=math.tau

def rebuild(A,M,ROOT):
    ops=[]; audit={'version':2,'bridge_members':[],'house_dimensions':{},'aircraft':{}}
    def asset(name):
        nonlocal ops
        ops=[];A[name]=ops
    def op(k,m,*d):ops.append([k,m,*d])
    def box(m,p,s,rot=(0,0,0)):op('box',m,list(p),list(s),list(rot))
    def beam(m,a,b,r=.04,n=8,r2=None):op('beam',m,list(a),list(b),r,r if r2 is None else r2,n)
    def ell(m,p,s,n=12):op('ell',m,list(p),list(s),n)
    def poly(m,v,f,smooth=False):op('poly',m,v,f,smooth)
    def quad(m,*v):poly(m,list(v),[[0,1,2,3]])
    def lathe(m,st,n=48,x=0,y=0):op('lathe',m,st,n,x,y)
    def tor(m,p,r,t,rot=(0,0,0)):op('tor',m,list(p),r,t,list(rot))
    def sub(a,b):return [a[i]-b[i] for i in range(3)]
    def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
    def unit(v):
        d=math.sqrt(sum(x*x for x in v));return [x/d for x in v]
    def mix(a,b,t):return [a[i]*(1-t)+b[i]*t for i in range(3)]
    def prism(m,a,b,w,h):
        axis=unit(sub(b,a));u=unit(cross(axis,[0,0,1] if abs(axis[2])<.9 else [0,1,0]));v=cross(axis,u)
        vs=[[p[k]+su*w*.5*u[k]+sv*h*.5*v[k] for k in range(3)] for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        poly(m,vs,[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])
    def ibeam(a,b,depth=.32,width=.25,th=.038,material='bridgepaint',record=True):
        # Extruded web and two flanges meet exactly at shared panel nodes.
        axis=unit(sub(b,a));u=unit(cross(axis,[0,0,1] if abs(axis[2])<.9 else [0,1,0]));v=cross(axis,u)
        def part(uc,vc,du,dv):
            vs=[[p[k]+(uc+su*du*.5)*u[k]+(vc+sv*dv*.5)*v[k] for k in range(3)] for p in [a,b] for su,sv in [(-1,-1),(1,-1),(1,1),(-1,1)]]
            poly(material,vs,[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])
        part(0,0,depth,th);part(-depth/2+th/2,0,th,width);part(depth/2-th/2,0,th,width)
        if record:audit['bridge_members'].append({'a':[round(x,5) for x in a],'b':[round(x,5) for x in b]})
    M.update({
      'air':{'color':'#ffffff','rough':.67,'metal':.06,'tex':'camo'},
      'black':{'color':'#161b1b','rough':.5,'metal':.1},
      'airframe':{'color':'#424e40','rough':.62,'metal':.07},
      'panel':{'color':'#28322e','rough':.7,'metal':.1},
      'inlet':{'color':'#5f6966','rough':.4,'metal':.65},
      'glass':{'color':'#163641','rough':.12,'metal':.52},
      'bridgepaint':{'color':'#786a57','rough':.84,'metal':.42,'tex':'rust'},
      'bridgerivet':{'color':'#554c3e','rough':.85,'metal':.40},
      'rail':{'color':'#92938b','rough':.36,'metal':.75},
      'masonry':{'color':'#918576','rough':1,'tex':'masonry'},
      'oldplaster':{'color':'#b6aa8d','rough':.96,'tex':'weathered'},
      'plastergrey':{'color':'#9c9e90','rough':.98,'tex':'weathered'},
      'plasterochre':{'color':'#b49a70','rough':.98,'tex':'weathered'},
      'roofold':{'color':'#80604c','rough':.96,'tex':'tilesv2'},
      'roofdark':{'color':'#716558','rough':.98,'tex':'tilesv2'},
      'lime':{'color':'#c7bb9d','rough':.96,'tex':'weathered'},
      'chipped':{'color':'#736b5a','rough':1,'tex':'weathered'},
      'brickred':{'color':'#876348','rough':.95,'tex':'brickv2'},
      'shutter':{'color':'#44574c','rough':.88,'tex':'wood'},
      'timber':{'color':'#6a5944','rough':.94,'tex':'wood'},
      'tilefragment':{'color':'#906a50','rough':.98,'tex':'tilesv2'},
      'mortar':{'color':'#b2ac99','rough':1,'tex':'weathered'}
    })
    # B-52D: rounded lower radome and raised flight deck, rather than a pointed cone.
    asset('b52')
    st=[[-23.8506,.025,.035,-.17],[-23.76,.34,.28,-.18],[-23.45,.80,.54,-.12],[-23.05,1.16,.77,-.01],[-22.5,1.44,1.05,.05],[-21.7,1.59,1.37,.15],[-20.8,1.67,1.68,.29],[-19.8,1.72,1.86,.36],[-18.4,1.78,1.94,.32],[-16,1.84,1.91,.19],[-12,1.85,1.87,.10],[-7,1.84,1.85,.02],[0,1.78,1.82,0],[6,1.57,1.75,.05],[11,1.34,1.51,.13],[16,.95,1.17,.25],[20,.58,.78,.35],[22,.38,.46,.4],[23.1,.2,.23,.42]]
    # Use an angle-dependent seam: black extends well above the geometric underside.
    vs=[];n=80
    for z,rx,ry,cy in st:
        for j in range(n):
            a=j*TAU/n;vs.append([rx*math.cos(a),cy+ry*math.sin(a),z])
    for material in ['air','black']:
        faces=[]
        for i in range(len(st)-1):
            for j in range(n):
                a=(j+.5)*TAU/n;z=(st[i][0]+st[i+1][0])*.5
                upper=math.sin(a)>(.36+.045*math.sin(z*.8)) and z>-23.2
                if upper==(material=='air'):faces.append([i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j])
        poly(material,vs,faces,True)
    sections_base=[[0,-8.1,10.8,1.24,.115],[3,-6.48,9.85,1.27,.105],[7,-3.85,8.4,1.28,.09],[12,-.47,6.77,1.20,.075],[18,3.73,4.96,.99,.067],[24,7.86,3.08,.61,.06],[28.194,10.79,1.75,.27,.055]]
    wing_area=2*sum((sections_base[i][2]+sections_base[i+1][2])*.5*(sections_base[i+1][0]-sections_base[i][0]) for i in range(len(sections_base)-1))
    factor=371.61216/wing_area
    for sgn in [-1,1]:
        sections=[[sgn*x,z,c*factor,y,h] for x,z,c,y,h in sections_base];op('airfoil','air',sections,36)
        for i in range(len(sections)-1):
            a,b=sections[i],sections[i+1];beam('panel',[a[0],a[3]+.06,a[1]+a[2]*.82],[b[0],b[3]+.035,b[1]+b[2]*.82],.012,5)
        # Four slim pylons, each suspending two distinctly cylindrical J57 nacelles.
        for xx,zz,yy in [(8.45,-4.15,-1.5),(18.9,3.3,-1.62)]:
            x=sgn*xx
            poly('black',[[x-.15,yy+.4,zz-.9],[x+.15,yy+.4,zz-.9],[x+.14,1.0,zz+2.5],[x-.14,1.0,zz+2.5],[x-.14,yy+.5,zz+2.55],[x+.14,yy+.5,zz+2.55]],[[0,1,2,3],[0,4,5,1],[1,5,2],[0,3,4],[3,2,5,4]])
            for side in [-1,1]:
                ex=x+side*.61;ns=[[zz-2.95,.47,.48,0],[zz-2.83,.57,.57,0],[zz-2.42,.60,.60,0],[zz+.45,.55,.57,0],[zz+2.25,.40,.42,.04],[zz+2.6,.35,.36,.04]]
                lathe('black',ns,48,ex,yy)
                # Metallic intake lip torus, dark cavity and recessed compressor.
                tor('inlet',(ex,yy,zz-2.96),.468,.04)
                beam('dark',(ex,yy,zz-2.78),(ex,yy,zz-2.75),.442,40)
                ell('inlet',(ex,yy,zz-2.805),(.105,.105,.17),16)
                for k in range(18):
                    a=k*TAU/18
                    quad('inlet',[ex+.12*math.cos(a),yy+.12*math.sin(a),zz-2.80],[ex+.4*math.cos(a+.20),yy+.4*math.sin(a+.20),zz-2.80],[ex+.4*math.cos(a+.28),yy+.4*math.sin(a+.28),zz-2.785],[ex+.13*math.cos(a+.14),yy+.13*math.sin(a+.14),zz-2.785])
                tor('inlet',(ex,yy+.04,zz+2.58),.34,.025);beam('dark',(ex,yy+.04,zz+2.60),(ex,yy+.04,zz+2.62),.31,32)
                # Circumferential service seams.
                for z in [zz-1.8,zz+.8]:tor('panel',(ex,yy,z),.552,.012)
        lathe('black',[[7.55,.015,.015,0],[7.8,.34,.32,0],[8.5,.60,.57,0],[10.2,.63,.60,0],[13.3,.52,.51,0],[15.1,.2,.20,0],[15.55,.01,.01,0]],40,sgn*26.2,.35)
        op('airfoil','air',[[sgn*.75,13.5,7.6,1.17,.09],[sgn*4.3,15.9,5.1,1.31,.075],[sgn*8.66,19.2,1.58,1.52,.06]],28)
    # Tall D fin and tail-gunner fairing. No H-model low tail or modern antennas.
    poly('black',[[-.23,1.05,11.5],[.23,1.05,11.5],[-.12,11.55,17.4],[.12,11.55,17.4],[-.095,11.55,20.35],[.095,11.55,20.35],[-.22,1.05,23.0],[.22,1.05,23.0]],[[0,2,4,6],[1,7,5,3],[0,1,3,2],[2,3,5,4],[4,5,7,6],[6,7,1,0]])
    for sgn in [-1,1]:
        beam('panel',(sgn*.237,1.6,21.4),(sgn*.103,11.3,19.85),.019,6)
        # Cockpit window band on the upper shoulder; narrow metal mullions.
        panes=[[(.07,1.38,-22.16),(.69,1.29,-22.04),(.87,2.005,-20.67),(.08,2.12,-20.75)],[(.80,1.27,-22.02),(1.25,1.05,-21.65),(1.55,1.75,-20.10),(.99,1.98,-20.64)],[(1.30,1.02,-21.58),(1.59,.86,-20.55),(1.72,1.41,-18.86),(1.60,1.74,-20.00)]]
        for pane in panes:
            pp=[[sgn*x,y,z] for x,y,z in pane];quad('glass',*pp)
            for i in range(4):beam('airframe',pp[i],pp[(i+1)%4],.035,6)
        beam('inlet',(sgn*1.48,.28,-21.7),(sgn*1.80,.22,-22.65),.02,6)
        # Skin access seams and sealed undercarriage doors.
        for z in [-11,-7,5.2]:box('panel',(sgn*.62,-1.784,z),(1.05,.025,3.3))
    for x in [-.16,.16]:
        for y in [.30,.53]:beam('black',(x,y,22.85),(x,y,23.8506),.055,12)
    for z in [-12,-5,8]:poly('black',[[-.03,1.88,z],[.03,1.88,z],[.03,2.25,z+.45],[-.03,2.25,z+.45]],[[0,1,2,3]])
    audit['aircraft']={'span_m':56.388,'length_m':47.7012,'engine_count':8,'wing_area_including_center_m2':wing_area*factor,'nose':'rounded radome and raised glazed cockpit','paint':'SEA top camouflage; black fuselage sides/belly and tall D tail','source_limit':'Reference interpretation, not factory loft or serial-specific repaint'}
    # LONG BIEN: two original-type anchor spans and a suspended span; unified node graph.
    # 75 m anchors, 27.5 m cantilever arms, 51.2 m suspended span follow the drawing.
    asset('bridge');deck=7.40;sidez=2.375
    tops=[]
    for p0 in [-128.1,53.1]:
        tops.extend([(p0-27.5,deck+4),(p0-13.75,deck+8.6)])
        tops.extend([(p0+j*15,deck+h) for j,h in enumerate([17.2,13.55,11.8,11.8,13.55,17.2])])
        tops.extend([(p0+88.75,deck+8.6),(p0+102.5,deck+4)])
    tops.extend([(-25.6+j*5.12,deck+4) for j in range(1,10)])
    tops=sorted(set((round(x,6),round(y,6)) for x,y in tops))
    # Low end approaches continue all the way to the banks, not terminating in mid-air.
    tops=[(-185,deck+3),(-170.3,deck+3.5)]+tops+[(170.3,deck+3.5),(185,deck+3)]
    plate_nodes=[]
    for sg in [-1,1]:
        z=sg*sidez
        for i,(x,y) in enumerate(tops):
            ibeam((x,deck,z),(x,y,z),.26,.23,.032)
            plate_nodes.extend([(x,y,z),(x,deck,z)])
            if i==len(tops)-1:continue
            bx,by=tops[i+1];mx=(x+bx)*.5
            ibeam((x,y,z),(bx,by,z),.40,.35,.055)
            ibeam((x,deck,z),(mx,deck,z),.40,.32,.052);ibeam((mx,deck,z),(bx,deck,z),.40,.32,.052)
            ibeam((x,y,z),(mx,deck,z),.28,.245,.034);ibeam((mx,deck,z),(bx,by,z),.28,.245,.034)
            plate_nodes.append((mx,deck,z))
            # Main compression diagonals have lacing: small zigzag strips between plates.
            if by>deck+8 or y>deck+8:
                aa=(x,y,z);bb=(mx,deck,z);d=sub(bb,aa);perp=unit(cross(d,[0,0,1]));length=math.sqrt(sum(c*c for c in d));count=max(3,int(length/.9))
                for j in range(count):
                    p=mix(aa,bb,j/count);q=mix(aa,bb,(j+1)/count);sign=1 if j%2 else -1
                    p=[p[k]+perp[k]*.11*sign for k in range(3)];q=[q[k]-perp[k]*.11*sign for k in range(3)];p[2]+=sg*.14;q[2]+=sg*.14;prism('bridgerivet',p,q,.048,.018)
        # Cross portals at exactly the same nodes. No x+6/y-1 unconnected endpoints.
    for i,(x,y) in enumerate(tops):
        ibeam((x,deck,-sidez),(x,deck,sidez),.42,.28,.045)
        if y>deck+5.0:
            ibeam((x,y,-sidez),(x,y,sidez),.28,.25,.035)
            # Tall portals contain a second transverse member and X above train clearance.
            yy=max(deck+5.4,y-3.0)
            if yy<y-.5:
                ibeam((x,yy,-sidez),(x,yy,sidez),.18,.18,.025,record=False)
                ibeam((x,yy,-sidez),(x,y,sidez),.12,.13,.025,record=False)
                ibeam((x,y,-sidez),(x,yy,sidez),.12,.13,.025,record=False)
        if i<len(tops)-1:
            bx,by=tops[i+1]
            # Roof ties only over through-truss sections; low pony trusses remain open.
            if min(y,by)>deck+5:
                ibeam((x,y,-sidez),(bx,by,sidez),.12,.14,.024)
                ibeam((x,y,sidez),(bx,by,-sidez),.12,.14,.024)
            ibeam((x,deck,-sidez),(bx,deck,sidez),.18,.17,.026)
            ibeam((x,deck,sidez),(bx,deck,-sidez),.18,.17,.026)
    # Riveted gusset plates wrap every load-bearing side node.
    for x,y,z in plate_nodes:
        sg=1 if z>0 else -1;zz=z+sg*.23
        vv=[[x-.39,y-.23,zz],[x-.27,y+.35,zz],[x+.25,y+.39,zz],[x+.43,y-.15,zz],[x+.12,y-.35,zz]]
        back=[[v[0],v[1],z+sg*.16] for v in vv];face=list(range(5));outer=face[::-1] if sg>0 else face;inner=[v+5 for v in (face if sg>0 else face[::-1])];poly('bridgepaint',vv+back,[outer,inner]+[[i,(i+1)%5,(i+1)%5+5,i+5] for i in range(5)])
        for dx,dy in [(-.22,-.11),(-.17,.15),(.10,.22),(.23,-.07),(.04,-.19)]:
            beam('bridgerivet',(x+dx,y+dy,z+sg*.14),(x+dx,y+dy,zz+sg*.01),.016,8);beam('bridgerivet',(x+dx,y+dy,zz),(x+dx,y+dy,zz+sg*.032),.028,10)
    # Deck, exterior carriageways, rails and railings are continuous across all panels.
    for z in [-3.43,3.43]:box('chipped',(0,deck+.04,z),(370,.16,2.0))
    for z in [-.7175,.7175]:
        box('rail',(0,deck+.19,z),(370,.13,.068));box('bridgepaint',(0,deck+.105,z),(370,.035,.16))
    for z in [-4.46,4.46,-2.375,2.375]:ibeam((-185,deck-.23,z),(185,deck-.23,z),.29,.22,.035,record=False)
    for j in range(462):box('timber',(-184.7+j*.80,deck-.01,0),(.20,.18,2.30))
    for x in [i*5-185 for i in range(75)]:
        ibeam((x,deck-.32,-4.5),(x,deck-.32,4.5),.33,.22,.04,record=False)
        for sg in [-1,1]:prism('bridgepaint',(x,deck-.9,sg*sidez),(x,deck-.32,sg*4.42),.13,.15)
    for sg in [-1,1]:
        z=sg*4.46
        for y in [deck+.35,deck+.82,deck+1.23]:box('bridgepaint',(0,y,z),(370,.065,.065))
        for j in range(308):box('bridgepaint',(-184.2+j*1.2,deck+.69,z),(.055,1.16,.055))
    # Tapered masonry piers with broad caps and separate bearing seats.
    for x in [-128.1,-53.1,53.1,128.1]:
        vs=[[x+sx*w,y,sz*d] for y,w,d in [(-3.0,3.0,4.4),(5.98,1.75,3.3)] for sx,sz in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        poly('masonry',vs,[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])
        box('stone',(x,6.17,0),(4.4,.40,7.2))
        for z in [-sidez,sidez]:
            box('bridgepaint',(x,6.52,z),(1.35,.30,1.0));box('bridgepaint',(x,7.01,z),(1.5,.22,1.12))
            for dx in [-.43,0,.43]:beam('rail',(x+dx,6.78,z-.43),(x+dx,6.78,z+.43),.14,12)
    for sg in [-1,1]:box('masonry',(sg*183,3.1,0),(5,7.8,10))
    degrees={}
    for m in audit['bridge_members']:
        for k in ['a','b']:
            p=tuple(m[k]);degrees[p]=degrees.get(p,0)+1
    audit['bridge']={'representation':'Two 75 m anchor spans, 27.5 m arms, one 51.2 m suspended section, connected end approaches; not the entire bridge in December 1972','length_m':370,'shared_nodes':len(degrees),'main_members':len(audit['bridge_members']),'dangling_main_endpoints':[list(p) for p,c in degrees.items() if c<2],'span_join_gap_m':0.0,'deck_elevation_m':deck,'truss_spacing_m':sidez*2}
    # Modelled fragments will be used by the time-reversible rigid-body effect.
    for k in range(4):
        asset('fragment'+str(k));rr=random.Random(430+k)
        if k==2:box('timber',(0,0,0),(.16,.10,1.2),(.04,.03,.01))
        elif k==1:
            vs=[[x,.07*math.cos(x*4),z] for z in [-.22,.22] for x in [-.27,0,.27]]
            poly('tilefragment',vs,[[0,1,4,3],[1,2,5,4]]);prism('tilefragment',vs[0],vs[3],.045,.075)
        else:
            vs=[[x+rr.uniform(-.07,.07),y+rr.uniform(-.04,.04),z+rr.uniform(-.06,.06)] for x,y,z in [(-.27,-.12,-.18),(.27,-.12,-.18),(.27,.12,-.18),(-.27,.12,-.18),(-.27,-.12,.18),(.27,-.12,.18),(.27,.12,.18),(-.27,.12,.18)]]
            poly('brickred' if k==0 else 'mortar',vs,[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])
    asset('slabroof');box('roofold',(0,0,0),(2.6,.10,3.2));box('timber',(0,-.085,0),(.1,.08,3.2))
    asset('slabwall');box('brickred',(0,0,0),(2,1.4,.16));box('oldplaster',(0,0,.092),(1.94,1.34,.025))
    asset('slabbeam');box('timber',(0,0,0),(.12,.18,2.8))
    # Eight narrow-frontage vernacular buildings. Dimensions drive contiguous layout.
    sizes=[(4.25,12.0,3.35),(4.7,13.4,6.35),(5.45,15.0,6.7),(3.95,11.3,3.7),(5.1,14.0,6.1),(4.35,12.8,6.5),(5.7,15.7,6.6),(4.85,13.0,3.8)]
    def roof(w,d,h,typ):
        rise=1.5 if h>5 else 1.2;edge=.22
        if typ in [1,4]:
            box('roofdark',(0,h+.06,0),(w,.15,d));box('lime',(0,h+.43,d/2),(w,.80,.18))
            box('lime',(0,h+.88,d/2),(w+.12,.14,.32))
            for sg in [-1,1]:box('lime',(sg*(w/2-.08),h+.34,0),(.17,.65,d))
        else:
            # Ridge crosses the narrow frontage, avoiding ubiquitous triangular facades.
            for sg in [-1,1]:
                quad('roofold',[-w/2-edge,h+rise,0],[w/2+edge,h+rise,0],[w/2+edge,h,sg*(d/2+.3)],[-w/2-edge,h,sg*(d/2+.3)])
                # The modest curved cap profile catches light; repeated tile detail is textured.
                beam('roofdark',(-w/2-edge,h+.02,sg*(d/2+.29)),(w/2+edge,h+.02,sg*(d/2+.29)),.065,8)
            for x in [-w/2,w/2]:poly('oldplaster',[[x,h,-d/2],[x,h,d/2],[x,h+rise,0]],[[0,1,2]])
            for j in range(int(w/.28)+2):
                x=-w/2+j*.28;beam('roofold',(x,h+rise+.075,0),(x+.275,h+rise+.075,0),.115,10)
        return rise
    def opening(x,y,z,w,h,door=False,open_angle=0):
        box('dark',(x,y,z-.135),(w,h,.08))
        for sg in [-1,1]:box('lime',(x+sg*(w/2+.04),y,z+.015),(.105,h+.20,.22))
        for sg in [-1,1]:box('lime',(x,y+sg*(h/2+.055),z+.03),(w+.19,.12,.24))
        if door:
            for j in range(8):box('timber',(x-w/2+(j+.5)*w/8,y,z-.032),(w/8-.015,h-.05,.07))
            box('panel',(x+.15,y-.05,z+.035),(.08,.05,.04))
        else:
            for sg in [-1,1]:
                lx=x+sg*w*.25;box('shutter',(lx,y,z-.01),(w*.47,h-.04,.072),(0,sg*open_angle,0))
                for j in range(11):box('shutter',(lx,y-h*.44+j*h*.087,z+.055),(w*.43,.068,.105),(.25,0,0))
                for yy in [-h*.40,h*.40]:box('panel',(lx,y+yy,z+.12),(w*.44,.027,.018))
    for vi,(w,d,h) in enumerate(sizes):
        material=['oldplaster','plasterochre','plastergrey','oldplaster','plastergrey','oldplaster','plasterochre','oldplaster'][vi];zf=d/2;rr=random.Random(231+vi)
        audit['house_dimensions']['house'+str(vi)]={'frontage':w,'depth':d,'height':h,'partywall_gap_target':.07}
        asset('house'+str(vi));box('stone',(0,.12,0),(w,.24,d));box(material,(0,h/2,0),(w,h,d));box('brickred',(0,.28,zf+.025),(w,.4,.065))
        box('lime',(0,2.88,zf+.07),(w,.12,.20))
        if h>5:box('lime',(0,3.28,zf+.09),(w,.15,.24))
        for sg in [-1,1]:box('lime',(sg*(w/2-.10),h/2,zf+.025),(.15,h,.12))
        # Deep openings, wooden shutters, iron hinges, threshold and rain protection.
        if vi in [0,3,7]:
            opening(0,1.37,zf+.06,w-.52,2.48,True);box('stone',(0,.14,zf+.26),(w-.2,.27,.55))
            quad('timber',[-w/2,2.74,zf],[w/2,2.74,zf],[w/2,2.45,zf+1.05],[-w/2,2.45,zf+1.05])
            for sg in [-1,1]:beam('timber',(sg*(w/2-.1),.12,zf+.95),(sg*(w/2-.1),2.47,zf+.95),.052,8)
        else:
            opening(-w*.20,1.37,zf+.06,1.35,2.42,True);opening(w*.26,1.60,zf+.06,1.10,1.54)
            for xx in [-.32,0,.32]:beam('panel',(w*.26+xx,.94,zf+.21),(w*.26+xx,2.28,zf+.21),.014,6)
        if h>5:
            for x in [-w*.245,w*.245]:opening(x,4.84,zf+.08,1.22,1.65,open_angle=.10 if vi%3==0 else 0)
            if vi in [1,5,6]:
                bw=w-.45;box('stone',(0,3.58,zf+.48),(bw,.16,1.05))
                for yy in [3.80,4.56]:beam('panel',(-bw/2,yy,zf+.99),(bw/2,yy,zf+.99),.032,8)
                for j in range(int(bw/.23)+1):beam('panel',(-bw/2+j*.23,3.80,zf+.99),(-bw/2+j*.23,4.56,zf+.99),.017,6)
                for sg in [-1,1]:beam('panel',(sg*bw/2,4.56,zf),(sg*bw/2,4.56,zf+.99),.032,8)
        roof(w,d,h,vi)
        # Drainpipes and weathered base reveal scale without modern equipment.
        beam('steel',(w/2-.15,.25,zf+.18),(w/2-.15,h-.08,zf+.18),.045,10)
        for yy in [1.25,2.6,4.0,5.6]:
            if yy<h:tor('steel',(w/2-.15,yy,zf+.18),.05,.014,(math.pi/2,0,0))
        for j in range(8):
            x=rr.uniform(-w*.43,w*.43);y=rr.uniform(.25,.8);ww=rr.uniform(.14,.55);hh=rr.uniform(.13,.40)
            vs=[[x+math.cos(k*TAU/7)*ww*(.7+rr.random()*.3),y+math.sin(k*TAU/7)*hh,zf+.061] for k in range(7)]
            poly('brickred' if j%3==0 else 'chipped',vs,[list(range(7))])
        # Rear openings and eaves visible in high-angle shots.
        for x in [-w*.23,w*.23]:opening(x,1.7,-d/2-.03,1.0,1.25)
        asset('townlod'+str(vi));box(material,(0,h/2,0),(w,h,d))
        # Distant roofs retain silhouette and shared tile maps without hundreds of caps.
        if vi in [1,4]:
            box('roofdark',(0,h+.06,0),(w,.15,d));box('lime',(0,h+.46,d/2),(w,.9,.16))
            for sg in [-1,1]:box('lime',(sg*(w/2-.08),h+.34,0),(.16,.65,d))
        else:
            rise=1.5 if h>5 else 1.2
            for sg in [-1,1]:quad('roofold',[-w/2-.2,h+rise,0],[w/2+.2,h+rise,0],[w/2+.2,h,sg*(d/2+.3)],[-w/2-.2,h,sg*(d/2+.3)])
            for x in [-w/2,w/2]:poly(material,[[x,h,-d/2],[x,h,d/2],[x,h+rise,0]],[[0,1,2]])
            beam('roofold',(-w/2-.2,h+rise+.06,0),(w/2+.2,h+rise+.06,0),.10,5)
        for x in [-w*.24,w*.24]:
            for y in ([1.5,4.8] if h>5 else [1.5]):box('shutter',(x,y,zf+.04),(1.15,1.55,.025))
        # Corresponding irregular remnants retain the original lot footprint.
        asset('ruin'+str(vi));box('chipped',(0,.13,0),(w,.26,d));rr=random.Random(980+vi)
        for sg in [-1,1]:
            heights=[rr.uniform(.5,1.8) for _ in range(7)];heights[1 if vi%2 else 5]=h*.64
            for j in range(6):
                z0=-d/2+j*d/6;z1=z0+d/6
                wall=[[sg*w/2,.1,z0],[sg*w/2,.1,z1],[sg*w/2,heights[j+1],z1],[sg*w/2,heights[j],z0]]
                poly(material,wall,[[0,1,2,3]]);prism('brickred',wall[2],wall[3],.18,.28)
        # Low connected rubble volume, not a regular sawtooth row.
        vs=[[0,1.0,0]]+[[math.cos(j*TAU/12)*w*.51,.22+rr.random()*.20,math.sin(j*TAU/12)*d*.48] for j in range(12)]
        poly('chipped',vs,[[0,j+1,(j+1)%12+1] for j in range(12)])
        for j in range(62):
            x=rr.uniform(-w*.54,w*.54);z=rr.uniform(-d*.5,d*.5);y=max(.14,.95*(1-(x/(w*.55))**2-(z/(d*.5))**2))+rr.random()*.24
            box(['brickred','mortar','roofold'][j%3],(x,y,z),(rr.uniform(.18,.5),rr.uniform(.1,.26),rr.uniform(.16,.5)),(rr.random()*2,rr.random()*5,rr.random()*2))
        for j in range(8):
            aa=[rr.uniform(-w*.5,w*.5),.25,rr.uniform(-d*.48,d*.48)];bb=[rr.uniform(-w*.5,w*.5),rr.uniform(.3,1.6),rr.uniform(-d*.48,d*.48)];prism('timber',aa,bb,.10,.17)
        quad('roofold',[-w*.45,.2,-d*.22],[w*.1,1.4,-d*.10],[w*.32,1.1,d*.25],[-w*.4,.3,d*.20])
    (ROOT/'assets/v2_design_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    return audit
