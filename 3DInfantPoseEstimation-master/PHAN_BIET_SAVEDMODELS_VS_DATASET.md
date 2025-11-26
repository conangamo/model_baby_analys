# 📚 Phân Biệt: SavedModels vs Dataset

## ❓ Câu Hỏi Thường Gặp

**"Dataset MINI-RGBD có phải là thư mục SavedModels trong dự án không?"**

**Trả lời: KHÔNG! Đây là 2 thứ hoàn toàn khác nhau.**

---

## 🔍 Sự Khác Biệt

### 1️⃣ **SavedModels** (Thư mục trong dự án)

**Là gì?**
- ✅ Các **model đã được train sẵn** (pretrained models)
- ✅ File `.tar` chứa weights của neural network
- ✅ Đã được train trên dataset MINI-RGBD
- ✅ Dùng để **chạy inference** (dự đoán pose từ ảnh/video mới)

**Ở đâu?**
- 📁 Thư mục: `SavedModels/SavedModels/`
- 📦 Download từ: [OneDrive link](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)
- 💾 Kích thước: Khoảng vài trăm MB đến vài GB

**Khi nào cần?**
- ✅ **LUÔN CẦN** nếu muốn chạy inference/evaluation
- ❌ Không cần nếu chỉ muốn train lại từ đầu

**Cấu trúc:**
```
SavedModels/
└── SavedModels/
    ├── MINI_RGBD_2D/
    │   └── model.tar
    ├── MINI_RGBD_Bbox/
    │   └── model.tar
    ├── MINI_RGBD_Lift3D/
    │   └── model.tar
    └── ...
```

---

### 2️⃣ **Dataset MINI-RGBD** (Cần download riêng)

**Là gì?**
- ✅ **Dữ liệu training/evaluation** (ảnh, video, annotations)
- ✅ Hàng nghìn ảnh và file annotation
- ✅ Dùng để **train model** hoặc **evaluate model**
- ✅ Dataset gốc từ nghiên cứu khoa học

