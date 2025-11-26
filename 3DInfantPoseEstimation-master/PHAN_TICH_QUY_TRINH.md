# 📋 PHÂN TÍCH QUY TRÌNH: CHỨC NĂNG PHÂN TÍCH TƯ THẾ VÀ CẢNH BÁO NGUY HIỂM

## 🎯 MỤC TIÊU

Thêm chức năng phân tích tư thế của trẻ em và phát hiện cảnh báo nguy hiểm dựa trên keypoints 3D từ model hiện có.

---

## 📊 INPUT & OUTPUT

### INPUT
- **Ảnh của trẻ em** (như hiện tại)
- **Keypoints 3D** từ model inference (16 joints, mỗi joint có x, y, z trong millimeters)

### OUTPUT
- **Ảnh visualization** (như hiện tại) + **Thông tin tư thế**
- **File JSON** (như hiện tại) + **Thông tin tư thế và cảnh báo**
- **Thông tin tư thế**: Nằm ngửa / Nằm sấp / Đứng / Ngồi / Đang ngủ
- **Cảnh báo nguy hiểm**: ⚠️ Nếu phát hiện tư thế nguy hiểm

---

## 🔄 QUY TRÌNH CHI TIẾT

### **BƯỚC 1: INFERENCE (Như hiện tại - KHÔNG THAY ĐỔI)**
```
Input: Ảnh
  ↓
Pre-process ảnh
  ↓
Model 2D Pose Estimation → pred_coords_2d (16 joints x 2D)
  ↓
Model 3D Lifting → pose3d_preds (16 joints x 3D)
```

**Output:** `pose3d_preds` - numpy array shape `(16, 3)` - tọa độ x, y, z (millimeters)

**Keypoints 3D có sẵn:**
- Index 0-5: Chân (r ankle, r knee, r hip, l hip, l knee, l ankle)
- Index 6: pelvis
- Index 7: thorax
- Index 8: upper neck
- Index 9: head top
- Index 10-15: Tay (r wrist, r elbow, r shoulder, l shoulder, l elbow, l wrist)

---

### **BƯỚC 2: TÍNH TOÁN CÁC ĐẠI LƯỢNG HÌNH HỌC (CODE MỚI)**

#### 2.1. Tính vector giữa các keypoints
```python
# Ví dụ: Vector từ hông đến đầu gối
hip_to_knee_vector = knee - hip

# Vector cột sống
spine_vector = thorax - pelvis

# Vector từ cổ đến đầu
neck_to_head_vector = head - neck
```

#### 2.2. Tính góc giữa các vector
```python
# Góc đầu gối (hip-knee-ankle)
def calculate_angle(p1, p2, p3):
    vec1 = p1 - p2
    vec2 = p3 - p2
    angle = arccos(dot(vec1, vec2) / (norm(vec1) * norm(vec2)))
    return angle

# Góc đầu gối phải
knee_angle_right = calculate_angle(hip_right, knee_right, ankle_right)
```

#### 2.3. Tính góc nghiêng của cơ thể
```python
# Góc của cột sống với mặt phẳng ngang (trục Y)
spine_angle_with_horizontal = arctan2(spine_z, spine_y)

# Hướng của đầu so với thân
head_direction = head - thorax
head_angle = arctan2(head_direction.z, head_direction.y)
```

#### 2.4. Tính vị trí tương đối
```python
# Độ cao tương đối của các bộ phận
head_height = head[1]  # Y coordinate
thorax_height = thorax[1]
pelvis_height = pelvis[1]

# So sánh vị trí
is_head_below_thorax = head_height < thorax_height
is_lying_down = abs(spine_angle_with_horizontal) > 45 degrees
```

#### 2.5. Tính độ cong của các khớp
```python
# Góc khớp vai (shoulder-elbow-wrist)
shoulder_angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
shoulder_angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)

# Góc khớp hông (pelvis-hip-knee)
hip_angle_left = calculate_angle(pelvis, hip_left, knee_left)
hip_angle_right = calculate_angle(pelvis, hip_right, knee_right)
```

---

### **BƯỚC 3: PHÂN LOẠI TƯ THẾ (CODE MỚI)**

