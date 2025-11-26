# 🚀 Quick Start Guide - Nhanh Chóng Bắt Đầu

## ✅ Virtual Environment Đã Được Tạo!

Môi trường Python 3.11 đã được thiết lập và cài đặt tất cả dependencies.

## 📝 Cách Sử Dụng

### 1. Kích hoạt Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Hoặc dùng script:**
```bash
activate_env.bat
```

Sau khi kích hoạt, bạn sẽ thấy `(venv)` ở đầu dòng lệnh.

### 2. Kiểm Tra Môi Trường

```bash
# Kiểm tra Python version (nên là 3.11.9)
python --version

# Kiểm tra packages đã cài
pip list

# Test import các thư viện chính
python -c "import torch; import torchvision; import numpy; import cv2; print('All OK!')"
```

### 3. Sử Dụng Dự Án

#### Xem Dataset Samples
```bash
python DataSets/Concrete/MINI_RGBDDataset.py
```

#### Chạy Evaluation (cần có models và datasets)
```bash
python PoseEstimation/Core/Evaluation.py
```

#### Chạy Training
```bash
# Train 2D pose model
python PoseEstimation/Core/Trainer.py

# Train Faster R-CNN bbox model
python FasterRCNN/Trainer.py
```

### 4. Thoát Virtual Environment

Khi xong việc, thoát môi trường:
```bash
deactivate
```

## ⚠️ Lưu Ý

1. **Luôn kích hoạt virtual environment** trước khi chạy code
2. **Cần có SavedModels** để chạy inference (download từ OneDrive trong README)
3. **Cần có datasets** để train/evaluate (xem SETUP_GUIDE.md)
4. **Sửa đường dẫn** trong `DataSets/Utils/Config.py` nếu cần

## 🆘 Nếu Gặp Lỗi

1. **"No module named X"**: Đảm bảo đã kích hoạt venv và chạy `pip install -r requirements.txt`
2. **"Python version không đúng"**: Kiểm tra `python --version` phải là 3.11.x
3. **"File not found"**: Kiểm tra đường dẫn trong Config.py

## 📚 Tài Liệu Chi Tiết

- Xem `SETUP_GUIDE.md` để biết cách setup đầy đủ
- Xem `README.md` để biết tổng quan về dự án


