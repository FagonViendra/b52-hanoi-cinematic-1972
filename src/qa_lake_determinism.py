import pathlib,io,base64,json
from PIL import Image,ImageChops
import numpy as np
from playwright.sync_api import sync_playwright
P=pathlib.Path.cwd();records=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,channel='chrome');page=b.new_page(viewport={'width':1440,'height':900},offline=True);page.goto((P/'index.html').as_uri());page.wait_for_function('window.__B52?.ready')
 def shot(kind):
  if kind=='canvas':return Image.open(io.BytesIO(base64.b64decode(page.evaluate("document.querySelector('canvas').toDataURL('image/png').split(',')[1]")))).convert('RGB')
  return Image.open(io.BytesIO(page.locator('#viewport').screenshot())).convert('RGB')
 for j in range(5):
  page.evaluate('window.__B52.seek(175)');page.wait_for_timeout(100);a={k:shot(k) for k in ['canvas','composited']};sa=page.evaluate('window.__B52.state()')
  page.evaluate('window.__B52.seek(99);window.__B52.seek(175)');page.wait_for_timeout(100);bb={k:shot(k) for k in ['canvas','composited']};sb=page.evaluate('window.__B52.state()')
  for k in a:
   aa=np.asarray(a[k]).astype(int);ab=np.asarray(bb[k]).astype(int);dif=np.abs(aa-ab);r={'cycle':j,'kind':k,'nonzero_pixels':int(np.any(dif,axis=2).sum()),'max_delta':int(dif.max()),'mean_delta':float(dif.mean()),'camera_equal':sa['position']==sb['position']};records.append(r)
   if r['nonzero_pixels']:
    a[k].save(P/'qa'/f'lake_before_{j}_{k}.png');bb[k].save(P/'qa'/f'lake_after_{j}_{k}.png');Image.fromarray(np.clip(dif*8,0,255).astype('uint8')).save(P/'qa'/f'lake_diff_{j}_{k}.png')
 b.close()
(P/'qa/lake_determinism_investigation.json').write_text(json.dumps(records,indent=2));print(json.dumps(records))
