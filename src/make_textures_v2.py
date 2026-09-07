"""Create original, deterministic texture maps. No third-party texture downloads."""
import pathlib,numpy as np,math,json
from PIL import Image,ImageDraw,ImageFilter,ImageFont
P=pathlib.Path(__file__).resolve().parents[1];out=P/'assets/textures';out.mkdir(exist_ok=True);rng=np.random.default_rng(19721218)

def noise(n,grid,seed):
 r=np.random.default_rng(seed);im=Image.fromarray((r.random((grid,grid))*255).astype('uint8'),'L').resize((n,n),Image.Resampling.BICUBIC)
 return np.asarray(im).astype(float)/255

def save(name,ar):Image.fromarray(np.uint8(np.clip(ar,0,255))).save(out/(name+'.jpg'),quality=92,subsampling=0)
# A broad, irregular three-color SEA pattern. Coordinates are aircraft x/z, not per-part UVs.
n=2048;xx,zz=np.meshgrid(np.linspace(-30,30,n),np.linspace(-25,25,n));a=noise(n,9,21);b=noise(n,17,41);field=a*.78+b*.22
colors=np.array([[58,72,51],[91,109,73],[146,137,97]])
mask=np.where(field<.42,0,np.where(field<.58,1,2));base=colors[mask].astype(float)
fine=noise(n,512,24)-.5;base+=fine[:,:,None]*6
img=Image.fromarray(np.uint8(np.clip(base,0,255)));d=ImageDraw.Draw(img)
def uv(x,z):return((x+30)/60*n,(z+25)/50*n)
# Subtle panel access seams and rivet lines follow the swept wing instead of a square grid.
for s in [-1,1]:
 for f in [.25,.56,.80]:
  points=[uv(s*x,z+ch*f) for x,z,ch in [(1.8,-7.1,10.2),(7,-3.85,8.4),(12,-.47,6.77),(18,3.73,4.96),(24,7.86,3.08),(28.1,10.79,1.75)]];d.line(points,fill=(55,64,49),width=1)
 for x,z,c in [(7,-3.85,8.4),(12,-.47,6.77),(18,3.73,4.96),(24,7.86,3.08)]:
  d.line([uv(s*x,z+.15),uv(s*x,z+c*.84)],fill=(71,78,56),width=1)
  for j in range(int(c*9)):
   px,py=uv(s*(x+.055),z+j*.10);d.ellipse((px-1,py-1,px+1,py+1),fill=(64,71,53))
try:font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',58)
except OSError:font=ImageFont.load_default()
x,y=uv(16.7,5.7);d.text((x,y),'USAF',font=font,fill=(38,48,43),anchor='mm')
# Historically generic national marking; deliberately no serial or unit identity.
x,y=uv(-18.3,5.6);rad=45;d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=(42,61,66));d.rectangle((x-78,y-18,x+78,y+18),fill=(42,61,66));d.rectangle((x-73,y-11,x+73,y+11),fill=(206,207,181));d.rectangle((x-73,y-3,x+73,y+3),fill=(130,69,58));star=[]
for i in range(10):a=-math.pi/2+i*math.pi/5;rr=40 if i%2==0 else 17;star.append((x+math.cos(a)*rr,y+math.sin(a)*rr))
d.polygon(star,fill=(211,215,193));img.save(out/'camo.jpg',quality=96,subsampling=0)
n=1024;yy,xx=np.mgrid[:n,:n]
# Weathered lime plaster: broad discolouration, granular aggregate and chipped patches.
coarse=noise(n,9,75);medium=noise(n,35,81);fine=noise(n,390,92);v=164+coarse*66+(medium-.5)*18+(fine-.5)*20
ar=np.stack([v,v-3,v-10],axis=2);stain=coarse<.31;ar[stain]*=.65
save('weathered',ar)
# Painted iron with rust islands and streaks; neutral so material tint remains meaningful.
a=noise(n,24,123);b=noise(n,150,122);m=a*.9+b*.1;base=np.empty((n,n,3));base[:]=[169,168,151];rust=m<.39;base[rust]=[125,97,66];base+=(b-.5)[:,:,None]*29
save('rust',base)
# Five by four overlapping clay tiles per metre, with a soft barrel-shaped highlight.
for name,countx,county in [('tilesv2',5,4),('brickv2',4,8),('masonry',3,5)]:
 im=Image.new('RGB',(n,n),(77,76,66));draw=ImageDraw.Draw(im);r=np.random.default_rng(401+countx);cw=n/countx;ch=n/county
 for row in range(county):
  for col in range(-1,countx+1):
   x=col*cw+(row%2)*(cw/2 if name!='tilesv2' else 0);y=row*ch;val=int(r.uniform(145,200))
   draw.rectangle((x+4,y+4,x+cw-3,y+ch-4),fill=(val,val-8,val-18))
   if name=='tilesv2':
    for j in range(int(cw)-7):
     u=j/cw;v=int(val*(.63+.38*math.sin(math.pi*u)));draw.line((x+4+j,y+5,x+4+j,y+ch-9),fill=(v,v-6,v-14),width=1)
    draw.line((x+4,y+ch-8,x+cw-4,y+ch-8),fill=(83,77,63),width=5)
 arr=np.asarray(im).astype(float)+(noise(n,280,413)-.5)[:,:,None]*23
 save(name,arr)
# Road surface avoids repeated diagonal wave moire; fine gravel and muted wet patches.
f=noise(n,420,544);a=noise(n,14,542);v=122+f*32+a*24;ar=np.stack([v,v-1,v-7],axis=2);save('road',ar)
print('TEXTURES',[(x.name,x.stat().st_size) for x in out.glob('*.jpg')])
