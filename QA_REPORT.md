# Báo cáo kiểm thử bản cuối

## Tệp được kiểm tra

`index.html`: 1,474,597 byte. SHA-256: `3b6537d6de3f404dab8f515385607389c9427621c5500b70d7723a5950739ef3`. Dựng lại bằng esbuild từ cùng nguồn cho kết quả giống từng byte. Blender 5.1.1; 30 tài sản. Chrome 152.0.7977.77, Windows 11, NVIDIA RTX 3050 Ti Laptop qua ANGLE/D3D11; viewport 1440 × 900, chất lượng Cân bằng.

## Các đợt tách biệt

1. Dựng Blender và xem 6 góc, đo bounding box. Cánh được kiểm tra thêm diện tích mặt bằng sau khi phát hiện lỗi tỷ lệ; đã xuất và kiểm thử lại.
2. Kiểm thử chức năng bản cuối: **39/39 đạt**. Hai lượt độc lập cuối đều đạt. Phố so RGB tuyệt đối; hồ cho phép tối đa 1 mức màu trên 0,001% pixel (lượt điều tra: 7 pixel chênh một mức). Gồm offline, tua ngược so sánh pixel, 2 tốc độ đo thời gian, bước từng khung, WASD/orbit, tải PNG/JSON, âm thanh, dialog, 3 chất lượng, giới hạn thời gian, 70 lần đổi cảnh sau warm-up, viewport ngang/dọc và kiểm tra lỗi JS/shader.
3. **57 ảnh**, đầu/giữa/cuối của 19 shot. Camera hữu hạn, độ cao nhỏ nhất trong các mẫu 1.81 m. Đã xem bảng ảnh toàn cảnh và các góc cận qua bridge; ảnh đầy đủ còn ở `qa/shots/`.
4. Phát hết 210 giây ở tốc độ 4×: kết thúc sau **52.507 giây thực**, dừng ở 210 giây. Không có lỗi JavaScript được ghi nhận.
5. Lượt cửa sổ Chrome thật, độc lập với headless: mở ngoại cảnh, phát đoạn Khâm Thiên và chụp nội dung trang ở `qa/headed_chrome.png`. Không ghi nhận lỗi JS/shader. Ảnh `desktop_verification.png` ban đầu ghi lại dashboard bridge đang ở trước, nên không được dùng làm bằng chứng phim chiếm foreground. Kiểm tra mở bản cuối tách riêng ở `qa/final_open_verification.json`.

Các báo cáo `pre_wing_*.json` là bản trước hiệu chỉnh cánh, không dùng làm số liệu bản cuối. `pass2_first_attempt.json` giữ kết quả ban đầu chưa đạt phần bộ nhớ để truy vết.

## Hiệu năng — headless, các đoạn lấy mẫu 4 giây sau 0,7 giây ổn định

| Đoạn | FPS trung bình | p95 khung (ms) | Chậm nhất (ms) | Khung >50 ms |
|---|---:|---:|---:|---:|
| Long Bien | 144.0 | 7.00 | 7.40 | 0 |
| B52 exterior | 144.0 | 7.10 | 7.30 | 0 |
| Hai Phong | 144.0 | 7.10 | 7.30 | 0 |
| Bach Mai impact | 144.0 | 7.00 | 7.30 | 0 |
| Kham Thien impact | 144.0 | 7.10 | 7.10 | 0 |
| Huu Tiep reflector | 144.0 | 7.10 | 7.30 | 0 |
| Aftermath | 144.0 | 7.10 | 7.20 | 0 |

## Hiệu năng — cửa sổ thật

Trong 900 mẫu còn lưu trong bộ đệm: **144.0 FPS**, p95 **7.10 ms**, khung chậm nhất **7.80 ms**. Đây là số đo rAF tại máy kiểm thử, không phải bảo đảm phổ quát. Không được kết luận “không bao giờ giật”; các outlier phải được giữ nguyên trong báo cáo.

## Kích thước máy bay

Sải cánh đo Blender: 56.400330 m; chiều dài: 47.701199 m; chiều cao hình học đang bay: 14.430000 m. Sải cánh danh định 56,388 m, dài 47,7012 m; đường nẹp làm bbox rộng hơn danh định khoảng 1.23 cm. Không so chiều cao thu càng với chiều cao máy bay đứng trên mặt đất.

## Phạm vi không được suy rộng

Không phải kiểm thử mọi máy/trình duyệt. Viewport 390 × 844 và 844 × 390 không phải điện thoại thật. Không đo độ chính xác nguyên trạng năm 1972 của từng công trình. Không chứng minh tối ưu toàn cục, không chứng minh không có lỗi ngoài các tình huống đã chạy. Đọc ISSUE_LOG.md về các lỗi đã sửa và giới hạn.
