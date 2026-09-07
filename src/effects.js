import * as THREE from 'three';
import {rng,V,prototypes,texture} from './geometry.js';
import {simulateDebris,supportHeight} from './debris_physics.js';
const TAU=Math.PI*2;
export function puffTexture(){
 const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d'),r=rng(882);
 for(let j=0;j<90;j++){let a=r()*TAU,rad=r()*65,px=128+Math.cos(a)*rad,py=128+Math.sin(a)*rad,sz=25+r()*53,g=x.createRadialGradient(px,py,0,px,py,sz);g.addColorStop(0,'rgba(255,255,255,.10)');g.addColorStop(.55,'rgba(235,240,238,.065)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(px-sz,py-sz,sz*2,sz*2);}
 const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;
}
let puff;
export class Billboards{
 constructor(count,color='#6e756c',additive=false,cloud=false){
  this.count=count;const geo=new THREE.PlaneGeometry(1,1);this.alpha=new THREE.InstancedBufferAttribute(new Float32Array(count),1);geo.setAttribute('particleAlpha',this.alpha);
  const mat=new THREE.MeshBasicMaterial({color,map:cloud?puffTexture():(puff??(puff=texture('dust'))),transparent:true,depthWrite:false,side:THREE.DoubleSide,blending:additive?THREE.AdditiveBlending:THREE.NormalBlending});
  mat.onBeforeCompile=s=>{s.vertexShader=s.vertexShader.replace('#include <common>','#include <common>\nattribute float particleAlpha;varying float vParticleAlpha;').replace('#include <begin_vertex>','#include <begin_vertex>\nvParticleAlpha=particleAlpha;');s.fragmentShader=s.fragmentShader.replace('#include <common>','#include <common>\nvarying float vParticleAlpha;').replace('#include <color_fragment>','#include <color_fragment>\ndiffuseColor.a*=vParticleAlpha;');};
  this.mesh=new THREE.InstancedMesh(geo,mat,count);this.mesh.frustumCulled=false;this.obj=new THREE.Object3D();this.mesh.renderOrder=4;this.mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
 }
 set(i,p,size,alpha,camera,angle=0,stretch=1){let o=this.obj;o.position.set(...p);o.quaternion.copy(camera.quaternion);o.rotateZ(angle);o.scale.set(size,size*stretch,1);o.updateMatrix();this.mesh.setMatrixAt(i,o.matrix);this.alpha.setX(i,Math.max(0,Math.min(1,alpha)));}
 finish(){this.mesh.instanceMatrix.needsUpdate=true;this.alpha.needsUpdate=true;}
}
export class Blast{
 constructor(parent,pos,start,seed=2,scale=1,options={}){
  this.start=start;this.pos=pos;this.scale=scale;this.root=new THREE.Group();this.root.position.set(...pos);parent.add(this.root);
  this.physics=simulateDebris(seed,280,options);this.audit=this.physics.audit;this.age=-1;this.lastMatrixTime=NaN;
  this.smoke=new Billboards(76,'#897c67');this.darkSmoke=new Billboards(24,'#655b4b');this.fire=new Billboards(12,'#f0af69',true);this.trails=new Billboards(42,'#817365');
  this.root.add(this.smoke.mesh,this.darkSmoke.mesh,this.fire.mesh,this.trails.mesh);
  const r=rng(seed+710);this.spec=Array.from({length:100},(_,i)=>({a:r()*TAU,r:r(),delay:r()*.6,up:r(),angle:r()*TAU}));
  this.parts=[];this.temp=new THREE.Object3D();
  for(let type=0;type<4;type++){
   const ids=this.physics.specs.map((s,i)=>s.type===type?i:-1).filter(i=>i>=0);
   for(const part of prototypes['fragment'+type]){
    let mesh=new THREE.InstancedMesh(part.geo,part.mat,ids.length);mesh.castShadow=mesh.receiveShadow=true;mesh.frustumCulled=false;mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    ids.forEach((id,i)=>mesh.setColorAt(i,new THREE.Color().setScalar(.65+r()*.50)));this.root.add(mesh);this.parts.push({mesh,ids});
   }
  }
  const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d'),g=x.createRadialGradient(128,128,20,128,128,120);g.addColorStop(0,'rgba(28,25,19,.90)');g.addColorStop(.45,'rgba(39,32,24,.72)');g.addColorStop(1,'rgba(40,34,25,0)');x.fillStyle=g;x.fillRect(0,0,256,256);
  const map=new THREE.CanvasTexture(c);map.colorSpace=THREE.SRGBColorSpace;this.scorch=new THREE.Mesh(new THREE.PlaneGeometry(11,11),new THREE.MeshBasicMaterial({map,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-1,side:THREE.DoubleSide}));this.scorch.rotation.x=-Math.PI/2;this.scorch.position.y=.04;this.root.add(this.scorch);
 }
 sample(i,age){let p=this.physics,at=Math.max(0,Math.min(p.frames-1,age*p.rate)),a=Math.floor(at),b=Math.min(a+1,p.frames-1),u=at-a,o=(i*p.frames+a)*6,q=(i*p.frames+b)*6;return Array.from({length:6},(_,k)=>p.tracks[o+k]*(1-u)+p.tracks[q+k]*u);}
 update(t,camera,gentle){
  const age=t-this.start;this.age=age;this.root.visible=age>=0;if(age<0)return;
  if(this.lastMatrixTime!==Math.min(age,12)){
   let visible=0;
   for(const part of this.parts)part.ids.forEach((id,index)=>{
    const spec=this.physics.specs[id],state=this.sample(id,age),o=this.temp;const show=age>=spec.spawn;
    o.position.set(state[0],Math.max(state[1],supportHeight(state[3],state[4],state[5],spec.dims)),state[2]);o.rotation.set(state[3],state[4],state[5]);o.scale.setScalar(show?spec.scale:0);o.updateMatrix();part.mesh.setMatrixAt(index,o.matrix);part.mesh.instanceMatrix.needsUpdate=true;if(show)visible++;
   });this.visibleFragments=visible;this.lastMatrixTime=Math.min(age,12);
  }
  this.smoke.mesh.visible=this.darkSmoke.mesh.visible=age<70;this.fire.mesh.visible=age<1.1;this.trails.mesh.visible=age<3.5;
  // The flash is brief. Most visible material is earth/plaster dust, not a sustained fireball.
  for(let i=0;i<12;i++){let q=this.spec[i],a=Math.max(0,age-i*.009);this.fire.set(i,[Math.cos(q.a)*a*5,1+a*4,Math.sin(q.a)*a*5],1.2+Math.sqrt(a)*7,a<.55?Math.exp(-a*9)*.38*(gentle?.18:1):0,camera,q.angle);}
  if(age<70)for(let i=0;i<76;i++){
   let q=this.spec[i],a=age-q.delay,tt=Math.max(0,a),ground=i<28,rad=ground?(2+11*(1-Math.exp(-tt*.8)))*(q.r*.8+.3):(1+2.4*tt/(1+tt*.16))*(q.r+.2),y=ground?.35+q.up*.6+Math.sqrt(tt)*.20:1.5+(4+q.up*4)*(1-Math.exp(-tt*.55))+tt*.30;
   let size=ground?(1.9+tt*1.2):(2.0+Math.sqrt(tt)*3.0);size*=.7+q.r*.8;
   let opacity=a<0?0:Math.min(1,tt*4)*Math.exp(-tt/(ground?9:32))*(ground?.43:.52);
   this.smoke.set(i,[Math.cos(q.a)*rad+tt*.34,y,Math.sin(q.a)*rad+tt*.10],size,opacity,camera,q.angle+tt*.016,ground?.55:1.08);
  }
  if(age<70)for(let i=0;i<24;i++){let q=this.spec[i+76],a=Math.max(0,age-q.delay),rr=(.4+q.r)*Math.min(4,a*2);this.darkSmoke.set(i,[Math.cos(q.a)*rr+a*.22,1.1+5*(1-Math.exp(-a*.6))+q.up*4+a*.16,Math.sin(q.a)*rr],(1.1+Math.sqrt(a)*2.0)*(q.r+.65),age<q.delay?0:Math.min(1,a*5)*Math.exp(-a/18)*.40,camera,q.angle+a*.02);}
  if(age<3.5)for(let i=0;i<42;i++){let id=i*3,s=this.physics.specs[id],state=this.sample(id,Math.max(0,age-.08)),v=Math.max(0,1-age/3.5);this.trails.set(i,[state[0],state[1],state[2]],.7+age*.35,age>s.spawn?v*.19:0,camera,this.spec[i].angle,1.6);}
  this.smoke.finish();this.darkSmoke.finish();this.fire.finish();this.trails.finish();
 }
}
export function leafTexture(){let c=document.createElement('canvas');c.width=c.height=256;let x=c.getContext('2d'),r=rng(1591);for(let j=0;j<16;j++){let ax=128+(r()-.5)*150,ay=128+(r()-.5)*150,angle=r()*TAU;x.save();x.translate(ax,ay);x.rotate(angle);x.strokeStyle='#435b38';x.lineWidth=2;x.beginPath();x.moveTo(0,30);x.lineTo(0,-40);x.stroke();for(let k=0;k<6;k++){for(let sign of[-1,1]){x.fillStyle=['#496044','#5a7046','#68794e'][j%3];x.beginPath();x.ellipse(sign*(7+k*.8),19-k*10,11,4,sign*-.6,0,TAU);x.fill();}}x.restore();}let t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;}

