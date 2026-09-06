import pathlib,json,hashlib,subprocess,zipfile,datetime
P=pathlib.Path(__file__).resolve().parents[1];Q=P/'qa'
f=json.loads((Q/'pass2_functional.json').read_text(encoding='utf-8'));p=json.loads((Q/'pass3_performance.json').read_text(encoding='utf-8'));h=json.loads((Q/'pass4_headed.json').read_text(encoding='utf-8'));b=json.loads((P/'assets/blender_measurements.json').read_text(encoding='utf-8'))
assert f['pass_count']==f['total']==39
assert not p['errors'] and p['finite_camera'] and p['full_film_ended']['t']==210
assert not h['errors'] and not h['state']['shaderErrors']
# Rebuild once more and verify that the delivered HTML is byte-for-byte reproducible.
before=hashlib.sha256((P/'index.html').read_bytes()).hexdigest();subprocess.run(['node','build.mjs'],cwd=P,check=True);after=hashlib.sha256((P/'index.html').read_bytes()).hexdigest();assert before==after
(Q/'reproducibility.json').write_text(json.dumps({'index_sha256_before':before,'index_sha256_after':after,'byte_identical_rebuild':before==after},indent=2),encoding='utf-8')
rows='\n'.join(f"| {x['name']} | {x['fps']:.1f} | {x['p95_ms']:.2f} | {x['max_ms']:.2f} | {x['over50ms']} |" for x in p['segments'])
dims=b['assets']['b52']['dimensions']
report=f'''# Báo cáo kiểm thử bản cuối

## Tệp được kiểm tra

`index.html`: {(P/'index.html').stat().st_size:,} byte. SHA-256: `{after}`. Dựng lại bằng esbuild từ cùng nguồn cho kết quả giống từng byte. Blender {b['blender']}; {len(b['assets'])} tài sản. Chrome {h['browser']}, Windows 11, NVIDIA RTX 3050 Ti Laptop qua ANGLE/D3D11; viewport 1440 × 900, chất lượng Cân bằng.

## Các đợt tách biệt

1. Dựng Blender và xem 6 góc, đo bounding box. Cánh được kiểm tra thêm diện tích mặt bằng sau khi phát hiện lỗi tỷ lệ; đã xuất và kiểm thử lại.
2. Kiểm thử chức năng bản cuối: **{f['pass_count']}/{f['total']} đạt**. Hai lượt độc lập cuối đều đạt. Phố so RGB tuyệt đối; hồ cho phép tối đa 1 mức màu trên 0,001% pixel (lượt điều tra: 7 pixel chênh một mức). Gồm offline, tua ngược so sánh pixel, 2 tốc độ đo thời gian, bước từng khung, WASD/orbit, tải PNG/JSON, âm thanh, dialog, 3 chất lượng, giới hạn thời gian, 70 lần đổi cảnh sau warm-up, viewport ngang/dọc và kiểm tra lỗi JS/shader.
3. **{p['camera_samples']} ảnh**, đầu/giữa/cuối của 19 shot. Camera hữu hạn, độ cao nhỏ nhất trong các mẫu {p['min_camera_height']:.2f} m. Đã xem bảng ảnh toàn cảnh và các góc cận qua bridge; ảnh đầy đủ còn ở `qa/shots/`.
4. Phát hết 210 giây ở tốc độ 4×: kết thúc sau **{p['full_film_wall_seconds']:.3f} giây thực**, dừng ở 210 giây. Không có lỗi JavaScript được ghi nhận.
5. Lượt cửa sổ Chrome thật, độc lập với headless: mở ngoại cảnh, phát đoạn Khâm Thiên và chụp nội dung trang ở `qa/headed_chrome.png`. Không ghi nhận lỗi JS/shader. Ảnh `desktop_verification.png` ban đầu ghi lại dashboard bridge đang ở trước, nên không được dùng làm bằng chứng phim chiếm foreground. Kiểm tra mở bản cuối tách riêng ở `qa/final_open_verification.json`.

Các báo cáo `pre_wing_*.json` là bản trước hiệu chỉnh cánh, không dùng làm số liệu bản cuối. `pass2_first_attempt.json` giữ kết quả ban đầu chưa đạt phần bộ nhớ để truy vết.

## Hiệu năng — headless, các đoạn lấy mẫu 4 giây sau 0,7 giây ổn định

| Đoạn | FPS trung bình | p95 khung (ms) | Chậm nhất (ms) | Khung >50 ms |
|---|---:|---:|---:|---:|
{rows}

## Hiệu năng — cửa sổ thật

Trong {h['frames']} mẫu còn lưu trong bộ đệm: **{h['fps']:.1f} FPS**, p95 **{h['p95_ms']:.2f} ms**, khung chậm nhất **{h['max_ms']:.2f} ms**. Đây là số đo rAF tại máy kiểm thử, không phải bảo đảm phổ quát. Không được kết luận “không bao giờ giật”; các outlier phải được giữ nguyên trong báo cáo.

## Kích thước máy bay

Sải cánh đo Blender: {dims[0]:.6f} m; chiều dài: {dims[1]:.6f} m; chiều cao hình học đang bay: {dims[2]:.6f} m. Sải cánh danh định 56,388 m, dài 47,7012 m; đường nẹp làm bbox rộng hơn danh định khoảng {(dims[0]-56.388)*100:.2f} cm. Không so chiều cao thu càng với chiều cao máy bay đứng trên mặt đất.

## Phạm vi không được suy rộng

Không phải kiểm thử mọi máy/trình duyệt. Viewport 390 × 844 và 844 × 390 không phải điện thoại thật. Không đo độ chính xác nguyên trạng năm 1972 của từng công trình. Không chứng minh tối ưu toàn cục, không chứng minh không có lỗi ngoài các tình huống đã chạy. Đọc ISSUE_LOG.md về các lỗi đã sửa và giới hạn.
'''
(P/'QA_REPORT.md').write_text(report,encoding='utf-8')
# Authoritative source and records; exclude cache, intermediate transfers and duplicate captures.
paths=[]
for x in P.rglob('*'):
 if not x.is_file():continue
 rel=x.relative_to(P)
 if any(v in {'node_modules','.git','iteration1','__pycache__'} for v in rel.parts):continue
 if x.suffix in {'.zip','.blend1','.b64','.pyc'}:continue
 if rel.name in {'MANIFEST_SHA256.json','desktop_verification.png'}:continue
 paths.append(x)
manifest={str(x.relative_to(P)).replace('\\','/'):{'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in paths}
(P/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');paths.append(P/'MANIFEST_SHA256.json')
archive=P/'B52_Hanoi_1972_Project.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for x in paths:z.write(x,'B52_Hanoi_Cinematic_1972/'+str(x.relative_to(P)).replace('\\','/'))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'html_bytes':(P/'index.html').stat().st_size,'html_sha256':after,'zip_bytes':archive.stat().st_size,'archive_files':len(paths),'functional':str(f['pass_count'])+'/'+str(f['total']),'headed_fps':h['fps'],'headed_p95_ms':h['p95_ms'],'headed_max_ms':h['max_ms'],'full_film_seconds':p['full_film_wall_seconds'],'assets':len(b['assets'])},indent=2))
