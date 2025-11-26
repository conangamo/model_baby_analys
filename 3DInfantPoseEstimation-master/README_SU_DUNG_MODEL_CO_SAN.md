# ✅ Hướng Dẫn Nhanh: Sử Dụng Model Có Sẵn

## 🎯 Mục Đích Của Bạn

Bạn muốn **dùng model có sẵn**, **KHÔNG cần train lại model từ đầu**.

---

## ✅ Những Gì Bạn CẦN

### 1. **SavedModels** (Bắt buộc)
- ✅ Download từ [OneDrive](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)
- ✅ Giải nén vào thư mục `SavedModels/` trong project
- ✅ Chứa các model đã train sẵn (pretrained models)

### 2. **Dependencies** (Bắt buộc)
- ✅ Cài đặt: `pip install -r requirements.txt`
- ✅ Kích hoạt virtual environment: `venv\Scripts\activate`

---

## ❌ Những Gì Bạn KHÔNG CẦN

### 1. **Dataset MINI-RGBD** (KHÔNG CẦN!)
- ❌ **KHÔNG CẦN** download dataset MINI-RGBD
- ❌ **KHÔNG CẦN** sửa đường dẫn dataset trong Config.py
- ❌ Dataset chỉ cần nếu muốn **train** hoặc **evaluate trên test set**

### 2. **Sửa Config.py** (KHÔNG CẦN!)
- ❌ **KHÔNG CẦN** sửa đường dẫn dataset trong Config.py
- ❌ Config.py chỉ cần sửa nếu muốn train/evaluate với dataset

---

## 🚀 Bước Tiếp Theo

### Bước 1: Kiểm tra SavedModels

Đảm bảo bạn có các file model:
```
SavedModels/SavedModels/
├── MINI_RGBD_2D/model.tar
├── MINI_RGBD_Bbox/model.tar
├── MINI_RGBD_FineTune/model.tar
└── ...
```

### Bước 2: Sử dụng Model

**Có 2 cách:**

#### Cách 1: Chạy Inference trên Ảnh/Video Mới (Khuyến nghị)
- Tạo script inference để load ảnh/video từ file
- Load model từ SavedModels
- Chạy inference và visualize kết quả
- **Xem hướng dẫn chi tiết:** `HUONG_DAN_SU_DUNG_MODEL_CO_SAN.md`

#### Cách 2: Evaluate trên Test Set (Cần dataset)
- **CẦN** download dataset MINI-RGBD
- **CẦN** sửa đường dẫn trong Config.py
- Chạy `python PoseEstimation/Core/Evaluation.py`
- **Xem hướng dẫn:** `HUONG_DAN_SUA_DUONG_DAN.md`

---

## 📝 Tóm Tắt

| Bạn muốn | Cần SavedModels? | Cần Dataset? | Cần sửa Config.py? |
|----------|------------------|--------------|-------------------|
| **Chạy inference** | ✅ Có | ❌ Không | ❌ Không |
| **Evaluate test set** | ✅ Có | ✅ Có | ✅ Có |
| **Train model** | ❌ Không | ✅ Có | ✅ Có |

---

## 🔍 Câu Hỏi Thường Gặp

### Q: Tôi có cần sửa đường dẫn trong Config.py không?
**A:** **KHÔNG**, nếu bạn chỉ muốn chạy inference trên ảnh/video mới. Chỉ cần sửa nếu muốn train/evaluate với dataset.

### Q: Tôi có cần download dataset MINI-RGBD không?
**A:** **KHÔNG**, nếu bạn chỉ muốn chạy inference. Dataset chỉ cần nếu muốn train hoặc evaluate trên test set.

### Q: SavedModels và Dataset có khác nhau không?
**A:** **CÓ!** 
- **SavedModels** = Model đã train sẵn (có trong dự án, download từ OneDrive)
- **Dataset MINI-RGBD** = Dữ liệu training (KHÔNG có trong dự án, cần download riêng, rất lớn)

**👉 Xem chi tiết:** `PHAN_BIET_SAVEDMODELS_VS_DATASET.md`

---

## 📚 Tài Liệu Chi Tiết

- **Hướng dẫn sử dụng model có sẵn:** `HUONG_DAN_SU_DUNG_MODEL_CO_SAN.md`
- **Phân biệt SavedModels vs Dataset:** `PHAN_BIET_SAVEDMODELS_VS_DATASET.md`
- **Hướng dẫn sửa đường dẫn:** `HUONG_DAN_SUA_DUONG_DAN.md`
- **FAQ:** `FAQ_DATASET.md`

---

## ✅ Checklist

- [x] Đã download và giải nén SavedModels
- [x] Đã cài đặt dependencies
- [x] Đã kích hoạt virtual environment
- [ ] **KHÔNG CẦN** download dataset MINI-RGBD
- [ ] **KHÔNG CẦN** sửa đường dẫn dataset trong Config.py

---

**🎉 Kết luận: Bạn chỉ cần SavedModels, KHÔNG CẦN dataset!**

