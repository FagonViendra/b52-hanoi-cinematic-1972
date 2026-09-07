"""Audit the exact tested HTML and build local-only v2 release packages."""
import pathlib,json,hashlib,subprocess,zipfile,argparse
P=pathlib.Path(__file__).resolve().parents[1];Q=P/'qa/v2'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name):return json.loads((Q/name).read_text(encoding='utf-8'))
args=argparse.ArgumentParser();args.add_argument('--package',action='store_true');opt=args.parse_args()
sha=digest(P/'index.html');f1=load('functional_repeat1.json');f2=load('functional_repeat2.json');visual=load('visual_review.json');perf=load('performance_final.json')
for d in [f1,f2,visual,perf]:assert d['build_sha256']==sha,'Evidence does not match the delivered HTML'
for f in [f1,f2]:assert f['pass_count']==f['total']==58 and not f['errors'] and not f['network']
assert visual['finite_camera'] and not visual['errors'] and visual['end_state']['t']==210 and len(visual['frames'])==57
assert visual['collapse']=={'houses':46,'structuralPieces':644,'settledAtEnd':644,'groundViolations':0}
assert not perf['errors'] and all(not x['state']['shaderErrors'] for x in perf['segments'])
audit=json.loads((P/'assets/v2_design_audit.json').read_text(encoding='utf-8'));assert not audit['bridge']['dangling_main_endpoints']
subprocess.run(['node','build.mjs'],cwd=P,check=True);assert digest(P/'index.html')==sha,'Rebuilding changed the tested HTML'
(Q/'reproducibility.json').write_text(json.dumps({'html_sha256':sha,'byte_identical_rebundle':True,'functional_reports_matched':2,'visual_report_matched':True,'performance_report_matched':True},indent=2),encoding='utf-8')
bm=json.loads((P/'assets/blender_measurements.json').read_text(encoding='utf-8'));dims=bm['assets']['b52']['dimensions']
labels={'bridge':'Cầu Long Biên','aircraft':'B-52D','dense_street':'Phố đông nhà','four_impacts_and_collapse':'Bốn vụ nổ + mảnh + sập nhà','lake_reflection':'Hồ có phản chiếu'}
qualities={'balanced':'Cân bằng','high':'Cao','low':'Nhẹ'}
rows=[]
for x in perf['segments']:
 rows.append(f"| {x['window']} | {qualities[x['quality']]} | {labels[x['scene']]} | {x['render_resolution'][0]}×{x['render_resolution'][1]} | {x['raf_fps']:.1f} | {x['raf_p95_ms']:.2f} | {x['gpu_p95_ms']:.2f} | {x['raf_max_ms']:.2f} |")
