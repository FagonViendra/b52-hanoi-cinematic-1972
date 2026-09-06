import pathlib,json,time
from playwright.sync_api import sync_playwright
P=pathlib.Path.cwd();logs=[];result={}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,channel='chrome')
 context=browser.new_context(viewport={'width':1440,'height':900},device_scale_factor=1,offline=True)
 page=context.new_page()
 page.on('pageerror',lambda e:logs.append({'type':'pageerror','text':str(e)}))
 page.on('console',lambda m:logs.append({'type':m.type,'text':m.text}) if m.type in ['error','warning'] else None)
 start=time.time();page.goto((P/'index.html').as_uri(),wait_until='load')
 page.wait_for_function("window.__B52?.ready || (document.getElementById('error') && !document.getElementById('error').classList.contains('hidden'))",timeout=120000)
 result['load_seconds']=time.time()-start;result['ready']=page.evaluate('!!window.__B52?.ready');result['error']=page.locator('#errtext').inner_text()
 if result['ready']:
  result['gpu']=page.evaluate('window.__B52.gpu');result['measurements']=page.evaluate('window.__B52.measurements');page.screenshot(path=str(P/'qa/00_title.png'));result['frames']=[]
  for t,name in [(6,'01_longbien'),(31,'02_aircraft'),(42,'03_cockpit'),(50,'04_bombs'),(65,'05_haiphong'),(88,'06_bachmai'),(101,'07_bachmai_blast'),(118,'08_khamthien_before'),(128.6,'09_khamthien_blast'),(148,'10_khamthien_after'),(160,'11_huutiep'),(175,'12_wreck_close'),(188,'13_dawn'),(199,'14_detail')]:
   page.evaluate('(t)=>window.__B52.seek(t)',t);page.wait_for_timeout(200);page.screenshot(path=str(P/'qa'/f'{name}.png'));result['frames'].append(page.evaluate('window.__B52.state()'))
 else:page.screenshot(path=str(P/'qa/startup_error.png'))
 result['console']=logs;(P/'qa/pass1_smoke.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k not in ['measurements','frames']},ensure_ascii=True));browser.close()
