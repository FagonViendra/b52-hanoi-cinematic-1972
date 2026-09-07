# Tái lập bản 2

## Điểm bắt đầu

Đọc `README_V2.md`, `HISTORY_V2.md`, `ISSUES_V2.md`, `QA_V2.md`. Bản 1 đã từng được kết luận quá sớm bằng kiểm thử chức năng; không lặp lại tiêu chí đó. Phải xem ảnh kết quả thực và diễn tiến chuyển động, không chỉ dòng PASS hoặc số lượng polygon.

Nguồn chuẩn: `src/assets_v2.py`, `build_assets.py`, `geometry.js`, `world.js`, `effects.js`, `debris_physics.js`, `collapse_v2.js`, `film_pipeline.js`, `history_v2.js`, `timeline.js`, `app.js`, `template.html`. Các script chỉnh sửa một lần của bản 1 và tệp truyền `.b64` không phải nguồn để chạy lại.

## Môi trường cố định

Đã dùng Windows 11, Blender 5.1.1, Python 3.11 + NumPy/Pillow/Playwright, Node 25.6.1, npm 11.9.0. `package-lock.json` khóa Three.js 0.180.0 và esbuild 0.25.10; không gọi chúng là phiên bản mới nhất. Phát HTML đã đóng gói không cần các công cụ dựng.

```powershell
$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$env:BLENDER_EXE = 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe'
npm.cmd ci --no-audit --no-fund
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
python .\src\make_textures_v2.py
if ($LASTEXITCODE -ne 0) { throw 'Texture base generation failed' }
python .\src\refine_materials_v2.py
if ($LASTEXITCODE -ne 0) { throw 'Final texture generation failed' }
python .\src\run_blender.py
if ($LASTEXITCODE -ne 0) { throw 'Blender build failed' }
node .\build.mjs
if ($LASTEXITCODE -ne 0) { throw 'HTML bundle failed' }
node .\src\test_debris_physics.mjs
if ($LASTEXITCODE -ne 0) { throw 'Physics invariants failed' }
python .\src\qa_v2_functional.py
if ($LASTEXITCODE -ne 0) { throw 'Functional regression failed' }
python .\src\qa_visual_v2.py
if ($LASTEXITCODE -ne 0) { throw 'Visual sequence failed' }
```

Hai script texture v2 trên là cặp bước có chủ đích: script thứ hai ghi đè bản đồ tường/khối xây quá tương phản và tạo `dust.png`. Không bỏ bước thứ hai. Tệp texture cuối đã lưu sẵn nên không cần tạo lại chỉ để sửa camera. Font Arial chỉ được dùng tại máy để raster hóa một số chữ vào ảnh; không phát hành tệp font. Khác nền tảng/font có thể khác pixel texture chữ; dùng texture được lưu để tái lập đúng bản giao.

`run_blender.py` gọi Blender với `--python-exit-code 2`. Phải kiểm tra mã thoát ngay sau mỗi chương trình native. Không nối nhiều lệnh rồi chỉ kiểm tra lệnh cuối. UTF-8 stdout tránh lỗi console Windows cp1252 làm dừng bước đọc log.

## Quy ước hình học và kiểm tra cầu

Recipe dùng mét, Y lên, mũi máy bay hướng -Z. Blender đổi trục `(x,y,z) -> (x,-z,y)`. Cả hai adapter phải đảo thứ tự mặt cánh phía âm X giống nhau; nếu không, kiểm tra pháp tuyến sẽ sơn nhầm mặt trên thành bụng đen trong Blender. Đầu cánh đã có mặt đóng.

`assets_v2.rebuild()` thay thế tài sản theo tên, không cộng trùng khi chạy lại. Audit `assets/v2_design_audit.json` ghi các nút/dầm cầu: 196 nút, 527 dầm chính, không có đầu mút chính cô lập. Đó chỉ là kiểm tra hình học liên kết, không phải chứng nhận khả năng chịu lực. Kiểm tra thêm bằng ảnh gần để phát hiện khoảng hở bản mã, thân đinh, gối cầu hoặc dầm dọc mà đồ thị nút không thể nhận ra. Không dùng một chỉ số duy nhất thay cho xem hình.

Dáng cầu đại diện cho các nhịp neo 75 m, tay chìa 27,5 m và nhịp treo 51,2 m từ bản vẽ tham chiếu, có đoạn tiếp cận. Cảnh không phải toàn bộ cầu đúng nguyên trạng ngày 26/12/1972. Từng chi tiết kim loại là gần đúng để quan sát.

## Thời gian và vật lý

