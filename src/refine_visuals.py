import pathlib,re,shutil
P=pathlib.Path.cwd(); (P/'qa/iteration1').mkdir(exist_ok=True)
for f in (P/'qa').glob('[0-9][0-9]_*.png'):shutil.copy2(f,P/'qa/iteration1'/f.name)
shutil.copy2(P/'qa/pass1_smoke.json',P/'qa/iteration1/pass1_smoke.json')
p=P/'src/world.js';s=p.read_text(encoding='utf-8-sig')
s=s.replace("air:{fog:'#657b8a',zenith:'#1b3247',horizon:'#b2af9c',density:.00065,key:'#ffe6bd',power:4,ambient:1.5", "air:{fog:'#657d95',zenith:'#172c43',horizon:'#657d95',density:.00065,key:'#bed5f0',power:2.7,ambient:1.25")
s=s.replace(" const sky=new THREE.Mesh",r'''
 skyMat.uniforms.sunPower={value:.10};
 skyMat.fragmentShader=`varying vec3 vDir;
 uniform vec3 top;uniform vec3 bottom;uniform vec3 sun;uniform float sunPower;
 void main(){vec3 d=normalize(vDir);float h=pow(max(0.,d.y),.6);vec3 c=mix(bottom,top,h);
 float glow=pow(max(0.,dot(d,sun)),110.);c+=vec3(.36,.28,.19)*glow*sunPower;
 gl_FragColor=vec4(c,1.);
 #include <colorspace_fragment>
 }`;
 const sky=new THREE.Mesh''')
s=s.replace("let ps=list.filter((p,i)=>i%4===v)","let ps=list.filter((p,i)=>i%8===v)")
s=s.replace("for(let v=0;v<4;v++)", "for(let v=0;v<8;v++)")
s=s.replace("let v=(j+(side===1?1:0))%4,z=(j-8)*8.5,ry=side<0?Math.PI/2:-Math.PI/2", "let v=(j+(side===1?3:0))%8,z=(j-8)*8.5,ry=(side<0?Math.PI/2:-Math.PI/2)+(r()-.5)*.025")
s=s.replace("side*(11.7+v*.2)", "side*(11.7+(v%4)*.19+(r()-.5)*.6)")
s=s.replace("list.length*27", "list.length*48").replace("j<27;j++", "j<48;j++").replace("o.scale.set(3.7*sc,3.7*sc,1)", "o.scale.set(2.45*sc,2.45*sc,1)")
s=s.replace("roughness:1,color:'#a8b096'", "roughness:1,color:'#a8b096',alphaToCoverage:true")
s=s.replace("[side*390,1.3,0],[460,5,1000]", "[side*390,2.4,0],[460,10,1000]").replace("20),3.8,", "20),7.4,").replace("r()*45),3.8,", "r()*45),7.4,")
s=s.replace("15+r()*35", "4+r()*23").replace("a:r()*6.28", "a:(r()-.5)*.2")
s=s.replace("d.sz,.68,camera,d.a,.48", "d.sz,.58,camera,d.a,.30")
s=s.replace("const mirror=new Reflector",r'''
 const mirror=new Reflector''').replace("color:0x50634b", "color:0x7d8674")
s=s.replace("mirror.rotation.x=-Math.PI/2",r'''
 mirror.material.uniforms.uTime={value:0};
 mirror.material.fragmentShader=mirror.material.fragmentShader.replace('uniform vec3 color;','uniform vec3 color;uniform float uTime;')
 .replace('vec4 base = texture2DProj( tDiffuse, vUv );',`vec4 uv=vUv;uv.x+=sin(vUv.y*49.+uTime*.55)*.0008*uv.w;uv.y+=sin(vUv.x*57.-uTime*.40)*.0006*uv.w;
 vec4 base=texture2DProj(tDiffuse,uv)*.4;
 base+=texture2DProj(tDiffuse,uv+vec4(.0006*uv.w,.0004*uv.w,0.,0.))*.3;
 base+=texture2DProj(tDiffuse,uv-vec4(.0006*uv.w,.0004*uv.w,0.,0.))*.3;`)
 .replace('blendOverlay( base.rgb, color )','mix(blendOverlay(base.rgb,color),vec3(.12,.16,.12),.26)');
 mirror.rotation.x=-Math.PI/2''')