**Ở đâu?**
- 📁 **KHÔNG có sẵn trong dự án** - cần download riêng
- 🌐 Download từ: [Website chính thức](https://www.iosb.fraunhofer.de/servlet/is/82920/)
- 💾 Kích thước: **Rất lớn** (hàng chục GB đến vài trăm GB)

**Khi nào cần?**
- ✅ Cần nếu muốn **train model mới**
- ✅ Cần nếu muốn **evaluate trên test set**
- ❌ **KHÔNG CẦN** nếu chỉ muốn chạy inference trên dữ liệu mới

**Cấu trúc:**
```
MINI-RGBD/
├── 01/
│   ├── rgb/
│   │   ├── syn_00000.png
│   │   ├── syn_00001.png
│   │   └── ... (1000 ảnh)
│   ├── joints_2Ddep/
│   │   ├── syn_joints_2Ddep_00000.txt
│   │   └── ... (1000 file)
│   ├── joints_3D/
│   │   ├── syn_joints_3D_00000.txt
│   │   └── ... (1000 file)
│   └── fg_mask/
│       ├── mask_00000.png
│       └── ... (1000 ảnh)
├── 02/
├── 03/
└── ... (12 video sequences)
```

---

## 📊 So Sánh

| Đặc điểm | SavedModels | Dataset MINI-RGBD |
|----------|-------------|-------------------|
| **Loại** | Model đã train | Dữ liệu raw |
| **Kích thước** | Vài trăm MB - vài GB | Hàng chục - vài trăm GB |
| **Có sẵn?** | Có (download từ OneDrive) | Không (download từ website) |
| **Dùng để** | Inference, Evaluation | Training, Evaluation |
| **Cần khi nào?** | Luôn cần (để chạy) | Chỉ cần khi train/evaluate |
| **Đường dẫn config** | Không cần cấu hình | Cần cấu hình trong Config.py |

---

## 🎯 Khi Nào Cần Dataset?

### ❌ **KHÔNG CẦN Dataset nếu:**
- Bạn chỉ muốn **chạy inference** trên ảnh/video mới
- Bạn chỉ muốn **test model** đã có sẵn
- Bạn không có đủ dung lượng lưu trữ (dataset rất lớn)

### ✅ **CẦN Dataset nếu:**
- Bạn muốn **train lại model** từ đầu
- Bạn muốn **fine-tune model** trên dữ liệu mới
- Bạn muốn **evaluate chính xác** trên test set
- Bạn muốn **nghiên cứu/thử nghiệm** với dataset

---

## 📥 Cách Download Dataset MINI-RGBD

### Bước 1: Truy cập website
🌐 Link: https://www.iosb.fraunhofer.de/servlet/is/82920/

### Bước 2: Đăng ký/Đăng nhập
- Có thể cần đăng ký tài khoản
- Hoặc liên hệ với tác giả để xin quyền truy cập

### Bước 3: Download dataset
- Download tất cả các file (có thể chia thành nhiều phần)
- Giải nén vào một thư mục (ví dụ: `F:/datasets/MINI-RGBD/`)

### Bước 4: Cấu hình đường dẫn
Sửa file `DataSets/Utils/Config.py`:
```python
MINI_RGBD = {
    "basePath": "F:/datasets/MINI-RGBD/",  # Đường dẫn đến thư mục đã giải nén
    ...
}
```

---

## 🔧 Cấu Hình Cho Từng Trường Hợp

### Trường Hợp 1: Chỉ Chạy Inference (Không cần dataset)

**Bạn cần:**
- ✅ SavedModels (download từ OneDrive)
- ❌ Dataset MINI-RGBD (không cần)

**Config.py:**
- Không cần sửa đường dẫn MINI_RGBD (có thể để mặc định hoặc comment lại)

**Chạy:**
```python
# Chạy inference trên ảnh/video mới
python inference.py  # (cần viết script này)
```

---

### Trường Hợp 2: Chạy Evaluation (Cần dataset)

**Bạn cần:**
- ✅ SavedModels (download từ OneDrive)
- ✅ Dataset MINI-RGBD (download từ website)

**Config.py:**
- Cần sửa đường dẫn MINI_RGBD

**Chạy:**
```python
# Chạy evaluation trên test set
python PoseEstimation/Core/Evaluation.py
```

---

### Trường Hợp 3: Train Model (Cần dataset)

**Bạn cần:**
- ✅ Dataset MINI-RGBD (download từ website)
- ❌ SavedModels (không cần, sẽ tạo mới sau khi train)

**Config.py:**
- Cần sửa đường dẫn MINI_RGBD
- Có thể cần cấu hình thêm MPII, MPI_INF (để transfer learning)

**Chạy:**
```python
# Train model
python PoseEstimation/Core/Trainer.py
```

---

## ⚠️ Lưu Ý Quan Trọng

1. **Dataset rất lớn**: MINI-RGBD có thể lên đến vài trăm GB
   - Đảm bảo có đủ dung lượng ổ cứng
   - Download có thể mất nhiều thời gian

2. **Quyền truy cập**: Dataset có thể cần đăng ký/xin quyền
   - Liên hệ với tác giả dataset nếu cần
   - Hoặc tìm dataset tương tự khác

3. **Không bắt buộc**: Nếu bạn chỉ muốn test/inference, không cần download dataset

4. **Đường dẫn**: Nếu không có dataset, có thể comment/ignore lỗi đường dẫn trong Config.py

---

## 🆘 Câu Hỏi Thường Gặp

### Q: Tôi có thể chạy code mà không có dataset không?
**A:** Có, nếu bạn chỉ muốn chạy inference. Nhưng một số script (như Evaluation.py) sẽ cần dataset.

### Q: Dataset có miễn phí không?
**A:** Tùy thuộc vào chính sách của tác giả. Một số dataset yêu cầu đăng ký hoặc xin quyền.

### Q: Tôi có thể dùng dataset khác không?
**A:** Có, nhưng cần:
- Cấu trúc dataset tương tự
- Sửa code để load dataset mới
- Hoặc tạo dataset loader mới

### Q: SavedModels có đủ để chạy không?
**A:** Có, nếu bạn chỉ muốn chạy inference. SavedModels chứa model đã train sẵn, không cần dataset.

---

## 📝 Tóm Tắt

| Bạn muốn làm gì? | Cần SavedModels? | Cần Dataset? |
|------------------|------------------|--------------|
| Chạy inference | ✅ Có | ❌ Không |
| Chạy evaluation | ✅ Có | ✅ Có |
| Train model | ❌ Không | ✅ Có |
| Fine-tune | ✅ Có (optional) | ✅ Có |

---

**Kết luận:**
- **SavedModels** = Model đã train sẵn (trong dự án, download từ OneDrive)
- **Dataset MINI-RGBD** = Dữ liệu training (download riêng từ website, rất lớn)
- **KHÁC NHAU HOÀN TOÀN!**

---

## 🔗 Link Hữu Ích

- **Download SavedModels**: [OneDrive](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)
- **Download MINI-RGBD Dataset**: [Website](https://www.iosb.fraunhofer.de/servlet/is/82920/)
- **Hướng dẫn sửa đường dẫn**: Xem file `HUONG_DAN_SUA_DUONG_DAN.md`

---

**Chúc bạn thành công! 🎉**

