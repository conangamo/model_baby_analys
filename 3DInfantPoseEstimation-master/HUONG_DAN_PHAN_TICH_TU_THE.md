# 📋 HƯỚNG DẪN SỬ DỤNG: PHÂN TÍCH TƯ THẾ VÀ CẢNH BÁO NGUY HIỂM

## ✅ Chức năng đã được thêm

Hệ thống đã được tích hợp chức năng phân tích tư thế và phát hiện cảnh báo nguy hiểm dựa trên keypoints 3D.

### Các tư thế có thể nhận diện:
- **lying_on_back**: Nằm ngửa
- **lying_on_stomach**: Nằm sấp (⚠️ NGUY HIỂM)
- **standing**: Đứng
- **sitting**: Ngồi
- **transitioning**: Đang chuyển tư thế
- **unknown**: Không xác định được

### Các cảnh báo nguy hiểm:
- **SIDS Risk**: Trẻ nằm sấp - nguy cơ SIDS (Sudden Infant Death Syndrome)
- **Suffocation Risk**: Tư thế có thể gây nghẹt thở (góc cổ quá gập)
- **Abnormal Posture**: Tư thế bất thường (góc khớp ngoài phạm vi bình thường)
- **Head Position**: Vị trí đầu không tối ưu

---

## 🚀 Cách sử dụng

### Bước 1: Chạy inference với ảnh

```bash
# Chạy inference và phân tích tư thế
python inference_with_keypoints.py --image path/to/image.jpg

# Hoặc chỉ định đường dẫn output
python inference_with_keypoints.py --image path/to/image.jpg --output output.png

# Lưu thêm CSV
python inference_with_keypoints.py --image path/to/image.jpg --save-csv
```

### Bước 2: Xem kết quả

Kết quả sẽ được lưu trong thư mục `Images/InferenceOutput/`:

1. **Ảnh visualization** (`*_result.png`):
   - Hiển thị ảnh input, 2D pose, 3D pose
   - **Thông tin tư thế** được hiển thị trên ảnh 2D pose
   - **Cảnh báo nguy hiểm** (nếu có) được hiển thị bằng màu đỏ/vàng

2. **File JSON** (`*_keypoints.json`):
   - Chứa tọa độ 2D và 3D của các keypoints
   - **Thêm section `pose_analysis`** với:
     - Tư thế được nhận diện
     - Độ tin cậy
     - Mức độ nguy hiểm
     - Cảnh báo chi tiết
     - Góc các khớp

3. **File CSV** (`*_keypoints.csv`) - tùy chọn:
   - Chứa tọa độ keypoints dạng bảng

---

## 📊 Output Format

### JSON Output Example

```json
{
  "keypoints_2d": {...},
  "keypoints_3d": {...},
  "pose_analysis": {
    "posture": "lying_on_stomach",
    "confidence": 0.92,
    "danger_level": "HIGH",
    "danger_message": "🚨 NGUY HIỂM: Trẻ đang nằm sấp - Nguy cơ SIDS!",
    "recommendation": "Khuyến nghị: Đặt trẻ nằm ngửa ngay lập tức",
    "reasoning": "Spine angle 25.3° (nằm ngang), head lower than thorax",
    "angles": {
      "spine_angle": 25.3,
      "knee_left": 165.2,
      "knee_right": 163.8,
      "neck_angle": 135.5
    },
    "warnings": [
      {
        "type": "SIDS_RISK",
        "severity": "HIGH",
        "message": "Trẻ đang nằm sấp - nguy cơ SIDS"
      }
    ]
  }
}
```

### Console Output Example

```
✅ 3D pose đã được dự đoán

5. Đang phân tích tư thế...
   📊 TƯ THẾ: lying_on_stomach
   - Độ tin cậy: 92.0%
   - Lý do: Spine angle 25.3° (nằm ngang), head lower than thorax
   🚨 NGUY HIỂM: Trẻ đang nằm sấp - Nguy cơ SIDS!
   💡 Khuyến nghị: Đặt trẻ nằm ngửa ngay lập tức
   - Góc cột sống: 25.3°
   - Góc đầu gối (TB): 164.5°
   ✅ Phân tích tư thế hoàn tất
```