Mọi thứ được đánh giá từ thời gian tuyệt đối 0–210 giây. Không tích lũy vị trí theo số callback requestAnimationFrame. `debris_physics.js` tạo quỹ đạo trước, seed cố định, tích phân 120 Hz và lưu 30 Hz trong 12 giây; sau đó giữ tư thế cuối. Mảnh nhỏ có trọng lực 9,81 m/s², cản khí kiểu tuyến tính, hệ số nảy khác nhau, tổn hao tiếp xúc và trạng thái ngủ. Va chạm là hộp giới hạn ở những nhà lân cận không hư hại, cùng mặt đất/mặt mái đơn giản. Không mô phỏng đầy đủ vật liệu, sóng nổ, tương tác mọi mảnh hoặc biến dạng dẻo.

`CollapseField` chia 46 nhà thành 644 bộ phận lớn. Kích thước và vị trí ban đầu lấy từ bề rộng/chiều sâu/độ cao nhà, xoay theo hướng nhà. Không đặt sẵn các mảnh lớn trên mặt đất rồi giả là cảnh sập. Mảnh tường nghỉ trên mặt nằm ngang; mảnh chạm mái phải vào trạng thái ngủ khi tốc độ rất nhỏ, tránh lặp va chạm hàng nghìn lần.

Kiểm tra: quỹ đạo hữu hạn, không xuống dưới nền, năng lượng vận tốc sau tiếp xúc không tăng, cùng seed cho cùng dữ liệu. Fixture vật cản còn đếm tâm mảnh lọt trong hộp sau giải va chạm. Các phép thử này không chứng minh vật lý của trận bom thật.

## Kết xuất, hiệu suất và tái lập

Thứ tự hậu kỳ: **RenderPass luôn bật -> SSAO (chỉ nền đất) -> SMAA -> OutputPass**. Không tắt RenderPass vì nghĩ SSAO tự dựng ảnh màu: việc đó từng giữ bộ đệm cảnh trước. Mặt khói trong suốt phải ẩn riêng trong pass pháp tuyến SSAO, nếu không xuất hiện viền hình chữ nhật không thuộc cảnh. Mặt phản chiếu cũng không dựng đệ quy khi scene.overrideMaterial đang dùng.

Kernel SSAO và noise được cố định seed. Nhà gần dùng chi tiết hình học, nhà xa giữ silhouette/texture nhưng bỏ hàng trăm chi tiết nắp ngói; instancing giảm số lệnh vẽ. Mảnh nhỏ và cấu kiện sập được instancing và lưu ma trận khi thời gian đã qua đoạn chuyển động. Khi dừng, chương trình vẽ thưa hơn; đó không phải tốc độ khi phát.

GPU timer dùng `EXT_disjoint_timer_query_webgl2`, lấy kết quả bất đồng bộ, loại mẫu khi disjoint. `window.__B52.resetSamples()` phải xóa cả mẫu rAF và GPU/query chờ; nếu không các mức chất lượng dùng lại mốc thời gian giống nhau sẽ bị lẫn số đo. Không chụp ảnh, chạy Blender hoặc mở nhiều bản kiểm thử trong khoảng lấy mẫu tốc độ. rAF, CPU submit và GPU elapsed là ba số khác nhau. Benchmark cần 1920×1080 và đoạn sau 130 giây khi cả bốn cụm mảnh đã xuất hiện, không chỉ thử cảnh máy bay nhẹ.

## Điểm móc kiểm tra

Sau `window.__B52.ready` có `seek(t)`, `play(bool)`, `setCamera(position,target,fov)`, `setFree(bool)`, `setQuality(q)`, `state()`, `gpuTiming()`, `resetSamples()`, `samples()`, `measurements`, `design`, `layout`, `physics`, `collapse` và `history`.

Bắt buộc thử lại 118 -> 148 -> 118, 127 -> 193 -> 127 và 42 -> 118 để phát hiện hư hại lưu sót hoặc bộ đệm màu cũ. Phố/cấu kiện so RGB tuyệt đối trong cùng trình duyệt; hồ cho phép sai khác tối đa 1 mức màu trên không quá 0,001% pixel, phải ghi số thực tế. Kiểm tra ảnh nguồn đã decode, nút lịch sử mỗi chương và thay lời dẫn trong cùng chương.

`qa_visual_v2.py` chụp 57 ảnh đầu/giữa/cuối 19 shot, 15 góc kiểm tra tự do, hồ sơ 7 chương và phát hết phim. `render_review_v2.py` tạo 10 góc Blender. Khi cần xem qua bridge, dùng helper hiện có để xuất PNG; helper không là thành phần phụ thuộc của HTML. Xem cả bảng ảnh và các crop chi tiết tại vị trí nghi lỗi.

Không tăng ngưỡng test để làm kết quả xanh. Lưu kết quả thất bại có ý nghĩa và nguyên nhân sửa, cùng SHA-256 của đúng bản được kiểm thử. Không dùng báo cáo bản 1 để chứng minh bản 2.
