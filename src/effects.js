import * as THREE from 'three';
import {rng,V} from './geometry.js';
const TAU=Math.PI*2;
export function puffTexture(){
 const c=document.createElement('canvas');c.width=c.height=256;const x=c.getContext('2d'),r=rng(882);
 for(let j=0;j<90;j++){let a=r()*TAU,rad=r()*65,px=128+Math.cos(a)*rad,py=128+Math.sin(a)*rad,sz=25+r()*53,g=x.createRadialGradient(px,py,0,px,py,sz);g.addColorStop(0,'rgba(255,255,255,.10)');g.addColorStop(.55,'rgba(235,240,238,.065)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(px-sz,py-sz,sz*2,sz*2);}
 const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;
}
let puff;
export class Billboards{
 constructor(count,color='#6e756c',additive=false){
  this.count=count;const geo=new THREE.PlaneGeometry(1,1);this.alpha=new THREE.InstancedBufferAttribute(new Float32Array(count),1);geo.setAttribute('particleAlpha',this.alpha);
  const mat=new THREE.MeshBasicMaterial({color,map:puff??(puff=puffTexture()),transparent:true,depthWrite:false,side:THREE.DoubleSide,blending:additive?THREE.AdditiveBlending:THREE.NormalBlending});
  mat.onBeforeCompile=s=>{s.vertexShader=s.vertexShader.replace('#include <common>','#include <common>\nattribute float particleAlpha;varying float vParticleAlpha;').replace('#include <begin_vertex>','#include <begin_vertex>\nvParticleAlpha=particleAlpha;');s.fragmentShader=s.fragmentShader.replace('#include <common>','#include <common>\nvarying float vParticleAlpha;').replace('#include <color_fragment>','#include <color_fragment>\ndiffuseColor.a*=vParticleAlpha;');};
  this.mesh=new THREE.InstancedMesh(geo,mat,count);this.mesh.frustumCulled=false;this.obj=new THREE.Object3D();this.mesh.renderOrder=4;this.mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
 }
 set(i,p,size,alpha,camera,angle=0,stretch=1){let o=this.obj;o.position.set(...p);o.quaternion.copy(camera.quaternion);o.rotateZ(angle);o.scale.set(size,size*stretch,1);o.updateMatrix();this.mesh.setMatrixAt(i,o.matrix);this.alpha.setX(i,Math.max(0,Math.min(1,alpha)));}
 finish(){this.mesh.instanceMatrix.needsUpdate=true;this.alpha.needsUpdate=true;}
}
export class Blast{
 constructor(parent,pos,start,seed=2,scale=1){
  this.start=start;this.pos=pos;this.scale=scale;this.r=rng(seed);this.root=new THREE.Group();parent.add(this.root);this.root.position.set(...pos);this.smoke=new Billboards(60,'#818279');this.fire=new Billboards(14,'#e28334',true);this.root.add(this.smoke.mesh,this.fire.mesh);this.light=new THREE.PointLight('#ffb66b',0,100*scale,1.5);this.light.position.y=5;this.root.add(this.light);
  this.spec=Array.from({length:60},(_,i)=>({a:this.r()*TAU,s:this.r(),up:this.r(),delay:i<15?0:this.r()*2.0}));
  const geo=new THREE.BoxGeometry(.35,.23,.45),mat=new THREE.MeshStandardMaterial({color:'#797365',roughness:1});this.debris=new THREE.InstancedMesh(geo,mat,28);this.debris.frustumCulled=false;this.root.add(this.debris);this.temp=new THREE.Object3D();
  this.ring=new THREE.Mesh(new THREE.RingGeometry(.82,1,64),new THREE.MeshBasicMaterial({color:'#c3b295',transparent:true,opacity:0,depthWrite:false,side:THREE.DoubleSide}));this.ring.rotation.x=-Math.PI/2;this.ring.position.y=.06;this.root.add(this.ring);
 }
 update(t,camera,gentle){
  let age=t-this.start;this.root.visible=age>=0&&age<70;if(!this.root.visible)return;let sc=this.scale;
  for(let i=0;i<60;i++){let s=this.spec[i],a=age-s.delay,life=Math.max(0,a),side=Math.min(life,14)*(i<16?2.0:0.3+s.s*.7),rise=i<16?.45+life*.16:1.5+Math.min(life,28)*(1.0+s.up*.7),size=(2+Math.sqrt(life)*3.3+s.s*2)*sc,alpha=a<0?0:Math.min(1,life*2)*Math.max(0,1-life/65)*.39;this.smoke.set(i,[Math.cos(s.a)*side*sc+life*.17*sc,rise*sc,Math.sin(s.a)*side*sc],size,alpha,camera,s.a+life*.015,i<16?.7:1.1);}
  for(let i=0;i<14;i++){let s=this.spec[i],a=age-i*.065,life=Math.max(0,a),alpha=a<0?0:Math.exp(-life*1.45)*(.18+s.up*.13)*(gentle?.22:1);this.fire.set(i,[Math.cos(s.a)*life*2*sc,(1+life*3.5)*sc,Math.sin(s.a)*life*2*sc],(3+life*5+s.s*5)*sc,alpha,camera,s.a);}
  this.light.intensity=Math.exp(-age*2.4)*(gentle?18:100)*sc;this.light.visible=false;
  let ringAge=Math.min(age,5);this.ring.scale.setScalar(Math.max(.01,ringAge*12*sc));this.ring.material.opacity=age<3?(.025*(1-age/3)):0;
  for(let i=0;i<28;i++){let s=this.spec[i],a=Math.max(0,age),o=this.temp;o.position.set(Math.cos(s.a)*Math.min(a,4)*(3+s.s*7)*sc,Math.max(.1,(7+s.up*11)*a-4.6*a*a)*sc,Math.sin(s.a)*Math.min(a,4)*(3+s.s*7)*sc);o.rotation.set(a*(1+s.up),a*(2+s.s),a+s.a);o.scale.setScalar(age<5?sc:0);o.updateMatrix();this.debris.setMatrixAt(i,o.matrix);}this.debris.instanceMatrix.needsUpdate=true;this.debris.visible=age<5;this.smoke.finish();this.fire.finish();
 }
}
export function leafTexture(){let c=document.createElement('canvas');c.width=c.height=256;let x=c.getContext('2d'),r=rng(1591);for(let j=0;j<16;j++){let ax=128+(r()-.5)*150,ay=128+(r()-.5)*150,angle=r()*TAU;x.save();x.translate(ax,ay);x.rotate(angle);x.strokeStyle='#435b38';x.lineWidth=2;x.beginPath();x.moveTo(0,30);x.lineTo(0,-40);x.stroke();for(let k=0;k<6;k++){for(let sign of[-1,1]){x.fillStyle=['#496044','#5a7046','#68794e'][j%3];x.beginPath();x.ellipse(sign*(7+k*.8),19-k*10,11,4,sign*-.6,0,TAU);x.fill();}}x.restore();}let t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;return t;}
