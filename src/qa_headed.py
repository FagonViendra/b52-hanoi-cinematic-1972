import pathlib,json,time,statistics
from playwright.sync_api import sync_playwright
from PIL import ImageGrab
P=pathlib.Path.cwd();out={'errors':[],'samples':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=False,channel='chrome');page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1,offline=True);out['browser']=browser.version
 page.on('pageerror',lambda e:out['errors'].append(str(e)));page.goto((P/'index.html').as_uri());page.wait_for_function('window.__B52?.ready',timeout=60000);page.bring_to_front();page.evaluate('window.__B52.seek(125);window.__B52.play(true)');page.wait_for_timeout(1000);page.evaluate('window.__B52.resetSamples()');page.wait_for_timeout(8000);page.evaluate('window.__B52.play(false)');ms=[x['ms'] for x in page.evaluate('window.__B52.samples()')];out.update({'frames':len(ms),'fps':1000/statistics.mean(ms),'p95_ms':sorted(ms)[int(len(ms)*.95)],'max_ms':max(ms),'gpu':page.evaluate('window.__B52.gpu'),'state':page.evaluate('window.__B52.state()')})
 page.evaluate('window.__B52.seek(175)');page.wait_for_timeout(350);page.screenshot(path=str(P/'qa/headed_chrome.png'));ImageGrab.grab().save(P/'qa/desktop_verification.png');out['desktop_foreground_validated']=False;browser.close()
(P/'qa/pass4_headed.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out))
