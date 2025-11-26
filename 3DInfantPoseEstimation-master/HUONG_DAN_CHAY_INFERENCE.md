# 🚀 Hướng Dẫn: Chạy Inference trên Ảnh/Video

## 📋 Yêu Cầu

- ✅ Đã download và giải nén SavedModels
- ✅ Đã cài đặt dependencies (`pip install -r requirements.txt`)
- ✅ Đã kích hoạt virtual environment

---

## 🎯 Cách Sử Dụng

### Bước 1: Kích hoạt Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Kiểm tra
python --version  # Nên là 3.11.x
```

### Bước 2: Chạy Inference trên Ảnh

#### Cách Đơn Giản (Khuyến nghị)

```bash
# Chạy inference trên ảnh
python inference_simple.py --image path/to/your/image.jpg
```

**Ví dụ:**
```bash
# Với ảnh trong thư mục project
python inference_simple.py --image test_image.jpg

# Với đường dẫn đầy đủ
python inference_simple.py --image F:/images/infant.jpg

# Lưu kết quả vào file cụ thể
python inference_simple.py --image test_image.jpg --output result.png
```

#### Cách Nâng Cao (Dùng Bbox Model)

Nếu bạn có bbox model và muốn tự động detect infant trong ảnh:

```bash
python inference_simple.py --image test_image.jpg --use-bbox
```

**Lưu ý:** 
- Bbox model sẽ tự động detect vị trí infant trong ảnh
- Nếu không dùng `--use-bbox`, script sẽ dùng center/scale từ ảnh (đơn giản hơn)

---

## 📁 Kết Quả

Sau khi chạy, kết quả sẽ được lưu vào:
```
Images/InferenceOutput/
└── [tên_ảnh]_result.png
```

Kết quả bao gồm:
1. **Input Image**: Ảnh gốc
2. **2D Pose Prediction**: Dự đoán pose 2D (keypoints trên ảnh)
3. **3D Pose Prediction**: Dự đoán pose 3D (skeleton 3D)

---

## 🔧 Các Tham Số

### `--image` (Bắt buộc)
- Đường dẫn đến ảnh input
- Hỗ trợ các định dạng: `.jpg`, `.jpeg`, `.png`, `.bmp`

### `--output` (Tùy chọn)
- Đường dẫn để lưu kết quả
- Nếu không chỉ định, sẽ lưu vào `Images/InferenceOutput/`

### `--use-bbox` (Tùy chọn)
- Sử dụng bbox model để tự động detect infant
- Nếu không dùng, script sẽ dùng center/scale từ ảnh

---

## 📝 Ví Dụ Đầy Đủ

### Ví Dụ 1: Chạy Inference Đơn Giản

```bash
# 1. Kích hoạt venv
venv\Scripts\activate

# 2. Chạy inference
python inference_simple.py --image my_image.jpg

# 3. Xem kết quả
# Kết quả sẽ ở: Images/InferenceOutput/my_image_result.png
```

### Ví Dụ 2: Chạy Inference với Bbox Model

```bash
# Chạy với bbox model
python inference_simple.py --image my_image.jpg --use-bbox --output result.png
```

### Ví Dụ 3: Chạy Inference trên Nhiều Ảnh

Tạo script batch:

```python
# batch_inference.py
import os
import subprocess

image_dir = "path/to/images"
output_dir = "output"

for image_file in os.listdir(image_dir):
    if image_file.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_dir, image_file)
        output_path = os.path.join(output_dir, f"{image_file}_result.png")
        
        cmd = f"python inference_simple.py --image {image_path} --output {output_path}"
        subprocess.run(cmd, shell=True)
```

---

## 🆘 Troubleshooting

### Lỗi: "FileNotFoundError: SavedModels/..."
**Nguyên nhân:** Chưa download hoặc giải nén SavedModels
**Giải pháp:**
1. Download SavedModels.zip từ [OneDrive](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)
2. Giải nén vào thư mục `SavedModels/` trong project root
3. Đảm bảo cấu trúc: `SavedModels/SavedModels/MINI_RGBD_2D/model.tar`

### Lỗi: "No module named 'X'"
**Nguyên nhân:** Chưa cài dependencies hoặc chưa kích hoạt venv
**Giải pháp:**
```bash
# Kích hoạt venv
venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt
```

### Lỗi: "CUDA out of memory"
**Nguyên nhân:** GPU không đủ bộ nhớ
**Giải pháp:**
- Script sẽ tự động fallback về CPU nếu GPU không đủ bộ nhớ
- Hoặc chỉnh sửa script để force dùng CPU: `device = torch.device("cpu")`

### Lỗi: "Image not found"
**Nguyên nhân:** Đường dẫn ảnh sai
**Giải pháp:**
- Kiểm tra đường dẫn ảnh có đúng không
- Dùng đường dẫn tuyệt đối nếu cần: `F:/images/test.jpg`

### Kết quả không chính xác
**Nguyên nhân:** 
- Ảnh không có infant hoặc infant quá nhỏ/lớn
- Ảnh có nhiều người/vật thể gây nhiễu

**Giải pháp:**
- Đảm bảo ảnh có infant rõ ràng ở giữa
- Thử dùng `--use-bbox` để tự động detect infant
- Crop ảnh để chỉ có infant ở giữa

---

## 💡 Mẹo Sử Dụng

1. **Ảnh tốt nhất:**
   - Ảnh có infant rõ ràng ở giữa
   - Ảnh có độ phân giải cao
   - Ảnh có ánh sáng tốt
   - Ảnh không có nhiều vật thể gây nhiễu

2. **Tốc độ:**
   - Chạy trên GPU sẽ nhanh hơn CPU
   - Nếu không có GPU, script sẽ tự động dùng CPU (chậm hơn)

3. **Batch Processing:**
   - Tạo script batch để xử lý nhiều ảnh cùng lúc
   - Xem ví dụ ở trên

---

## 📚 Tài Liệu Liên Quan

- **Hướng dẫn sử dụng model có sẵn:** `HUONG_DAN_SU_DUNG_MODEL_CO_SAN.md`
- **Phân biệt SavedModels vs Dataset:** `PHAN_BIET_SAVEDMODELS_VS_DATASET.md`
- **FAQ:** `FAQ_DATASET.md`

---

## ✅ Checklist

Trước khi chạy, đảm bảo:
- [x] Đã kích hoạt virtual environment
- [x] Đã có SavedModels trong thư mục `SavedModels/`
- [x] Đã có ảnh để test
- [x] Đã cài đặt dependencies

---

**Chúc bạn thành công! 🎉**

