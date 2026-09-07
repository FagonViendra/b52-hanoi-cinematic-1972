# Kiểm chứng bản 2 — hình ảnh, chức năng và hiệu năng

## Đúng bản được kiểm thử

HTML: **7,948,696 byte**, SHA-256 `f64699ad5909280194b247728a0f3380a902b88dd0b2f99b71646b25c92e9f33`. Hai báo cáo chức năng, báo cáo hình ảnh và báo cáo tốc độ đều ghi cùng SHA này. Rebundle từ nguồn/recipe đã lưu tạo HTML giống từng byte. Điều này không đòi tệp Blender nhị phân có metadata phải byte-identical giữa phiên bản Blender khác nhau.

Blender 5.1.1, 45 tài sản. Máy bay có bounding box: sải 56.396963 m, dài 47.701199 m, cao hình học thu càng 13.770000 m. Sải nominal 56,388 m, dài 47,7012 m; nẹp/chi tiết tạo khác biệt nhỏ ở bounding box. Không coi hộp bao đúng là đủ chứng minh hình dáng đúng — lỗi dây cung và winding từng được phát hiện bằng ảnh.

## Các đợt tách biệt

**Chức năng:** 58/58 đạt trong hai tiến trình Chrome độc lập cuối (`functional_repeat1.json`, `functional_repeat2.json`). Gồm offline, tua ngược so RGB, tốc độ, từng khung, free camera, ảnh/camera export, các mức chất lượng, kích thước nhỏ, nguồn lịch sử theo chương và thay lời dẫn theo góc.

**Trực quan:** 10 góc Blender chi tiết, 57 ảnh đầu/giữa/cuối 19 đường máy, 15 góc tự do/diễn tiến nổ và 7 ảnh hồ sơ lịch sử. Đã mở ảnh thật qua bridge để kiểm tra cả mũi/cánh, nút cầu/gối, mặt tiền và chuỗi mảnh bay–rơi–nằm lại. Ảnh trước lỗi normals được đặt tên rõ `aircraft_before_normals_fix.png`; không dùng làm ảnh cuối.

**Phát toàn bộ:** 210 giây ở 4× kết thúc trong 52.513 giây thực và dừng đúng 210. Không ghi nhận lỗi JS/shader trong các phép thử cuối. Không suy ra không thể có lỗi chưa được thử.

**Cầu và nhà:** audit ghi 196 nút/527 dầm chính, 0 đầu mút chính cô lập. Ảnh gần còn kiểm tra bản mã có bề dày và vị trí gối/dầm, vì đồ thị nút không đủ để chứng minh chúng chạm nhau. Khâm Thiên có 1.070 instance bối cảnh, khe mặt tiền thường 7,5 cm; các con số này chỉ mô tả mô hình.

**Vật lý:** 280 mảnh nhỏ mỗi vụ, 1.120 mảnh sau bốn vụ ở Khâm Thiên. 46 nhà có 644 phần mái/tường/xà rơi; 644/644 về trạng thái nghỉ, không vi phạm nền trong phép kiểm tra. Test hộp vật cản riêng kiểm tra có va chạm tường/mái, không tâm mảnh lọt hộp và không có số không hữu hạn. Tua cùng thời điểm của sập nhà cho RGB như nhau trong cùng phiên. Không gọi đó là kiểm định hiện trường vụ nổ.

**Bộ nhớ:** đã lặp 70 lần chuyển cảnh sau warm-up, không tăng số geometry/texture trong bộ đếm renderer trong phép thử. Không thay thế phép đo chạy nhiều giờ hoặc đo toàn bộ RAM tiến trình.

## Tốc độ đo sau khi dừng các lượt render Blender/ảnh của dự án

152.0.7977.77 / Windows 11 / `ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Ti Laptop GPU (0x000025A0) Direct3D11 vs_5_0 ps_5_0, D3D11)`. Viewport 1920×1080, device scale factor 1. Có ghi kích thước render thực, vì mức Nhẹ chủ động giảm xuống 1536×864. Headless lấy mẫu 4 giây sau 1 giây warm-up; cửa sổ thật lấy 5 giây. Không chụp ảnh trong khoảng lấy mẫu. Dữ liệu số gốc: `qa/v2/performance_final.json`.

| Cửa sổ | Mức | Cảnh | Render thực | FPS trung bình rAF | p95 rAF (ms) | p95 GPU (ms) | Khung chậm nhất (ms) |
|---|---|---|---|---:|---:|---:|---:|
| headless | Cân bằng | Cầu Long Biên | 1920×1080 | 144.0 | 7.00 | 4.27 | 7.10 |
| headless | Cân bằng | B-52D | 1920×1080 | 144.0 | 7.00 | 4.02 | 7.10 |
| headless | Cân bằng | Phố đông nhà | 1920×1080 | 143.7 | 7.00 | 5.41 | 13.80 |
| headless | Cân bằng | Bốn vụ nổ + mảnh + sập nhà | 1920×1080 | 96.2 | 14.00 | 10.22 | 20.90 |
| headless | Cân bằng | Hồ có phản chiếu | 1920×1080 | 143.0 | 7.00 | 6.70 | 14.00 |
| headless | Cao | Bốn vụ nổ + mảnh + sập nhà | 1920×1080 | 79.7 | 14.00 | 10.06 | 20.90 |
| headless | Nhẹ | Bốn vụ nổ + mảnh + sập nhà | 1536×864 | 132.8 | 13.90 | 5.00 | 14.00 |
| headed | Cân bằng | Bốn vụ nổ + mảnh + sập nhà | 1920×1080 | 115.8 | 14.00 | 8.99 | 14.10 |
| headed | Cao | Bốn vụ nổ + mảnh + sập nhà | 1920×1080 | 116.2 | 13.90 | 8.64 | 20.90 |

Cột GPU lấy từ EXT_disjoint_timer_query_webgl2, không lấy thời gian CPU gọi render thay thế. Mẫu GPU được reset giữa các mức; lượt đầu `perf_initial.json` không phải số cuối. FPS thấp nhất **theo trung bình của các đoạn đã đo** là 79.7; không có nghĩa mọi khung đều đạt tối thiểu FPS đó. Headless và cửa sổ thật khác nhau về trạng thái hệ thống/nhịp trình duyệt; không chọn riêng số cao để quảng bá. Không có mẫu rAF >50 ms trong các khoảng này; số đo ngắn không bảo đảm không bao giờ giật.

## Giới hạn phép so ảnh và nền tảng

Phố/cấu kiện so RGB tuyệt đối ở thời gian lặp. Riêng phản chiếu hồ có ngưỡng đã công bố: tối đa 1 mức màu 8-bit trên không quá 0,001% pixel; xem số thực tế trong các test JSON. Viewport 390×844 và 844×390 là mô phỏng kích thước trình duyệt, không là điện thoại thật. Chưa thử mọi GPU, Safari hoặc liên tục nhiều giờ.

Nguồn lịch sử và điều chưa có chứng cứ: `HISTORY_V2.md`. Sai sót trong quá trình thực hiện: `ISSUES_V2.md`. Cách tái lập: `REPRODUCE_V2.md`. Báo cáo bản 1 không dùng để chứng minh bản 2.
