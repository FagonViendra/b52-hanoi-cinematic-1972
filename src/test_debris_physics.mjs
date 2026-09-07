import {simulateDebris,supportHeight} from './debris_physics.js';
import fs from 'node:fs';
const results=[];
for(const seed of [41,22,23,882,889,898,910]){
 const a=simulateDebris(seed,280),b=simulateDebris(seed,280);
 let max=0,min=Infinity;for(let i=0;i<a.tracks.length;i++){if(!Number.isFinite(a.tracks[i]))throw Error('Non-finite');max=Math.max(max,Math.abs(a.tracks[i]-b.tracks[i]));if(i%6===1)min=Math.min(min,a.tracks[i]);}
 if(max!==0||min<0||a.audit.floorViolations||a.audit.maxContactEnergyRatio>1.000001)throw Error('Physical invariant failure');results.push({seed,...a.audit,reproducible:max===0,minCenterHeight:min});
}
fs.writeFileSync('qa/v2/debris_physics_tests.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results));

const colliders=[{min:[5,0,-10],max:[8,6,10]},{min:[-14,0,-12],max:[-6,5,-4]}];
const col=simulateDebris(773,280,{colliders});
let centersInside=0,nonFinite=0;for(let i=0;i<280;i++)for(let f=1;f<col.frames;f++){let o=(i*col.frames+f)*6,x=col.tracks[o],y=col.tracks[o+1],z=col.tracks[o+2];if(![x,y,z].every(Number.isFinite))nonFinite++;for(const c of colliders)if(x>c.min[0]+.001&&x<c.max[0]-.001&&y>c.min[1]+.001&&y<c.max[1]-.001&&z>c.min[2]+.001&&z<c.max[2]-.001)centersInside++;}
const summary={...col.audit,centersInside,nonFinite};fs.writeFileSync('qa/v2/debris_collision_test.json',JSON.stringify(summary,null,2));console.log('COLLISION_TEST',summary);
if(centersInside||nonFinite||col.audit.settledAtEnd<280||col.audit.wallContacts===0||col.audit.roofContacts===0)throw Error('Building contact invariant failed');
