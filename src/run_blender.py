import pathlib,subprocess,sys,os,shutil
p=pathlib.Path(__file__).resolve().parents[1]
blender=os.environ.get('BLENDER_EXE') or shutil.which('blender') or r'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe'
if not pathlib.Path(blender).is_file():raise SystemExit('Set BLENDER_EXE to the Blender executable.')
(p/'qa').mkdir(exist_ok=True)
with (p/'qa/blender_refined.log').open('w',encoding='utf-8') as log:
 for file in ['build_assets.py','render_assets.py']:
  args=[blender,'--background','--python-exit-code','2','--python',str(p/'src'/file)]
  if file=='build_assets.py':args+=['--','--out',str(p)]
  r=subprocess.run(args,cwd=p,stdout=log,stderr=subprocess.STDOUT)
  if r.returncode:print('BLENDER_FAILED',file,'see qa/blender_refined.log');sys.exit(r.returncode)
print('REFINED_BLENDER_AND_SIX_RENDERS_COMPLETE')
