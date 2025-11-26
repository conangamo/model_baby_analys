# Quy trình phát triển kết quả & phân tích tư thế

## 1. Chuẩn hóa đầu vào
- **Kiểm tra bbox:** chạy inference với `--use-bbox` hoặc tự cung cấp bbox đã kiểm chứng để tránh crop lệch khỏi cơ thể.
- **Tiền xử lý ảnh:** áp dụng cân bằng sáng/denoise nhẹ trước khi đưa vào model; đảm bảo ảnh đầu vào luôn được resize về 256×256 đúng tỷ lệ.
- **Kiểm tra cấu hình:** rà lại `DataSets/Utils/Config.py` và các đường dẫn SavedModels để chắc chắn không load nhầm checkpoint.

## 2. Cải thiện mô hình 2D
- **Fine-tune ResNet50:** gom dữ liệu trẻ thật (dù ít), chuẩn bị annotation 2D, huấn luyện lại bằng `PoseEstimation/Core/Trainer.py`.
- **Augment chuyên biệt:** thêm xoay ±30°, flip, jitter màu vào pipeline train để model vững trước nhiều tư thế/kịch bản ánh sáng.
- **Post-process mềm:** cân nhắc thay argmax bằng soft-argmax hoặc tăng kích thước heatmap (ví dụ 128) để tọa độ mượt hơn.

## 3. Nâng cấp lifting 3D
- **Huấn luyện lại LiftingNetwork:** dùng bộ keypoint 2D/3D gần domain hiện tại (có thể lấy output 2D mới + GT 3D) để fine-tune `LiftingNetwork3D`.
- **Regularize & chuẩn hóa:** thêm dropout nhỏ và chuẩn hóa đầu vào theo pelvis để giảm nhiễu khi 2D sai lệch chút ít.
- **End-to-end:** nếu có dữ liệu depth, xem xét huấn luyện đồng thời 2D & 3D để tối ưu chung toàn pipeline.

## 4. Điều chỉnh PoseAnalyzer
- **Hiệu chỉnh ngưỡng:** thống kê góc thực tế từ dữ liệu của bạn rồi cập nhật `ANGLE_THRESHOLDS` và `POSITION_THRESHOLDS` cho sát thực tế.
- **Xử lý thiếu khớp:** thêm logic giảm trọng số cảnh báo khi keypoint quan trọng vắng mặt hoặc độ tin cậy thấp.
- **Ghi log trung gian:** log spine angle, head delta, neck angle… cho từng ảnh để truy vết nhanh trường hợp phân tích sai.

## 5. Đánh giá & lặp lại
- **Bộ test mini:** chuẩn bị vài chục ảnh đã gán nhãn posture/danger thật, chạy inference, so sánh kết quả → đo % chính xác.
- **Ưu tiên điểm yếu:** nếu sai nhiều ở crop → cải thiện bbox; nếu sai ở 2D → tập trung fine-tune 2D trước khi chạm PoseAnalyzer.
- **Lưu snapshot:** sau mỗi lần chỉnh, lưu checkpoint + config để tiện rollback và so sánh về sau.

> Khi cần script huấn luyện hoặc template log, có thể mở rộng tài liệu này bằng cách thêm ví dụ lệnh, bảng theo dõi hoặc checklist cho từng giai đoạn.

