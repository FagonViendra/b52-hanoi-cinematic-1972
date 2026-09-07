# Bản 2 — Những đêm tháng Chạp

Bản đang chạy là `index.html` tại thư mục này. Đây là bản sửa theo ảnh tham chiếu sau nhận xét về hình dáng B-52D, nút nối cầu, nhà thưa và hiệu ứng nổ. Các báo cáo trong `qa/v2/`, `QA_V2.md`, `HISTORY_V2.md` và `ISSUES_V2.md` thay thế kết luận chất lượng của bản 1. ZIP cũ `B52_Hanoi_1972_Project.zip` chỉ là bản lưu, không phải bản mới.

## Mở và sử dụng

Mở `index.html` bằng Chrome/Edge có tăng tốc đồ họa. Mã, hình học, bề mặt và năm ảnh tham chiếu nằm trong HTML; không cần mạng để phát. Mạng chỉ cần khi tự mở liên kết nguồn. Âm thanh tắt mặc định; có tùy chọn giảm chớp/rung.

Phim dài 210 giây, 7 chương, 19 đường máy. Space phát/dừng; thanh thời gian và nút chương để tua; tốc độ 0,25×–4×. F chuyển góc phim ↔ tự do. Trong góc tự do: kéo chuột trái xoay, phải dịch, cuộn zoom; W A S D di chuyển, Q E hạ/nâng, Shift tăng tốc. H ẩn giao diện; P lưu PNG; C lưu camera JSON. D bật thống kê trong góc phim. Khi tạm dừng, chương trình chủ động giảm số lần vẽ để tiết kiệm GPU; không lấy FPS lúc đứng yên làm số đo khi phát.

Nút **Lịch sử đoạn này** mở hồ sơ đúng chương đang xem: dữ kiện, nguồn và phần diễn giải được tách riêng. Lời dẫn phía dưới đổi theo từng góc, không chỉ lặp một dòng chung.

## Những thay đổi chính

B-52D được dựng lại với mũi tròn, kính buồng lái, thân sơn đen cao lên hông, đuôi đứng cao, bốn cụm động cơ đôi có miệng hút, cánh quạt nhìn sâu và vòi xả. Bản đồ ngụy trang và dấu hiệu quốc gia được tạo mới, không gán số hiệu hoặc một phi vụ có thật.

Cầu là một khối hình học liên tục dài 370 m đại diện cho hệ dầm chìa–nhịp treo: thanh thép ghép bản, giằng, bản mã có bề dày, đinh tán, dầm ngang/dọc, ray, tà vẹt, lan can, trụ và gối đỡ. Đây không phải bản vẽ thi công hoặc nguyên trạng toàn bộ cầu tháng 12/1972.

Khu Khâm Thiên có 1.070 mẫu nhà trong cảnh, gồm lớp mặt tiền chi tiết và các khối phía xa nhẹ hơn. Khoảng cách thông thường giữa các mặt tiền là 7,5 cm; có ngõ hẹp được bố trí riêng. Con số mô hình không phải thống kê số nhà thực tế năm 1972.

Mỗi vụ nổ có 280 mảnh gạch/ngói/vữa/gỗ 3D với trọng lực, lực cản, giảm năng lượng khi chạm đất hoặc vật cản đơn giản; mảnh nằm lại sau khi ngừng chuyển động. Bốn vụ trong chương Khâm Thiên tạo 1.120 mảnh nhỏ. Ngoài ra 644 mảng mái, tường và xà gỗ được đặt tại vị trí của 46 nhà hư hại để rơi sụp, thay vì chỉ bật/tắt nguyên cả ngôi nhà. Khói bụi dùng ảnh thể tích do chương trình tự tạo, không chỉ một đốm sáng Gaussian.

## Chất lượng và giới hạn

Đây vẫn là phục dựng 3D thời gian thực mang tính diễn giải, không phải phim quay thật, quét 3D hiện vật hoặc khảo sát từng nhà. Hình học, thời tiết, góc máy, điểm nổ và điều kiện đầu của mảnh văng được tác giả thiết kế. Mô phỏng có trọng lực/va chạm không đồng nghĩa đã tái hiện vật lý một trận bom cụ thể. Không có tính toán lượng nổ, tương tác sóng áp suất, mô phỏng kết cấu vật liệu hay va chạm giữa mọi mảnh với nhau.

Chế độ tự do là công cụ quan sát, có thể đi xuyên vật thể; các cảnh không tạo thành bản đồ thế giới liên tục. Chất lượng Cân bằng/Cao dùng bóng tiếp xúc SSAO và chống răng cưa SMAA; Nhẹ tắt hậu kỳ, bóng và phản chiếu hồ. Kết quả tốc độ theo máy/khung hình nằm trong `QA_V2.md`, không được suy rộng thành cam kết mọi máy.

## Tệp nguồn và tái lập

`assets/Northern_Vietnam_1972.blend` và `assets/library.glb` là tài sản được xuất thật bằng Blender. `src/assets_v2.py` định nghĩa hình học hiện hành; `src/debris_physics.js` và `src/collapse_v2.js` định nghĩa chuyển động. Xem `REPRODUCE_V2.md` trước khi sửa. Không chạy lại những script `refine_*.py` của bản 1. Seed, phiên bản thư viện, lệnh dựng, kiểm tra và sai sót đã gặp đều được lưu trên đĩa.