#### 3.1. Nhận diện tư thế NẰM NGỬA
**Điều kiện:**
- Góc cột sống với mặt phẳng ngang < 45 độ
- Đầu ở vị trí cao hơn hoặc bằng với thân (head.y >= thorax.y)
- Chân và tay ở vị trí tự nhiên (không cong quá mức)

```python
if spine_angle_with_horizontal < 45 and head_height >= thorax_height:
    posture = "lying_on_back"
```

#### 3.2. Nhận diện tư thế NẰM SẤP (⚠️ NGUY HIỂM)
**Điều kiện:**
- Góc cột sống với mặt phẳng ngang < 45 độ
- Đầu ở vị trí thấp hơn hoặc bằng với thân (head.y <= thorax.y)
- Mặt quay xuống dưới

```python
if spine_angle_with_horizontal < 45 and head_height <= thorax_height:
    posture = "lying_on_stomach"  # ⚠️ DANGER
```

#### 3.3. Nhận diện tư thế ĐỨNG
**Điều kiện:**
- Góc cột sống với mặt phẳng ngang > 75 độ (gần thẳng đứng)
- Chân thẳng (góc đầu gối > 150 độ)
- Đầu ở vị trí cao nhất

```python
if spine_angle_with_horizontal > 75 and knee_angles > 150:
    posture = "standing"
```

#### 3.4. Nhận diện tư thế NGỒI
**Điều kiện:**
- Góc cột sống với mặt phẳng ngang > 45 độ (không nằm)
- Góc đầu gối < 120 độ (chân cong)
- Hông thấp hơn đầu

```python
if spine_angle_with_horizontal > 45 and knee_angles < 120:
    posture = "sitting"
```

#### 3.5. Nhận diện tư thế NGỦ
**Điều kiện:**
- Tư thế nằm (ngửa hoặc sấp)
- Cộng thêm: Nếu có video, kiểm tra tư thế giữ nguyên > 30 giây

```python
# Nếu có video/frames liên tiếp
if posture in ["lying_on_back", "lying_on_stomach"] and duration_still > 30:
    posture = "sleeping"
```

---

### **BƯỚC 4: PHÁT HIỆN TƯ THẾ NGUY HIỂM (CODE MỚI)**

#### 4.1. Phát hiện NẰM SẤP (SIDS - Sudden Infant Death Syndrome)
```python
if posture == "lying_on_stomach":
    danger_level = "HIGH"
    danger_message = "⚠️ CẢNH BÁO: Trẻ đang nằm sấp - Nguy cơ SIDS!"
    recommendation = "Khuyến nghị: Đặt trẻ nằm ngửa ngay lập tức"
```

#### 4.2. Phát hiện tư thế NGHẸT THỞ
**Điều kiện:**
- Góc cổ quá gập (< 45 độ)
- Đầu bị ép xuống gối/bề mặt
- Khoảng cách từ đầu đến thân quá gần

```python
neck_angle = calculate_angle(thorax, neck, head)
if neck_angle < 45 and head_height < thorax_height:
    danger_level = "HIGH"
    danger_message = "⚠️ CẢNH BÁO: Tư thế có thể gây nghẹt thở!"
```

#### 4.3. Phát hiện tư thế BẤT THƯỜNG
**Điều kiện:**
- Góc khớp ngoài phạm vi bình thường
- Vị trí tay/chân bất thường

```python
# Kiểm tra góc khớp bất thường
if any_joint_angle < 30 or any_joint_angle > 180:
    danger_level = "MEDIUM"
    danger_message = "⚠️ CẢNH BÁO: Phát hiện tư thế bất thường"
```

#### 4.4. Xác định mức độ nguy hiểm
```python
DANGER_LEVELS = {
    "NONE": "✅ An toàn",
    "LOW": "⚠️ Cần theo dõi",
    "MEDIUM": "⚠️ Cảnh báo",
    "HIGH": "🚨 Nguy hiểm - Cần can thiệp ngay"
}
```

---

### **BƯỚC 5: XỬ LÝ MISSING KEYPOINTS (CODE MỚI)**

#### 5.1. Kiểm tra keypoints hợp lệ
```python
# Keypoints có thể bị detect sai hoặc missing
# Giá trị (0, 0, 0) hoặc nằm ngoài phạm vi hợp lý

def is_valid_keypoint(keypoint, threshold=1.0):
    # Kiểm tra keypoint không phải (0, 0, 0)
    if np.allclose(keypoint, [0, 0, 0], atol=threshold):
        return False
    # Kiểm tra keypoint trong phạm vi hợp lý
    if np.any(np.abs(keypoint) > 1000):  # millimeters
        return False
    return True
```

