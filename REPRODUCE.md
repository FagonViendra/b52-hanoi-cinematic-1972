# Tái lập cho người hoặc AI tiếp theo

## Bản nguồn chuẩn

Mã hiện hành trong `src/build_assets.py`, `geometry.js`, `effects.js`, `world.js`, `timeline.js`, `app.js`, `template.html` là bản nguồn cuối. Các tệp `refine_*.py` là nhật ký sửa đổi đã áp dụng; KHÔNG chạy lại chúng trên bản cuối vì một số phép chèn không có tính idempotent. `src/incoming.b64` là tệp truyền nguồn tạm thời, không phải nguồn chuẩn và không nằm trong gói bàn giao.

## Môi trường đã dùng

Windows 11, Blender 5.1.1, Python 3.11, Node.js/npm. Three.js 0.180.0, esbuild 0.25.10, khóa bằng `package-lock.json`. Playwright, Pillow và NumPy dùng cho kiểm thử. GPU kiểm thử: NVIDIA GeForce RTX 3050 Ti Laptop, backend ANGLE/D3D11 của Chrome. Không tuyên bố đây là thư viện mới nhất; các phiên bản được cố định để tái lập.

## Dựng lại

Mở PowerShell tại thư mục dự án:

```powershell
npm.cmd ci --no-audit --no-fund
$env:BLENDER_EXE = 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe'
python .\src\run_blender.py
node .\build.mjs
python .\src\qa_smoke.py
python .\src\qa_functional.py
python .\src\qa_performance.py
```

`run_blender.py` dựng `.blend`, GLB và recipe, sau đó render sáu góc. Blender được gọi với `--python-exit-code 2`; lỗi Python phải tạo mã thoát khác không. Cảnh báo gốc của Blender được ghi vào log, không bị nhầm với lỗi thực thi.

Chỉ tạo lại recipe để phát triển web, không thay thế việc kiểm chứng Blender:

```powershell
python .\src\build_assets.py --out .
node .\build.mjs
```

## Hình học và kiểm tra

Seed gốc: 19721218. Recipe dùng mét, Y hướng lên, mũi B-52 hướng -Z. Blender nhận đổi trục `(x, y, z) -> (x, -z, y)`. Hình học được mô tả bằng các phép box, beam, ellipsoid, torus, poly, lathe và airfoil. Poly có thể có cờ smooth để mặt vỏ kim loại nối chung đỉnh có pháp tuyến liên tục.

Máy bay có bốn cụm động cơ đôi, không phải bốn động cơ. So sánh sải cánh và chiều dài nominal với `assets/blender_measurements.json` và `window.__B52.measurements`. Các đường nẹp mỏng có thể làm bounding box vượt sải cánh danh định khoảng một centimet; sai khác tessellation giữa Blender và Three ở mức dưới một milimet không đồng nghĩa lỗi tỷ lệ.

Blender và web dùng cùng hình học, nhưng vật liệu thủ tục không hoàn toàn giống nhau. GLB không chứa bản bake đầy đủ của nhiễu màu Blender; HTML tạo bề mặt bằng Canvas/shader riêng. Vì thế không tuyên bố GLB là bản sao pixel của khung hình web.

## Camera và thời gian

Đường máy nằm ở `timeline.js`. Thời gian phim là một biến tuyệt đối 0–210 giây, không tích lũy trạng thái theo số khung hình. Mỗi hiệu ứng dùng `age = t - start`; tàn tích dùng trạng thái intact/ruin chọn lại từ `t`. Không dùng Math.random trong vòng lặp hoạt hình. Nhờ vậy tua ngược phải khôi phục hình ảnh và không để sót khói/đổ nát từ cảnh trước.

Camera dùng Catmull-Rom theo độ dài đường cong. Màn hình dọc tăng khoảng cách nhìn để không cắt ngang máy bay. Camera tự do không có va chạm; phải ghi rõ giới hạn này trong giao diện. Không để WASD vừa di chuyển vừa bật thống kê.

