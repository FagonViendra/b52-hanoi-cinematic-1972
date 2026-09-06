# Nhật ký lỗi, trách nhiệm và giới hạn

## Lỗi do phần thực hiện của AI

1. **Truyền nguồn ban đầu:** một chuỗi gzip/base64 bị chép sai và bị lặp trong thao tác sửa đầu tiên, dẫn đến lỗi giải nén. Đã phục hồi và đối chiếu CRC/SHA trước khi dựng. Những lần sau dùng các tệp văn bản nhỏ, không dùng bản truyền hỏng làm nguồn.
2. **Giả định API Blender:** truy cập node bằng tên tiếng Anh thất bại trên bản Blender có giao diện địa phương hóa. Đã tạo node bằng type, tìm Background bằng type; không phụ thuộc tên hiển thị.
3. **Mã thoát/cảnh báo:** PowerShell ban đầu coi cảnh báo stderr của Blender là lỗi. Quy trình mới thu log qua subprocess và bắt mã thoát Python bằng `--python-exit-code 2`. Không đánh đồng “tiến trình kết thúc” với “mô hình hợp lệ”.
4. **Hình học kiến trúc:** đầu hồi nhà hở, hướng mái dãy bệnh viện sai, nhà quá lặp và tàn tích giống hàng cọc. Đã đóng đầu hồi, đổi trục mái, thêm kiểu nhà và tạo mép gãy/rubble nối tiếp. Mô hình vẫn là kiến trúc diễn giải, không có hồ sơ đo vẽ từng nhà.
5. **Mảnh xác:** các bản đầu quá giống lồng ống hoặc các tam giác giấy gấp. Đã thay bằng lưới vỏ cong chung đỉnh, khối vỏ gãy, gân và cụm bánh. Hình dạng cuối chưa phải bản quét chính xác hiện vật.
6. **Máy bay:** một ảnh kiểm tra từ trên bị cắt mũi/đuôi; một góc dưới bụng phim cắt cánh quá nhiều. Đã tăng khung ortho và khoảng cách đường máy. Kiểm tra bổ sung sau đó phát hiện cánh có dây cung quá rộng dù sải cánh/chiều dài đã đúng. Đã hiệu chỉnh diện tích mặt bằng và lưu phép tính ở `qa/wing_planform_audit.json`. Đây là một thiếu sót của cách kiểm tra chỉ bằng bounding box; không phải lỗi của người dùng.
7. **Shader và mỹ thuật:** bầu trời thiếu đổi màu sRGB, có quầng mặt trời trong cảnh đêm, nước lặp dạng ô, mây dựng như dải đứng, ngụy trang quá nhạt, nổ bị sáng trắng. Đã sửa không gian màu, bỏ đĩa sáng ở cảnh đêm, đổi nhiễu nước, làm lớp mây ngang, giảm sáng lửa và chỉnh màu ngụy trang.
8. **Giao diện nhỏ:** nút hàng dưới bị ép xuống dòng ở viewport ngang 844 px. Đã giữ chữ nút trên một dòng và đổi quy tắc responsive. Camera màn hình dọc được lùi xa để tránh cắt máy bay.
9. **Kiểm tra bộ nhớ:** lượt đầu thấy geometry tăng 265 -> 266 và đánh trượt. Không bỏ qua kết quả; đã chạy warm-up độc lập rồi 70 lần đổi cảnh, kiểm tra ổn định. Tăng lần đầu là lazy upload của hình học mới thấy, không có tăng tiếp trong lượt kiểm tra lặp đã chạy.
10. **Hai lệnh kiểm tra văn bản:** dùng nhầm từ “sixty” / “forty” thay cho số nguyên ở Select-Object. Hai lệnh chỉ đọc thất bại, không làm thay đổi dữ liệu. Đã sửa thành số và đọc lại nguồn.

## Trở ngại công cụ/nguồn, không phải lỗi của người dùng

- Có lần gọi bridge trả “fetch failed”; đã kiểm tra tệp chưa được ghi rồi gửi lại phần nhỏ. Một lần gọi kiểm thử trình duyệt không được thực thi vì dịch vụ không xác định được trạng thái an toàn; bản kiểm thử dùng cấu hình Playwright/Chrome mặc định đã chạy, không tắt bảo vệ trình duyệt.
- Một số trang tài liệu và PDF trả 402/403, lỗi nội bộ hoặc hết thời gian. Không coi nội dung không đọc được là chứng cứ. Những số liệu lấy được được phân biệt với giả định hình học. Một PDF kiểm tra hình dáng là nghiên cứu B-52 họ H, chỉ dùng đối chiếu diện tích chung, không gán thành bản vẽ chế tạo biến thể D.
- Một kết quả ảnh mang “1972” trong tên tệp lại được chụp năm 2021; đã loại. Hai ảnh hiện trạng 2007/2009 được ghi đúng năm và chỉ dùng làm tham chiếu hiện vật/kết cấu.
- Nhiều ảnh lịch sử không có giấy phép tái phân phối rõ ràng; hồ sơ dẫn liên kết thay vì nhúng trái phép.
- PC bridge và vùng tệp tải xuống trong cuộc trò chuyện là hai môi trường khác nhau. Dự án chính được tạo trực tiếp trong thư mục PC đã nêu; không bịa đường dẫn sandbox cho tệp chưa được chuyển.

