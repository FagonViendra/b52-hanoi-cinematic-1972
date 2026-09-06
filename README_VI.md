# Những đêm tháng Chạp — Miền Bắc 1972

Bản phim 3D tương tác dài 210 giây, 7 chương, 19 đường máy. Đây là phục dựng diễn giải lịch sử; không phải ảnh tư liệu, bản đồ trắc địa hay tái hiện một phi vụ cụ thể.

## Mở ngay

Mở `index.html` bằng Chrome hoặc Edge có tăng tốc đồ họa. Tệp chứa sẵn mã Three.js, hình học, bề mặt và hai ảnh tham chiếu; không cần máy chủ hay mạng để phát. Các liên kết tư liệu trong cửa sổ “Tư liệu & địa điểm” chỉ cần mạng khi người xem chủ động mở.

Âm thanh tắt mặc định. Có mô phỏng tiếng nổ và chớp sáng; bật “Giảm chớp & rung máy” trong Hướng dẫn để giảm cường độ.

## Điều khiển

- Space: phát/dừng. Thanh thời gian hoặc các nút chương: tua. Mũi tên trái/phải: lùi/tiến 5 giây. Dấu phẩy/chấm: lùi/tiến 1/24 giây.
- Tốc độ: 0,25×, 0,5×, 1×, 2×, 4×. F: góc phim ↔ quan sát tự do. Vào quan sát tự do sẽ tạm dừng thời gian.
- Khi xem tự do: kéo trái xoay, kéo phải dịch, cuộn zoom; W A S D bay, Q E hạ/nâng, Shift tăng tốc. Camera không có va chạm vật lý; F đưa về đường máy.
- H ẩn/hiện giao diện; P lưu ảnh PNG khung 3D, không bao gồm chữ giao diện; C lưu vị trí camera JSON; D hiện thống kê khi ở góc phim.

## Các chương

| Thời gian phim | Địa điểm/chủ đề | Tính chất |
|---|---|---|
| 00:00–00:26 | Sông Hồng / cầu Long Biên, Hà Nội | Cảnh định vị; cầu được rút gọn |
| 00:26–00:58 | Ngoại cảnh B-52D trên mây | Tám động cơ; thời gian/độ cao thả bom nén |
| 00:58–01:22 | Bờ sông Cấm, Hải Phòng | Khu cảng diễn giải, không chỉ định bến hay mục tiêu |
| 01:22–01:52 | Bệnh viện Bạch Mai | Mốc sự kiện rạng sáng 22/12/1972 |
| 01:52–02:34 | Khâm Thiên, Hà Nội | Mốc sự kiện đêm 26/12/1972 |
| 02:34–03:02 | Hồ Hữu Tiệp, Ngọc Hà | Mảnh xác, mốc 27/12/1972 |
| 03:02–03:30 | Sau những đêm bom | Cảnh suy tưởng; ánh sáng được dàn dựng |

Các chương thuộc những thời điểm khác nhau. Không được diễn giải đường cắt phim thành một đường bay liên tục từ máy bay sang từng địa điểm.

## Nội dung dự án

`assets/Northern_Vietnam_1972.blend` là thư viện Blender thực. `assets/library.glb` là bản xuất hình học. `assets/recipe.json` chứa tham số dùng chung để dựng hình web và Blender. `assets/blender_measurements.json` lưu kích thước đo. `src/` chứa toàn bộ mã tạo hình, cảnh, đường máy, điều khiển và kiểm thử. `references/` chứa hai ảnh CC BY 2.0. `qa/` chứa ảnh render, kiểm thử và log.

Đọc `HISTORY_SOURCES.md` để phân biệt chứng cứ và dàn dựng; `REPRODUCE.md` để dựng lại; `QA_REPORT.md` và `ISSUE_LOG.md` để xem kiểm thử và các giới hạn còn lại.

Không cần Blender để xem HTML. Không cần cài Node/Python để phát tệp đã đóng gói. Các công cụ đó chỉ cần cho việc sửa hoặc tái lập.
