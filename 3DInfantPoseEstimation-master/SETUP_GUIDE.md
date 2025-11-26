# Hướng Dẫn Setup Dự Án 3D Infant Pose Estimation

## 📋 Yêu Cầu Hệ Thống

### ⚠️ QUAN TRỌNG: Python Version

**KHÔNG KHUYẾN NGHỊ dùng Python 3.13** (quá mới, nhiều thư viện chưa hỗ trợ)

**Khuyến nghị:** Python **3.10** hoặc **3.11** (ổn định nhất cho ML/AI)
- ✅ Python 3.10: Hỗ trợ tốt nhất, ổn định
- ✅ Python 3.11: Tốt, nhanh hơn 3.10
- ⚠️ Python 3.12: Có thể dùng nhưng một số packages chưa test kỹ
- ❌ Python 3.13: **KHÔNG nên dùng** - PyTorch, NumPy và nhiều packages khác chưa hỗ trợ đầy đủ

**Lý do:**
- PyTorch thường chậm hỗ trợ Python version mới (3-6 tháng sau khi Python ra mắt)
- Code này được viết năm 2020, test với Python 3.7-3.10
- Python 3.13 mới ra (10/2024), nhiều dependencies chưa có bản build

**Cách kiểm tra Python version:**
```bash
python --version
# hoặc
python3 --version
```

**Nếu đang dùng Python 3.13, hãy:**
1. Cài Python 3.10 hoặc 3.11 (có thể cài song song)
2. Dùng virtual environment với version phù hợp (xem hướng dẫn bên dưới)

### Yêu Cầu Khác

- CUDA (tùy chọn, nếu có GPU)
- RAM: ít nhất 8GB (khuyến nghị 16GB+)
- GPU: NVIDIA GPU với CUDA support (khuyến nghị cho training)

## 🔧 Bước 0: Thiết Lập Python Environment (QUAN TRỌNG!)

### ⚡ Cách Nhanh Nhất (Tự Động)

**Windows:**
```bash
# Chạy script tự động (sẽ tạo venv với Python 3.11 và cài tất cả dependencies)
setup_venv.bat

# Sau đó kích hoạt environment:
activate_env.bat
# hoặc
venv\Scripts\activate
```

**Linux/Mac:**
```bash
# Chạy script tự động
chmod +x setup_venv.sh
./setup_venv.sh

# Sau đó kích hoạt:
source venv/bin/activate
```

### Cách Thủ Công (Nếu muốn tự làm từng bước)

#### Option A: Dùng Virtual Environment (Khuyến nghị)
```bash
# Tạo virtual environment với Python 3.11 (nếu đã cài)
py -3.11 -m venv venv  # Windows
# hoặc
python3.11 -m venv venv  # Linux/Mac

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Kiểm tra version
python --version  # Nên hiển thị Python 3.11.x
```

#### Option B: Dùng Conda (Khuyến nghị nếu có Anaconda/Miniconda)
```bash
# Tạo environment với Python 3.10
conda create -n infant_pose python=3.10
conda activate infant_pose

# Kiểm tra
python --version
```

#### Option C: Cài Python 3.10 song song (Windows)
```bash
# Download Python 3.10 từ python.org
# Khi cài, chọn "Add to PATH" hoặc "Add Python to environment variables"
# Sau đó dùng:
py -3.10 -m venv venv
venv\Scripts\activate
```

## 🔧 Bước 1: Cài Đặt Dependencies

### Option 1: Sử dụng requirements.txt (Khuyến nghị)
```bash
pip install -r requirements.txt
```

### Option 2: Cài đặt thủ công
```bash
# Core frameworks
pip install torch torchvision
pip install numpy scipy
pip install opencv-python Pillow
pip install matplotlib prettytable
```

### Option 3: Với GPU support
```bash
# Cài PyTorch với CUDA (ví dụ: CUDA 11.8)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

## 📦 Bước 2: Download Models và Datasets

### 2.1. Download Pre-trained Models
1. Download `SavedModels.zip` từ [OneDrive](https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7)
2. Giải nén và đặt thư mục `SavedModels` vào thư mục gốc của project

### 2.2. Download Datasets (Tùy chọn)
Nếu bạn muốn train hoặc evaluate trên dataset gốc:

- **MPI_INF_3DHP**: Download từ [website chính thức](https://vcai.mpi-inf.mpg.de/projects/SingleShotMultiPerson/)
- **MPII**: Download từ [website chính thức](http://human-pose.mpi-inf.mpg.de/)
- **MINI-RGBD**: Download từ [website chính thức](https://www.iosb.fraunhofer.de/servlet/is/82920/)

## ⚙️ Bước 3: Cấu Hình Dataset Paths

**QUAN TRỌNG**: Sửa file `DataSets/Utils/Config.py` để chỉ định đường dẫn dataset của bạn:

```python
# Sửa các đường dẫn này trong Config.py:

