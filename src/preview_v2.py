import pathlib,json,time,sys
from playwright.sync_api import sync_playwright
P=pathlib.Path.cwd();Q=P/'qa/v2';Q.mkdir(exist_ok=True);logs=[];results={}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,channel='chrome');p=b.new_page(viewport={'width':1440,'height':900},offline=True);p.on('pageerror',lambda e:logs.append(str(e)));p.on('console',lambda m:logs.append(m.text) if m.type=='error' else None)
 start=time.time();p.goto((P/'index.html').as_uri());p.wait_for_function("window.__B52?.ready || !document.querySelector('#error').classList.contains('hidden')",timeout=120000);results['load_seconds']=time.time()-start;results['ready']=p.evaluate('!!window.__B52?.ready')
 if results['ready']:
  for t,name in [(6,'bridge_wide'),(20,'bridge_close'),(31,'b52_hero'),(42,'b52_cockpit'),(50,'b52_release'),(118,'street_before'),(126.55,'impact_055'),(127.0,'impact_100'),(130.3,'impact_late'),(145,'street_after'),(175,'lake')]:
   p.evaluate('(t)=>window.__B52.seek(t)',t);p.wait_for_timeout(100);p.screenshot(path=str(Q/(name+'.png')));results[name]=p.evaluate('window.__B52.state()')
 else:results['startup_error']=p.locator('#errtext').inner_text();p.screenshot(path=str(Q/'startup_error.png'))
 b.close()
results['errors']=logs;(Q/'preview1.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps({'ready':results['ready'],'load_seconds':results['load_seconds'],'errors':logs,'frames':len(results)-3}));sys.exit(0 if results['ready'] and not logs else 2)
