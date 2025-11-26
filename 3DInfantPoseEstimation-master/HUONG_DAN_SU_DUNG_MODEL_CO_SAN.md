# 🚀 Hướng Dẫn: Sử Dụng Model Có Sẵn (Không Cần Train)

## 🎯 Mục Đích

Hướng dẫn này dành cho những ai **chỉ muốn sử dụng model đã train sẵn** để chạy inference (dự đoán pose từ ảnh/video), **KHÔNG cần train lại model**.

---

## ✅ Những Gì Bạn Cần

### 1. **SavedModels** (Bắt buộc)
- ✅ Model đã train sẵn
- ✅ Download từ [OneDrive](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)
- ✅ Giải nén vào thư mục `SavedModels/` trong dự án

### 2. **Dataset MINI-RGBD** (KHÔNG CẦN!)
- ❌ **KHÔNG CẦN** download dataset để train
- ❌ **KHÔNG CẦN** sửa đường dẫn dataset trong Config.py
- ✅ Chỉ cần nếu muốn **evaluate trên test set** (tùy chọn)

---

## 📋 Checklist Nhanh

- [x] Đã download và giải nén SavedModels
- [x] Đã cài đặt dependencies (pip install -r requirements.txt)
- [x] Đã kích hoạt virtual environment
- [ ] **KHÔNG CẦN** download dataset MINI-RGBD
- [ ] **KHÔNG CẦN** sửa đường dẫn dataset trong Config.py

---

## 🔧 Setup Cơ Bản

### Bước 1: Kích hoạt Virtual Environment

```bash
# Windows
venv\Scripts\activate

# Kiểm tra
python --version  # Nên là 3.11.x
```

### Bước 2: Kiểm tra SavedModels

Đảm bảo bạn có các file model trong:
```
SavedModels/SavedModels/
├── MINI_RGBD_2D/
│   └── model.tar
├── MINI_RGBD_Bbox/
│   └── model.tar
├── MINI_RGBD_FineTune/
│   └── model.tar
└── ...
```

### Bước 3: Kiểm tra Dependencies

```bash
python -c "import torch; import torchvision; import numpy; import cv2; print('All OK!')"
```

---

## 🚀 Sử Dụng Model

### Cách 1: Chạy Inference trên Ảnh/Video Mới (Khuyến nghị)

**Tạo script inference đơn giản:**

```python
# inference_simple.py
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)

from PoseEstimation.ModelArchs import ModelGenerator
from PoseEstimation.Core import Inference
import DataSets.Utils.Config as cfg

# Setup
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load models
batchSize = 1
_, pose2DModel, liftingModel = ModelGenerator.getEndToEndHesseModel(
    batchSize, device, onlyLoadTest=True
)

# Load pretrained weights
model_dir = "SavedModels/SavedModels"
pose2D_path = os.path.join(model_dir, "MINI_RGBD_2D/model.tar")
lifting_path = os.path.join(model_dir, "MINI_RGBD_FineTune/model.tar")

print("Loading models...")
checkpoint = torch.load(pose2D_path, map_location=device)
pose2DModel.load_state_dict(checkpoint["model_state_dict"])
pose2DModel.eval()

checkpoint = torch.load(lifting_path, map_location=device)
liftingModel.load_state_dict(checkpoint["model_state_dict"])
liftingModel.eval()

print("Models loaded successfully!")

# TODO: Thêm code để:
# 1. Load ảnh/video từ đường dẫn
# 2. Pre-process ảnh (resize, normalize, etc.)
# 3. Chạy inference
# 4. Visualize kết quả
```

---

### Cách 2: Chạy Evaluation trên Test Set (Cần dataset)

**⚠️ LƯU Ý:** Cách này **CẦN** có dataset MINI-RGBD.

Nếu bạn muốn evaluate trên test set:

