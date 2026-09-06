import pathlib,subprocess,time,ctypes,json
from ctypes import wintypes
from PIL import ImageGrab
P=pathlib.Path.cwd();u=ctypes.windll.user32
subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe','--new-window',(P/'index.html').as_uri()])
time.sleep(4)
found=[]
callback=ctypes.WINFUNCTYPE(wintypes.BOOL,wintypes.HWND,wintypes.LPARAM)
@callback
def inspect(hwnd,param):
 n=u.GetWindowTextLengthW(hwnd);buf=ctypes.create_unicode_buffer(n+1);u.GetWindowTextW(hwnd,buf,n+1)
 if '1972' in buf.value and 'Chrome' in buf.value and u.IsWindowVisible(hwnd):found.append((hwnd,buf.value))
 return True
u.EnumWindows(inspect,0)
result={'opened_file':str(P/'index.html'),'matching_windows':len(found),'foreground_confirmed':False}
if found:
 hwnd,title=found[-1];u.ShowWindow(hwnd,9);result['set_foreground_result']=bool(u.SetForegroundWindow(hwnd));time.sleep(.6)
 result['foreground_confirmed']=u.GetForegroundWindow()==hwnd
 if result['foreground_confirmed']:
  rect=wintypes.RECT();u.GetWindowRect(hwnd,ctypes.byref(rect));ImageGrab.grab(bbox=(rect.left,rect.top,rect.right,rect.bottom)).save(P/'qa/final_desktop_film.png');result['screenshot']='qa/final_desktop_film.png';result['foreground_unchanged_after_capture']=u.GetForegroundWindow()==hwnd
 result['window_title']=title
(P/'qa/final_open_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=True))
