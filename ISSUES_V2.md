# Sai sót và giới hạn — bản 2

## Trách nhiệm

Không ghi nhận lỗi do người dùng. Nhận xét về hình dáng B-52, mối nối cầu, nhà thưa và nổ thiếu mảnh văng là cơ sở hợp lý để mở lại công việc. Kết luận bản 1 quá sớm là lỗi của phần thực hiện AI: kiểm thử chức năng đã bị dùng thay cho tiêu chí trực quan và độ phù hợp lịch sử.

## Những lỗi được tìm thấy và sửa trong lần làm này

| Vấn đề | Cách phát hiện / xử lý |
|---|---|
| B-52D cũ mũi quá nhọn, động cơ và mảng màu chưa khớp ảnh | Tải và xem ảnh USAF từ nhiều phía; dựng lại thân, mũi tròn/kính, tám J57, pylon mảnh, màu đen lên hông và đuôi D; giữ kiểm tra tỷ lệ kích thước. |
| Cầu cũ là dàn ống lặp và có đầu giằng kết thúc trong không khí | Đọc sơ đồ dầm chìa–nhịp treo, xem ảnh bản thép/rivet; dựng cầu liên tục bằng đồ thị nút, dầm ghép bản và các đầu mút dùng chung tọa độ. |
| Đồ thị nút đúng vẫn chưa chứng minh bản mã chạm vào dầm | Ảnh cận Blender cho thấy bản mã một mặt có khoảng hở nhỏ; thay bằng bản mã có bề dày, xuyên qua phạm vi mép thép, thêm thân/đầu đinh. Xem lại gối cầu và dầm biên riêng. |
| Lớp phong hóa ban đầu loang như ngụy trang trên tường | Xem ảnh phố và mặt tiền; giảm tương phản bề mặt, thay bằng vết nứt mảnh, chân tường bẩn và mảng vữa sứt nhỏ. |
| Hậu kỳ SSAO giữ ảnh B-52 cũ trên cảnh đất hoặc làm nền trống | Đã tắt sai RenderPass khi bật SSAO. Sửa thứ tự: RenderPass luôn chạy trước AO; thêm test tua từ máy bay sang phố và so pixel. Không có lỗi JavaScript không đồng nghĩa hình đúng. |
| AO tạo viền đen lớn ở mái xa | Bán kính và ngưỡng khoảng cách quá cao; giảm cự ly AO, thêm SMAA. Không tăng bừa độ đậm để gọi là chân thật. |
| Tấm khói trong suốt thành viền chữ nhật trên trời | Pass pháp tuyến coi plane khói là mặt đặc. Loại mesh trong suốt khỏi pass AO và khôi phục visibility sau pass; xem lại chuỗi nổ sau khi sửa. |
| Mẫu SSAO thay đổi ngẫu nhiên giữa phiên | Cố định kernel/noise bằng seed; kiểm tra quay lại cùng thời điểm. |
| Bản benchmark đầu lẫn mẫu GPU giữa các mức chất lượng | Hàm reset ban đầu chỉ xóa rAF, không xóa GPU/query đang chờ. Sửa reset cả hai; số `perf_initial.json` không dùng làm bằng chứng cuối. |
| Nhà phía xa dùng hình học chi tiết không cần thiết | Giữ hình dáng/texture nhưng giảm ridge caps và chi tiết nhỏ ở tài sản LOD; đo lại GPU thay vì chỉ giảm số nhà. |
| Một cánh trên Blender thành màu đen trong khi web đúng | Adapter Blender thiếu đảo winding ở phía âm X. Khi gán bụng đen theo pháp tuyến, sai khác lộ rõ. Đảo mặt đúng ở cả hai adapter, đóng đầu cánh, xuất/render lại; giữ ảnh trước sửa để truy vết. |
| Mảnh văng lớn quá đồng đều, thiếu cảm giác vật liệu | Phân bố kích thước nhỏ nhiều/lớn ít, chia gạch, ngói cong, vữa và thanh gỗ; dùng ảnh bụi thể tích tạo mới thay đốm sáng kéo dài. |
| Mảnh đụng mái lặp va chạm hàng nghìn lần, vài mảnh không nghỉ | Thêm tiêu chí nghỉ trên mặt mái và chiều cao đỡ theo tư thế. Fixture riêng kiểm tra tâm mảnh không lọt hộp, tất cả mảnh nghỉ và không có số NaN. |
| Có hạt văng nhưng ngôi nhà vẫn đổi nguyên khối quá đột ngột | Tạo 14 phần mái/tường/xà mỗi nhà bị hư hại, lấy đúng vị trí/kích thước ban đầu và cho rơi; cùng thời gian tua lại phải khôi phục được. Đây vẫn là phân mảnh dàn dựng, không phải FEM. |
| Một số lệnh đọc log dừng vì cp1252 không in được tiếng Việt | Đặt `PYTHONIOENCODING=utf-8`; kiểm tra mã thoát từng lệnh native. Lỗi console không được bỏ qua để tiếp tục với dữ liệu thiếu. |
| Batch xem ảnh có đường dẫn chưa tải thành công | Kiểm tra tệp thật, tách nhóm ảnh đã có; không tuyên bố đã xem ảnh chỉ vì URL có trong log. |
| Hồ sơ cũ còn nói chỉ nhúng hai ảnh | Cập nhật thành năm ảnh, đúng quyền sử dụng và niên đại. Lời dẫn/hồ sơ được chia riêng cho từng đoạn, không chỉ thêm một danh sách nguồn. |