MPI_INF = {
    "basePath": "/path/to/your/mpi-inf-3dhp/",  # Thay đổi đường dẫn này
    ...
}

MINI_RGBD = {
    "basePath": "/path/to/your/MINI-RGBD/",  # Thay đổi đường dẫn này
    ...
}

MPII = {
    "annotationFileDirectory": "/path/to/your/MPII/annotations",  # Thay đổi
    "imageDirectory": "/path/to/your/MPII/images/",  # Thay đổi
    ...
}
```

## ✅ Bước 4: Kiểm Tra Setup

### Test 1: Kiểm tra imports
```python
python -c "import torch; import torchvision; import numpy; import cv2; print('All imports successful!')"
```

### Test 2: Chạy thử dataset loader
```python
# Chạy file này để test dataset loading
python DataSets/Concrete/MINI_RGBDDataset.py
```

### Test 3: Kiểm tra model loading
```python
# Chạy evaluation (cần có models và datasets)
python PoseEstimation/Core/Evaluation.py
```

## 🚀 Bước 5: Sử Dụng Dự Án

### Chạy Evaluation
```python
# Chỉnh sửa file Evaluation.py để load đúng models và datasets
python PoseEstimation/Core/Evaluation.py
```

### Chạy Training
```python
# Train 2D pose model
python PoseEstimation/Core/Trainer.py

# Train 3D lifting model
# (Cần chỉnh sửa ModelGenerator để setup đúng)

# Train Faster R-CNN bbox model
python FasterRCNN/Trainer.py
```

### Visualize Dataset
```python
# Xem samples từ dataset
python DataSets/Concrete/MINI_RGBDDataset.py
```

## ⚠️ Lưu Ý Quan Trọng

1. **Hardcode Paths**: Code có nhiều đường dẫn hardcode, cần sửa thủ công trong `Config.py`

2. **Models**: Cần download `SavedModels.zip` từ OneDrive để chạy inference

3. **Datasets**: Datasets rất lớn (hàng GB), chỉ cần download nếu muốn train/evaluate

4. **GPU**: Khuyến nghị dùng GPU cho training. Code sẽ tự động fallback về CPU nếu không có GPU

5. **Windows Path**: Nếu dùng Windows, đảm bảo sử dụng forward slash `/` hoặc raw string `r"C:\path"` trong Config.py

## 🐛 Troubleshooting

### Lỗi: "Python 3.13 không tương thích với PyTorch"
**Giải pháp:**
- Cài Python 3.10 hoặc 3.11
- Dùng virtual environment (xem Bước 0)
- Kiểm tra: `python --version` phải là 3.10.x hoặc 3.11.x

### Lỗi: "No module named 'X'"
- Cài đặt module thiếu: `pip install X`
- Đảm bảo đang ở đúng virtual environment

### Lỗi: "PyTorch không cài được trên Python 3.13"
- PyTorch chưa hỗ trợ Python 3.13 đầy đủ
- Phải dùng Python 3.10 hoặc 3.11

### Lỗi: CUDA out of memory
- Giảm batch size trong Trainer.py
- Hoặc dùng CPU (chậm hơn)

### Lỗi: File not found (dataset paths)
- Kiểm tra và sửa đường dẫn trong `Config.py`

### Lỗi: Model not found
- Đảm bảo đã download và giải nén `SavedModels.zip`

### Lỗi: "pip không tìm thấy torch cho Python 3.13"
- PyTorch chưa có wheel cho Python 3.13
- Dùng Python 3.10 hoặc 3.11

## 📚 Tài Liệu Tham Khảo

- Paper: Xem `report.pdf` trong project
- Video demo: [YouTube](https://www.youtube.com/watch?v=rvivVQzxUIc)
- Presentation: [YouTube](https://www.youtube.com/watch?v=edN4z7h-9Gc&feature=youtu.be&ab_channel=BernhardKainz)

