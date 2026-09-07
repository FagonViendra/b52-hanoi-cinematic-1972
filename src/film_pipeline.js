import {DataTexture,RedFormat,FloatType,RepeatWrapping} from 'three';
import {seeded} from './debris_physics.js';
import {SMAAPass} from 'three/addons/postprocessing/SMAAPass.js';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {SSAOPass} from 'three/addons/postprocessing/SSAOPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
export class FilmPipeline{
 constructor(renderer,scene,camera){
  this.renderer=renderer;this.scene=scene;this.camera=camera;this.quality='balanced';
  this.composer=new EffectComposer(renderer);this.renderPass=new RenderPass(scene,camera);this.ao=new SSAOPass(scene,camera,innerWidth,innerHeight,16);
  const rng=seeded(19721218);this.ao.kernel.forEach((v,i)=>v.set(rng()*2-1,rng()*2-1,rng()).normalize().multiplyScalar(.1+.9*(i/16)**2));
  this.ao.noiseTexture.dispose();const noise=new DataTexture(new Float32Array(Array.from({length:16},()=>rng()*2-1)),4,4,RedFormat,FloatType);noise.wrapS=noise.wrapT=RepeatWrapping;noise.needsUpdate=true;this.ao.noiseTexture=noise;this.ao.ssaoMaterial.uniforms.tNoise.value=noise;
  const baseOverride=this.ao._overrideVisibility.bind(this.ao);
  this.ao._overrideVisibility=()=>{baseOverride();this.scene.traverse(o=>{if(!o.visible||!o.isMesh)return;const mats=Array.isArray(o.material)?o.material:[o.material];if(mats.some(m=>m?.transparent)){o.visible=false;this.ao._visibilityCache.push(o);}});};
  this.ao.kernelRadius=.75;this.ao.minDistance=.00001;this.ao.maxDistance=.0035;
  this.composer.addPass(this.renderPass);this.composer.addPass(this.ao);this.smaa=new SMAAPass();this.composer.addPass(this.smaa);this.composer.addPass(new OutputPass());
  this.gl=renderer.getContext();this.ext=this.gl.getExtension('EXT_disjoint_timer_query_webgl2');this.pending=[];this.samples=[];this.frame=0;
 }
 resize(w,h){this.composer.setPixelRatio(this.renderer.getPixelRatio());this.composer.setSize(w,h);}
 setQuality(q){this.quality=q;}
 render(location,t){
  const gl=this.gl,ext=this.ext;
  if(ext){const disjoint=gl.getParameter(ext.GPU_DISJOINT_EXT);this.pending=this.pending.filter(p=>{if(!gl.getQueryParameter(p.query,gl.QUERY_RESULT_AVAILABLE))return true;if(!disjoint){this.samples.push({ms:gl.getQueryParameter(p.query,gl.QUERY_RESULT)/1e6,location:p.location,t:p.t});if(this.samples.length>900)this.samples.shift();}gl.deleteQuery(p.query);return false;});}
  let query=null;if(ext&&this.pending.length<5&&(this.frame++%10===0)){query=gl.createQuery();gl.beginQuery(ext.TIME_ELAPSED_EXT,query);}
  if(this.quality==='low'){this.renderer.render(this.scene,this.camera);}else{this.ao.enabled=location!=='air';this.renderPass.enabled=true;this.composer.render();}
  if(query){gl.endQuery(ext.TIME_ELAPSED_EXT);this.pending.push({query,location,t});}
 }
 resetTiming(){this.samples=[];for(const q of this.pending)this.gl.deleteQuery(q.query);this.pending=[];}
 info(){return{gpuTimerSupported:!!this.ext,samples:this.samples.slice(),postprocessing:this.quality==='low'?'none':'SSAO16 + SMAA + output',pendingQueries:this.pending.length};}
}
