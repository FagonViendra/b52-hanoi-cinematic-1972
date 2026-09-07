import pathlib,numpy as np,math
from PIL import Image,ImageDraw,ImageFilter
P=pathlib.Path.cwd();T=P/'assets/textures'
r=np.random.default_rng(792)
def noise(n,g,seed):return np.asarray(Image.fromarray((np.random.default_rng(seed).random((g,g))*255).astype('uint8')).resize((n,n),Image.Resampling.BICUBIC)).astype(float)/255
n=1024;v=220+(noise(n,9,75)-.5)*15+(noise(n,40,81)-.5)*8+(noise(n,420,92)-.5)*12
ar=np.stack([v,v-2,v-6],axis=2);im=Image.fromarray(np.uint8(np.clip(ar,0,255)));d=ImageDraw.Draw(im)
for i in range(40):
 x=int(r.uniform(0,n));y=int(r.uniform(0,n));l=int(r.uniform(15,180));points=[(x,y)]
 for j in range(4):x+=int(r.uniform(-9,9));y+=l//4;points.append((x,y))
 d.line(points,fill=(165,162,152),width=1)
im.save(T/'weathered.jpg',quality=93,subsampling=0)
# Brick pier texture with fine courses instead of implausibly giant stone blocks.
im=Image.new('RGB',(1024,1024),(152,145,126));d=ImageDraw.Draw(im)
for row in range(16):
 for col in range(-1,9):
  x=col*128+(row%2)*64;y=row*64;v=int(r.uniform(169,199));d.rectangle((x+3,y+3,x+124,y+60),fill=(v,v-11,v-20))
ar=np.asarray(im).astype(float)+(noise(1024,350,93)-.5)[:,:,None]*10;Image.fromarray(np.uint8(np.clip(ar,0,255))).save(T/'masonry.jpg',quality=93)
# Ray-integrated original volumetric dust sprite, evaluated offline, not a Gaussian glow.
n=320;yy,xx=np.mgrid[-1:1:complex(n),-1:1:complex(n)];rr=np.random.default_rng(643)
lobes=[(rr.uniform(-.55,.55),rr.uniform(-.55,.55),rr.uniform(-.45,.45),rr.uniform(.22,.38)) for _ in range(20)]
trans=np.ones((n,n));rgb=np.zeros((n,n,3));alpha=np.zeros((n,n));grain=noise(n,75,61)
for z in np.linspace(-1,1,56):
 dens=np.zeros((n,n));gx=np.zeros((n,n));gy=np.zeros((n,n));gz=np.zeros((n,n))
 for a,b,c,sz in lobes:
  dd=np.exp(-((xx-a)**2+(yy-b)**2+(z-c)**2)/(sz*sz)*2.0)
  dens+=dd;gx+=(xx-a)*dd/(sz*sz);gy+=(yy-b)*dd/(sz*sz);gz+=(z-c)*dd/(sz*sz)
 dens=np.maximum(0,dens-.10)*(0.68+grain*.62);norm=np.sqrt(gx*gx+gy*gy+gz*gz)+1e-5
 lit=np.clip((-.5*gx-.75*gy-.7*gz)/norm,0,1);shade=.32+.53*lit;op=1-np.exp(-dens*.11);contrib=trans*op
 rgb+=contrib[:,:,None]*shade[:,:,None];alpha+=contrib;trans*=1-op
rgb=np.divide(rgb,alpha[:,:,None]+1e-6);rgba=np.dstack([np.clip(rgb,0,1),np.clip(alpha,0,1)])
Image.fromarray(np.uint8(rgba*255),'RGBA').save(T/'dust.png')
print('SOFT_PLASTER_AND_VOLUME_SPRITE_READY')
