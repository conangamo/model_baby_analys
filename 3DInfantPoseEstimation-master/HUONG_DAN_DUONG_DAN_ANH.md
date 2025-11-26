# 📷 Hướng Dẫn: Cách Chỉ Định Đường Dẫn Ảnh

## 🎯 Cú Pháp Cơ Bản

```bash
python inference_simple.py --image <ĐƯỜNG_DẪN_ĐẾN_ẢNH>
```

Bạn cần thay `<ĐƯỜNG_DẪN_ĐẾN_ẢNH>` bằng đường dẫn thực tế đến file ảnh của bạn.

---

## 📂 Các Cách Chỉ Định Đường Dẫn

### 1. **Đường Dẫn Tương Đối** (Relative Path)

Đường dẫn tính từ thư mục hiện tại (thư mục chứa script).

#### Ví dụ 1: Ảnh cùng thư mục với script
```bash
# Nếu ảnh ở cùng thư mục với inference_simple.py
python inference_simple.py --image my_image.jpg
```

#### Ví dụ 2: Ảnh trong thư mục con
```bash
# Ảnh ở trong thư mục "images"
python inference_simple.py --image images/infant.jpg

# Ảnh ở trong thư mục "test_images"
python inference_simple.py --image test_images/baby.png
```

#### Ví dụ 3: Ảnh ở thư mục cha
```bash
# Ảnh ở thư mục cha (một cấp trên)
python inference_simple.py --image ../my_image.jpg

# Ảnh ở thư mục cha của cha (hai cấp trên)
python inference_simple.py --image ../../my_image.jpg
```

---

### 2. **Đường Dẫn Tuyệt Đối** (Absolute Path)

Đường dẫn đầy đủ từ ổ đĩa đến file.

#### Ví dụ cho Windows:
```bash
# Ảnh trên ổ C
python inference_simple.py --image C:/Users/YourName/Pictures/infant.jpg

# Ảnh trên ổ D
python inference_simple.py --image D:/MyImages/baby.png

# Ảnh trên ổ F
python inference_simple.py --image F:/datasets/infant_pose/image1.jpg
```

**Lưu ý:** Trong Windows, bạn có thể dùng cả `/` (forward slash) hoặc `\` (backslash):
```bash
# Dùng forward slash (khuyến nghị)
python inference_simple.py --image F:/images/baby.jpg

# Dùng backslash (cần escape hoặc dùng raw string)
python inference_simple.py --image "F:\images\baby.jpg"
```

---

## 🔍 Các Ví Dụ Cụ Thể

### Ví Dụ 1: Ảnh Trong Thư Mục Project

Giả sử cấu trúc thư mục như sau:
```
3DInfantPoseEstimation-master/
├── inference_simple.py
├── test_images/
│   ├── baby1.jpg
│   └── baby2.png
└── Images/
    └── test.jpg
```

**Cách chạy:**
```bash
# Từ thư mục gốc của project
python inference_simple.py --image test_images/baby1.jpg
python inference_simple.py --image Images/test.jpg
```

---

### Ví Dụ 2: Ảnh Ở Nơi Khác (Windows)

Giả sử ảnh của bạn ở: `F:\MyPhotos\InfantPose\baby_photo.jpg`

**Cách chạy:**
```bash
# Dùng forward slash
python inference_simple.py --image F:/MyPhotos/InfantPose/baby_photo.jpg

# Hoặc dùng backslash (trong dấu ngoặc kép)
python inference_simple.py --image "F:\MyPhotos\InfantPose\baby_photo.jpg"
```

---

### Ví Dụ 3: Ảnh Trên Desktop

**Cách chạy:**
```bash
# Windows - Desktop thường ở C:/Users/YourName/Desktop
python inference_simple.py --image C:/Users/YourName/Desktop/my_image.jpg

# Hoặc dùng biến môi trường
python inference_simple.py --image %USERPROFILE%/Desktop/my_image.jpg
```

---

## 💡 Mẹo Hữu Ích

### 1. **Copy Đường Dẫn Từ File Explorer (Windows)**

**Cách 1: Copy đường dẫn**
1. Mở File Explorer
2. Điều hướng đến file ảnh
3. Click vào thanh địa chỉ (address bar)
4. Copy đường dẫn (Ctrl+C)
5. Thay `\` thành `/` trong đường dẫn
6. Dán vào lệnh

**Ví dụ:**
- Đường dẫn từ File Explorer: `F:\MyPhotos\baby.jpg`
- Đường dẫn trong lệnh: `F:/MyPhotos/baby.jpg`

**Cách 2: Shift + Right Click**
1. Giữ Shift và click chuột phải vào file ảnh
2. Chọn "Copy as path"
3. Paste vào lệnh (thay `\` thành `/`)

---

### 2. **Kiểm Tra Đường Dẫn Đúng**

Trước khi chạy, bạn có thể kiểm tra file có tồn tại không:

**Windows PowerShell:**
```powershell
# Kiểm tra file có tồn tại không
Test-Path "F:/MyPhotos/baby.jpg"
```

**Windows CMD:**
```cmd
# Kiểm tra file có tồn tại không
dir "F:\MyPhotos\baby.jpg"
```

---

### 3. **Dùng Dấu Ngoặc Kép**

Nếu đường dẫn có khoảng trắng, hãy dùng dấu ngoặc kép:

```bash
# Đúng
python inference_simple.py --image "F:/My Photos/baby photo.jpg"

