// Deterministic artist-directed debris motion. No blast yield or damage calculations.
// Metres/seconds, gravity, aerodynamic drag, dissipative contacts and settled rubble.
export function seeded(seed){return()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};}
export function supportHeight(rx,ry,rz,d){
 const a=Math.cos(rx),b=Math.sin(rx),c=Math.cos(ry),s=Math.sin(ry),e=Math.cos(rz),f=Math.sin(rz);
 return Math.abs(a*f+b*e*s)*d[0]*.5+Math.abs(a*e-b*f*s)*d[1]*.5+Math.abs(b*c)*d[2]*.5;
}
export function simulateDebris(seed,count=280,options={}){
 const random=seeded(seed),rate=30,substeps=4,dt=1/(rate*substeps),seconds=12,frames=seconds*rate+1;
 const groundY=options.groundY||0;const colliders=options.colliders||[],specs=[],tracks=new Float32Array(count*frames*6);
 let floorViolations=0,wallContacts=0,roofContacts=0,floorContacts=0,maxContactEnergyRatio=0;
 for(let i=0;i<count;i++){
  const initial=options.initial?.[i];const type=initial?.type??i%4,scale=(type===2?.7+random()*.75:.35+Math.pow(random(),1.55)*1.10)*(i<20?1.4:1);
  const base=type===2?[.16,.10,1.2]:type===1?[.54,.075,.44]:[.58,.3,.44];const dims=initial?.dims||base.map(x=>x*scale);
  const angle=random()*Math.PI*2,rr=.4+random()*3.8;let p=[Math.cos(angle)*rr,.4+random()*4.1,Math.sin(angle)*rr];
  const speed=(type===2?8:11)+random()*13;let v=[Math.cos(angle)*speed,5+random()*15,Math.sin(angle)*speed];
  let rot=[random()*6.28,random()*6.28,random()*6.28],omega=[(random()-.5)*9,(random()-.5)*9,(random()-.5)*9];
  const spawn=random()*.18,drag=type===1?.65:type===2?.40:.17,restitution=type===1?.14:type===2?.32:.23;
  if(initial){p=[...initial.position];v=[...(initial.velocity||[0,0,0])];rot=[...(initial.rotation||[0,0,0])];omega=[...(initial.omega||[0,0,0])];}
  let contacts=0,rest=false,settleStart=-1;specs.push({type,scale,spawn,dims,initialVelocity:[...v],restitution,drag});
  p[1]=Math.max(p[1],groundY+supportHeight(...rot,dims)+.03);
  function store(frame){let offset=(i*frames+frame)*6;tracks.set(p,offset);tracks.set(rot,offset+3);}
  store(0);
  for(let frame=1;frame<frames;frame++){
   for(let sub=0;sub<substeps;sub++){
    const time=(frame-1)/rate+(sub+1)*dt;if(time<spawn||rest)continue;
    let old=[...p];const damp=Math.exp(-drag*dt);v[0]*=damp;v[2]*=damp;v[1]=(v[1]-9.81*dt)*damp;
    for(let k=0;k<3;k++){p[k]+=v[k]*dt;rot[k]+=omega[k]*dt;}
    let h=supportHeight(...rot,dims);
    if(p[1]<groundY+h){
     let before=v.reduce((a,x)=>a+x*x,0);p[1]=groundY+h;
     if(v[1]<0){v[1]=-v[1]*restitution;v[0]*=.60;v[2]*=.60;omega=omega.map(x=>x*.45);contacts++;floorContacts++;}
     let after=v.reduce((a,x)=>a+x*x,0);if(before>0)maxContactEnergyRatio=Math.max(maxContactEnergyRatio,after/before);
     if(contacts>3||Math.abs(v[1])<.48){settleStart=time;v=[0,0,0];omega=[0,0,0];rot=[initial?.restRotation?.[0]||0,rot[1],initial?.restRotation?.[2]||0];p[1]=groundY+supportHeight(...rot,dims);rest=true;}
    }
    if(!rest)for(const c of colliders){
     let pad=Math.max(dims[0],dims[2])*.35;
     if(p[0]>c.min[0]-pad&&p[0]<c.max[0]+pad&&p[2]>c.min[2]-pad&&p[2]<c.max[2]+pad&&p[1]>c.min[1]&&p[1]<c.max[1]+h){
      const faces=[Math.abs(p[0]-(c.min[0]-pad)),Math.abs(p[0]-(c.max[0]+pad)),Math.abs(p[2]-(c.min[2]-pad)),Math.abs(p[2]-(c.max[2]+pad)),Math.abs(p[1]-(c.max[1]+h))];let f=faces.indexOf(Math.min(...faces));
      if(f===0){p[0]=c.min[0]-pad;v[0]=-Math.abs(v[0])*.25;}else if(f===1){p[0]=c.max[0]+pad;v[0]=Math.abs(v[0])*.25;}else if(f===2){p[2]=c.min[2]-pad;v[2]=-Math.abs(v[2])*.25;}else if(f===3){p[2]=c.max[2]+pad;v[2]=Math.abs(v[2])*.25;}else{p[1]=c.max[1]+h+.001;v[1]=Math.abs(v[1])*.2;roofContacts++;if(v[1]<.6){rot=[initial?.restRotation?.[0]||0,rot[1],initial?.restRotation?.[2]||0];p[1]=c.max[1]+supportHeight(...rot,dims)+.001;v=[0,0,0];omega=[0,0,0];rest=true;settleStart=time;}}
      omega=omega.map(x=>x*.65);wallContacts++;
     }
    }
    if(p[1]<groundY-.001)floorViolations++;
   }
   store(frame);
  }
  specs[i].settled=rest;specs[i].settleTime=settleStart;
 }
 return{specs,tracks,count,frames,rate,seconds,audit:{gravity:9.81,integrationHz:rate*substeps,samplingHz:rate,fragmentCount:count,floorContacts,wallContacts,roofContacts,floorViolations,maxContactEnergyRatio,settledAtEnd:specs.filter(s=>s.settled).length}};
}
