# 🚀 Hướng Dẫn Nhanh: Chạy Inference

## ✅ Đã Hoàn Thành Setup Cho Bạn!

Bạn đã chọn **"Trường Hợp 1: Chỉ Chạy Inference"**, vậy bạn **KHÔNG CẦN**:
- ❌ Download dataset MINI-RGBD
- ❌ Sửa đường dẫn dataset trong Config.py
- ❌ Train model

Bạn **CHỈ CẦN**:
- ✅ SavedModels (download từ OneDrive)
- ✅ Dependencies đã cài đặt
- ✅ Script inference (`inference_simple.py`)

---

## 🎯 Bước Tiếp Theo

### Bước 1: Kiểm tra Setup

```bash
# Kích hoạt virtual environment
venv\Scripts\activate

# Chạy script test
python test_inference.py
```

Script sẽ kiểm tra:
- ✅ Imports có đầy đủ không
- ✅ SavedModels có tồn tại không
- ✅ Có thể load models không

### Bước 2: Chạy Inference

```bash
# Chạy inference trên ảnh của bạn
python inference_simple.py --image path/to/your/image.jpg
```
python inference_with_keypoints.py --image Images/baby7.jpg
**Ví dụ:**
```bash
# Với ảnh trong thư mục project
python inference_simple.py --image test_image.jpg

# Với đường dẫn đầy đủ
python inference_simple.py --image F:/images/infant.jpg

# Lưu kết quả vào file cụ thể
python inference_simple.py --image test_image.jpg --output result.png
```

### Bước 3: Xem Kết Quả

Kết quả sẽ được lưu vào:
```
Images/InferenceOutput/
└── [tên_ảnh]_result.png
```

Kết quả bao gồm:
1. **Input Image**: Ảnh gốc
2. **2D Pose Prediction**: Dự đoán pose 2D (keypoints)
3. **3D Pose Prediction**: Dự đoán pose 3D (skeleton 3D)

---

## 📋 Checklist

Trước khi chạy, đảm bảo:
- [x] Đã kích hoạt virtual environment
- [x] Đã download SavedModels từ OneDrive
- [x] Đã giải nén SavedModels vào thư mục `SavedModels/`
- [x] Đã có ảnh để test
- [x] Đã chạy `test_inference.py` và pass tất cả tests

---

## 🆘 Nếu Gặp Lỗi

### Lỗi: "FileNotFoundError: SavedModels/..."
**Giải pháp:**
1. Download SavedModels.zip từ [OneDrive](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)
2. Giải nén vào thư mục `SavedModels/` trong project root
3. Đảm bảo cấu trúc: `SavedModels/SavedModels/MINI_RGBD_2D/model.tar`

### Lỗi: "No module named 'X'"
**Giải pháp:**
```bash
# Kích hoạt venv
venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt
```

### Lỗi: "Image not found"
**Giải pháp:**
- Kiểm tra đường dẫn ảnh có đúng không
- Dùng đường dẫn tuyệt đối nếu cần: `F:/images/test.jpg`

---

## 📚 Tài Liệu Chi Tiết

- **Hướng dẫn chạy inference:** `HUONG_DAN_CHAY_INFERENCE.md`
- **Hướng dẫn sử dụng model có sẵn:** `HUONG_DAN_SU_DUNG_MODEL_CO_SAN.md`
- **Phân biệt SavedModels vs Dataset:** `PHAN_BIET_SAVEDMODELS_VS_DATASET.md`

---

## ✅ Tóm Tắt

| Bạn muốn | Cần SavedModels? | Cần Dataset? | Cần sửa Config.py? |
|----------|------------------|--------------|-------------------|
| **Chạy inference** | ✅ Có | ❌ Không | ❌ Không |

---

**🎉 Chúc bạn thành công!**

