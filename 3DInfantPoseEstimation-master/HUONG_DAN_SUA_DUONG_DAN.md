# 📝 Hướng Dẫn Chi Tiết: Sửa Đường Dẫn trong Config.py

## 🎯 Mục Đích

File `DataSets/Utils/Config.py` chứa các cấu hình đường dẫn đến datasets. Các đường dẫn hiện tại được hardcode cho Linux server (`/vol/bitbucket/...`). Bạn cần sửa chúng thành đường dẫn trên máy Windows của bạn.

---

## ⚠️ QUAN TRỌNG: SavedModels vs Dataset

**Trước khi bắt đầu, hãy hiểu rõ sự khác biệt:**

### 📦 **SavedModels** (Thư mục trong dự án)
- ✅ **Là gì?** Model đã được train sẵn (pretrained models)
- ✅ **Có sẵn?** Có, download từ [OneDrive](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)
- ✅ **Dùng để:** Chạy inference/evaluation
- ✅ **Kích thước:** Vài trăm MB - vài GB

### 📊 **Dataset MINI-RGBD** (Cần download riêng)
- ❌ **Là gì?** Dữ liệu training/evaluation (ảnh, video, annotations)
- ❌ **Có sẵn?** KHÔNG - cần download riêng từ [website](https://www.iosb.fraunhofer.de/servlet/is/82920/)
- ❌ **Dùng để:** Train model hoặc evaluate trên test set
- ❌ **Kích thước:** Rất lớn (hàng chục - vài trăm GB)

**👉 Xem file `PHAN_BIET_SAVEDMODELS_VS_DATASET.md` để biết thêm chi tiết!**

**Lưu ý:** 
- Nếu bạn **chỉ muốn chạy inference**, bạn **KHÔNG CẦN** download dataset
- Nếu bạn muốn **train hoặc evaluate**, bạn **CẦN** download dataset và sửa đường dẫn trong Config.py

---

## 📂 Các Đường Dẫn Cần Sửa

File `Config.py` có 4 datasets chính cần cấu hình:

1. **MPI_INF** - MPI-INF-3DHP dataset
2. **MINI_RGBD** - MINI-RGBD dataset  
3. **MPII** - MPII dataset
4. **MAHVEA** - MAVHEA infant dataset

---

## 🔧 Cách Sửa Đường Dẫn (Chi Tiết Từng Bước)

### ⚠️ QUAN TRỌNG: Định Dạng Đường Dẫn Windows

Trong Python, có 3 cách viết đường dẫn Windows:

**Cách 1: Dùng forward slash `/` (KHUYẾN NGHỊ)**
```python
"basePath": "F:/datasets/MINI-RGBD/"
```

**Cách 2: Dùng raw string với backslash**
```python
"basePath": r"F:\datasets\MINI-RGBD\\"
```
*(Lưu ý: cần 2 dấu `\\` ở cuối)*

**Cách 3: Dùng os.path.join (phức tạp hơn)**
```python
import os
"basePath": os.path.join("F:", "datasets", "MINI-RGBD") + os.sep
```

**👉 Khuyến nghị: Dùng Cách 1 (forward slash) - đơn giản nhất!**

---

## 📋 Hướng Dẫn Sửa Từng Dataset

### 1️⃣ Dataset MINI_RGBD

**⚠️ LƯU Ý QUAN TRỌNG:**
- Dataset MINI-RGBD **KHÔNG có sẵn** trong dự án
- Bạn cần **download riêng** từ [website chính thức](https://www.iosb.fraunhofer.de/servlet/is/82920/)
- Dataset rất lớn (hàng chục - vài trăm GB)
- **KHÔNG PHẢI** là thư mục SavedModels trong dự án
- Xem file `PHAN_BIET_SAVEDMODELS_VS_DATASET.md` để hiểu rõ sự khác biệt

**Vị trí trong file:** Dòng 166

**Đường dẫn cần sửa:**
```python
MINI_RGBD = {
    "basePath": "/vol/bitbucket/sje116/Hesse/",  # ← SỬA DÒNG NÀY
    ...
}
```

**Ví dụ sửa cho Windows:**
```python
MINI_RGBD = {
    "basePath": "F:/datasets/MINI-RGBD/",  # Đường dẫn đến thư mục MINI-RGBD đã download
    # hoặc
    "basePath": "D:/MyDatasets/Hesse/",    # Tên thư mục có thể khác
    ...
}
```

**Cách download dataset:**
1. Truy cập: https://www.iosb.fraunhofer.de/servlet/is/82920/
2. Đăng ký/đăng nhập (có thể cần xin quyền truy cập)
3. Download tất cả các file dataset
4. Giải nén vào một thư mục (ví dụ: `F:/datasets/MINI-RGBD/`)
5. Sửa đường dẫn trong Config.py như trên

**Cấu trúc thư mục MINI-RGBD cần có:**
```
MINI-RGBD/
├── 01/
│   ├── rgb/
│   │   ├── syn_00000.png
│   │   ├── syn_00001.png
│   │   └── ...
│   ├── joints_2Ddep/
│   │   ├── syn_joints_2Ddep_00000.txt
│   │   └── ...
│   ├── joints_3D/
│   │   ├── syn_joints_3D_00000.txt
│   │   └── ...
│   └── fg_mask/
│       ├── mask_00000.png
│       └── ...
├── 02/
├── 03/
└── ...
```

**Cách kiểm tra:**
- Mở File Explorer
- Điều hướng đến thư mục chứa dataset MINI-RGBD
- Copy đường dẫn từ thanh địa chỉ (ví dụ: `F:\datasets\MINI-RGBD`)
- Thay `\` thành `/` và thêm `/` ở cuối
- Kết quả: `F:/datasets/MINI-RGBD/`

---

### 2️⃣ Dataset MPI_INF (MPI-INF-3DHP)

**Vị trí trong file:** Dòng 5-132

**Đường dẫn cần sửa:**
```python
MPI_INF = {
    "pelvicIndex": 4,
    "numJoints": 28,
    "basePath": "/vol/bitbucket/sje116/mpi-inf-3dhp/mpi_inf_3dhp/",  # ← SỬA DÒNG NÀY
    ...
}
```

**Ví dụ sửa cho Windows:**
```python
MPI_INF = {
    "pelvicIndex": 4,
    "numJoints": 28,
    "basePath": "F:/datasets/mpi-inf-3dhp/mpi_inf_3dhp/",
    ...
}
```

**Cấu trúc thư mục MPI-INF-3DHP:**
```
mpi-inf-3dhp/
└── mpi_inf_3dhp/
    ├── S1/
    │   ├── Seq1/
    │   │   ├── imageSequence/
    │   │   │   ├── img_001001.jpg
    │   │   │   └── ...
    │   │   └── annot.mat
    │   └── Seq2/
    ├── S2/
    ├── S3/
    └── ...
```

---

### 3️⃣ Dataset MPII

**Vị trí trong file:** Dòng 257-319

**Đường dẫn cần sửa:**
```python
MPII = {
    "numJoints": 16,
    "modeDatasets": {"train": ["train", "trainval"], "val": ["valid"]},
    "annotationFileDirectory": "/vol/bitbucket/sje116/MPII/annotations",  # ← SỬA DÒNG NÀY
    "imageDirectory": "/vol/bitbucket/sje116/MPII/images/",              # ← SỬA DÒNG NÀY
    ...
}
```

**Ví dụ sửa cho Windows:**
```python
MPII = {
    "numJoints": 16,
    "modeDatasets": {"train": ["train", "trainval"], "val": ["valid"]},
    "annotationFileDirectory": "F:/datasets/MPII/annotations",
    "imageDirectory": "F:/datasets/MPII/images/",
    ...
}
```

**Cấu trúc thư mục MPII:**
```
MPII/
├── annotations/
│   ├── train.h5
│   ├── valid.h5
│   └── ...
└── images/
    ├── 000001163.jpg
    ├── 000003072.jpg
    └── ...
```

---

### 4️⃣ Dataset MAHVEA (MAVHEA)

**Vị trí trong file:** Dòng 320-327

**Đường dẫn cần sửa:**
```python
MAHVEA = {
    "labelsFname": "/vol/bitbucket/sje116/InfantData/label.json",      # ← SỬA DÒNG NÀY
    "baseDirectory": "/vol/bitbucket/sje116/InfantData",                # ← SỬA DÒNG NÀY
    "videoDirectory": "/vol/bitbucket/sje116/video",                    # ← SỬA DÒNG NÀY
    ...
}
```

**Ví dụ sửa cho Windows:**
```python
MAHVEA = {
    "labelsFname": "F:/datasets/InfantData/label.json",
    "baseDirectory": "F:/datasets/InfantData",
    "videoDirectory": "F:/datasets/video",
    ...
}
```

**Cấu trúc thư mục MAVHEA:**
```
InfantData/
├── label.json
├── video1/
│   ├── frame001.jpg
│   ├── frame002.jpg
│   └── ...
├── video2/
└── ...
```

---

## ✅ Checklist: Kiểm Tra Sau Khi Sửa

### Bước 1: Kiểm tra cú pháp Python
```bash
python -c "import DataSets.Utils.Config as cfg; print('Config loaded successfully!')"
```

Nếu không có lỗi → ✅ Đường dẫn hợp lệ!

### Bước 2: Kiểm tra đường dẫn có tồn tại
```python
import os
import DataSets.Utils.Config as cfg

# Kiểm tra MINI_RGBD
if os.path.exists(cfg.MINI_RGBD["basePath"]):
    print("✅ MINI_RGBD path exists")
else:
    print("❌ MINI_RGBD path NOT found:", cfg.MINI_RGBD["basePath"])

# Kiểm tra MPII
if os.path.exists(cfg.MPII["imageDirectory"]):
    print("✅ MPII image directory exists")
else:
    print("❌ MPII image directory NOT found:", cfg.MPII["imageDirectory"])
```

### Bước 3: Test load dataset
```python
from DataSets.Concrete.MINI_RGBDDataset import MINI_RGBDDataset
from DataSets.Utils.TargetType import TargetType

try:
    dataset = MINI_RGBDDataset("train", TargetType.joint2D)
    print("✅ Dataset loaded successfully!")
    print(f"Number of samples: {len(dataset)}")
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
```

---

## 🚨 Các Lỗi Thường Gặp và Cách Sửa

### Lỗi 1: `FileNotFoundError` hoặc `OSError: [WinError 3]`
**Nguyên nhân:** Đường dẫn không tồn tại hoặc sai định dạng

**Cách sửa:**
1. Kiểm tra đường dẫn có đúng không (copy từ File Explorer)
2. Đảm bảo có dấu `/` ở cuối đường dẫn
3. Đảm bảo thay `\` thành `/`
4. Kiểm tra tên thư mục có đúng chính tả không

**Ví dụ:**
```python
# ❌ SAI:
"basePath": "F:\datasets\MINI-RGBD"     # Thiếu dấu / ở cuối, dùng backslash

# ✅ ĐÚNG:
"basePath": "F:/datasets/MINI-RGBD/"    # Forward slash, có / ở cuối
```

---

### Lỗi 2: `SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes`
**Nguyên nhân:** Python hiểu `\` trong string là escape character

**Cách sửa:**
- Dùng forward slash `/` thay vì backslash `\`
- Hoặc dùng raw string `r"F:\path"`

**Ví dụ:**
```python
# ❌ SAI:
"basePath": "F:\datasets\MINI-RGBD\"    # \b và \M bị hiểu sai

# ✅ ĐÚNG:
"basePath": "F:/datasets/MINI-RGBD/"    # Forward slash
# hoặc
"basePath": r"F:\datasets\MINI-RGBD\\"  # Raw string (2 dấu \\ ở cuối)
```

---

### Lỗi 3: Dataset không load được
**Nguyên nhân:** Cấu trúc thư mục dataset không đúng

**Cách sửa:**
1. Kiểm tra cấu trúc thư mục có đúng như hướng dẫn ở trên không
2. Kiểm tra tên file có đúng format không (ví dụ: `syn_00000.png`)
3. Kiểm tra có thiếu file nào không

---

## 📝 Ví Dụ Hoàn Chỉnh: Config.py cho Windows

Dưới đây là ví dụ một phần config.py đã được sửa cho Windows:

```python
# ... (giữ nguyên phần import và generic config) ...

MPI_INF = {
    "pelvicIndex": 4,
    "numJoints": 28,
    "basePath": "F:/datasets/mpi-inf-3dhp/mpi_inf_3dhp/",  # ← ĐÃ SỬA
    # ... (giữ nguyên phần còn lại) ...
}

MINI_RGBD = {
    "basePath": "F:/datasets/MINI-RGBD/",  # ← ĐÃ SỬA
    # ... (giữ nguyên phần còn lại) ...
}

MPII = {
    "numJoints": 16,
    "modeDatasets": {"train": ["train", "trainval"], "val": ["valid"]},
    "annotationFileDirectory": "F:/datasets/MPII/annotations",  # ← ĐÃ SỬA
    "imageDirectory": "F:/datasets/MPII/images/",              # ← ĐÃ SỬA
    # ... (giữ nguyên phần còn lại) ...
}

MAHVEA = {
    "labelsFname": "F:/datasets/InfantData/label.json",      # ← ĐÃ SỬA
    "baseDirectory": "F:/datasets/InfantData",                # ← ĐÃ SỬA
    "videoDirectory": "F:/datasets/video",                    # ← ĐÃ SỬA
    # ... (giữ nguyên phần còn lại) ...
}
```

---

## 💡 Mẹo và Best Practices

1. **Dùng biến môi trường (tùy chọn, nâng cao):**
   ```python
   import os
   DATASET_ROOT = os.getenv("DATASET_ROOT", "F:/datasets/")
   
   MINI_RGBD = {
       "basePath": os.path.join(DATASET_ROOT, "MINI-RGBD") + "/",
       ...
   }
   ```

2. **Dùng đường dẫn tương đối (nếu dataset ở trong project):**
   ```python
   import os
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   
   MINI_RGBD = {
       "basePath": os.path.join(BASE_DIR, "datasets", "MINI-RGBD") + os.sep,
       ...
   }
   ```

3. **Comment rõ ràng:**
   ```python
   MINI_RGBD = {
       # Đường dẫn đến thư mục MINI-RGBD dataset
       # Format: [ổ đĩa]:/[đường dẫn]/[tên thư mục]/
       "basePath": "F:/datasets/MINI-RGBD/",
       ...
   }
   ```

---

## 🆘 Cần Giúp Đỡ?

Nếu vẫn gặp vấn đề:

1. Kiểm tra lại các bước trên
2. Chạy script kiểm tra (xem phần Checklist)
3. Xem log lỗi chi tiết để biết đường dẫn nào bị sai
4. Đảm bảo dataset đã được download và giải nén đúng cách

---

## 📌 Tóm Tắt Nhanh

1. ✅ Mở file `DataSets/Utils/Config.py`
2. ✅ Tìm các đường dẫn bắt đầu bằng `/vol/bitbucket/...`
3. ✅ Thay thế bằng đường dẫn Windows của bạn (dùng `/` thay vì `\`)
4. ✅ Đảm bảo có dấu `/` ở cuối đường dẫn
5. ✅ Kiểm tra lại bằng script test

**Ví dụ chuyển đổi:**
```
Linux:   /vol/bitbucket/sje116/Hesse/
Windows: F:/datasets/MINI-RGBD/
```

---

**Chúc bạn thành công! 🎉**

