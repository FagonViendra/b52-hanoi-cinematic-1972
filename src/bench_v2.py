import pathlib,json,time,statistics
from playwright.sync_api import sync_playwright
P=pathlib.Path.cwd();report={'segments':[],'errors':[]}
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,channel='chrome');page=b.new_page(viewport={'width':1440,'height':900},offline=True);page.on('pageerror',lambda e:report['errors'].append(str(e)));page.goto((P/'index.html').as_uri());page.wait_for_function('window.__B52?.ready',timeout=60000)
 report['gpu']=page.evaluate('window.__B52.gpu');report['layout']=page.evaluate('window.__B52.layout');report['physics']=page.evaluate('window.__B52.physics')
 for q,t,label in [('balanced',4,'bridge'),('balanced',29,'air'),('balanced',124.2,'impact'),('balanced',169,'lake'),('high',124.2,'impact_high'),('low',124.2,'impact_low')]:
  page.evaluate('([q,t])=>{window.__B52.setQuality(q);window.__B52.seek(t);window.__B52.play(true)}',[q,t]);page.wait_for_timeout(700);page.evaluate('window.__B52.resetSamples()');page.wait_for_timeout(3000);page.evaluate('window.__B52.play(false)');ss=page.evaluate('window.__B52.samples()');gg=page.evaluate('window.__B52.gpuTiming()');ms=[s['ms'] for s in ss if s['ms']<1000];gpu=[s['ms'] for s in gg['samples'] if t+.7<=s['t']<=t+3.8];item={'quality':q,'scene':label,'raf_fps':1000/statistics.mean(ms),'raf_p95_ms':sorted(ms)[int(.95*(len(ms)-1))],'gpu_supported':gg['gpuTimerSupported'],'gpu_samples':len(gpu),'gpu_median_ms':statistics.median(gpu) if gpu else None,'gpu_p95_ms':sorted(gpu)[int(.95*(len(gpu)-1))] if gpu else None,'state':page.evaluate('window.__B52.state()')};report['segments'].append(item);print(json.dumps(item),flush=True)
 b.close()
(P/'qa/v2/perf_initial.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