## Trở ngại công cụ và nguồn

Một số lượt tải trang bảo tàng trực tiếp trả 403 và một ảnh Commons trả 429. Đã dùng nội dung trang đọc được và ảnh khác có nguồn cụ thể; không gọi dữ liệu không tải được là đã xem. Bản vẽ cổ, ảnh sửa cầu hiện nay và ảnh năm 1972 không được coi là cùng một thời điểm. Không phát hành hình tham chiếu có quyền chưa được kiểm tra chỉ vì đã tải về được.

Bridge và vùng tệp tải xuống của cuộc trò chuyện là hai môi trường riêng. Tệp chạy, Blender, ảnh và gói nguồn được lưu thực trên PC. Không tạo đường dẫn sandbox giả cho HTML/ZIP chưa được chuyển sang vùng tệp cuộc trò chuyện. Không cần ghi nhớ xuyên hội thoại: phương pháp và điểm vào cho AI sau đã nằm trong AGENTS.md và REPRODUCE_V2.md.

## Những giới hạn còn phải giữ nguyên trong cách diễn đạt

**Lịch sử:** Không có bộ đo vẽ đầy đủ nguyên trạng năm 1972 cho từng nhà, từng dãy bệnh viện hoặc mỗi nhịp cầu sau sửa chữa. Cầu 370 m là đoạn đại diện; nhà 1.070 mẫu là mật độ cảnh, không phải thống kê lịch sử. Không gán số hiệu, tổ lái hoặc tọa độ mục tiêu thực cho đường máy.

**Vật lý:** Điều kiện đầu và thời điểm phân mảnh do tác giả chọn. Có trọng lực, cản khí, tiêu tán tiếp xúc và nghỉ nhưng không có mô phỏng áp suất nổ, FEM vật liệu, mọi mảnh va chạm nhau hoặc tính toán năng lượng từ lượng nổ. Không được gọi hiệu ứng là tái dựng pháp chứng chính xác.

**Hình ảnh:** Đây là 3D thời gian thực có bề mặt/chi tiết và bố cục được nâng cấp, chưa phải phim quay thật, quét địa hình hay mô hình hiện vật từ photogrammetry. Blender và web dùng chung hình học/texture nhưng ánh sáng và pipeline khác, nên không giống từng pixel.

**Quan sát và hiệu suất:** Camera tự do không có va chạm nhân vật và có thể xuyên vật thể. Kiểm thử trên Windows/Chrome/RTX3050Ti không chứng minh mọi điện thoại, Safari hoặc GPU đều chạy giống nhau. Giao diện nhỏ là kiểm tra viewport, không phải thiết bị thật. FPS phải đi cùng độ phân giải, DPR và mức chất lượng; phải phân biệt rAF với thời gian GPU. Những lượt thử hữu hạn không chứng minh tối ưu toàn cục hoặc không bao giờ giật trong nhiều giờ.

Không có cơ sở để khẳng định đã tìm ra phương án tối ưu duy nhất. Các lựa chọn hiện tại được kiểm tra bằng kết quả hình ảnh, độ ổn định tua và số đo GPU trong phạm vi đã ghi; những phần chưa có chứng cứ được nêu rõ thay vì gán lỗi cho người dùng.

## Kiểm tra đóng gói cuối

Kiểm tra whitespace của Git ban đầu coi CRLF Windows là khoảng trắng thừa và in quá nhiều nội dung HTML có ảnh nhúng. Đã chuyển phép kiểm tra sang chấp nhận CRLF, không dump các artifact nhúng lớn và vẫn giữ SHA-256 riêng. Một dòng `.gitignore` cũ không kết thúc bằng newline làm phần chú thích thêm vào dính vào mẫu `*.bak`; đã tách lại. Đây là lỗi thao tác của AI, không thay đổi logic/phim đã kiểm thử. Ảnh chụp cửa sổ cuối vẫn được tạo và xác nhận đúng cửa sổ dù bước kiểm tra Git sau đó từng trả lỗi.
