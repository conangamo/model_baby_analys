# ❓ FAQ: Dataset MINI-RGBD

## Câu Hỏi: "Dataset MINI-RGBD có phải là thư mục SavedModels không?"

### ❌ TRẢ LỜI: KHÔNG! Đây là 2 thứ hoàn toàn khác nhau!

---

## 📦 SavedModels (Trong dự án)

```
SavedModels/
└── SavedModels/
    ├── MINI_RGBD_2D/
    │   └── model.tar
    └── ...
```

- ✅ **Có sẵn trong dự án** (sau khi download từ OneDrive)
- ✅ **Là model đã train sẵn** (pretrained models)
- ✅ **Kích thước:** Vài trăm MB - vài GB
- ✅ **Dùng để:** Chạy inference/evaluation
- ✅ **Download từ:** [OneDrive link](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)

---

## 📊 Dataset MINI-RGBD (Cần download riêng)

```
MINI-RGBD/
├── 01/
│   ├── rgb/          (1000 ảnh)
│   ├── joints_2Ddep/ (1000 file)
│   ├── joints_3D/    (1000 file)
│   └── fg_mask/      (1000 ảnh)
├── 02/
└── ... (12 video sequences)
```

- ❌ **KHÔNG có sẵn** - cần download riêng
- ❌ **Là dữ liệu training/evaluation** (ảnh, video, annotations)
- ❌ **Kích thước:** Rất lớn (hàng chục - vài trăm GB)
- ❌ **Dùng để:** Train model hoặc evaluate
- ❌ **Download từ:** [Website chính thức](https://www.iosb.fraunhofer.de/servlet/is/82920/)

---

## 🎯 Bạn Cần Gì?

### Chỉ muốn chạy inference?
- ✅ **Cần:** SavedModels
- ❌ **KHÔNG cần:** Dataset MINI-RGBD

### Muốn train/evaluate?
- ✅ **Cần:** Dataset MINI-RGBD
- ✅ **Có thể cần:** SavedModels (để fine-tune)

---

## 📥 Cách Download Dataset MINI-RGBD

1. Truy cập: https://www.iosb.fraunhofer.de/servlet/is/82920/
2. Đăng ký/đăng nhập (có thể cần xin quyền)
3. Download tất cả các file
4. Giải nén vào thư mục (ví dụ: `F:/datasets/MINI-RGBD/`)
5. Sửa đường dẫn trong `DataSets/Utils/Config.py`:
   ```python
   MINI_RGBD = {
       "basePath": "F:/datasets/MINI-RGBD/",  # ← Sửa đường dẫn này
       ...
   }
   ```

---

## 📚 Xem Thêm

- **Chi tiết đầy đủ:** Xem file `PHAN_BIET_SAVEDMODELS_VS_DATASET.md`
- **Hướng dẫn sửa đường dẫn:** Xem file `HUONG_DAN_SUA_DUONG_DAN.md`

---

## ✅ Tóm Tắt

| | SavedModels | Dataset MINI-RGBD |
|---|---|---|
| **Có sẵn?** | ✅ Có (download từ OneDrive) | ❌ Không (download từ website) |
| **Là gì?** | Model đã train | Dữ liệu raw |
| **Kích thước** | Vài GB | Hàng trăm GB |
| **Cần khi nào?** | Luôn cần (để chạy) | Chỉ khi train/evaluate |

---

**Kết luận: SavedModels ≠ Dataset MINI-RGBD!**