#### 5.2. Xử lý khi thiếu keypoints quan trọng
```python
# Nếu thiếu keypoints quan trọng, không thể phân tích
required_keypoints = ["head", "neck", "thorax", "pelvis"]
if any(not is_valid_keypoint(keypoints[name]) for name in required_keypoints):
    return {
        "posture": "unknown",
        "confidence": 0.0,
        "error": "Missing required keypoints"
    }
```

#### 5.3. Sử dụng keypoints thay thế
```python
# Nếu thiếu head, có thể dùng neck + ước lượng
if not is_valid_keypoint(head) and is_valid_keypoint(neck):
    # Ước lượng head dựa trên neck
    estimated_head = neck + [0, 50, 0]  # ước lượng
```

---

### **BƯỚC 6: TÍCH HỢP VÀO INFERENCE SCRIPT (CODE MỚI)**

#### 6.1. Import module phân tích
```python
from PoseEstimation.PoseAnalyzer import PoseAnalyzer
```

#### 6.2. Sau khi có pose3d_preds
```python
# Sau dòng 225 trong inference_with_keypoints.py:
pose3d_preds = pose3d_output.detach().cpu().view(-1, num_joints, 3).numpy()

# THÊM: Phân tích tư thế
analyzer = PoseAnalyzer(config=cfg.MPII)
analysis_result = analyzer.analyze_pose(pose3d_preds[0])
```

#### 6.3. Thêm vào output JSON
```python
# Trong save_keypoints_json, thêm:
data["pose_analysis"] = {
    "posture": analysis_result["posture"],
    "posture_confidence": analysis_result["confidence"],
    "danger_level": analysis_result["danger_level"],
    "danger_message": analysis_result["danger_message"],
    "recommendation": analysis_result["recommendation"]
}
```

#### 6.4. Thêm vào visualization
```python
# Trong visualization, thêm text overlay:
ax2.text(10, 30, f"Tư thế: {analysis_result['posture']}", 
         fontsize=12, color='blue', bbox=dict(boxstyle='round', facecolor='white'))
if analysis_result['danger_level'] != "NONE":
    ax2.text(10, 60, analysis_result['danger_message'], 
             fontsize=14, color='red', weight='bold',
             bbox=dict(boxstyle='round', facecolor='yellow'))
```

---

## 📁 CẤU TRÚC FILE CẦN TẠO

### **1. PoseEstimation/PoseAnalyzer.py**
Module chính để phân tích tư thế
- Class: `PoseAnalyzer`
- Methods:
  - `analyze_pose(keypoints_3d)` - Phân tích tư thế chính
  - `calculate_angles(keypoints_3d)` - Tính các góc khớp
  - `detect_posture(keypoints_3d)` - Nhận diện tư thế
  - `detect_danger(keypoints_3d, posture)` - Phát hiện nguy hiểm
  - `is_valid_keypoint(keypoint)` - Kiểm tra keypoint hợp lệ

### **2. PoseEstimation/PostureClassifier.py** (Optional - tách logic)
Module phân loại tư thế
- Class: `PostureClassifier`
- Methods:
  - `classify_lying_on_back()` - Nhận diện nằm ngửa
  - `classify_lying_on_stomach()` - Nhận diện nằm sấp
  - `classify_standing()` - Nhận diện đứng
  - `classify_sitting()` - Nhận diện ngồi

### **3. PoseEstimation/DangerDetector.py** (Optional - tách logic)
Module phát hiện nguy hiểm
- Class: `DangerDetector`
- Methods:
  - `detect_sids_risk()` - Phát hiện nguy cơ SIDS
  - `detect_suffocation_risk()` - Phát hiện nguy cơ nghẹt thở
  - `detect_abnormal_posture()` - Phát hiện tư thế bất thường

---

## 🔧 CÁC HÀM TIỆN ÍCH CẦN TẠO

### **1. Hàm tính toán hình học**
```python
def calculate_angle(p1, p2, p3):
    """Tính góc tại p2 giữa p1-p2-p3"""
    pass

def calculate_distance(p1, p2):
    """Tính khoảng cách giữa 2 điểm"""
    pass

def calculate_vector(p1, p2):
    """Tính vector từ p1 đến p2"""
    pass

def angle_with_horizontal(vector):
    """Tính góc của vector với mặt phẳng ngang"""
    pass
```

