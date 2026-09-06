import * as THREE from 'three';
import {V} from './geometry.js';
export const DURATION=210;
export const chapters=[
 {start:0,end:26,id:'bridge',short:'Long Biên',date:'HÀ NỘI · KHÔNG GIAN MỞ ĐẦU',title:'Sông Hồng · Cầu Long Biên',text:'Thành phố bên dòng sông. Đoạn cầu rút gọn dùng để định vị không gian, không mô tả một trận đánh xác định.'},
 {start:26,end:58,id:'air',short:'Trên mây',date:'MIỀN BẮC · THÁNG 12 / 1972',title:'B-52D · Trên tầng mây',text:'Tám động cơ, bốn cụm đôi. Ngoại cảnh diễn giải; đội hình, thời gian và độ cao trong cảnh thả bom đã được nén.'},
 {start:58,end:82,id:'port',short:'Hải Phòng',date:'HẢI PHÒNG · KHÔNG GIAN CẢNG',title:'Bờ sông Cấm',text:'Kho gạch, cần cẩu giàn và tàu sông. Cảnh cảng được dàn dựng, không phải sơ đồ một bến hoặc một phi vụ cụ thể.'},
 {start:82,end:112,id:'hospital',short:'Bạch Mai',date:'HÀ NỘI · RẠNG SÁNG 22 / 12 / 1972',title:'Bệnh viện Bạch Mai',text:'Một địa điểm dân sự bị tàn phá. Ngày sự kiện có đối chiếu tư liệu; hình học công trình và nhịp nổ là diễn giải.'},
 {start:112,end:154,id:'street',short:'Khâm Thiên',date:'HÀ NỘI · ĐÊM 26 / 12 / 1972',title:'Phố Khâm Thiên',text:'Từ những mái ngói đến những căn nhà đổ nát. Không mô phỏng thương tích trực diện, không gán danh tính cho từng ngôi nhà.'},
 {start:154,end:182,id:'lake',short:'Hữu Tiệp',date:'NGỌC HÀ, HÀ NỘI · 27 / 12 / 1972',title:'Hồ Hữu Tiệp',text:'Mảnh xác máy bay giữa mặt hồ. Phục dựng chỉ một phần kết cấu; không đưa công trình bảo tồn hiện đại vào năm 1972.'},
 {start:182,end:210,id:'after',short:'Sau đêm bom',date:'KHÂM THIÊN · CẢNH SUY TƯỞNG',title:'Sau những đêm bom',text:'Ngày tháng có thể ghi lại. Mất mát không chỉ là những con số. Ánh sáng bình minh trong cảnh được dàn dựng.'}
];
const S=(a,b,id,name,p0,p1,p2,q0,q1,fov=46)=>({a,b,id,name,path:new THREE.CatmullRomCurve3([V(p0),V(p1),V(p2)],false,'centripetal'),q0:V(q0),q1:V(q1),fov});
export const shots=[
 S(0,14,'bridge','TOÀN CẢNH SÔNG HỒNG',[-135,31,164],[-111,27,142],[-88,23,120],[0,10,0],[12,10,0],46),
 S(14,26,'bridge','TRƯỢT DỌC KẾT CẤU THÉP',[118,12,23],[91,11,20],[62,10.6,18],[20,11,0],[-25,11,0],43),
 S(26,38,'air','NGOẠI CẢNH MÁY BAY',[73,118,-80],[62,112,-70],[53,108,-62],[0,93,0],[0,93,-1],43),
 S(38,46,'air','TIẾN GẦN BUỒNG LÁI',[-27,103,-45],[-22,100,-38],[-18,99,-33],[0,94,-14],[0,94,-16],43),
 S(46,58,'air','DƯỚI BỤNG MÁY BAY · THỜI GIAN NÉN',[42,58,48],[37,55,39],[32,52,30],[0,85,1],[0,82,0],57),
 S(58,70,'port','TOÀN CẢNH BẾN SÔNG',[83,26,110],[72,23,90],[61,21,72],[-30,7,-17],[-29,7,-30],47),
 S(70,82,'port','DỌC MÉP CẦU CẢNG',[39,7,68],[34,7,48],[31,7,29],[-29,7,-48],[-32,8,-58],48),
 S(82,94,'hospital','MẶT TIỀN BỆNH VIỆN',[13,5.7,48],[8,5.1,42],[3,4.7,36],[0,5.1,0],[0,5.2,0],47),
 S(94,103,'hospital','SÂN BỆNH VIỆN',[-26,6.2,37],[-23,5.4,33],[-20,5.0,29],[14,5,-4],[20,6,-5],47),
 S(103,112,'hospital','NHÌN LẠI TỪ TRÊN CAO',[52,28,51],[48,31,47],[43,34,42],[4,3,-7],[5,3,-9],47),
 S(112,124,'street','PHỐ TRƯỚC TRẬN BOM',[0,2.7,68],[.3,2.9,58],[.5,3.2,48],[0,4,-20],[0,4,-31],50),
 S(124,132,'street','QUA NHỮNG MÁI NGÓI',[36,26,38],[32,25,32],[28,24,26],[0,3,-10],[0,3,-15],51),
 S(132,143,'street','BỤI TRONG LÒNG PHỐ',[0,4,76],[.3,3.8,66],[.6,3.7,57],[-1,5,-12],[-1,5,-22],50),
 S(143,154,'street','DẤU VẾT SAU VỤ NỔ',[-40,26,40],[-33,24,29],[-27,21,18],[0,3,-7],[0,3,-17],51),
 S(154,168,'lake','MẶT HỒ VÀ KHU DÂN CƯ',[39,19,35],[34,16,31],[28,12,28],[0,2,0],[-1,2,1],47),
 S(168,182,'lake','MẢNH XÁC · PHẢN CHIẾU',[12,4.8,14],[6,4,16],[-3,3.7,16],[-1,1.8,1],[-1,1.8,1],47),
 S(182,194,'after','BÌNH MINH ĐƯỢC DÀN DỰNG',[1,14,70],[-1,12,60],[-3,10,50],[0,2,-15],[0,2,-22],49),
 S(194,204,'after','NHỮNG VẬT CÒN LẠI',[3.8,2.3,33],[3.1,2.0,28],[2.6,1.8,23],[-9,1,21],[-10,1,16],46),
 S(204,210,'after','ĐỂ KHÔNG QUÊN',[35,33,68],[37,36,70],[39,40,72],[0,2,-20],[0,2,-24],49)
];
shots.forEach(s=>s.path.updateArcLengths());
export function chapterAt(t){return chapters.find(c=>t>=c.start&&t<c.end)||chapters.at(-1);}
export function shotAt(t){return shots.find(s=>t>=s.a&&t<s.b)||shots.at(-1);}
export function filmCamera(camera,t,gentle=false){let s=shotAt(t),u=THREE.MathUtils.clamp((t-s.a)/(s.b-s.a),0,1),v=u*u*(3-2*u),target=s.q0.clone().lerp(s.q1,v);camera.position.copy(s.path.getPointAt(v));if(camera.aspect<1.2){camera.position.sub(target).multiplyScalar(Math.min(2.9,1.2/camera.aspect)).add(target);}if(!gentle){let shake=0;for(let a of[98,100.5,126,127.1,128.4,130]){let age=t-a;if(age>=0&&age<1.8)shake+=Math.exp(-age*3.7)*.075;}camera.position.x+=Math.sin(t*53)*shake;camera.position.y+=Math.sin(t*61)*shake*.6;}camera.up.set(0,1,0);camera.lookAt(target);if(camera.fov!==s.fov){camera.fov=s.fov;camera.updateProjectionMatrix();}return{target,shot:s,index:shots.indexOf(s),u};}
export class Soundscape{
 constructor(){this.ctx=null;this.enabled=false;}
 async toggle(){
  if(!this.ctx){const C=window.AudioContext||window.webkitAudioContext;if(!C)throw Error('Trình duyệt không hỗ trợ Web Audio.');this.ctx=new C();let ctx=this.ctx,compressor=ctx.createDynamicsCompressor();compressor.threshold.value=-15;compressor.ratio.value=8;compressor.connect(ctx.destination);this.master=ctx.createGain();this.master.gain.value=.45;this.master.connect(compressor);const buf=ctx.createBuffer(1,ctx.sampleRate*4,ctx.sampleRate),v=buf.getChannelData(0);let z=0,s=17;for(let i=0;i<v.length;i++){s=(Math.imul(s,1664525)+1013904223)>>>0;z=.97*z+.03*(s/2147483648-1);v[i]=z*4;}let src=ctx.createBufferSource();src.buffer=buf;src.loop=true;let filter=ctx.createBiquadFilter();filter.type='lowpass';filter.frequency.value=1100;this.noise=ctx.createGain();this.noise.gain.value=0;src.connect(filter).connect(this.noise).connect(this.master);src.start();this.engine=ctx.createGain();this.engine.gain.value=0;this.engine.connect(this.master);for(let freq of[42,79]){let o=ctx.createOscillator();o.type='triangle';o.frequency.value=freq;o.connect(this.engine);o.start();}this.siren=ctx.createOscillator();this.siren.type='sine';this.sg=ctx.createGain();this.sg.gain.value=0;this.siren.connect(this.sg).connect(this.master);this.siren.start();}
  this.enabled=!this.enabled;if(this.enabled)await this.ctx.resume();return this.enabled;
 }
 update(t,id,playing,gentle){if(!this.ctx)return;let active=this.enabled&&playing,ct=this.ctx.currentTime,boom=0;for(let a of(id==='hospital'?[98,100.5]:id==='street'?[126,127.1,128.4,130]:id==='port'?[73.5]:[])){let d=t-a;if(d>=0&&d<3)boom+=Math.exp(-d*2.4)*.55;}this.noise.gain.setTargetAtTime(active?(.02+boom*(gentle?.35:1)):0,ct,.08);this.engine.gain.setTargetAtTime(active&&id==='air'?.035:0,ct,.1);this.sg.gain.setTargetAtTime(active&&id==='street'&&t<125?.018:0,ct,.1);this.siren.frequency.setTargetAtTime(480+Math.sin(t*.8)*175,ct,.12);}
}