report=f'''# Kiểm chứng bản 2 — hình ảnh, chức năng và hiệu năng

## Đúng bản được kiểm thử

HTML: **{(P/'index.html').stat().st_size:,} byte**, SHA-256 `{sha}`. Hai báo cáo chức năng, báo cáo hình ảnh và báo cáo tốc độ đều ghi cùng SHA này. Rebundle từ nguồn/recipe đã lưu tạo HTML giống từng byte. Điều này không đòi tệp Blender nhị phân có metadata phải byte-identical giữa phiên bản Blender khác nhau.

Blender {bm['blender']}, {len(bm['assets'])} tài sản. Máy bay có bounding box: sải {dims[0]:.6f} m, dài {dims[1]:.6f} m, cao hình học thu càng {dims[2]:.6f} m. Sải nominal 56,388 m, dài 47,7012 m; nẹp/chi tiết tạo khác biệt nhỏ ở bounding box. Không coi hộp bao đúng là đủ chứng minh hình dáng đúng — lỗi dây cung và winding từng được phát hiện bằng ảnh.

## Các đợt tách biệt

**Chức năng:** 58/58 đạt trong hai tiến trình Chrome độc lập cuối (`functional_repeat1.json`, `functional_repeat2.json`). Gồm offline, tua ngược so RGB, tốc độ, từng khung, free camera, ảnh/camera export, các mức chất lượng, kích thước nhỏ, nguồn lịch sử theo chương và thay lời dẫn theo góc.

**Trực quan:** 10 góc Blender chi tiết, 57 ảnh đầu/giữa/cuối 19 đường máy, 15 góc tự do/diễn tiến nổ và 7 ảnh hồ sơ lịch sử. Đã mở ảnh thật qua bridge để kiểm tra cả mũi/cánh, nút cầu/gối, mặt tiền và chuỗi mảnh bay–rơi–nằm lại. Ảnh trước lỗi normals được đặt tên rõ `aircraft_before_normals_fix.png`; không dùng làm ảnh cuối.

**Phát toàn bộ:** 210 giây ở 4× kết thúc trong {visual['full_playback_wall_seconds']:.3f} giây thực và dừng đúng 210. Không ghi nhận lỗi JS/shader trong các phép thử cuối. Không suy ra không thể có lỗi chưa được thử.

**Cầu và nhà:** audit ghi {audit['bridge']['shared_nodes']} nút/{audit['bridge']['main_members']} dầm chính, 0 đầu mút chính cô lập. Ảnh gần còn kiểm tra bản mã có bề dày và vị trí gối/dầm, vì đồ thị nút không đủ để chứng minh chúng chạm nhau. Khâm Thiên có 1.070 instance bối cảnh, khe mặt tiền thường 7,5 cm; các con số này chỉ mô tả mô hình.

**Vật lý:** 280 mảnh nhỏ mỗi vụ, 1.120 mảnh sau bốn vụ ở Khâm Thiên. 46 nhà có 644 phần mái/tường/xà rơi; 644/644 về trạng thái nghỉ, không vi phạm nền trong phép kiểm tra. Test hộp vật cản riêng kiểm tra có va chạm tường/mái, không tâm mảnh lọt hộp và không có số không hữu hạn. Tua cùng thời điểm của sập nhà cho RGB như nhau trong cùng phiên. Không gọi đó là kiểm định hiện trường vụ nổ.

**Bộ nhớ:** đã lặp 70 lần chuyển cảnh sau warm-up, không tăng số geometry/texture trong bộ đếm renderer trong phép thử. Không thay thế phép đo chạy nhiều giờ hoặc đo toàn bộ RAM tiến trình.

## Tốc độ đo sau khi dừng các lượt render Blender/ảnh của dự án

{perf['browser']} / Windows 11 / `{perf['gpu']}`. Viewport 1920×1080, device scale factor 1. Có ghi kích thước render thực, vì mức Nhẹ chủ động giảm xuống 1536×864. Headless lấy mẫu 4 giây sau 1 giây warm-up; cửa sổ thật lấy 5 giây. Không chụp ảnh trong khoảng lấy mẫu. Dữ liệu số gốc: `qa/v2/performance_final.json`.

| Cửa sổ | Mức | Cảnh | Render thực | FPS trung bình rAF | p95 rAF (ms) | p95 GPU (ms) | Khung chậm nhất (ms) |
|---|---|---|---|---:|---:|---:|---:|
{chr(10).join(rows)}

Cột GPU lấy từ EXT_disjoint_timer_query_webgl2, không lấy thời gian CPU gọi render thay thế. Mẫu GPU được reset giữa các mức; lượt đầu `perf_initial.json` không phải số cuối. FPS thấp nhất **theo trung bình của các đoạn đã đo** là {min(x['raf_fps'] for x in perf['segments']):.1f}; không có nghĩa mọi khung đều đạt tối thiểu FPS đó. Headless và cửa sổ thật khác nhau về trạng thái hệ thống/nhịp trình duyệt; không chọn riêng số cao để quảng bá. Không có mẫu rAF >50 ms trong các khoảng này; số đo ngắn không bảo đảm không bao giờ giật.

## Giới hạn phép so ảnh và nền tảng

Phố/cấu kiện so RGB tuyệt đối ở thời gian lặp. Riêng phản chiếu hồ có ngưỡng đã công bố: tối đa 1 mức màu 8-bit trên không quá 0,001% pixel; xem số thực tế trong các test JSON. Viewport 390×844 và 844×390 là mô phỏng kích thước trình duyệt, không là điện thoại thật. Chưa thử mọi GPU, Safari hoặc liên tục nhiều giờ.

Nguồn lịch sử và điều chưa có chứng cứ: `HISTORY_V2.md`. Sai sót trong quá trình thực hiện: `ISSUES_V2.md`. Cách tái lập: `REPRODUCE_V2.md`. Báo cáo bản 1 không dùng để chứng minh bản 2.
'''
(P/'QA_V2.md').write_text(report,encoding='utf-8')
print('RELEASE_CHECK_OK',sha,'58/58 x 2',len(bm['assets']),'assets')
if not opt.package:raise SystemExit(0)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip();status=subprocess.check_output(['git','status','--porcelain'],cwd=P,text=True)
assert not status.strip(),'Commit the audited source before packaging: '+status
meta={'version':'2.0.0','before_commit':'5e35fc5','after_commit':head,'html_sha256':sha,'html_bytes':(P/'index.html').stat().st_size,'functional_tests':'58/58, two independent repeats','local_release_only':True,'history':'HISTORY_V2.md','qa':'QA_V2.md'}
(P/'RELEASE_V2.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
rootnames=['index.html','README_V2.md','REPRODUCE_V2.md','HISTORY_V2.md','ISSUES_V2.md','QA_V2.md','AGENTS.md','build.mjs','package.json','package-lock.json','THIRD_PARTY_LICENSES.txt','LICENSE','RELEASE_V2.json']
files=[P/n for n in rootnames if (P/n).is_file()]
source_names=['build_assets.py','assets_v2.py','geometry.js','world.js','effects.js','debris_physics.js','collapse_v2.js','film_pipeline.js','history_v2.js','timeline.js','app.js','template.html','make_textures_v2.py','refine_materials_v2.py','run_blender.py','render_assets.py','render_review_v2.py','preview_v2.py','test_debris_physics.mjs','qa_v2_functional.py','qa_visual_v2.py','qa_performance_v2.py','open_final_v2.py','release_v2.py']
files += [P/'src'/n for n in source_names]
files += [x for x in (P/'assets').rglob('*') if x.is_file() and x.suffix in ['.blend','.glb','.json','.jpg','.png']]
files += [P/'references'/n for n in ['longbien.jpg','huutiep.jpg']]
files += [P/'references/v2'/n for n in ['b52_drop.jpg','b52_front.jpg','bridge_under.jpg','RELEASE_IMAGE_CREDITS.json','reference_manifest.json']]
files += [x for x in Q.rglob('*') if x.is_file() and x.suffix in ['.png','.jpg','.json','.log']]
files=sorted(set(files));assert all(f.is_file() for f in files)
manifest={x.relative_to(P).as_posix():{'bytes':x.stat().st_size,'sha256':digest(x)} for x in files};(P/'MANIFEST_V2_SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');files.append(P/'MANIFEST_V2_SHA256.json')
archive=P/'B52_Hanoi_1972_v2_Project.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for x in files:z.write(x,'B52_Hanoi_Cinematic_1972_v2/'+x.relative_to(P).as_posix())
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
viewer=P/'B52_Hanoi_1972_v2_Viewer.zip'
with zipfile.ZipFile(viewer,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n in ['index.html','THIRD_PARTY_LICENSES.txt','HISTORY_V2.md','RELEASE_V2.json']:z.write(P/n,n)
 z.writestr('README.txt','Ban 2 / Version 2. Extract and open index.html in Chrome or Edge. Offline playback; audio off by default. F: free camera; Space: play/pause. Historical sources and limitations are inside the viewer. Complete Blender source, QA and reproduction method are in the separate v2 Project ZIP.\n')
with zipfile.ZipFile(viewer) as z:assert z.testzip() is None;assert hashlib.sha256(z.read('index.html')).hexdigest()==sha
print(json.dumps({'before_commit':'5e35fc5','after_commit':head,'project_zip_bytes':archive.stat().st_size,'project_files':len(files),'viewer_zip_bytes':viewer.stat().st_size,'html_sha256':sha},indent=2))