### **2. Hàm kiểm tra điều kiện**
```python
def is_lying_down(spine_angle):
    """Kiểm tra có đang nằm không"""
    pass

def is_head_below_thorax(head_y, thorax_y):
    """Kiểm tra đầu có thấp hơn thân không"""
    pass

def are_joints_straight(joint_angles, threshold=150):
    """Kiểm tra các khớp có thẳng không"""
    pass
```

---

## 📊 THAM SỐ VÀ NGƯỠNG

### **Ngưỡng góc (degrees)**
- Nằm ngang: < 45 độ
- Nghiêng: 45-75 độ
- Đứng: > 75 độ

### **Ngưỡng góc khớp (degrees)**
- Đầu gối thẳng: > 150 độ
- Đầu gối cong (ngồi): < 120 độ
- Góc cổ bình thường: 90-180 độ
- Góc cổ nguy hiểm: < 45 độ

### **Ngưỡng vị trí (millimeters)**
- Đầu thấp hơn thân: head.y < thorax.y - 50mm
- Keypoint hợp lệ: |x|, |y|, |z| < 1000mm
- Keypoint missing: (0, 0, 0) hoặc gần (0, 0, 0)

---

## ✅ CHECKLIST TRIỂN KHAI

### **Phase 1: Module cơ bản**
- [ ] Tạo file `PoseEstimation/PoseAnalyzer.py`
- [ ] Implement các hàm tính toán hình học
- [ ] Implement hàm phân loại tư thế cơ bản
- [ ] Test với keypoints mẫu

### **Phase 2: Phát hiện nguy hiểm**
- [ ] Implement phát hiện nằm sấp (SIDS)
- [ ] Implement phát hiện nghẹt thở
- [ ] Implement phát hiện tư thế bất thường
- [ ] Test với các trường hợp nguy hiểm

### **Phase 3: Tích hợp**
- [ ] Tích hợp vào `inference_with_keypoints.py`
- [ ] Thêm output vào JSON
- [ ] Thêm visualization vào ảnh output
- [ ] Test end-to-end

### **Phase 4: Tối ưu**
- [ ] Xử lý missing keypoints
- [ ] Cải thiện độ chính xác phân loại
- [ ] Tối ưu hiệu suất
- [ ] Viết documentation

---

## 🎯 KẾT QUẢ MONG ĐỢI

### **Output JSON mẫu:**
```json
{
  "keypoints_2d": {...},
  "keypoints_3d": {...},
  "pose_analysis": {
    "posture": "lying_on_stomach",
    "posture_confidence": 0.92,
    "danger_level": "HIGH",
    "danger_message": "⚠️ CẢNH BÁO: Trẻ đang nằm sấp - Nguy cơ SIDS!",
    "recommendation": "Khuyến nghị: Đặt trẻ nằm ngửa ngay lập tức",
    "angles": {
      "spine_angle": 25.3,
      "knee_left": 165.2,
      "knee_right": 163.8,
      "neck_angle": 135.5
    }
  }
}
```

### **Output Console:**
```
✅ 3D pose đã được dự đoán
📊 Phân tích tư thế:
   - Tư thế: lying_on_stomach
   - Độ tin cậy: 92%
   🚨 NGUY HIỂM: Trẻ đang nằm sấp - Nguy cơ SIDS!
   💡 Khuyến nghị: Đặt trẻ nằm ngửa ngay lập tức
```

---

## 📝 LƯU Ý QUAN TRỌNG

1. **Không cần training lại model** - Chỉ cần logic phân tích
2. **Sử dụng model hiện có** - Keypoints 3D từ model hiện tại
3. **Dễ dàng sử dụng** - Chỉ cần chạy inference với ảnh
4. **Có thể mở rộng** - Dễ thêm tư thế mới hoặc điều kiện mới
5. **Xử lý edge cases** - Missing keypoints, góc bất thường

---

## 🚀 BƯỚC TIẾP THEO

Sau khi phân tích xong, tôi sẽ:
1. Tạo các module theo quy trình trên
2. Test từng bước một
3. Tích hợp vào inference script
4. Viết documentation chi tiết