## Giới hạn còn lại của bản giao

Đây là ngoại cảnh 3D thời gian thực theo phong cách diễn giải, chưa phải hình ảnh giống quay người thật, photogrammetry hoặc phục dựng khảo cổ từng công trình. Địa hình hữu hạn; cầu rút gọn; cảng và phố không có tọa độ đo đạc. Chuyển động bom, nổ, khói và thay trạng thái nhà nhằm kể chuyện, không phải mô phỏng khí động, kết cấu hay đạn đạo chính xác. Không có mô hình người/diễn xuất nhân vật, không có nội thất B-52, không có lồng tiếng tư liệu.

Camera tự do có thể xuyên vật thể; đây là chế độ quan sát, không phải điều khiển nhân vật có va chạm. Bản xuất GLB và HTML không có shader/bề mặt pixel-identical. Phản chiếu hồ và khói là kỹ thuật gần đúng.

Chưa kiểm thử trên Safari, điện thoại thật hoặc mọi GPU. Viewport nhỏ chỉ là mô phỏng kích thước trình duyệt. FPS là thống kê khoảng cách giữa các callback requestAnimationFrame; CPU submit không phải thời gian GPU đo bằng timestamp query. Những khoảng lấy mẫu hữu hạn không chứng minh không bao giờ có giật hoặc rò rỉ trong hàng giờ. Có khung chậm đơn lẻ trong lượt chạy cửa sổ; xem số thực tế ở QA_REPORT.md, không diễn giải thành “không hề khựng”.

**Không ghi nhận lỗi nào do người dùng gây ra.** Các thiếu sót dựng hình, bố cục, mã và chiến lược kiểm tra nêu trên thuộc phần thực hiện của AI.

## Điều tra bổ sung so sánh ảnh hồ

Sau hiệu chỉnh cánh, một lượt kiểm thử so sánh PNG tuyệt đối và một lượt so sánh RGB tuyệt đối đánh trượt cảnh hồ. Đã lưu cả báo cáo trượt, ảnh trước/sau và ảnh chênh lệch, không ghi đè để che kết quả. Phép đo RGB tìm thấy **7 pixel trong 1.296.000 pixel, mỗi pixel chênh tối đa 1 mức màu 8-bit**, trung bình chênh khoảng 0,0000018 trên mỗi kênh. Không có biến đổi hình học nhìn thấy; ảnh chênh lệch khuếch đại đã được xem. Năm vòng kiểm tra hồ độc lập khác cho chênh lệch bằng 0.

Tiêu chí cảnh hồ được ghi rõ thành tối đa 1 mức màu, trên không quá 0,001% số pixel. Không gọi điều đó là “giống từng pixel tuyệt đối”. Kiểm tra phố nguyên vẹn/đổ nát vẫn yêu cầu bằng nhau tuyệt đối. Nguyên nhân sâu trong lượng tử hóa/làm tròn pipeline GPU chưa được xác định chắc chắn; không khẳng định đã sửa một lỗi shader khi chưa có bằng chứng. Hai lượt kiểm thử độc lập cuối cùng phải đạt tiêu chí đã công bố này.

## Xác nhận cửa sổ và mã thoát tổng hợp

Ảnh `desktop_verification.png` của lượt chạy cửa sổ thật đã chụp dashboard bridge đang ở trước, không phải phim; môi trường đang có nhiều tác vụ. Không dùng ảnh này để chứng minh phim ở foreground. Ảnh `headed_chrome.png` là nội dung trang của chính trình duyệt `headless=False` được kiểm thử; phép đo rAF và lỗi vẫn lấy từ trang đó. Lượt mở tệp cuối kiểm tra handle foreground riêng và lưu `final_open_verification.json`; chỉ khi có xác nhận đúng handle mới chụp `final_desktop_film.png`.

Một pipeline PowerShell chạy nhiều chương trình nối tiếp đã kết thúc mã 0 dù phép so ảnh hồ trung gian đánh trượt 38/39; chương trình cuối trả mã 0 đã che trạng thái trung gian ở cấp pipeline. Không dùng mã tổng hợp đó để duyệt phát hành. Các lượt lặp sau kiểm tra `$LASTEXITCODE` ngay sau từng test; bước đóng gói còn đọc và assert nội dung báo cáo 39/39, lỗi shader/JS rỗng, phim kết thúc đủ thời gian và checksum dựng lại trước khi tạo ZIP. Đây là lỗi tổ chức kiểm thử của AI, không phải lỗi của người dùng.

Ảnh cuối `final_desktop_film.png` đã được cắt theo đúng khung cửa sổ dự án để không đưa các ứng dụng khác trên desktop vào gói bàn giao. Ảnh dashboard `desktop_verification.png` không đưa vào ZIP.
