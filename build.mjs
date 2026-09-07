import {build} from 'esbuild';
import fs from 'node:fs';
await build({entryPoints:['src/app.js'],bundle:true,minify:true,format:'iife',outfile:'vendor/app.bundle.js',target:'es2020',legalComments:'inline',logLevel:'info'});
let html=fs.readFileSync('src/template.html','utf8').replace(/^\uFEFF/,'');
const values={__RECIPE__:fs.readFileSync('assets/recipe.json','utf8'),__SCRIPT__:fs.readFileSync('vendor/app.bundle.js','utf8').replace(/<\/script/gi,'<\\/script'),__REF_LONGBIEN__:'data:image/jpeg;base64,'+fs.readFileSync('references/longbien.jpg').toString('base64'),__REF_HUUTIEP__:'data:image/jpeg;base64,'+fs.readFileSync('references/huutiep.jpg').toString('base64')};
for(const[key,file]of Object.entries({__REF_B52_DROP__:'b52_drop.jpg',__REF_B52_FRONT__:'b52_front.jpg',__REF_BRIDGE_UNDER__:'bridge_under.jpg'}))values[key]='data:image/jpeg;base64,'+fs.readFileSync('references/v2/'+file).toString('base64');
for(const[k,v]of Object.entries(values))html=html.replace(k,()=>v);
fs.writeFileSync('index.html',html);fs.writeFileSync('THIRD_PARTY_LICENSES.txt','Three.js (MIT)\n\n'+fs.readFileSync('node_modules/three/LICENSE','utf8')+'\n\nReference photos: two CC BY 2.0, one CC0 1.0 and two U.S. Air Force public-domain-in-the-USA images. Full attribution and dates: HTML archive and HISTORY_V2.md. Original procedural textures are project-authored. No font files are distributed.\n');
console.log('OFFLINE_HTML_BYTES',Buffer.byteLength(html));
