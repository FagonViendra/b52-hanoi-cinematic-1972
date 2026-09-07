import pathlib,json,time,statistics,hashlib,sys
from playwright.sync_api import sync_playwright
P=pathlib.Path.cwd();Q=P/'qa/v2';out={'build_sha256':hashlib.sha256((P/'index.html').read_bytes()).hexdigest(),'segments':[],'errors':[]}
def percent(xs,p):return sorted(xs)[int((len(xs)-1)*p)] if xs else None
with sync_playwright() as pw:
 for headed in [False,True]:
  b=pw.chromium.launch(headless=not headed,channel='chrome');page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1,offline=True);page.on('pageerror',lambda e:out['errors'].append(str(e)));page.goto((P/'index.html').as_uri());page.wait_for_function('window.__B52?.ready',timeout=60000);out['browser']=b.version;out['gpu']=page.evaluate('window.__B52.gpu')
  page.evaluate("window.__QA={on:false,times:[],last:0};function sample(now){let q=window.__QA;if(q.on){if(q.last)q.times.push(now-q.last);q.last=now;}requestAnimationFrame(sample)}requestAnimationFrame(sample)")
  cases=[('balanced',130.3,'four_impacts_and_collapse'),('high',130.3,'four_impacts_and_collapse')] if headed else [('balanced',4,'bridge'),('balanced',29,'aircraft'),('balanced',115,'dense_street'),('balanced',130.3,'four_impacts_and_collapse'),('balanced',169,'lake_reflection'),('high',130.3,'four_impacts_and_collapse'),('low',130.3,'four_impacts_and_collapse')]
  for quality,start,label in cases:
   page.evaluate('([q,t])=>{window.__B52.setQuality(q);window.__B52.seek(t);window.__B52.play(true)}',[quality,start]);page.wait_for_timeout(1000)
   page.evaluate('window.__B52.resetSamples();window.__QA.times=[];window.__QA.last=0;window.__QA.on=true');wall=time.perf_counter();page.wait_for_timeout(5000 if headed else 4000);elapsed=time.perf_counter()-wall;data=page.evaluate('window.__QA.on=false;({raf:window.__QA.times,gpu:window.__B52.gpuTiming(),app:window.__B52.samples(),state:window.__B52.state(),resolution:[document.querySelector("canvas").width,document.querySelector("canvas").height]})');page.evaluate('window.__B52.play(false)')
   ms=data['raf'];gpu=[s['ms'] for s in data['gpu']['samples']];cpu=[s['cpu'] for s in data['app']];item={'window':'headed' if headed else 'headless','quality':quality,'scene':label,'timeline_start':start,'viewport':[1920,1080],'dpr':1,'render_resolution':data['resolution'],'wall_seconds':elapsed,'frames':len(ms),'raf_fps':1000/statistics.mean(ms),'raf_p95_ms':percent(ms,.95),'raf_max_ms':max(ms),'frames_over50ms':sum(x>50 for x in ms),'gpu_supported':data['gpu']['gpuTimerSupported'],'gpu_samples':len(gpu),'gpu_median_ms':statistics.median(gpu) if gpu else None,'gpu_p95_ms':percent(gpu,.95),'gpu_max_ms':max(gpu) if gpu else None,'cpu_submit_p95_ms':percent(cpu,.95),'state':data['state']};out['segments'].append(item);print(json.dumps({k:v for k,v in item.items() if k!='state'}),flush=True)
   if headed:
    page.evaluate('window.__B52.seek(127);document.getElementById("stats").checked=true;document.getElementById("debug").classList.remove("hidden")');page.screenshot(path=str(Q/('headed_'+quality+'_1080p.png')))
  b.close()
assert not out['errors'];assert all(not s['state']['shaderErrors'] for s in out['segments']);out['minimum_measured_fps']=min(s['raf_fps'] for s in out['segments']);(Q/'performance_final.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('MINIMUM_FPS',out['minimum_measured_fps'])
