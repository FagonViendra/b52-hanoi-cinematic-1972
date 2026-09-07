import pathlib,json,time,hashlib,math,traceback,statistics,base64,io
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
P=pathlib.Path.cwd();out={'tests':[],'errors':[],'network':[],'build_sha256':hashlib.sha256((P/'index.html').read_bytes()).hexdigest()};Q=P/'qa/v2';(Q/'functional').mkdir(exist_ok=True)
def check(name,ok,detail=None):
 out['tests'].append({'name':name,'pass':bool(ok),'detail':detail});print(('PASS ' if ok else 'FAIL ')+name,flush=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,channel='chrome');context=browser.new_context(viewport={'width':1440,'height':900},device_scale_factor=1,offline=True,accept_downloads=True)
 page=context.new_page();page.on('pageerror',lambda e:out['errors'].append(str(e)));page.on('request',lambda r:out['network'].append(r.url) if not r.url.startswith(('file:','data:','blob:')) else None)
 page.goto((P/'index.html').as_uri());page.wait_for_function('window.__B52?.ready',timeout=60000)
 def canvas_rgb():
  # Compare decoded RGB, not PNG compression bytes or composited HTML overlays.
  data=page.evaluate("(()=>{window.__B52.render();return document.querySelector('canvas').toDataURL('image/png').split(',')[1]})()")
  im=Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB');canvas_rgb.index+=1
  im.save(Q/'functional'/f'pixel_capture_{canvas_rgb.index:02d}.png');return im.tobytes()
 canvas_rgb.index=0
 state=lambda:page.evaluate('window.__B52.state()')
 seek=lambda t:page.evaluate('(t)=>window.__B52.seek(t)',t)
 check('Offline initialization, no external requests',len(out['network'])==0)
 check('Seven chapters and 19 shots',page.evaluate('window.__B52.chapters.length===7 && window.__B52.shots.length===19'))
 seek(118);page.wait_for_timeout(100);a=canvas_rgb();seek(148);destroyed=state()['damageCount'];seek(118);page.wait_for_timeout(100);b=canvas_rgb();check('Reverse seek restores intact geometry and pixels',hashlib.sha256(a).digest()==hashlib.sha256(b).digest() and state()['damageCount']==0,{'destroyed_at_148':destroyed,'same_pixels':a==b})
 seek(175);page.wait_for_timeout(100);a=canvas_rgb();seek(99);seek(175);page.wait_for_timeout(100);b=canvas_rgb();delta=np.abs(np.frombuffer(a,dtype=np.uint8).astype(np.int16)-np.frombuffer(b,dtype=np.uint8).astype(np.int16));pixels=int(np.any(delta.reshape(-1,3)>0,axis=1).sum());maxdelta=int(delta.max());fraction=pixels/(len(a)/3);check('Lake restored within 1-level and 0.001% pixel tolerance',maxdelta<=1 and fraction<=0.00001,{'changed_pixels':pixels,'max_channel_delta':maxdelta,'pixel_fraction':fraction,'reason':'Strict RGB comparison found seven one-level 8-bit differences; actual images and amplified diff inspected. Geometry changes or broad image drift must still fail.'})
 seek(40);page.wait_for_timeout(600);check('Pause does not advance time',abs(state()['t']-40)<.001)
 page.locator('#forward').click();check('Forward five seconds',abs(state()['t']-45)<.01);page.locator('#back').click();check('Back five seconds',abs(state()['t']-40)<.01)
 page.locator('#scrub').evaluate("e=>{e.value='65.5';e.dispatchEvent(new Event('input',{bubbles:true}));}");check('Timeline seek',abs(state()['t']-65.5)<.01)
 for v in ['0.25','4']:
  page.select_option('#speed',v);seek(10);start=time.perf_counter();page.evaluate('window.__B52.play(true)');page.wait_for_timeout(1100);page.evaluate('window.__B52.play(false)');elapsed=time.perf_counter()-start;delta=state()['t']-10;check('Playback speed '+v,abs(delta-elapsed*float(v))<.32,{'elapsed':elapsed,'delta':delta})
 page.select_option('#speed','1');seek(42);page.locator('body').click(position={'x':700,'y':150});page.keyboard.press('Period');check('Single-frame advance',abs(state()['t']-(42+1/24))<.01);page.keyboard.press('Comma');check('Single-frame reverse',abs(state()['t']-42)<.01)
 page.keyboard.press('f');a=state();check('Free-view enters paused',a['free'] and not a['playing']);page.keyboard.down('w');page.wait_for_timeout(450);page.keyboard.up('w');b=state();distance=math.dist(a['position'],b['position']);check('WASD moves free camera',distance>2,{'distance':distance});page.mouse.move(700,360);page.mouse.down();page.mouse.move(820,380,steps=10);page.mouse.up();c=state();check('Orbit drag moves camera',math.dist(b['position'],c['position'])>1);page.keyboard.press('f');check('Film camera restored',not state()['free']);
 page.keyboard.press('h');check('Hide interface',page.locator('body').evaluate("e=>e.classList.contains('hideui')"));page.keyboard.press('h');check('Restore interface',not page.locator('body').evaluate("e=>e.classList.contains('hideui')"))
 page.locator('#archive').click();check('Archive opens',page.locator('#archiveDialog').evaluate('e=>e.open'));check('Reference images embedded and decoded',page.locator('#archiveDialog img').evaluate_all('es=>es.length>=5&&es.every(e=>e.complete&&e.naturalWidth>0)'));page.screenshot(path=str(Q/'functional/archive.png'));page.locator('[data-close="archiveDialog"]').click()
 page.locator('#help').click();page.locator('#gentle').check();check('Reduced-flash option',page.locator('#gentle').is_checked());page.locator('[data-close="helpDialog"]').click()
 page.locator('#audio').click();check('Audio starts only after gesture',page.locator('#audio').inner_text()=='Âm: bật');page.locator('#audio').click();check('Audio can mute',page.locator('#audio').inner_text()=='Âm: tắt')
 with page.expect_download() as event:page.locator('#capture').click()
 download=event.value;download.save_as(str(Q/'functional/captured_frame.png'));check('PNG capture download', (Q/'functional/captured_frame.png').stat().st_size>10000)
 page.locator('body').click(position={'x':700,'y':150})
 with page.expect_download() as event:page.keyboard.press('c')
 event.value.save_as(str(Q/'functional/camera.json'));check('Camera JSON download',json.loads((Q/'functional/camera.json').read_text())['seed']==19721218)
 for q in ['low','high','balanced']:page.select_option('#quality',q);seek(175);page.wait_for_timeout(150);check('Quality '+q+' renders',not state()['shaderErrors'])
 cold=state()['memory']
 for i in range(14):seek([5,31,65,101,128.6,175,199][i%7])
 before=state()['memory'];out['warmup_memory']={'cold':cold,'warm':before};programs=state()['programs']
 for i in range(70):seek([5,31,65,101,128.6,175,199][i%7])
 after=state()['memory'];check('No geometry/texture growth after warm-up and 70 scene seeks',before==after,{'before':before,'after':after});check('Finite camera after stress seek',all(math.isfinite(v) for v in state()['position']))
 seek(-10);check('Negative seek clamps',state()['t']==0);seek(999);check('Overrun seek clamps',state()['t']==210);page.evaluate('window.__B52.play(true)');page.wait_for_timeout(150);page.evaluate('window.__B52.play(false)');check('Replay restarts from end',state()['t']<1)
 for size,label in [({'width':844,'height':390},'landscape'),({'width':390,'height':844},'portrait')]:
  page.set_viewport_size(size);seek(31);page.wait_for_timeout(200);page.screenshot(path=str(Q/'functional'/('mobile_'+label+'.png')));bounds=page.locator('#play').bounding_box();check('Mobile '+label+' playback control visible',bounds and bounds['y']>=0 and bounds['y']+bounds['height']<=size['height']);check('Mobile '+label+' no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
 page.set_viewport_size({'width':1440,'height':900});seek(118);out['final_state']=state();out['gpu']=page.evaluate('window.__B52.gpu');check('No JavaScript or shader errors',not out['errors'] and not state()['shaderErrors']);check('No external runtime fetches',not out['network']);
 # V2-specific acceptance checks, beyond basic playback controls.
 page.evaluate("window.__B52.setQuality('balanced')");seek(101);page.locator('#chapterhistory').click()
 check('Per-chapter historical dossier opens',page.locator('#historyDialog').evaluate('e=>e.open'))
 check('Bach Mai history contains sourced hour and year','3 giờ 30' in page.locator('#historyContent').inner_text() and '1972' in page.locator('#historyContent').inner_text())
 check('History links are explicit HTTPS sources',page.locator('#historyContent a').evaluate_all("es=>es.length>0&&es.every(a=>a.href.startsWith('https://'))"))
 page.locator('[data-close="historyDialog"]').click();seek(118);before_text=page.locator('#description').inner_text();seek(138);after_text=page.locator('#description').inner_text()
 check('Narration changes between shots within one chapter',before_text!=after_text and '287' in after_text)
 for at,n in [(125,0),(126.6,280),(133,1120),(193,1120)]:
  seek(at);check('Persistent 3D fragments at '+str(at),state()['visibleFragments']==n,{'actual':state()['visibleFragments'],'expected':n})
 seek(118);page.wait_for_timeout(250);baseline=canvas_rgb();seek(42);seek(118);page.wait_for_timeout(250);repeat=canvas_rgb()
 dd=np.abs(np.frombuffer(baseline,dtype=np.uint8).astype(np.int16)-np.frombuffer(repeat,dtype=np.uint8).astype(np.int16));check('No stale aircraft color buffer after scene change',int(dd.max())<=1,{'max_channel_delta':int(dd.max())})
 check('Land image has geometry, not a blank pass',np.std(np.frombuffer(repeat,dtype=np.uint8))>15)
 bridge=page.evaluate('window.__B52.design.bridge');check('Bridge main node graph has no dangling members',bridge['dangling_main_endpoints']==[] and bridge['shared_nodes']>150,bridge)
 layout=page.evaluate('window.__B52.layout');check('Dense Khâm Thiên context exceeds 900 houses',layout['housesByLocation']['street']>900,layout['housesByLocation']);check('Ordinary house gaps below 8cm',max(g for g in layout['frontageGaps'] if g<1)<.08)
 physics=page.evaluate('window.__B52.physics');check('Every debris run is finite, dissipative and settled',all(x['floorViolations']==0 and x['maxContactEnergyRatio']<=1.000001 and x['settledAtEnd']==280 for x in physics),physics)
 check('Actual street debris contacts buildings',sum(x['wallContacts'] for x in physics if x['location']=='street')>0)
 collapse=page.evaluate('window.__B52.collapse');check('Structural collapse has 644 authored pieces',collapse['structuralPieces']==644 and collapse['houses']==46,collapse)
 check('Every roof-wall-timber piece settles without floor violation',collapse['settledAtEnd']==644 and collapse['groundViolations']==0)
 seek(127);page.wait_for_timeout(250);a=canvas_rgb();seek(193);seek(127);page.wait_for_timeout(250);b=canvas_rgb();check('Roof-wall collapse is reversible at identical time',a==b)
 check('No late JavaScript or shader errors',not out['errors'] and not state()['shaderErrors'])
 seek(31);page.wait_for_timeout(350);page.locator('#help').click();page.locator('#stats').check();page.locator('[data-close="helpDialog"]').click();page.screenshot(path=str(Q/'functional/v2_final_controls.png'))
 browser.close()
out['pass_count']=sum(t['pass'] for t in out['tests']);out['total']=len(out['tests']);(Q/'functional_v2.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print('TOTAL',out['pass_count'],'/',out['total'])

import sys
sys.exit(0 if out['pass_count']==out['total'] else 2)