s=s.replace("scene.fog=new THREE.FogExp2(a.fog,a.density)", "scene.fog=new THREE.FogExp2(a.horizon,a.density)")
s=s.replace("skyMat.uniforms.top.value.set(a.zenith);", "skyMat.uniforms.top.value.set(a.zenith);skyMat.uniforms.sunPower.value=['air','hospital','street'].includes(id)?0:.10;")
s=s.replace("  for(const m of waterMaterials)m.uniforms.uTime.value=t;", "  for(const m of waterMaterials){m.uniforms.uTime.value=t;m.uniforms.haze.value.set(locations[current].horizon);}mirror.material.uniforms.uTime.value=t;")
# Replace regular gridded water with multi-scale irregular wave shading and distance haze.
needle="  let m=new THREE.Mesh(new THREE.PlaneGeometry(w,d),mat);"
replace=r'''
  mat.fragmentShader=`uniform float uTime;uniform vec3 base;uniform vec3 haze;varying vec3 vPos;
 float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
 float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
 void main(){vec2 p=vPos.xz;float dist=length(cameraPosition-vPos);float n=noise(p*.13+vec2(uTime*.065,0.));
 float wave=sin(p.x*.7+p.y*1.4+n*6.+uTime*.5)*.55+sin(p.x*1.75-p.y*.44+n*9.-uTime*.8)*.25;
 float fade=1./(1.+dist*.025);vec3 eye=normalize(cameraPosition-vPos);float f=pow(1.-max(.0,eye.y),3.);
 vec3 c=mix(base,haze,f*.45);c+=vec3(wave*.020+n*.009)*fade;
 c=mix(c,haze,1.-exp(-dist*dist*.0000022));gl_FragColor=vec4(c,1.);
 #include <tonemapping_fragment>
 #include <colorspace_fragment>
 }`;
  let m=new THREE.Mesh(new THREE.PlaneGeometry(w,d),mat);'''
s=s.replace(needle,replace)
# Fill terminating streets and the horizon with a lower-density urban backdrop.
needle=" let poles=[];"
s=s.replace(needle,r'''
 houses(street,Array.from({length:22},(_,i)=>({p:[(i-11)*9,0,-100-(i%3)*13],ry:.03*(i%3),s:.8+(i%4)*.075})));
 houses(lake||street,[]);
 let poles=[];'''.replace(" houses(lake||street,[]);\n",''))
# Thin visual mass at the riverbank should not float at the old elevation.
s=s.replace("p:[side*(175+(j%5)*20),3.8", "p:[side*(175+(j%5)*20),7.4")
p.write_text(s,encoding='utf-8')
p=P/'src/geometry.js';s=p.read_text(encoding='utf-8-sig').replace("'#727454'","'#515b3b'").replace("['#35453a','#494b38','#8d815d']","['#28392d','#40472f','#6f6545']")
p.write_text(s,encoding='utf-8')
p=P/'src/effects.js';s=p.read_text(encoding='utf-8-sig')
s=s.replace("'#ec8d37'","'#e28334'").replace("Math.exp(-life*1.25)*(.6+s.up*.4)*(gentle?.22:1)","Math.exp(-life*1.45)*(.18+s.up*.13)*(gentle?.22:1)")
s=s.replace("(.20*(1-age/3))","(.025*(1-age/3))")
p.write_text(s,encoding='utf-8')
p=P/'src/timeline.js';s=p.read_text(encoding='utf-8-sig')
s=s.replace("[29,69,32],[25,67,23],[20,65,16],[0,89,1],[0,84,0],57", "[42,58,48],[37,55,39],[32,52,30],[0,85,1],[0,82,0],57")
p.write_text(s,encoding='utf-8')
print('Sky color space, night sky, water, camera, housing variety and particle refinements saved.')
