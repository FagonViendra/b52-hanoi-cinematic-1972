import {build} from 'esbuild';
import fs from 'node:fs';
await build({entryPoints:['src/app.js'],bundle:true,minify:true,format:'iife',outfile:'vendor/app.bundle.js',target:'es2020',legalComments:'inline',logLevel:'info'});
let html=fs.readFileSync('src/template.html','utf8').replace(/^\uFEFF/,'');
const values={__RECIPE__:fs.readFileSync('assets/recipe.json','utf8'),__SCRIPT__:fs.readFileSync('vendor/app.bundle.js','utf8').replace(/<\/script/gi,'<\\/script'),__REF_LONGBIEN__:'data:image/jpeg;base64,'+fs.readFileSync('references/longbien.jpg').toString('base64'),__REF_HUUTIEP__:'data:image/jpeg;base64,'+fs.readFileSync('references/huutiep.jpg').toString('base64')};
for(const[k,v]of Object.entries(values))html=html.replace(k,()=>v);
fs.writeFileSync('index.html',html);fs.writeFileSync('THIRD_PARTY_LICENSES.txt','Three.js (MIT)\n\n'+fs.readFileSync('node_modules/three/LICENSE','utf8')+'\n\nReference photos: CC BY 2.0. Full attribution in the HTML archive and HISTORY_SOURCES.md.\n');
console.log('OFFLINE_HTML_BYTES',Buffer.byteLength(html));
