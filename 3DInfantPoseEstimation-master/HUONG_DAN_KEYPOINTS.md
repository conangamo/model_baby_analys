# 📊 Hướng Dẫn: Output Keypoints (Tọa Độ Các Khớp)

## ✅ Đúng! Output là Tọa Độ Các Khớp

Model này output **tọa độ các khớp (keypoints)** của infant, bao gồm:

1. **2D Keypoints**: Tọa độ (x, y) trên ảnh (pixel coordinates)
2. **3D Keypoints**: Tọa độ (x, y, z) trong không gian 3D (millimeters)

---

## 📋 Các Khớp (Joints) Được Dự Đoán

Model dự đoán **16 khớp** theo format MPII:

1. **r ankle** - Mắt cá chân phải
2. **r knee** - Đầu gối phải
3. **r hip** - Hông phải
4. **l hip** - Hông trái
5. **l knee** - Đầu gối trái
6. **l ankle** - Mắt cá chân trái
7. **pelvis** - Xương chậu
8. **thorax** - Ngực
9. **upper neck** - Cổ trên
10. **head top** - Đỉnh đầu
11. **r wrist** - Cổ tay phải
12. **r elbow** - Khuỷu tay phải
13. **r shoulder** - Vai phải
14. **l shoulder** - Vai trái
15. **l elbow** - Khuỷu tay trái
16. **l wrist** - Cổ tay trái

---

## 🎯 Output Format

### 1. **2D Keypoints** (Tọa Độ 2D)

- **Format**: Pixel coordinates trên ảnh
- **Đơn vị**: Pixel
- **Ví dụ**: `(x, y)` = `(320.5, 240.3)`
  - `x`: Tọa độ ngang (từ trái sang phải)
  - `y`: Tọa độ dọc (từ trên xuống dưới)

### 2. **3D Keypoints** (Tọa Độ 3D)

- **Format**: 3D coordinates trong không gian
- **Đơn vị**: Millimeters (mm)
- **Ví dụ**: `(x, y, z)` = `(120.5, -50.3, 200.1)`
  - `x`: Tọa độ ngang
  - `y`: Tọa độ dọc
  - `z`: Tọa độ sâu (depth)

---

## 📁 Cách Lưu Keypoints Ra File

### Cách 1: Dùng Script Mới (Khuyến nghị)

Script `inference_with_keypoints.py` sẽ tự động lưu keypoints:

```bash
# Chạy inference và lưu keypoints (JSON)
python inference_with_keypoints.py --image Images/baby.jpg

# Lưu cả JSON và CSV
python inference_with_keypoints.py --image Images/baby.jpg --save-csv
```

**Output sẽ có:**
- `Images/InferenceOutput/baby_result.png` - Ảnh visualization
- `Images/InferenceOutput/baby_keypoints.json` - Keypoints dạng JSON
- `Images/InferenceOutput/baby_keypoints.csv` - Keypoints dạng CSV (nếu dùng --save-csv)

---

### Cách 2: Dùng Script Cũ + Tự Extract

Script `inference_simple.py` chỉ tạo ảnh visualization. Nếu muốn lấy keypoints, bạn cần sửa code hoặc dùng script mới.

---

## 📄 Format File JSON

File JSON có cấu trúc như sau:

```json
{
  "keypoints_2d": {
    "format": "pixel_coordinates",
    "description": "2D keypoints in image pixel coordinates (x, y)",
    "joints": {
      "r ankle": {
        "x": 320.5,
        "y": 450.2
      },
      "r knee": {
        "x": 315.8,
        "y": 380.1
      },
      ...
    }
  },
  "keypoints_3d": {
    "format": "millimeters",
    "description": "3D keypoints in millimeters (x, y, z)",
    "joints": {
      "r ankle": {
        "x": 120.5,
        "y": -50.3,
        "z": 200.1
      },
      "r knee": {
        "x": 115.2,
        "y": -30.1,
        "z": 180.5
      },
      ...
    }
  }
}
```

---

## 📊 Format File CSV

File CSV có cấu trúc như sau:

```csv
Joint Name,2D_X,2D_Y,3D_X,3D_Y,3D_Z
r ankle,320.50,450.20,120.50,-50.30,200.10
r knee,315.80,380.10,115.20,-30.10,180.50
...
```

---

## 💻 Cách Đọc Keypoints Từ File

### Đọc từ JSON (Python)

