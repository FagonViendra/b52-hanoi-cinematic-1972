import * as THREE from 'three';
import {Reflector} from 'three/addons/objects/Reflector.js';
import {asset,batch,box,wire,textPlane,texture,palette,rng,V} from './geometry.js';
import {Blast,Billboards,leafTexture} from './effects.js';
export const locations={
 bridge:{fog:'#91a6a7',zenith:'#304957',horizon:'#b1b4a8',density:.0021,key:'#ffe2b3',power:3.6,ambient:1.65,center:[0,8,0]},
 air:{fog:'#657d95',zenith:'#172c43',horizon:'#657d95',density:.00065,key:'#bed5f0',power:2.7,ambient:1.25,center:[0,92,0]},
 port:{fog:'#7a9399',zenith:'#263d4d',horizon:'#9ca9a5',density:.0035,key:'#ded4b5',power:2.6,ambient:1.2,center:[-18,8,0]},
 hospital:{fog:'#283c49',zenith:'#111f30',horizon:'#485764',density:.008,key:'#9bb5d2',power:1.5,ambient:.86,center:[0,4,0]},
 street:{fog:'#253542',zenith:'#101e2c',horizon:'#394958',density:.009,key:'#a3bdd7',power:1.45,ambient:.88,center:[0,4,-5]},
 lake:{fog:'#94a4a3',zenith:'#516574',horizon:'#c4c2b1',density:.005,key:'#f6ddae',power:3,ambient:1.6,center:[0,2,0]},
 after:{fog:'#9b9d90',zenith:'#5d707c',horizon:'#d6c6a6',density:.007,key:'#ffe1ad',power:3.2,ambient:1.5,center:[0,3,-5]}
};
export function createWorld(){
 const scene=new THREE.Scene(),roots={},blasts=[],waterMaterials=[],damage=[],r=rng(19721218);
 const hemi=new THREE.HemisphereLight('#b0c8d7','#474232',1.5);scene.add(hemi);
 const key=new THREE.DirectionalLight('#ffe3b8',3.4);key.position.set(-65,95,40);key.castShadow=true;key.shadow.mapSize.set(1536,1536);key.shadow.bias=-.00012;key.shadow.normalBias=.12;key.shadow.camera.near=2;key.shadow.camera.far=400;key.shadow.camera.left=key.shadow.camera.bottom=-160;key.shadow.camera.right=key.shadow.camera.top=160;scene.add(key,key.target);
 const skyMat=new THREE.ShaderMaterial({side:THREE.BackSide,depthWrite:false,toneMapped:false,uniforms:{top:{value:new THREE.Color('#304957')},bottom:{value:new THREE.Color('#b1b4a8')},sun:{value:V([-.45,.22,-.75]).normalize()}},vertexShader:'varying vec3 vDir;void main(){vDir=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',fragmentShader:'varying vec3 vDir;uniform vec3 top;uniform vec3 bottom;uniform vec3 sun;void main(){vec3 d=normalize(vDir);float h=pow(max(0.,d.y),.55);vec3 c=mix(bottom,top,h);float s=pow(max(0.,dot(d,sun)),700.);c+=vec3(.65,.45,.22)*s;gl_FragColor=vec4(c,1.);}' });
 const flash=new THREE.PointLight('#ffb76d',0,140,1.5);scene.add(flash);

 skyMat.uniforms.sunPower={value:.10};
 skyMat.fragmentShader=`varying vec3 vDir;
 uniform vec3 top;uniform vec3 bottom;uniform vec3 sun;uniform float sunPower;
 void main(){vec3 d=normalize(vDir);float h=pow(max(0.,d.y),.6);vec3 c=mix(bottom,top,h);
 float glow=pow(max(0.,dot(d,sun)),110.);c+=vec3(.36,.28,.19)*glow*sunPower;
 gl_FragColor=vec4(c,1.);
 #include <colorspace_fragment>
 }`;
 const sky=new THREE.Mesh(new THREE.SphereGeometry(1700,32,16),skyMat);sky.renderOrder=-100;scene.add(sky);
 let groundTex=texture('road');groundTex.repeat.set(90,90);const groundMat=new THREE.MeshStandardMaterial({color:'#8a8470',map:groundTex,roughness:1,bumpMap:groundTex,bumpScale:.025});
 const roadTex=texture('road');roadTex.repeat.set(2,25);const roadMat=new THREE.MeshStandardMaterial({color:'#686d64',map:roadTex,roughness:.96,bumpMap:roadTex,bumpScale:.04});
 const leafMat=new THREE.MeshStandardMaterial({map:leafTexture(),alphaTest:.4,side:THREE.DoubleSide,roughness:1,color:'#a8b096',alphaToCoverage:true});
 function root(name){let g=new THREE.Group();g.name=name;scene.add(g);roots[name]=g;return g;}
 function ground(g,y=-.04,size=1000){let m=new THREE.Mesh(new THREE.PlaneGeometry(size,size),groundMat);m.rotation.x=-Math.PI/2;m.position.y=y;m.receiveShadow=true;g.add(m);return m;}
 function trees(g,list){batch('tree',list,g);let mesh=new THREE.InstancedMesh(new THREE.PlaneGeometry(1,1),leafMat,list.length*48),o=new THREE.Object3D();let i=0;for(const p of list)for(let j=0;j<48;j++){let a=r()*Math.PI*2,rad=r()*2.7,sc=p.s??1;o.position.set(p.p[0]+Math.cos(a)*rad*sc,p.p[1]+(4.8+r()*2.6)*sc,p.p[2]+Math.sin(a)*rad*sc);o.rotation.set((r()-.5)*2.3,r()*6.28,r()*2);o.scale.set(2.45*sc,2.45*sc,1);o.updateMatrix();mesh.setMatrixAt(i++,o.matrix);}mesh.castShadow=mesh.receiveShadow=true;g.add(mesh);}
 function water(g,w,d,pos,color='#556e70'){
  let mat=new THREE.ShaderMaterial({uniforms:{uTime:{value:0},base:{value:new THREE.Color(color)},haze:{value:new THREE.Color('#9caba9')}},vertexShader:'varying vec3 vPos;void main(){vPos=(modelMatrix*vec4(position,1.)).xyz;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:'uniform float uTime;uniform vec3 base;uniform vec3 haze;varying vec3 vPos;void main(){float w=sin(vPos.x*.75+uTime*.5+sin(vPos.z*.13))*sin(vPos.z*1.3-uTime*.7);float w2=sin(vPos.x*3.1+vPos.z*1.8+uTime);vec3 eye=normalize(cameraPosition-vPos);float f=pow(1.-max(.0,eye.y),3.);vec3 c=mix(base,haze,f*.62);c+=w*.026+w2*.007;gl_FragColor=vec4(c,1.);\n#include <tonemapping_fragment>\n#include <colorspace_fragment>\n}'});

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
  let m=new THREE.Mesh(new THREE.PlaneGeometry(w,d),mat);m.rotation.x=-Math.PI/2;m.position.set(...pos);g.add(m);waterMaterials.push(mat);return m;
 }
 function houses(g,list){for(let v=0;v<8;v++){let ps=list.filter((p,i)=>i%8===v);if(ps.length)batch('house'+v,ps,g);}}
 function cable(g,a,b){let mid=V(a).add(V(b)).multiplyScalar(.5);mid.y-=.7;let curve=new THREE.CatmullRomCurve3([V(a),mid,V(b)]),m=new THREE.Mesh(new THREE.TubeGeometry(curve,12,.023,4,false),palette.dark);g.add(m);}
 // RED RIVER: a deliberately shortened bridge segment, not a surveyed whole.
 let bridge=root('bridge');ground(bridge,-3);
 water(bridge,900,1000,[0,0,0],'#5b7778');batch('bridge',Array.from({length:7},(_,i)=>({p:[(i-3)*40,0,0]})),bridge);
 for(let side of[-1,1]){box(bridge,[side*390,2.4,0],[460,10,1000],groundMat);let ps=[];for(let j=0;j<45;j++)ps.push({p:[side*(175+(j%5)*20),7.4,(Math.floor(j/5)-4)*26],ry:side>0?-Math.PI/2:Math.PI/2,s:.9+r()*.25});houses(bridge,ps);trees(bridge,Array.from({length:22},(_,i)=>({p:[side*(162+r()*45),7.4,(i-11)*25],s:1.0+r()*.6})));}
 let barge=asset('boat');barge.position.set(18,.45,68);barge.rotation.y=.32;bridge.add(barge);batch('bicycle',[{p:[55,7.85,2.1],ry:Math.PI/2,s:.85}],bridge);
 // AIRCRAFT: a camera-relative exterior tableau above an illustrative cloud deck.
 let air=root('air'),plane=asset('b52');plane.position.y=92;air.add(plane);let wingmen=[];for(const p of[[96,99,145],[-128,103,245]]){let a=asset('b52');a.position.set(...p);air.add(a);wingmen.push(a);}
 const bay=new THREE.Group();plane.add(bay);box(bay,[0,-1.85,.2],[2.5,.035,8.6],'dark');let doors=[];for(let s of[-1,1]){let h=new THREE.Group();h.position.set(s*1.3,-1.82,.2);let d=asset('baydoor');d.position.x=-s*.69;h.add(d);plane.add(h);doors.push({h,s});}
 const bombs=[];for(let i=0;i<21;i++){let b=asset('bomb');b.rotation.x=-Math.PI/2;air.add(b);bombs.push(b);}
 const clouds=new Billboards(65,'#cad2cf');air.add(clouds.mesh);let cloudData=Array.from({length:65},()=>({p:[(r()-.5)*1500,4+r()*23,(r()-.5)*1400],sz:110+r()*160,a:(r()-.5)*.2}));
 // RIVER PORT: period vocabulary, not the plan of a named target or a sortie.
 let port=root('port');ground(port,-1.2);water(port,700,850,[330,0,0],'#50696d');box(port,[-108,.2,0],[220,2.0,600],'stone');box(port,[0,.2,0],[2,3,600],'stone');
 batch('warehouse',Array.from({length:7},(_,i)=>({p:[-35-(i%2)*34,1.3,(i-3)*42],ry:0,s:.9})),port);batch('crane',[{p:[-8,1.3,-39],ry:Math.PI/2},{p:[-8,1.3,45],ry:Math.PI/2,s:.85}],port);batch('chimney',[{p:[-91,1.3,-64]},{p:[-122,1.3,27],s:.7}],port);
 let ship=asset('boat');ship.position.set(21,.6,15);ship.rotation.y=-.07;port.add(ship);let crates=new THREE.InstancedMesh(new THREE.BoxGeometry(2.2,1.8,2.0),palette.wood,70),obj=new THREE.Object3D();for(let i=0;i<70;i++){obj.position.set(-9-r()*14,2.2+(i%4===0?1.8:0),-120+r()*240);obj.rotation.y=r()*.2;obj.updateMatrix();crates.setMatrixAt(i,obj.matrix);}crates.castShadow=crates.receiveShadow=true;port.add(crates);houses(port,Array.from({length:24},(_,i)=>({p:[-150-(i%3)*15,1.3,(Math.floor(i/3)-4)*20],s:.9})));blasts.push(new Blast(port,[-83,1.3,-80],73.5,41,1.2));
 // BACH MAI: interpretive facade and wings, with the documented date separate.
 let hospital=root('hospital');ground(hospital);let central=asset('hospital');hospital.add(central);
 let sign=textPlane('BỆNH VIỆN BẠCH MAI',12.8,1.15,'bold 76px Arial','#a99b7d');sign.position.set(0,6.25,3.52);sign.material=new THREE.MeshStandardMaterial({map:sign.material.map,transparent:true,roughness:1,side:THREE.DoubleSide,depthWrite:false});hospital.add(sign);
 batch('ward',[{p:[-23,0,-3]},{p:[-23,0,-23]},{p:[14,0,-33],ry:0}],hospital);let injuredWard=asset('ward');injuredWard.position.set(24,0,-3);hospital.add(injuredWard);let fallenWard=new THREE.Group();hospital.add(fallenWard);for(let i=0;i<4;i++)batch('ruin'+i,[{p:[14+i*7,0,-3],s:1.15}],fallenWard);
 for(let side of[-1,1]){box(hospital,[side*23,.6,30],[31,1.2,.5],'brick');box(hospital,[side*39,.6,4],[.5,1.2,53],'brick');}trees(hospital,[{p:[-32,0,18],s:1.1},{p:[32,0,21],s:1.2},{p:[-44,0,-30],s:1.4},{p:[41,0,-28],s:1.2}]);batch('bicycle',[{p:[-11,.0,6],ry:.3},{p:[-12,.0,6.5],ry:.5}],hospital);
 box(hospital,[0,.05,18],[12,.07,22],roadMat);blasts.push(new Blast(hospital,[25,0,-8],98,22,1.1),new Blast(hospital,[-14,0,-33],100.5,23,.85));
 // KHAM THIEN: a finite tiled-house streetscape, reversible damage states.
 let street=root('street');ground(street);box(street,[0,.006,0],[13,.035,210],roadMat);for(let side of[-1,1])box(street,[side*6.8,.13,0],[.4,.27,210],'stone');
 let rows=[];for(let side of[-1,1])for(let j=0;j<17;j++){let v=(j+(side===1?3:0))%8,z=(j-8)*8.5,ry=(side<0?Math.PI/2:-Math.PI/2)+(r()-.5)*.025;rows.push({p:[side*(11.7+(v%4)*.19+(r()-.5)*.6),0,z],ry,v,s:1,hit:126+Math.abs(z+17)*.031+(side>0?.65:0)});}
 for(let v=0;v<8;v++){let ps=rows.filter(p=>p.v===v);damage.push({ps,intact:batch('house'+v,ps,street),ruin:batch('ruin'+v,ps,street),states:[]});}
 // Background blocks remain intact, keeping the damage footprint visually bounded.
 houses(street,Array.from({length:32},(_,i)=>({p:[(i%2===0?-1:1)*(31+(i%4)*3),0,(Math.floor(i/2)-8)*11],ry:i%2===0?Math.PI/2:-Math.PI/2,s:.9+r()*.25})));

 houses(street,Array.from({length:22},(_,i)=>({p:[(i-11)*9,0,-100-(i%3)*13],ry:.03*(i%3),s:.8+(i%4)*.075})));
 let poles=[];for(let side of[-1,1])for(let j=0;j<5;j++)poles.push({p:[side*6.2,0,(j-2)*32],ry:Math.PI/2});batch('pole',poles,street);for(let side of[-1,1])for(let j=0;j<4;j++)for(let off of[-.6,.6])cable(street,[side*6.2,8.5,(j-2)*32+off],[side*6.2,8.5,(j-1)*32+off]);
 trees(street,[{p:[-7.4,0,-57],s:.85},{p:[7.4,0,54],s:.85},{p:[-29,0,9],s:1.3},{p:[25,0,-47],s:1.2}]);batch('bicycle',[{p:[-6.4,.02,40],ry:.13},{p:[6.4,.02,-32],ry:-.1}],street);
 for(const[text,z,side]of[['TẠP HÓA',40,-1],['HIỆU SÁCH',-38,1],['SỬA XE',18,-1]]){let t=textPlane(text,3.2,.75,'bold 72px Georgia','#d9ceae','#343e35');t.rotation.y=side<0?Math.PI/2:-Math.PI/2;t.position.set(side*6.95,2.8,z);street.add(t);t.userData.hit=126+Math.abs(z+17)*.031;}
 for(const[p,t,s]of[[[-10,0,-23],126,1.1],[[11,0,2],127.1,1.0],[[-9,0,29],128.4,.9],[[10,0,-53],130,1.0]])blasts.push(new Blast(street,p,t,Math.floor(t*7),s));
 // NGOC HA / HUU TIEP: no later memorial fencing or modern towers.
 let lake=root('lake');ground(lake,-2);for(const[p,s]of[[[0,-.05,29],[150,1.7,28]],[[0,-.05,-29],[150,1.7,28]],[[43,-.05,0],[36,1.7,30]],[[-43,-.05,0],[36,1.7,30]]])box(lake,p,s,groundMat);
 for(const[p,s]of[[[0,.27,15.3],[52,.65,.6]],[[0,.27,-15.3],[52,.65,.6]],[[25.9,.27,0],[.6,.65,31]],[[-25.9,.27,0],[.6,.65,31]]])box(lake,p,s,'stone');
 
 const mirror=new Reflector(new THREE.PlaneGeometry(51.2,30),{textureWidth:768,textureHeight:768,color:0x7d8674,clipBias:.006});
 mirror.material.uniforms.uTime={value:0};
 mirror.material.fragmentShader=mirror.material.fragmentShader.replace('uniform vec3 color;','uniform vec3 color;uniform float uTime;')
 .replace('vec4 base = texture2DProj( tDiffuse, vUv );',`vec4 uv=vUv;uv.x+=sin(vUv.y*49.+uTime*.55)*.0008*uv.w;uv.y+=sin(vUv.x*57.-uTime*.40)*.0006*uv.w;
 vec4 base=texture2DProj(tDiffuse,uv)*.4;
 base+=texture2DProj(tDiffuse,uv+vec4(.0006*uv.w,.0004*uv.w,0.,0.))*.3;
 base+=texture2DProj(tDiffuse,uv-vec4(.0006*uv.w,.0004*uv.w,0.,0.))*.3;`)
 .replace('blendOverlay( base.rgb, color )','mix(blendOverlay(base.rgb,color),vec3(.12,.16,.12),.26)');
 mirror.rotation.x=-Math.PI/2;mirror.position.y=.13;lake.add(mirror);
 const wreck=asset('wreck');wreck.position.set(-1,.08,1);wreck.rotation.y=.28;lake.add(wreck);
 let lh=[];for(let side of[-1,1])for(let j=0;j<8;j++)lh.push({p:[(j-3.5)*8.1,.8,side*24],ry:side>0?Math.PI:0,s:.85+(j%3)*.075});for(let side of[-1,1])for(let j=0;j<3;j++)lh.push({p:[side*34,.8,(j-1)*10],ry:side>0?-Math.PI/2:Math.PI/2,s:.9});houses(lake,lh);
 trees(lake,[{p:[-24,.8,15],s:1.2},{p:[25,.8,-15],s:1.15},{p:[-29,.8,-14],s:1.4},{p:[23,.8,22],s:.9},{p:[-3,.8,-18],s:.7}]);batch('bicycle',[{p:[16,.8,17],ry:1.1}],lake);
 let ripples=[];for(let j=0;j<6;j++){let m=new THREE.Mesh(new THREE.RingGeometry(2.0+j*.9,2.012+j*.9,72),new THREE.MeshBasicMaterial({color:'#99ad8e',transparent:true,opacity:.13,depthWrite:false,side:THREE.DoubleSide}));m.rotation.x=-Math.PI/2;m.position.set(-1,.142,1);lake.add(m);ripples.push(m);}
 let current='',quality='balanced';const temp=new THREE.Object3D();
 function setLocation(id){
  if(current===id)return;current=id;let actual=id==='after'?'street':id;for(const[name,g]of Object.entries(roots))g.visible=name===actual;let a=locations[id];scene.fog=new THREE.FogExp2(a.horizon,a.density);skyMat.uniforms.top.value.set(a.zenith);skyMat.uniforms.sunPower.value=['air','hospital','street'].includes(id)?0:.10;skyMat.uniforms.bottom.value.set(a.horizon);hemi.intensity=a.ambient;hemi.color.set(id==='after'?'#d1c9b2':'#b0c7d6');key.color.set(a.key);key.intensity=a.power;key.target.position.set(...a.center);key.position.copy(key.target.position).add(V(id==='after'?[-60,32,40]:[-65,95,40]));key.castShadow=quality!=='low'&&id!=='air';mirror.visible=id==='lake'&&quality!=='low';
 }
 function update(t,camera,gentle){
  for(const m of waterMaterials){m.uniforms.uTime.value=t;m.uniforms.haze.value.set(locations[current].horizon);}mirror.material.uniforms.uTime.value=t;
  if(current==='bridge'){barge.position.z=68-(t%26)*.3;}
  if(current==='air'){
   plane.rotation.z=Math.sin(t*.20)*.025;plane.rotation.x=Math.sin(t*.13)*.006;plane.position.y=92+Math.sin(t*.3)*.15;
   let open=Math.max(0,Math.min(1,(t-44)/1.5));for(const d of doors)d.h.rotation.z=d.s*open*1.48;
   for(let i=0;i<bombs.length;i++){let age=t-(46.3+i*.32),b=bombs[i];b.visible=age>=0&&age<5.7;if(b.visible){b.position.set((i%3-1)*.48,89.7-4.1*age*age,.2+(i%7-3)*.7+age*.25);b.rotation.x=-Math.PI/2+Math.min(age,2)*.06;b.rotation.z=Math.sin(age+i)*.07;}}
   for(let i=0;i<cloudData.length;i++){let d=cloudData[i],p=[d.p[0],d.p[1],d.p[2]+(t-26)*5];clouds.set(i,p,d.sz,.58,camera,d.a,.30);}clouds.finish();
  }
  if(current==='hospital'){injuredWard.visible=t<98.25;fallenWard.visible=t>=98.25;}
  if(current==='street'||current==='after'){
   for(const d of damage){d.ps.forEach((p,i)=>{let hit=t>=p.hit;if(d.states[i]===hit)return;d.states[i]=hit;for(const[g,show]of[[d.intact,!hit],[d.ruin,hit]]){temp.position.set(...p.p);temp.rotation.set(0,p.ry,0);temp.scale.setScalar(show?p.s:0);temp.updateMatrix();g.children.forEach(m=>{m.setMatrixAt(i,temp.matrix);m.instanceMatrix.needsUpdate=true;});}});}
   for(const ob of street.children)if(ob.userData.hit)ob.visible=t<ob.userData.hit;
  }
  let pulse=0;for(const blast of blasts)if(blast.root.parent.visible){blast.update(t,camera,gentle);let age=t-blast.start,p=age>=0?Math.exp(-age*2.4)*blast.scale:0;if(p>pulse){pulse=p;flash.position.copy(blast.root.position);flash.position.y+=5;}}flash.intensity=pulse*(gentle?18:100);
  if(current==='lake')ripples.forEach((m,i)=>{m.scale.setScalar(1+Math.sin(t*.4+i)*.04);m.material.opacity=.08+Math.sin(t*.5+i)*.025;});
 }
 function setQuality(q){quality=q;key.castShadow=q!=='low'&&current!=='air';mirror.visible=current==='lake'&&q!=='low';if(q==='low'){if(!lake.userData.flatwater)lake.userData.flatwater=water(lake,51.2,30,[0,.13,0],'#536947');lake.userData.flatwater.visible=true;}else if(lake.userData.flatwater)lake.userData.flatwater.visible=false;}
 setLocation('bridge');return{scene,roots,key,hemi,sky,plane,mirror,blasts,setLocation,update,setQuality,get location(){return current;},get damageCount(){return damage.reduce((n,d)=>n+d.states.filter(Boolean).length,0);}};
}
