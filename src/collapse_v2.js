import * as THREE from 'three';
import {prototypes} from './geometry.js';
import {simulateDebris,seeded,supportHeight} from './debris_physics.js';
export class CollapseField{
 constructor(parent,lots,dimensions){
  this.parts=[];this.houses=[];this.obj=new THREE.Object3D();this.yaw=new THREE.Quaternion();const axis=new THREE.Vector3(0,1,0),r=seeded(91026);
  for(const lot of lots){if(!Number.isFinite(lot.hit))continue;const[w,d,h]=dimensions[lot.v],rise=h>5?1.5:1.2,flat=[1,4].includes(lot.v),initial=[];
   for(let row=0;row<4;row++)for(let col=0;col<2;col++){let x=(col-.5)*w/2,z=(row-1.5)*d/4,y=flat?h:h+rise*(1-Math.abs(z)/(d/2));initial.push({type:0,position:[x,y,z],dims:[w/2,.10,d/4],rotation:[flat?0:Math.sign(z)*Math.atan(rise/(d/2)),0,0],omega:[(r()-.5)*1.3,(r()-.5)*.4,(r()-.5)*.8],velocity:[(r()-.5)*1.6,.4+r()*.6,(r()-.5)*2.0]});}
   for(let col=0;col<2;col++)initial.push({type:1,position:[(col-.5)*w/2,h-.85,d/2],dims:[w/2,1.4,.16],rotation:[0,0,0],omega:[1.0+r(),(r()-.5)*.5,(r()-.5)*.4],velocity:[(r()-.5),0,1.5+r()],restRotation:[Math.PI/2,0,0]});
   for(let col=0;col<4;col++)initial.push({type:2,position:[(col-1.5)*w/4,h-.35,0],dims:[.12,.18,d*.65],rotation:[0,0,0],omega:[(r()-.5)*1.7,(r()-.5)*.6,(r()-.5)*1.3],velocity:[(r()-.5)*1.3,0,(r()-.5)*1.6]});
   let physics=simulateDebris(1780+this.houses.length,initial.length,{initial,groundY:.45});this.houses.push({lot,initial,physics,yaw:new THREE.Quaternion().setFromAxisAngle(axis,lot.ry),last:NaN});
  }
  const bases=[[2.6,.10,3.2],[2,1.4,.16],[.12,.18,2.8]];
  for(let type=0;type<3;type++){
   let placements=[];this.houses.forEach((h,house)=>h.initial.forEach((s,piece)=>{if(s.type===type)placements.push({house,piece,dims:s.dims});}));
   for(const p of prototypes[['slabroof','slabwall','slabbeam'][type]]){let mesh=new THREE.InstancedMesh(p.geo,p.mat,placements.length);mesh.castShadow=mesh.receiveShadow=true;mesh.frustumCulled=false;parent.add(mesh);this.parts.push({mesh,placements,base:bases[type]});}
  }
  this.count=this.houses.reduce((n,h)=>n+h.initial.length,0);this.audit={houses:this.houses.length,structuralPieces:this.count,settledAtEnd:this.houses.reduce((n,h)=>n+h.physics.audit.settledAtEnd,0),groundViolations:this.houses.reduce((n,h)=>n+h.physics.audit.floorViolations,0)};
 }
 update(t){
  let changed=false;for(const h of this.houses){let age=Math.max(-1,Math.min(12,t-h.lot.hit));if(age!==h.last){changed=true;h.last=age;}}
  if(!changed)return;
  for(const part of this.parts){part.placements.forEach((p,i)=>{
   const house=this.houses[p.house],age=t-house.lot.hit,o=this.obj;
   if(age<0){o.scale.setScalar(0);o.updateMatrix();part.mesh.setMatrixAt(i,o.matrix);return;}
   const physics=house.physics,at=Math.min(physics.frames-1,age*physics.rate),a=Math.floor(at),b=Math.min(physics.frames-1,a+1),u=at-a,off=(p.piece*physics.frames+a)*6,nxt=(p.piece*physics.frames+b)*6;
   let state=Array.from({length:6},(_,k)=>physics.tracks[off+k]*(1-u)+physics.tracks[nxt+k]*u);
   o.position.set(state[0],Math.max(state[1],.45+supportHeight(state[3],state[4],state[5],p.dims)),state[2]).applyQuaternion(house.yaw).add(new THREE.Vector3(...house.lot.p));o.rotation.set(state[3],state[4],state[5]);o.quaternion.premultiply(house.yaw);o.scale.set(p.dims[0]/part.base[0],p.dims[1]/part.base[1],p.dims[2]/part.base[2]);o.updateMatrix();part.mesh.setMatrixAt(i,o.matrix);
  });part.mesh.instanceMatrix.needsUpdate=true;}
 }
}