```python
import json

# Đọc file JSON
with open('Images/InferenceOutput/baby_keypoints.json', 'r') as f:
    data = json.load(f)

# Lấy 2D keypoints
keypoints_2d = data['keypoints_2d']['joints']
print(f"2D coordinates của 'r ankle': ({keypoints_2d['r ankle']['x']}, {keypoints_2d['r ankle']['y']})")

# Lấy 3D keypoints
keypoints_3d = data['keypoints_3d']['joints']
print(f"3D coordinates của 'r ankle': ({keypoints_3d['r ankle']['x']}, {keypoints_3d['r ankle']['y']}, {keypoints_3d['r ankle']['z']})")
```

### Đọc từ CSV (Python)

```python
import csv

# Đọc file CSV
with open('Images/InferenceOutput/baby_keypoints.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['Joint Name']}: 2D=({row['2D_X']}, {row['2D_Y']}), 3D=({row['3D_X']}, {row['3D_Y']}, {row['3D_Z']})")
```

---

## 🎯 Ứng Dụng Của Keypoints

Keypoints có thể dùng để:

1. **Phân tích tư thế**: Xác định tư thế của infant (nằm, ngồi, đứng)
2. **Theo dõi chuyển động**: Track movement của infant qua thời gian
3. **Phát hiện bất thường**: Phát hiện các tư thế bất thường
4. **Đo lường**: Tính toán góc khớp, khoảng cách giữa các khớp
5. **Visualization**: Vẽ skeleton trên ảnh/video

---

## 📝 Ví Dụ Sử Dụng

### Ví Dụ 1: Tính Khoảng Cách Giữa 2 Khớp

```python
import json
import numpy as np

# Đọc keypoints
with open('baby_keypoints.json', 'r') as f:
    data = json.load(f)

# Lấy 3D coordinates
knee = data['keypoints_3d']['joints']['r knee']
ankle = data['keypoints_3d']['joints']['r ankle']

# Tính khoảng cách
distance = np.sqrt(
    (knee['x'] - ankle['x'])**2 + 
    (knee['y'] - ankle['y'])**2 + 
    (knee['z'] - ankle['z'])**2
)

print(f"Khoảng cách giữa đầu gối và mắt cá chân phải: {distance:.2f} mm")
```

### Ví Dụ 2: Tính Góc Khớp

```python
import json
import numpy as np

# Đọc keypoints
with open('baby_keypoints.json', 'r') as f:
    data = json.load(f)

# Lấy 3D coordinates của 3 khớp tạo thành góc
hip = np.array([data['keypoints_3d']['joints']['r hip']['x'],
                data['keypoints_3d']['joints']['r hip']['y'],
                data['keypoints_3d']['joints']['r hip']['z']])
knee = np.array([data['keypoints_3d']['joints']['r knee']['x'],
                 data['keypoints_3d']['joints']['r knee']['y'],
                 data['keypoints_3d']['joints']['r knee']['z']])
ankle = np.array([data['keypoints_3d']['joints']['r ankle']['x'],
                  data['keypoints_3d']['joints']['r ankle']['y'],
                  data['keypoints_3d']['joints']['r ankle']['z']])

# Tính vector
vec1 = hip - knee
vec2 = ankle - knee

# Tính góc
cos_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
angle = np.arccos(np.clip(cos_angle, -1, 1)) * 180 / np.pi

print(f"Góc đầu gối phải: {angle:.2f} độ")
```

---

## ✅ Tóm Tắt

| Thông Tin | Mô Tả |
|-----------|-------|
| **Output** | Tọa độ các khớp (keypoints) |
| **2D Keypoints** | (x, y) trong pixel coordinates |
| **3D Keypoints** | (x, y, z) trong millimeters |
| **Số lượng joints** | 16 khớp |
| **Format lưu** | JSON, CSV (tùy chọn) |
| **Script** | `inference_with_keypoints.py` |

---

## 🚀 Cách Sử Dụng

```bash
# 1. Kích hoạt venv
venv\Scripts\activate

# 2. Chạy inference và lưu keypoints
python inference_with_keypoints.py --image Images/baby.jpg --save-csv

# 3. Xem kết quả
# - Ảnh: Images/InferenceOutput/baby_result.png
# - JSON: Images/InferenceOutput/baby_keypoints.json
# - CSV: Images/InferenceOutput/baby_keypoints.csv
```

---

**Chúc bạn thành công! 🎉**