1. **Download dataset MINI-RGBD** từ [website](https://www.iosb.fraunhofer.de/servlet/is/82920/)
2. **Sửa đường dẫn** trong `DataSets/Utils/Config.py`:
   ```python
   MINI_RGBD = {
       "basePath": "F:/datasets/MINI-RGBD/",  # Đường dẫn đến dataset
       ...
   }
   ```
3. **Chạy evaluation:**
   ```bash
   python PoseEstimation/Core/Evaluation.py
   ```

**👉 Nếu bạn KHÔNG muốn evaluate, có thể bỏ qua bước này!**

---

## 📝 Cấu Hình Config.py

### ❌ **KHÔNG CẦN sửa đường dẫn dataset nếu:**

- Bạn chỉ muốn chạy inference trên ảnh/video mới
- Bạn không muốn evaluate trên test set
- Bạn không muốn train model

### ✅ **CẦN sửa đường dẫn dataset nếu:**

- Bạn muốn evaluate trên test set MINI-RGBD
- Bạn muốn train model mới
- Bạn muốn fine-tune model

---

## 🎯 Trường Hợp Cụ Thể

### Trường Hợp 1: Chỉ Chạy Inference (Khuyến nghị)

**Bạn có:**
- ✅ SavedModels
- ❌ Không có dataset

**Bạn cần làm:**
1. ✅ Download SavedModels từ OneDrive
2. ✅ Giải nén vào thư mục `SavedModels/`
3. ❌ **KHÔNG CẦN** download dataset
4. ❌ **KHÔNG CẦN** sửa Config.py
5. ✅ Tạo script inference để chạy trên ảnh/video mới

**Kết quả:**
- ✅ Có thể chạy inference trên ảnh/video bất kỳ
- ❌ Không thể evaluate trên test set (cần dataset)

---

### Trường Hợp 2: Chạy Inference + Evaluate

**Bạn có:**
- ✅ SavedModels
- ✅ Dataset MINI-RGBD

**Bạn cần làm:**
1. ✅ Download SavedModels từ OneDrive
2. ✅ Download dataset MINI-RGBD từ website
3. ✅ Sửa đường dẫn trong Config.py
4. ✅ Chạy inference hoặc evaluation

**Kết quả:**
- ✅ Có thể chạy inference trên ảnh/video bất kỳ
- ✅ Có thể evaluate trên test set

---

## 🔍 Kiểm Tra Setup

### Test 1: Kiểm tra SavedModels

```bash
# Kiểm tra xem có file model không
dir SavedModels\SavedModels\MINI_RGBD_2D
# Nên thấy: model.tar
```

### Test 2: Kiểm tra có thể load model không

```python
import torch
import os

model_path = "SavedModels/SavedModels/MINI_RGBD_2D/model.tar"
if os.path.exists(model_path):
    checkpoint = torch.load(model_path, map_location='cpu')
    print("✅ Model có thể load được!")
    print(f"Keys: {checkpoint.keys()}")
else:
    print("❌ Không tìm thấy model!")
```

### Test 3: Kiểm tra imports

```bash
python -c "from PoseEstimation.ModelArchs import ModelGenerator; print('✅ Import OK!')"
```

---

## 🆘 Troubleshooting

### Lỗi: "FileNotFoundError: SavedModels/..."
**Nguyên nhân:** Chưa download hoặc giải nén SavedModels
**Giải pháp:**
1. Download SavedModels.zip từ OneDrive
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
- Giảm batch size
- Hoặc dùng CPU: `device = torch.device("cpu")`

### Lỗi: "Dataset path not found" khi chạy Evaluation
**Nguyên nhân:** Đang cố chạy evaluation nhưng chưa có dataset
**Giải pháp:**
- Nếu chỉ muốn inference: **KHÔNG CẦN** chạy Evaluation.py
- Nếu muốn evaluate: Download dataset và sửa Config.py

---

## 📚 Tài Liệu Liên Quan

- **Phân biệt SavedModels vs Dataset:** Xem `PHAN_BIET_SAVEDMODELS_VS_DATASET.md`
- **Hướng dẫn sửa đường dẫn:** Xem `HUONG_DAN_SUA_DUONG_DAN.md`
- **FAQ:** Xem `FAQ_DATASET.md`

---

## ✅ Tóm Tắt

| Bạn muốn | Cần SavedModels? | Cần Dataset? | Cần sửa Config.py? |
|----------|------------------|--------------|-------------------|
| **Chạy inference** | ✅ Có | ❌ Không | ❌ Không |
| **Evaluate test set** | ✅ Có | ✅ Có | ✅ Có |
| **Train model** | ❌ Không | ✅ Có | ✅ Có |

---

## 🎉 Kết Luận

**Nếu bạn chỉ muốn dùng model có sẵn:**

1. ✅ **CẦN:** SavedModels (download từ OneDrive)
2. ❌ **KHÔNG CẦN:** Dataset MINI-RGBD
3. ❌ **KHÔNG CẦN:** Sửa đường dẫn dataset trong Config.py
4. ✅ **CẦN:** Tạo script inference để chạy trên ảnh/video mới

**Chúc bạn thành công! 🚀**