# Sai (sẽ bị lỗi)
python inference_simple.py --image F:/My Photos/baby photo.jpg
```

---

## 🎯 Ví Dụ Hoàn Chỉnh

### Bước 1: Tìm Ảnh Của Bạn

Ví dụ: Ảnh của bạn ở `F:\lapTrinhAI\duAnNoiTreEm\images\infant.jpg`

### Bước 2: Chuyển Đổi Đường Dẫn

Thay `\` thành `/`:
- Gốc: `F:\lapTrinhAI\duAnNoiTreEm\images\infant.jpg`
- Sau khi chuyển: `F:/lapTrinhAI/duAnNoiTreEm/images/infant.jpg`

### Bước 3: Chạy Lệnh

```bash
# Kích hoạt virtual environment
venv\Scripts\activate

# Chạy inference
python inference_simple.py --image F:/lapTrinhAI/duAnNoiTreEm/images/infant.jpg
```

---

## 🆘 Xử Lý Lỗi

### Lỗi: "FileNotFoundError: [Errno 2] No such file or directory"

**Nguyên nhân:** Đường dẫn không đúng hoặc file không tồn tại

**Giải pháp:**
1. Kiểm tra đường dẫn có đúng không
2. Kiểm tra file có tồn tại không
3. Đảm bảo đã thay `\` thành `/`
4. Đảm bảo đã dùng dấu ngoặc kép nếu có khoảng trắng

**Ví dụ:**
```bash
# Kiểm tra file
dir "F:\MyPhotos\baby.jpg"

# Nếu file tồn tại, chạy lệnh
python inference_simple.py --image F:/MyPhotos/baby.jpg
```

---

### Lỗi: "Permission denied"

**Nguyên nhân:** Không có quyền truy cập file

**Giải pháp:**
1. Kiểm tra quyền truy cập file
2. Đảm bảo file không bị khóa bởi chương trình khác
3. Thử chạy với quyền Administrator

---

## 📝 Tóm Tắt

| Loại Đường Dẫn | Ví Dụ | Khi Nào Dùng |
|----------------|-------|--------------|
| **Tương đối** | `images/baby.jpg` | Ảnh trong/near project |
| **Tuyệt đối** | `F:/MyPhotos/baby.jpg` | Ảnh ở nơi khác |
| **Desktop** | `C:/Users/Name/Desktop/img.jpg` | Ảnh trên Desktop |

---

## ✅ Checklist

Trước khi chạy:
- [ ] Đã tìm được đường dẫn đến ảnh
- [ ] Đã thay `\` thành `/` (nếu dùng Windows path)
- [ ] Đã dùng dấu ngoặc kép nếu đường dẫn có khoảng trắng
- [ ] Đã kiểm tra file có tồn tại không
- [ ] Đã kích hoạt virtual environment

---

## 🚀 Ví Dụ Thực Tế

### Ví Dụ 1: Ảnh Trong Thư Mục Project

```bash
# Tạo thư mục test_images trong project
mkdir test_images

# Copy ảnh vào thư mục test_images
# Sau đó chạy:
python inference_simple.py --image test_images/my_baby.jpg
```

### Ví Dụ 2: Ảnh Trên Ổ Đĩa Khác

```bash
# Ảnh trên ổ F
python inference_simple.py --image F:/datasets/infant/images/baby001.jpg

# Lưu kết quả vào file cụ thể
python inference_simple.py --image F:/datasets/infant/images/baby001.jpg --output result.png
```

### Ví Dụ 3: Nhiều Ảnh (Batch)

Tạo file `run_batch.py`:
```python
import os
import subprocess

# Danh sách ảnh
images = [
    "F:/images/baby1.jpg",
    "F:/images/baby2.jpg",
    "F:/images/baby3.jpg",
]

for image in images:
    cmd = f'python inference_simple.py --image "{image}"'
    subprocess.run(cmd, shell=True)
```

---

**Chúc bạn thành công! 🎉**

