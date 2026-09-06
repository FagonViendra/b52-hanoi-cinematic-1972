import pathlib,json,time,statistics,sys,math
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
P=pathlib.Path.cwd();Q=P/'qa';(Q/'shots').mkdir(exist_ok=True)
def pct(xs,p):return sorted(xs)[min(len(xs)-1,int((len(xs)-1)*p))] if xs else 0
out={'segments':[],'errors':[],'viewports':{'width':1440,'height':900},'quality':'balanced'}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,channel='chrome');page=browser.new_page(viewport=out['viewports'],device_scale_factor=1,offline=True)
 page.on('pageerror',lambda e:out['errors'].append(str(e)));page.goto((P/'index.html').as_uri());page.wait_for_function('window.__B52?.ready',timeout=60000)
 out['gpu']=page.evaluate('window.__B52.gpu');shots=page.evaluate('window.__B52.shots');states=[];frames=[]
 for i,s in enumerate(shots):
  for j,t in enumerate([s['a']+.75,(s['a']+s['b'])/2,s['b']-.75]):
   page.evaluate('(t)=>window.__B52.seek(t)',t);page.wait_for_timeout(50);name=f'shot_{i+1:02d}_{j}.png';page.screenshot(path=str(Q/'shots'/name));state=page.evaluate('window.__B52.state()');state['name']=name;states.append(state)
   if j==1:frames.append((Q/'shots'/name,s['name']))
 out['camera_samples']=len(states);out['finite_camera']=all(all(math.isfinite(v) for v in s['position']) for s in states);out['min_camera_height']=min(s['position'][1] for s in states);out['frames']=states
 # A separate timed run without screenshot overhead.
 for t,label in [(4,'Long Bien'),(30,'B52 exterior'),(63,'Hai Phong'),(97,'Bach Mai impact'),(125,'Kham Thien impact'),(158,'Huu Tiep reflector'),(186,'Aftermath')]:
  page.evaluate('(t)=>window.__B52.seek(t)',t);page.evaluate('window.__B52.play(true)');page.wait_for_timeout(700);page.evaluate('window.__B52.resetSamples()');page.wait_for_timeout(4000);page.evaluate('window.__B52.play(false)');samples=page.evaluate('window.__B52.samples()');ms=[f['ms'] for f in samples];cpu=[f['cpu'] for f in samples];state=page.evaluate('window.__B52.state()')
  result={'name':label,'frames':len(ms),'fps':1000/statistics.mean(ms) if ms else 0,'median_ms':statistics.median(ms) if ms else 0,'p95_ms':pct(ms,.95),'max_ms':max(ms) if ms else 0,'over50ms':sum(x>50 for x in ms),'cpu_submit_p95_ms':pct(cpu,.95),'draw_calls':state['drawCalls'],'triangles':state['triangles']};out['segments'].append(result);print(json.dumps(result),flush=True)
 # Complete 210-second timeline at 4x, including every chapter switch.
 page.select_option('#speed','4');page.evaluate('window.__B52.seek(0);window.__B52.resetSamples();window.__B52.play(true)');start=time.perf_counter();page.wait_for_function('window.__B52.state().t>=210 && !window.__B52.state().playing',timeout=70000);out['full_film_wall_seconds']=time.perf_counter()-start;out['full_film_ended']=page.evaluate('window.__B52.state()');print('FULL_FILM_END',out['full_film_wall_seconds'],flush=True)
 browser.close()
# Contact sheet is a review aid; full-size frames are retained.
w,h=480,300;sheet=Image.new('RGB',(w*4,(h+28)*5),(17,25,31));draw=ImageDraw.Draw(sheet)
for i,(file,title) in enumerate(frames):
 im=Image.open(file).convert('RGB');im.thumbnail((w,h));x=(i%4)*w;y=(i//4)*(h+28);sheet.paste(im,(x,y));draw.text((x+10,y+h+5),f'{i+1:02d}  '+title.encode('ascii','replace').decode(),fill=(220,209,181))
sheet.save(Q/'contact_sheet_19_shots.jpg',quality=91)
(Q/'pass3_performance.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print('FRAME_REVIEW_COUNT',len(states));print('ERRORS',out['errors']);sys.exit(0 if not out['errors'] and out['finite_camera'] else 2)
