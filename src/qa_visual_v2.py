import pathlib,json,time,math,sys,hashlib
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont
P=pathlib.Path.cwd();Q=P/'qa/v2/review';Q.mkdir(exist_ok=True);out={'errors':[],'frames':[],'free_views':[],'build_sha256':hashlib.sha256((P/'index.html').read_bytes()).hexdigest()}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,channel='chrome');page=b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1,offline=True);page.on('pageerror',lambda e:out['errors'].append(str(e)));page.goto((P/'index.html').as_uri());page.wait_for_function('window.__B52?.ready',timeout=60000);out['gpu']=page.evaluate('window.__B52.gpu');out['collapse']=page.evaluate('window.__B52.collapse');out['physics']=page.evaluate('window.__B52.physics')
 for i,s in enumerate(page.evaluate('window.__B52.shots')):
  for j,t in enumerate([s['a']+.7,(s['a']+s['b'])/2,s['b']-.7]):
   page.evaluate('(t)=>window.__B52.seek(t)',t);page.wait_for_timeout(60);name=f'shot_{i+1:02d}_{j}.png';page.screenshot(path=str(Q/name));state=page.evaluate('window.__B52.state()');out['frames'].append({'file':name,**state})
 # Source UI for every chapter, not just the archive landing page.
 for t,label in [(6,'bridge'),(31,'air'),(65,'port'),(101,'hospital'),(138,'street'),(175,'lake'),(193,'after')]:
  page.evaluate('(t)=>window.__B52.seek(t)',t);page.locator('#chapterhistory').click();page.screenshot(path=str(Q/('history_'+label+'.png')));page.locator('[data-close="historyDialog"]').click()
 page.evaluate("document.body.classList.add('hideui')")
 free=[(20,[-48,11,10],[-53.1,7.7,2.37],45,'bridge_bearing_web'),(20,[-43,3.5,12],[-53.1,7,0],48,'bridge_under_web'),(20,[-19,11,9],[-25.6,11.4,2.37],45,'bridge_suspended_web'),(31,[0,99,-100],[0,94,0],39,'aircraft_front_web'),(31,[0,182,0],[0,92,0],46,'aircraft_top_web'),(31,[88,96,0],[0,94,0],41,'aircraft_side_web')]
 for t,p,target,fov,name in free:
  page.evaluate('({t,p,target,fov})=>{window.__B52.seek(t);window.__B52.setCamera(p,target,fov)}',{'t':t,'p':p,'target':target,'fov':fov});page.wait_for_timeout(130);page.screenshot(path=str(Q/(name+'.png')));out['free_views'].append({'name':name,**page.evaluate('window.__B52.state()')})
 for i,t in enumerate([125.9,126.08,126.25,126.55,127.0,128.0,130.5,134,145]):
  page.evaluate('(t)=>{window.__B52.seek(t);window.__B52.setCamera([8,12,11],[-9,3.5,-23],53)}',t);page.wait_for_timeout(120);name=f'debris_{i:02d}.png';page.screenshot(path=str(Q/name));out['free_views'].append({'name':name,**page.evaluate('window.__B52.state()')})
 page.evaluate("window.__B52.setFree(false);document.body.classList.remove('hideui')");page.select_option('#speed','4');page.evaluate('window.__B52.seek(0);window.__B52.play(true)');start=time.perf_counter();page.wait_for_function('window.__B52.state().t>=210 && !window.__B52.state().playing',timeout=70000);out['full_playback_wall_seconds']=time.perf_counter()-start;out['end_state']=page.evaluate('window.__B52.state()');b.close()
try:font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
except OSError:font=ImageFont.load_default()
for typ,files,cols,w,h in [('film',[(f'shot_{i+1:02d}_1.png',f'Góc {i+1:02d}') for i in range(19)],4,480,300),('debris',[(f'debris_{i:02d}.png',f't = {t:.2f} s') for i,t in enumerate([125.9,126.08,126.25,126.55,127.0,128.0,130.5,134,145])],3,640,400)]:
 rows=math.ceil(len(files)/cols);im=Image.new('RGB',(cols*w,rows*(h+27)),(16,25,32));d=ImageDraw.Draw(im)
 for i,(name,label) in enumerate(files):
  tile=Image.open(Q/name).convert('RGB').resize((w,h),Image.Resampling.LANCZOS);x=(i%cols)*w;y=(i//cols)*(h+27);im.paste(tile,(x,y));d.text((x+12,y+h+4),label,font=font,fill=(222,210,179))
 im.save(Q/(typ+'_contact.jpg'),quality=93)
out['finite_camera']=all(all(math.isfinite(v) for v in f['position']) for f in out['frames']+out['free_views']);(P/'qa/v2/visual_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'frames':len(out['frames']),'free_views':len(out['free_views']),'full_playback_wall_seconds':out['full_playback_wall_seconds'],'finite_camera':out['finite_camera'],'errors':out['errors'],'collapse':out['collapse']}));sys.exit(0 if not out['errors'] and out['finite_camera'] else 2)
