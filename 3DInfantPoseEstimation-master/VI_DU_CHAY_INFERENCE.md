# 🎯 Ví Dụ Cụ Thể: Cách Chạy Inference

## 📋 Hướng Dẫn Nhanh

### Bước 1: Kích Hoạt Virtual Environment

```bash
venv\Scripts\activate
```

### Bước 2: Tìm Đường Dẫn Ảnh

**Cách 1: Copy từ File Explorer**
1. Mở File Explorer
2. Tìm file ảnh của bạn
3. Click vào thanh địa chỉ (address bar)
4. Copy đường dẫn (Ctrl+C)
5. Thay `\` thành `/`

**Cách 2: Drag and Drop**
1. Mở Command Prompt/PowerShell
2. Gõ: `python inference_simple.py --image `
3. Kéo thả file ảnh vào cửa sổ terminal
4. Đường dẫn sẽ tự động được điền (nhưng cần thay `\` thành `/`)

---

## 🎯 Các Ví Dụ Cụ Thể

### Ví Dụ 1: Ảnh Cùng Thư Mục

**Cấu trúc:**
```
3DInfantPoseEstimation-master/
├── inference_simple.py
└── my_image.jpg
```

**Lệnh:**
```bash
python inference_simple.py --image my_image.jpg
```

---

### Ví Dụ 2: Ảnh Trong Thư Mục Con

**Cấu trúc:**
```
3DInfantPoseEstimation-master/
├── inference_simple.py
└── test_images/
    └── baby.jpg
```

**Lệnh:**
```bash
python inference_simple.py --image test_images/baby.jpg
```

---

### Ví Dụ 3: Ảnh Trên Ổ Đĩa Khác (Windows)

**Đường dẫn:** `F:\MyPhotos\infant\baby_photo.jpg`

**Lệnh:**
```bash
# Dùng forward slash
python inference_simple.py --image F:/MyPhotos/infant/baby_photo.jpg

# Hoặc dùng backslash trong dấu ngoặc kép
python inference_simple.py --image "F:\MyPhotos\infant\baby_photo.jpg"
```

---

### Ví Dụ 4: Ảnh Trên Desktop

**Đường dẫn:** `C:\Users\YourName\Desktop\my_image.jpg`

**Lệnh:**
```bash
python inference_simple.py --image C:/Users/YourName/Desktop/my_image.jpg
```

---

### Ví Dụ 5: Ảnh Có Khoảng Trắng Trong Tên

**Đường dẫn:** `F:\My Photos\baby photo.jpg`

**Lệnh:**
```bash
# Phải dùng dấu ngoặc kép
python inference_simple.py --image "F:/My Photos/baby photo.jpg"
```

---

## 🔧 Các Tùy Chọn Khác

### Lưu Kết Quả Vào File Cụ Thể

```bash
python inference_simple.py --image my_image.jpg --output result.png
```

### Dùng Bbox Model (Tự Động Detect Infant)

```bash
python inference_simple.py --image my_image.jpg --use-bbox
```

### Kết Hợp Cả Hai

```bash
python inference_simple.py --image my_image.jpg --output result.png --use-bbox
```

---

## 📝 Workflow Hoàn Chỉnh

### Bước 1: Chuẩn Bị

```bash
# 1. Kích hoạt virtual environment
venv\Scripts\activate

# 2. Kiểm tra setup
python test_inference.py
```

### Bước 2: Chuẩn Bị Ảnh

1. Tìm ảnh của bạn
2. Copy đường dẫn
3. Thay `\` thành `/`

### Bước 3: Chạy Inference

```bash
# Ví dụ với ảnh trên ổ F
python inference_simple.py --image F:/images/baby.jpg
```

### Bước 4: Xem Kết Quả

Kết quả sẽ được lưu vào:
```
Images/InferenceOutput/
└── baby_result.png
```

---

## 🆘 Troubleshooting

### Lỗi: "FileNotFoundError"

**Nguyên nhân:** Đường dẫn không đúng

**Giải pháp:**
1. Kiểm tra đường dẫn có đúng không
2. Thử dùng đường dẫn tuyệt đối
3. Đảm bảo đã thay `\` thành `/`

**Ví dụ:**
```bash
# Kiểm tra file có tồn tại không (PowerShell)
Test-Path "F:/images/baby.jpg"

# Nếu trả về True, file tồn tại
# Sau đó chạy:
python inference_simple.py --image F:/images/baby.jpg
```

---

### Lỗi: "Permission denied"

**Giải pháp:**
1. Đảm bảo file không bị khóa
2. Thử copy ảnh vào thư mục project và chạy lại

---

## 💡 Mẹo

1. **Tạo thư mục test_images trong project** để dễ quản lý:
   ```bash
   mkdir test_images
   # Copy ảnh vào đây, sau đó:
   python inference_simple.py --image test_images/my_image.jpg
   ```

2. **Dùng đường dẫn ngắn gọn** bằng cách đặt ảnh trong project

3. **Batch processing:** Tạo script để xử lý nhiều ảnh cùng lúc

---

## ✅ Checklist

- [ ] Đã kích hoạt virtual environment
- [ ] Đã tìm được đường dẫn ảnh
- [ ] Đã thay `\` thành `/` (nếu cần)
- [ ] Đã kiểm tra file tồn tại
- [ ] Đã chạy lệnh inference

---

**Chúc bạn thành công! 🎉**