## Đồ họa và hiệu năng

Mã shader màu phải phân biệt không gian tuyến tính với đầu ra sRGB. Shader bầu trời từng thiếu chuyển đổi và tạo màu sai; giữ phần colorspace. Không vẽ đĩa mặt trời giả trong cảnh đêm. Mặt nước có giảm chi tiết theo khoảng cách, hồ có phản chiếu phẳng với nhiễu nhỏ. Đây không phải ray tracing hay thể tích khí quyển vật lý.

Hình học của từng tài sản được gộp theo vật liệu, sau đó instancing cho dãy nhà. Dùng một PointLight chớp chung thay vì tăng/giảm số đèn theo mỗi vụ nổ, nhằm giảm biên dịch lại shader. Chuẩn bị shader trước khi hiện màn hình bắt đầu. Chế độ Nhẹ tắt shadow và phản chiếu hồ.

## API kiểm thử

Sau `window.__B52.ready === true`:

```javascript
window.__B52.seek(118);          // Dừng và đến thời điểm chính xác
window.__B52.play(true);
window.__B52.setFree(true);
window.__B52.setCamera([12,6,18], [0,2,0], 47);
window.__B52.setQuality('balanced');
window.__B52.setGentle(true);
window.__B52.state();
window.__B52.measurements;
window.__B52.resetSamples();
window.__B52.samples();
```

Bắt buộc kiểm tra tua 118 -> 148 -> 118 và so sánh pixel; kiểm tra hồ 175 -> 99 -> 175. Kiểm tra bộ nhớ sau warm-up rồi ít nhất 70 lần đổi cảnh; tăng một geometry ở lần thấy vật thể đầu tiên là lazy upload, chỉ được phân biệt với rò rỉ bằng lượt lặp ổn định tiếp theo, không được bỏ qua bằng lời giải thích không có phép thử.

Chụp đầu/giữa/cuối từng shot; mở ảnh thật để soi, không dùng chỉ thống kê thành công của công cụ. Khi đo FPS phải chạy riêng không chụp ảnh trong khoảng lấy mẫu. FPS đo trên máy kiểm thử không phải bảo đảm cho mọi máy. Không gọi kích thước viewport mô phỏng là kiểm thử trên điện thoại thật.

## Chụp qua bridge PC

Script Playwright lưu PNG vào `qa/`. Sau đó dùng `bridge_images.py` của bridge hiện có để xuất ảnh cho AI xem. Đường dẫn helper thuộc máy chủ bridge, không phải thành phần bắt buộc của bản phim. Máy không có bridge vẫn mở trực tiếp PNG được.

Giữ lại README, hồ sơ nguồn, giấy phép ảnh, báo cáo kiểm thử, nhật ký lỗi và SHA-256. Không chỉnh ngày lịch sử chỉ để làm mạch dựng dễ hơn; không gán xác suất chắc chắn cho kiến trúc không có bản vẽ.

Bổ sung kiểm tra mặt bằng: sải cánh và chiều dài không đủ phát hiện một cánh quá rộng dây cung. Đọc `qa/wing_planform_audit.json`, tính diện tích chiếu bao gồm quy ước phần tâm ngoại suy, rồi đối chiếu ảnh trên. Hiệu chỉnh diện tích không thay thế bản vẽ D riêng; giữ nguyên ghi chú này trong hồ sơ.

So sánh ảnh hồ: không dùng chỉ SHA của tệp PNG làm phép so sánh hình ảnh. Giải mã RGB trước. Bản cuối cho phép tối đa 1 mức màu 8-bit trên tối đa 0,001% pixel đối với phản chiếu hồ; lưu số pixel thực tế. Ngưỡng được đặt sau phép điều tra thấy 7 pixel chênh một mức, không được tự tăng ngưỡng để cho qua thay đổi hình học. Cảnh phố vẫn so sánh chính xác tuyệt đối.
