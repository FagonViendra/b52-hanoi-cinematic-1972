import * as THREE from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
export const seed=19721218;
export function rng(s=seed){return()=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return s/4294967296;};}
export const rand=rng(),V=(a)=>new THREE.Vector3(...a),palette={},prototypes={},measurements={};
export function texture(kind,base='#a6a293'){
 const c=document.createElement('canvas');c.width=c.height=512;const x=c.getContext('2d'),r=rng(seed+kind.length*173);x.fillStyle=base;x.fillRect(0,0,512,512);
 if(kind==='camo'){
  x.fillStyle='#515b3b';x.fillRect(0,0,512,512);
  for(let i=0;i<36;i++){let xx=r()*700-90,yy=r()*700-90,rad=45+r()*95;x.fillStyle=['#28392d','#40472f','#6f6545'][i%3];x.beginPath();for(let j=0;j<9;j++){let a=j*Math.PI*2/8,rr=rad*(.6+r()*.5),px=xx+Math.cos(a)*rr,py=yy+Math.sin(a)*rr;if(j===0)x.moveTo(px,py);else x.quadraticCurveTo(xx+Math.cos(a-.2)*rad,yy+Math.sin(a-.2)*rad,px,py);}x.fill();}
 }else if(kind==='brick'){
  x.fillStyle='#585b53';x.fillRect(0,0,512,512);for(let row=0;row<16;row++)for(let col=-1;col<8;col++){let g=153+Math.floor(r()*57);x.fillStyle=`rgb(${g},${g-14},${g-23})`;x.fillRect(col*78+(row%2)*39,row*32,75,29);}
 }else if(kind==='tile'){
  for(let row=0;row<8;row++)for(let col=0;col<16;col++){let g=125+r()*42,gr=x.createLinearGradient(col*32,0,col*32+32,0);gr.addColorStop(0,`rgb(${g*.75},${g*.74},${g*.72})`);gr.addColorStop(.5,`rgb(${g+45},${g+40},${g+33})`);gr.addColorStop(1,`rgb(${g*.6},${g*.57},${g*.53})`);x.fillStyle=gr;x.fillRect(col*32,row*64,32,62);x.fillStyle='#414540';x.fillRect(col*32,row*64+60,32,3);}
 }else if(kind==='wood'){
  for(let i=0;i<200;i++){let yy=r()*512;x.strokeStyle=`rgba(25,30,24,${r()*.18})`;x.lineWidth=.3+r()*2;x.beginPath();x.moveTo(0,yy);x.bezierCurveTo(160,yy+r()*15,340,yy-r()*10,512,yy);x.stroke();}
 }else if(kind==='road'){
  x.fillStyle='#8c8b7e';x.fillRect(0,0,512,512);for(let i=0;i<80;i++){x.strokeStyle='#555f5633';x.lineWidth=r()*3;x.beginPath();let px=r()*512,py=r()*512;x.moveTo(px,py);for(let j=0;j<4;j++){px+=(r()-.5)*80;py+=r()*40;x.lineTo(px,py);}x.stroke();}
 }
 if(kind!=='camo')for(let i=0;i<18000;i++){let g=r()>.5?255:0;x.fillStyle=`rgba(${g},${g},${g},${r()*.085})`;x.fillRect(r()*512,r()*512,1+r()*3,1+r()*3);}
 for(let i=0;i<35;i++){let xx=r()*512,yy=r()*512,rr=10+r()*55,g=x.createRadialGradient(xx,yy,0,xx,yy,rr);g.addColorStop(0,'rgba(20,25,20,.055)');g.addColorStop(1,'rgba(20,25,20,0)');x.fillStyle=g;x.fillRect(xx-rr,yy-rr,rr*2,rr*2);}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=4;return t;
}
function rotMatrix(a){return new THREE.Matrix4().makeRotationZ(a[2]).multiply(new THREE.Matrix4().makeRotationY(a[1])).multiply(new THREE.Matrix4().makeRotationX(a[0]));}
function meshFrom(vs,faces,smooth){const ids=[];for(const f of faces)for(let j=1;j<f.length-1;j++)ids.push(f[0],f[j],f[j+1]);let g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vs.flat(),3));g.setIndex(ids);if(smooth)g.computeVertexNormals();g=g.toNonIndexed();if(!smooth)g.computeVertexNormals();return g;}
function geometry(rec){
 const[kind,mat,...d]=rec;let g;
 if(kind==='box'){const[p,s,rot]=d;g=new THREE.BoxGeometry(...s);g.applyMatrix4(rotMatrix(rot));g.translate(...p);}
 else if(kind==='ell'){const[p,s,n]=d;g=new THREE.SphereGeometry(1,n,Math.max(6,n>>1));g.scale(...s);g.translate(...p);}
 else if(kind==='tor'){const[p,r,t,rot]=d;g=new THREE.TorusGeometry(r,t,10,24);g.applyMatrix4(rotMatrix(rot));g.translate(...p);}
 else if(kind==='beam'){const[a,b,r1,r2,n]=d,dir=V(b).sub(V(a));g=new THREE.CylinderGeometry(r2,r1,dir.length(),n,1,false);g.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),dir.clone().normalize()));g.translate(...V(a).add(V(b)).multiplyScalar(.5).toArray());}
 else if(kind==='poly')g=meshFrom(d[0],d[1],!!d[2]);
 else if(kind==='lathe'){
  const[st,n,x,y]=d,vs=[],fs=[];for(const[z,rx,ry,cy]of st)for(let j=0;j<n;j++){let a=j*2*Math.PI/n;vs.push([x+rx*Math.cos(a),y+cy+ry*Math.sin(a),z]);}for(let i=0;i<st.length-1;i++)for(let j=0;j<n;j++)fs.push([i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j]);g=meshFrom(vs,fs,true);
 }else if(kind==='airfoil'){
  const[secs,steps]=d,n=steps*2,vs=[],fs=[];for(const[x,lead,chord,y,thick]of secs)for(let j=0;j<n;j++){let a=j*Math.PI*2/n,f=(1-Math.cos(a))*.5,t=5*thick*chord*(.2969*Math.sqrt(f)-.126*f-.3516*f*f+.2843*f**3-.1015*f**4);vs.push([x,y+(j<=steps?t:-t),lead+f*chord]);}for(let i=0;i<secs.length-1;i++)for(let j=0;j<n;j++){let f=[i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j];if(secs[0][0]>secs.at(-1)[0])f.reverse();fs.push(f);}g=meshFrom(vs,fs,true);
 }else throw Error('Unknown geometry operation: '+kind);
 if(g.index)g=g.toNonIndexed();if(!g.getAttribute('normal'))g.computeVertexNormals();const p=g.getAttribute('position'),n=g.getAttribute('normal'),uv=[];
 for(let i=0;i<p.count;i++){let x=p.getX(i),y=p.getY(i),z=p.getZ(i),nx=Math.abs(n.getX(i)),ny=Math.abs(n.getY(i)),nz=Math.abs(n.getZ(i));if(mat==='air')uv.push(x*.022+z*.007,z*.031+y*.016);else if(ny>nx&&ny>nz)uv.push(x*.23,z*.23);else if(nx>nz)uv.push(z*.23,y*.23);else uv.push(x*.23,y*.23);}
 g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));return g;
}
export async function initAssets(data,onProgress){
 for(const[name,d]of Object.entries(data.materials)){
  let opt={color:d.color,roughness:d.rough??.85,metalness:d.metal??0,side:THREE.DoubleSide};if(d.tex){opt.map=texture(d.tex);if(d.tex==='camo')opt.color='#ffffff';else{opt.bumpMap=opt.map;opt.bumpScale=d.tex==='tile'?.10:.035;}}if(d.emissive){opt.emissive=d.emissive;opt.emissiveIntensity=.65;}
  const m=new THREE.MeshStandardMaterial(opt);m.name=name;palette[name]=m;
  if(name==='air')m.onBeforeCompile=(s)=>{s.vertexShader=s.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 localNormal;').replace('#include <beginnormal_vertex>','#include <beginnormal_vertex>\nlocalNormal=objectNormal;');s.fragmentShader=s.fragmentShader.replace('#include <common>','#include <common>\nvarying vec3 localNormal;').replace('#include <map_fragment>','#include <map_fragment>\nfloat underside=1.0-smoothstep(-0.65,-0.15,normalize(localNormal).y);diffuseColor.rgb=mix(diffuseColor.rgb,vec3(0.013,0.019,0.020),underside*0.91);');};
 }
 let index=0;for(const[name,recs]of Object.entries(data.assets)){
  let buckets={};for(const rec of recs)(buckets[rec[1]]??=[]).push(geometry(rec));prototypes[name]=Object.entries(buckets).map(([mat,gs])=>{let geo=mergeGeometries(gs,false);geo.computeBoundingBox();geo.computeBoundingSphere();gs.forEach(g=>g.dispose());return{geo,mat:palette[mat]};});
  let b=new THREE.Box3();prototypes[name].forEach(p=>b.union(p.geo.boundingBox));measurements[name]={min:b.min.toArray(),max:b.max.toArray(),size:b.getSize(new THREE.Vector3()).toArray(),triangles:prototypes[name].reduce((a,p)=>a+p.geo.attributes.position.count/3,0)};onProgress?.(++index/Object.keys(data.assets).length,name);await new Promise(r=>setTimeout(r,0));
 }
}
export function asset(name){let group=new THREE.Group();group.name=name;for(const p of prototypes[name]){let m=new THREE.Mesh(p.geo,p.mat);m.castShadow=m.receiveShadow=true;group.add(m);}return group;}
export function batch(name,placements,parent){
 const group=new THREE.Group();group.name='instances_'+name;const temp=new THREE.Object3D();for(const part of prototypes[name]){let mesh=new THREE.InstancedMesh(part.geo,part.mat,placements.length);mesh.castShadow=mesh.receiveShadow=true;placements.forEach((p,i)=>{temp.position.set(...(p.p||[0,0,0]));temp.rotation.set(0,p.ry||0,0);temp.scale.setScalar(p.s??1);temp.updateMatrix();mesh.setMatrixAt(i,temp.matrix);});mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();group.add(mesh);}parent?.add(group);return group;
}
export function textPlane(text,width,height,font='bold 70px Arial',color='#e7d8b8',bg=null){const c=document.createElement('canvas');c.width=1024;c.height=256;const x=c.getContext('2d');if(bg){x.fillStyle=bg;x.fillRect(0,0,1024,256);}x.fillStyle=color;x.font=font;x.textAlign='center';x.textBaseline='middle';x.fillText(text,512,128,970);let map=new THREE.CanvasTexture(c);map.colorSpace=THREE.SRGBColorSpace;let m=new THREE.Mesh(new THREE.PlaneGeometry(width,height),new THREE.MeshBasicMaterial({map,transparent:!bg,side:THREE.DoubleSide,depthWrite:false}));return m;}
export function box(parent,p,s,mat,rot=0){let m=new THREE.Mesh(new THREE.BoxGeometry(...s),typeof mat==='string'?palette[mat]:mat);m.position.set(...p);m.rotation.y=rot;m.receiveShadow=true;m.castShadow=true;parent.add(m);return m;}
export function wire(parent,a,b,color='#313934',r=.025){let dir=V(b).sub(V(a)),m=new THREE.Mesh(new THREE.CylinderGeometry(r,r,dir.length(),5),new THREE.MeshStandardMaterial({color,roughness:.9}));m.position.copy(V(a).add(V(b)).multiplyScalar(.5));m.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.normalize());parent.add(m);return m;}
