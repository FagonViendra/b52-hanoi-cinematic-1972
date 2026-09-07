import pathlib,subprocess,time,ctypes,json,hashlib
from ctypes import wintypes
from PIL import ImageGrab
P=pathlib.Path(__file__).resolve().parents[1];u=ctypes.windll.user32
u.GetForegroundWindow.restype=wintypes.HWND;u.GetWindowRect.argtypes=[wintypes.HWND,ctypes.POINTER(wintypes.RECT)];u.SetForegroundWindow.argtypes=[wintypes.HWND];u.ShowWindow.argtypes=[wintypes.HWND,ctypes.c_int]
callback=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
def find():
 windows=[]
 @callback
 def each(hwnd,param):
  n=u.GetWindowTextLengthW(hwnd);text=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,text,n+1)
  if '1972' in text.value and u.IsWindowVisible(hwnd):windows.append((hwnd,text.value))
  return True
 u.EnumWindows(each,0);return windows
before={h for h,t in find()};url=(P/'index.html').as_uri()+'?build=v2'
subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe','--new-window',url]);time.sleep(7)
after=find();new=[x for x in after if x[0] not in before];assert new,'No new project window identified; do not capture another application.'
hwnd,title=new[-1];u.ShowWindow(hwnd,3);u.SetForegroundWindow(hwnd);time.sleep(.8);assert u.GetForegroundWindow()==hwnd,'Project did not retain foreground'
r=wintypes.RECT();u.GetWindowRect(hwnd,ctypes.byref(r));box=(max(0,r.left),max(0,r.top),min(u.GetSystemMetrics(0),r.right),min(u.GetSystemMetrics(1),r.bottom));ImageGrab.grab(bbox=box).save(P/'qa/v2/final_project_window.png')
result={'version':'2.0.0','html_sha256':hashlib.sha256((P/'index.html').read_bytes()).hexdigest(),'new_window_identified':True,'foreground_confirmed':u.GetForegroundWindow()==hwnd,'window_title':title,'capture_scope':'only maximized project window, not other desktop apps','rectangle':box,'opened_url':url}
(P/'qa/v2/final_open.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=True))
