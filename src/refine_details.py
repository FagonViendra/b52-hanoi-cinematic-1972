import pathlib
P=pathlib.Path.cwd();p=P/'src/build_assets.py';s=p.read_text(encoding='utf-8-sig')
s=s.replace(" 'silver':{'color':'#a6b0ac'", " 'wreckskin':{'color':'#74796c','rough':0.91,'metal':0.18,'tex':'metal'},\n 'silver':{'color':'#a6b0ac'")
s=s.replace("elif k=='poly': vs,fs=d", "elif k=='poly': vs,fs=d[:2]; smooth=bool(d[2]) if len(d)>2 else False")
a=s.index("asset('wreck')");b=s.index("asset('pole')",a)
s=s[:a]+r'''asset('wreck')
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
''' + s[b:]
# Cargo boat details: raised bulwarks, deck planking, fenders, mast rigging and hatches.
needle="asset('chimney');"
insert=r'''
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
asset('chimney');'''
s=s.replace(needle,insert)
p.write_text(s,encoding='utf-8')
p=P/'src/geometry.js';s=p.read_text(encoding='utf-8-sig').replace("else if(kind==='poly')g=meshFrom(d[0],d[1],false)","else if(kind==='poly')g=meshFrom(d[0],d[1],!!d[2])");p.write_text(s,encoding='utf-8')
p=P/'src/render_assets.py';s=p.read_text(encoding='utf-8-sig');s=s.replace("P=pathlib.Path(r'C:\\Users\\fagon\\OneDrive\\Documents\\B52_Hanoi_Cinematic_1972')", "P=pathlib.Path(__file__).resolve().parents[1]");p.write_text(s,encoding='utf-8')
print('Connected dented wreck skin, cargo boat fittings and portable render script saved.')