---

## 🎨 Visualization

### Màu sắc cảnh báo trên ảnh:

- **🟢 Xanh lá**: An toàn (danger_level = NONE)
- **🟡 Vàng**: Cần theo dõi (danger_level = LOW)
- **🟠 Cam**: Cảnh báo (danger_level = MEDIUM)
- **🔴 Đỏ**: Nguy hiểm (danger_level = HIGH)

### Thông tin hiển thị trên ảnh:

1. **Góc trên trái ảnh 2D pose**:
   - Tư thế được nhận diện
   - Độ tin cậy (%)

2. **Góc dưới trái ảnh 2D pose**:
   - Cảnh báo nguy hiểm (nếu có)
   - Khuyến nghị (nếu có)
   - Hoặc thông báo "✅ An toàn"

3. **Góc trên trái ảnh 3D pose**:
   - Góc cột sống
   - Góc đầu gối trái/phải

---

## 🔧 Cách hoạt động

### 1. Phân tích tư thế dựa trên:
- **Góc cột sống** với mặt phẳng ngang
- **Vị trí tương đối** của đầu so với thân
- **Góc đầu gối** (để phân biệt đứng/ngồi)

### 2. Phát hiện nguy hiểm dựa trên:
- **Nằm sấp**: Góc cột sống < 45° + đầu thấp hơn thân → SIDS risk
- **Nghẹt thở**: Góc cổ < 45° → Suffocation risk
- **Bất thường**: Góc khớp < 30° hoặc > 180° → Abnormal posture

### 3. Xử lý missing keypoints:
- Tự động kiểm tra keypoint hợp lệ
- Báo lỗi nếu thiếu keypoints quan trọng
- Ước lượng keypoint nếu có thể

---

## 📝 Lưu ý

1. **Không cần training lại**: Chức năng này chỉ là post-processing, không cần train model mới
2. **Sử dụng model hiện có**: Chỉ cần keypoints 3D từ model hiện tại
3. **Độ chính xác**: Phụ thuộc vào độ chính xác của model pose estimation
4. **Xử lý edge cases**: Tự động xử lý missing keypoints và góc bất thường

---

## ⚠️ Cảnh báo quan trọng

**Hệ thống này chỉ là công cụ hỗ trợ, KHÔNG thay thế sự giám sát của con người.**

- Luôn để mắt đến trẻ, đặc biệt khi trẻ ngủ
- Kiểm tra trẻ thường xuyên
- Nếu phát hiện cảnh báo nguy hiểm, cần kiểm tra ngay lập tức
- Không dựa hoàn toàn vào hệ thống tự động

---

## 🐛 Troubleshooting

### Lỗi: "Missing required keypoints"
- **Nguyên nhân**: Model không detect được keypoints quan trọng (pelvis, thorax)
- **Giải pháp**: Kiểm tra ảnh input, đảm bảo trẻ được nhìn thấy rõ

### Lỗi: "Cannot calculate spine angle"
- **Nguyên nhân**: Không tính được góc cột sống
- **Giải pháp**: Kiểm tra keypoints pelvis và thorax có hợp lệ không

### Kết quả "unknown"
- **Nguyên nhân**: Thiếu keypoints hoặc không đủ thông tin để phân loại
- **Giải pháp**: Kiểm tra ảnh input, đảm bảo tất cả keypoints được detect

---

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra lại ảnh input
2. Kiểm tra model đã được load đúng chưa
3. Xem console output để biết chi tiết lỗi
4. Tham khảo file `PHAN_TICH_QUY_TRINH.md` để hiểu cách hoạt động

---

**Chúc bạn sử dụng thành công! 🎉**

