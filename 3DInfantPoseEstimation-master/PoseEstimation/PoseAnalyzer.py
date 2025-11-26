"""
Module phân tích tư thế và phát hiện nguy hiểm dựa trên keypoints 3D
"""

import numpy as np
import math


class PoseAnalyzer:
    """
    Class phân tích tư thế của trẻ em từ keypoints 3D
    """
    
    def __init__(self, config=None):
        """
        Khởi tạo PoseAnalyzer
        
        Args:
            config: Config dictionary chứa thông tin về joints (từ cfg.MPII)
        """
        # Helper để sinh mapping đồng nhất cho joints
        def _generate_variants(name):
            variants = set()
            if name is None:
                return variants
            base = name.strip()
            variants.add(base)
            variants.add(base.lower())
            variants.add(base.replace(" ", "_"))
            variants.add(base.lower().replace(" ", "_"))
            variants.add(base.replace(" ", ""))
            variants.add(base.lower().replace(" ", ""))
            variants.add(base.lower().replace("-", "_"))
            variants.add(base.lower().replace("-", ""))
            return variants

        if config is None:
            # Default indices theo MPII format
            default_joint_names = [
                "r ankle", "r knee", "r hip",
                "l hip", "l knee", "l ankle",
                "pelvis", "thorax", "upper neck", "head top",
                "r wrist", "r elbow", "r shoulder",
                "l shoulder", "l elbow", "l wrist"
            ]
        else:
            # Sử dụng config từ cfg.MPII
            default_joint_names = config.get("jointNames", [])

        self.joint_names = default_joint_names
        self.joint_indices = {}

        for idx, name in enumerate(self.joint_names):
            for variant in _generate_variants(name):
                self.joint_indices[variant] = idx
        
        # Ngưỡng góc (degrees) - Đã được điều chỉnh để chính xác hơn
        self.ANGLE_THRESHOLDS = {
            'lying_horizontal': 60,      # Góc cột sống < 60° = nằm (tăng từ 45°)
            'lying_definite': 35,        # Góc cột sống < 35° = chắc chắn nằm
            'standing_vertical': 70,     # Góc cột sống > 70° = đứng (giảm từ 75°)
            'standing_definite': 80,     # Góc cột sống > 80° = chắc chắn đứng
            'knee_straight': 150,        # Góc đầu gối > 150° = thẳng
            'knee_bent_sitting': 130,    # Góc đầu gối < 130° = cong (ngồi) (tăng từ 120°)
            'neck_danger': 45,           # Góc cổ < 45° = nguy hiểm
            'neck_comfortable': 90,      # Góc cổ > 90° = thoải mái
            'prone_spine_angle': 55,
            'prone_knee_straight': 150,
            'shoulder_relaxed_lower': 5,
            'shoulder_relaxed_upper': 178,
            'shoulder_alert_upper': 180
        }
        
        # Ngưỡng vị trí (millimeters)
        self.POSITION_THRESHOLDS = {
            'head_below_thorax': 50,     # Đầu thấp hơn thân > 50mm = nằm sấp
            'head_back_margin': 80,      # Đầu cao hơn thân > 80mm = nằm ngửa rõ ràng
            'head_ambiguous_margin': 30, # Trong khoảng ±30mm coi là nghi ngờ
            'keypoint_valid_max': 1000   # Keypoint hợp lệ nếu |x|,|y|,|z| < 1000mm
        }
    
    def get_joint(self, keypoints, joint_name):
        """
        Lấy tọa độ keypoint theo tên
        
        Args:
            keypoints: numpy array shape (16, 3) hoặc (num_joints, 3)
            joint_name: Tên joint (string)
        
        Returns:
            numpy array shape (3,) - tọa độ [x, y, z]
        """
        if joint_name is None:
            return None
        idx = self.joint_indices.get(joint_name)
        if idx is None:
            normalized = joint_name.lower().replace(" ", "_").replace("-", "_")
            idx = self.joint_indices.get(normalized)
        if idx is None:
            normalized_no_space = joint_name.lower().replace(" ", "").replace("-", "")
            idx = self.joint_indices.get(normalized_no_space)
        if idx is None or idx >= len(keypoints):
            return None
        return keypoints[idx]
    
    def is_valid_keypoint(self, keypoint, threshold=1.0, allow_zero=False):
        """
        Kiểm tra keypoint có hợp lệ không
        
        Args:
            keypoint: numpy array shape (3,) hoặc None
            threshold: Ngưỡng để coi là (0,0,0)
            allow_zero: Cho phép keypoint là (0,0,0) - dùng cho pelvis (gốc tọa độ)
        
        Returns:
            bool: True nếu hợp lệ, False nếu không
        """
        if keypoint is None:
            return False
        
        # Kiểm tra keypoint không phải (0, 0, 0) - trừ pelvis
        if not allow_zero:
            if np.allclose(keypoint, [0, 0, 0], atol=threshold):
                return False
        
        # Kiểm tra keypoint trong phạm vi hợp lý
        # Chỉ kiểm tra nếu không phải pelvis (pelvis có thể gần 0)
        if not allow_zero:
            if np.any(np.abs(keypoint) > self.POSITION_THRESHOLDS['keypoint_valid_max']):
                return False
        
        # Kiểm tra có chứa NaN hoặc Inf không
        if np.any(np.isnan(keypoint)) or np.any(np.isinf(keypoint)):
            return False
        
        return True
    
    def calculate_vector(self, p1, p2):
        """
        Tính vector từ p1 đến p2
        
        Args:
            p1, p2: numpy array shape (3,) - tọa độ 3D
        
        Returns:
            numpy array shape (3,) - vector
        """
        if p1 is None or p2 is None:
            return None
        return p2 - p1
    
    def calculate_distance(self, p1, p2):
        """
        Tính khoảng cách giữa 2 điểm
        
        Args:
            p1, p2: numpy array shape (3,) - tọa độ 3D
        
        Returns:
            float: Khoảng cách (millimeters)
        """
        if p1 is None or p2 is None:
            return None
        return np.linalg.norm(p2 - p1)
    
    def calculate_angle(self, p1, p2, p3):
        """
        Tính góc tại p2 giữa p1-p2-p3
        
        Args:
            p1, p2, p3: numpy array shape (3,) - tọa độ 3D
        
        Returns:
            float: Góc tính bằng degrees (0-180)
        """
        if p1 is None or p2 is None or p3 is None:
            return None
        
        # Vector từ p2 đến p1 và p2 đến p3
        vec1 = p1 - p2
        vec2 = p3 - p2
        
        # Tính góc giữa 2 vector
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        # Tránh chia cho 0
        if norm1 == 0 or norm2 == 0:
            return None
        
        cos_angle = np.clip(dot_product / (norm1 * norm2), -1.0, 1.0)
        angle_rad = np.arccos(cos_angle)
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
    
    def angle_with_horizontal(self, vector):
        """
        Tính góc của vector với mặt phẳng ngang (trục Y)
        
        Args:
            vector: numpy array shape (3,) - vector [x, y, z]
        
        Returns:
            float: Góc tính bằng degrees (0-90)
                  0° = nằm ngang hoàn toàn
                  90° = thẳng đứng hoàn toàn
        """
        if vector is None:
            return None
        
        # Góc với trục Y (chiều thẳng đứng)
        # Y là trục chiều cao (vertical)
        # Góc với mặt phẳng ngang = 90° - góc với trục Y
        if np.linalg.norm(vector) == 0:
            return None
        
        # Tính góc với trục Y (vertical)
        # dot(vector, [0,1,0]) = vector[1]
        # norm(vector) * 1 = norm(vector)
        cos_angle_with_y = abs(vector[1]) / np.linalg.norm(vector)
        angle_with_y_rad = np.arccos(np.clip(cos_angle_with_y, -1.0, 1.0))
        angle_with_y_deg = np.degrees(angle_with_y_rad)
        
        # Góc với mặt phẳng ngang = 90° - góc với trục Y
        angle_with_horizontal = 90.0 - angle_with_y_deg
        
        return angle_with_horizontal
    
    def calculate_all_angles(self, keypoints):
        """
        Tính tất cả các góc khớp quan trọng
        
        Args:
            keypoints: numpy array shape (16, 3) - keypoints 3D
        
        Returns:
            dict: Dictionary chứa các góc
        """
        angles = {}
        
        # Lấy các keypoints
        pelvis = self.get_joint(keypoints, 'pelvis')
        thorax = self.get_joint(keypoints, 'thorax')
        neck = self.get_joint(keypoints, 'upper_neck')
        head = self.get_joint(keypoints, 'head_top')
        
        r_hip = self.get_joint(keypoints, 'r_hip')
        r_knee = self.get_joint(keypoints, 'r_knee')
        r_ankle = self.get_joint(keypoints, 'r_ankle')
        
        l_hip = self.get_joint(keypoints, 'l_hip')
        l_knee = self.get_joint(keypoints, 'l_knee')
        l_ankle = self.get_joint(keypoints, 'l_ankle')
        
        r_shoulder = self.get_joint(keypoints, 'r_shoulder')
        r_elbow = self.get_joint(keypoints, 'r_elbow')
        r_wrist = self.get_joint(keypoints, 'r_wrist')
        
        l_shoulder = self.get_joint(keypoints, 'l_shoulder')
        l_elbow = self.get_joint(keypoints, 'l_elbow')
        l_wrist = self.get_joint(keypoints, 'l_wrist')
        
        # Góc cột sống với mặt phẳng ngang
        # Pelvis có thể là (0,0,0) vì là gốc tọa độ - cho phép zero
        if self.is_valid_keypoint(pelvis, allow_zero=True) and self.is_valid_keypoint(thorax):
            spine_vector = self.calculate_vector(pelvis, thorax)
            angles['spine_angle'] = self.angle_with_horizontal(spine_vector)
        else:
            angles['spine_angle'] = None
        
        # Góc đầu gối
        if self.is_valid_keypoint(r_hip) and self.is_valid_keypoint(r_knee) and self.is_valid_keypoint(r_ankle):
            angles['knee_right'] = self.calculate_angle(r_hip, r_knee, r_ankle)
        else:
            angles['knee_right'] = None
        
        if self.is_valid_keypoint(l_hip) and self.is_valid_keypoint(l_knee) and self.is_valid_keypoint(l_ankle):
            angles['knee_left'] = self.calculate_angle(l_hip, l_knee, l_ankle)
        else:
            angles['knee_left'] = None
        
        # Góc cổ
        if self.is_valid_keypoint(thorax) and self.is_valid_keypoint(neck) and self.is_valid_keypoint(head):
            angles['neck_angle'] = self.calculate_angle(thorax, neck, head)
        else:
            angles['neck_angle'] = None
        
        # Góc khớp vai
        if self.is_valid_keypoint(r_shoulder) and self.is_valid_keypoint(r_elbow) and self.is_valid_keypoint(r_wrist):
            angles['shoulder_right'] = self.calculate_angle(r_shoulder, r_elbow, r_wrist)
        else:
            angles['shoulder_right'] = None
        
        if self.is_valid_keypoint(l_shoulder) and self.is_valid_keypoint(l_elbow) and self.is_valid_keypoint(l_wrist):
            angles['shoulder_left'] = self.calculate_angle(l_shoulder, l_elbow, l_wrist)
        else:
            angles['shoulder_left'] = None
        
        return angles
    
    def detect_posture(self, keypoints):
        """
        Nhận diện tư thế của trẻ
        
        Args:
            keypoints: numpy array shape (16, 3) - keypoints 3D
        
        Returns:
            dict: {
                'posture': str,  # 'lying_on_back', 'lying_on_stomach', 'standing', 'sitting', 'unknown'
                'confidence': float,  # 0.0 - 1.0
                'angles': dict,
                'reasoning': str
            }
        """
        # Kiểm tra keypoints quan trọng
        pelvis = self.get_joint(keypoints, 'pelvis')
        thorax = self.get_joint(keypoints, 'thorax')
        neck = self.get_joint(keypoints, 'upper_neck')
        head = self.get_joint(keypoints, 'head_top')
        
        # Pelvis có thể là (0,0,0) vì là gốc tọa độ - cho phép zero
        if not (self.is_valid_keypoint(pelvis, allow_zero=True) and self.is_valid_keypoint(thorax)):
            return {
                'posture': 'unknown',
                'confidence': 0.0,
                'angles': {},
                'reasoning': 'Missing required keypoints (pelvis or thorax)'
            }
        
        # Tính các góc
        angles = self.calculate_all_angles(keypoints)
        spine_angle = angles.get('spine_angle')
        
        if spine_angle is None:
            return {
                'posture': 'unknown',
                'confidence': 0.0,
                'angles': angles,
                'reasoning': 'Cannot calculate spine angle'
            }
        
        # So sánh vị trí Y (chiều cao)
        # Lưu ý: Trong hệ tọa độ 3D, Y âm = cao hơn (vì pelvis ~ 0, head/thorax thường âm)
        # Kiểm tra head có hợp lệ không (head có thể có giá trị âm lớn, đó là bình thường)
        head_is_valid = head is not None and self.is_valid_keypoint(head)
        head_y = head[1] if head_is_valid else None
        thorax_y = thorax[1] if thorax is not None else None
        pelvis_y = pelvis[1] if pelvis is not None else None
        neck_is_valid = neck is not None and self.is_valid_keypoint(neck)
        neck_y = neck[1] if neck_is_valid else None
        head_thorax_delta = None
        if head_y is not None and thorax_y is not None:
            head_thorax_delta = thorax_y - head_y  # dương => head cao hơn
        
        # Tính khoảng cách và tỷ lệ chiều cao
        head_to_thorax_distance = abs(head_y - thorax_y) if (head_y is not None) else None
        thorax_to_pelvis_distance = abs(thorax_y - pelvis_y)
        
        # Tính body ratio (tỷ lệ chiều cao thân trên/thân dưới)
        if head_y is not None:
            upper_body_height = abs(head_y - thorax_y) + abs(thorax_y - pelvis_y)
            body_ratio = head_to_thorax_distance / thorax_to_pelvis_distance if thorax_to_pelvis_distance > 0 else None
        else:
            body_ratio = None
        head_height_above_pelvis = None
        if head_y is not None and pelvis_y is not None:
            head_height_above_pelvis = pelvis_y - head_y
        
        # Lấy góc đầu gối trung bình, min, max
        knee_angles = []
        if angles.get('knee_right') is not None:
            knee_angles.append(angles['knee_right'])
        if angles.get('knee_left') is not None:
            knee_angles.append(angles['knee_left'])
        avg_knee_angle = np.mean(knee_angles) if knee_angles else None
        min_knee_angle = min(knee_angles) if knee_angles else None
        max_knee_angle = max(knee_angles) if knee_angles else None
        
        legs_drawn_posture = (
            spine_angle is not None
            and 60 <= spine_angle <= 110
            and min_knee_angle is not None
            and min_knee_angle < 100
            and head_thorax_delta is not None
            and head_thorax_delta >= 30
            and head_y is not None
            and thorax_y is not None
            and head_y < thorax_y
        )

        # Phân loại tư thế với logic cải tiến - THỨ TỰ QUAN TRỌNG!
        confidence = 1.0
        reasoning = []
        force_safe_posture = False
        
        # ========== PHÂN LOẠI CHÍNH DỰA TRÊN NHIỀU YẾU TỐ ==========
        
        # 1. Kiểm tra NẰM (lying) - Điều kiện: Góc cột sống < 60°
        is_lying_angle = spine_angle < self.ANGLE_THRESHOLDS['lying_horizontal']
        is_lying_with_support = (spine_angle < 65 and 
                                 head_y is not None and 
                                 head_y < thorax_y)  # Head cao hơn (Y nhỏ hơn = cao hơn)
        
        if is_lying_angle or is_lying_with_support:
            # Đang nằm - kiểm tra ngửa hay sấp
            if head_y is not None and thorax_y is not None:
                head_delta = thorax_y - head_y  # dương: head cao hơn
                back_margin = self.POSITION_THRESHOLDS.get('head_back_margin', 80)
                stomach_margin = self.POSITION_THRESHOLDS.get('head_below_thorax', 50)
                ambiguous_margin = self.POSITION_THRESHOLDS.get('head_ambiguous_margin', 30)

                if head_delta > back_margin:
                    # Head significantly higher than thorax = lying on back
                    if spine_angle < self.ANGLE_THRESHOLDS['lying_definite']:
                        posture = 'lying_on_back'
                        confidence = 0.95
                        reasoning.append(f"Spine angle {spine_angle:.1f}° (definitely lying), head higher than thorax by {head_delta:.1f} mm")
                    else:
                        posture = 'lying_on_back'
                        confidence = 0.85
                        reasoning.append(f"Spine angle {spine_angle:.1f}° (lying), head higher than thorax by {head_delta:.1f} mm")
                elif head_delta < -stomach_margin:
                    # Head clearly lower than thorax = lying on stomach
                    posture = 'lying_on_stomach'
                    confidence = 0.90
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (lying), head lower than thorax by {abs(head_delta):.1f} mm ⚠️")
                else:
                    # Ambiguous zone – dùng thêm neck angle để quyết định
                    neck_angle = angles.get('neck_angle')
                    if neck_angle is not None and neck_angle < 130:
                        posture = 'lying_on_stomach'
                        confidence = 0.85
                        reasoning.append(f"Spine angle {spine_angle:.1f}° (lying), head offset {head_delta:.1f} mm, bent neck {neck_angle:.1f}° → likely stomach ⚠️")
                    elif neck_angle is not None and neck_angle > 150:
                        posture = 'lying_on_back'
                        confidence = 0.85
                        reasoning.append(f"Spine angle {spine_angle:.1f}° (lying), head offset {head_delta:.1f} mm, straight neck {neck_angle:.1f}° → back")
                    else:
                        # Nếu neck angle không giúp nhiều, chọn dựa trên dấu của head_delta nhỏ
                        if head_delta >= -ambiguous_margin:
                            posture = 'lying_on_back'
                            confidence = 0.75
                            reasoning.append(f"Spine angle {spine_angle:.1f}° (lying), head roughly level with thorax (+{head_delta:.1f} mm)")
                        else:
                            posture = 'lying_on_stomach'
                            confidence = 0.80
                            reasoning.append(f"Spine angle {spine_angle:.1f}° (lying), head slightly below thorax ({head_delta:.1f} mm) ⚠️")
            else:
                # No head info, rely only on spine_angle
                if spine_angle < self.ANGLE_THRESHOLDS['lying_definite']:
                    posture = 'lying'
                    confidence = 0.80
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (definitely lying), head position unknown")
                else:
                    posture = 'lying'
                    confidence = 0.70
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (lying), head position unknown")
        
        elif legs_drawn_posture:
            posture = 'lying_with_legs_drawn_up'
            confidence = max(confidence, 0.92)
            reasoning.append(
                f"Spine angle {spine_angle:.1f}° with knees flexed (min {min_knee_angle:.1f}°) and head higher than thorax by {head_thorax_delta:.1f} mm → lying with legs drawn up"
            )
            force_safe_posture = True

        # 3. Kiểm tra STANDING - ƯU TIÊN CAO khi spine > 70° (kiểm tra trước SITTING!)
        # Điều kiện: Spine angle > 70° VÀ chân không gập quá sâu
        elif (
            spine_angle > self.ANGLE_THRESHOLDS['standing_vertical']
            and head_height_above_pelvis is not None
            and head_height_above_pelvis >= self.POSITION_THRESHOLDS.get('standing_head_clearance', 150)
        ):
            # Nếu có ít nhất một chân gập rất sâu (< 80°) thì ưu tiên xem là sitting/transition
            if min_knee_angle is not None and min_knee_angle < 80:
                posture = 'sitting'
                confidence = 0.80
                reasoning.append(
                    f"Spine angle {spine_angle:.1f}° (upright) nhưng chân gập sâu (min {min_knee_angle:.1f}°) → sitting"
                )
            # Nếu spine > 80° → standing chắc chắn (rất thẳng)
            elif spine_angle > self.ANGLE_THRESHOLDS['standing_definite']:
                posture = 'standing'
                confidence = 0.95
                reasoning.append(f"Spine angle {spine_angle:.1f}° (definitely standing, very upright)")
            
            # Spine 70-80° → cần kiểm tra chân
            elif max_knee_angle is not None or min_knee_angle is not None:
                # Có ít nhất 1 chân thẳng (>140°) → standing
                if max_knee_angle is not None and max_knee_angle > 140:
                    posture = 'standing'
                    confidence = 0.90
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (standing), at least one straight leg ({max_knee_angle:.1f}°)")
                # Có ít nhất 1 chân khá thẳng (>110°) VÀ trung bình > 85° → standing
                elif max_knee_angle is not None and max_knee_angle > 110 and avg_knee_angle is not None and avg_knee_angle > 85:
                    posture = 'standing'
                    confidence = 0.85
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (standing), at least one fairly straight leg ({max_knee_angle:.1f}°, avg {avg_knee_angle:.1f}°)")
                # Cả 2 chân không quá gập (min > 100°) → standing
                elif min_knee_angle is not None and min_knee_angle > 100:
                    posture = 'standing'
                    confidence = 0.85
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (standing), both legs not too bent (min {min_knee_angle:.1f}°)")
                # Trung bình > 120° VÀ min > 90° → standing (một chân có thể hơi gập)
                elif avg_knee_angle is not None and avg_knee_angle > 120 and min_knee_angle is not None and min_knee_angle > 90:
                    posture = 'standing'
                    confidence = 0.80
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (standing), average knee {avg_knee_angle:.1f}° (one leg may be slightly bent)")
                # Trung bình > 90° VÀ max > 105° → standing (một chân khá thẳng, một chân hơi gập)
                elif avg_knee_angle is not None and avg_knee_angle > 90 and max_knee_angle is not None and max_knee_angle > 105:
                    posture = 'standing'
                    confidence = 0.80
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (standing), one leg fairly straight ({max_knee_angle:.1f}°), average {avg_knee_angle:.1f}°")
                # Các trường hợp khác → vẫn có thể standing nhưng confidence thấp hơn
                else:
                    posture = 'standing'
                    confidence = 0.75
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (standing), legs somewhat bent (avg {avg_knee_angle:.1f}° if available, max {max_knee_angle:.1f}° if available)")
            else:
                # Không có thông tin chân → dựa vào spine angle
                posture = 'standing'
                confidence = 0.75
                reasoning.append(f"Spine angle {spine_angle:.1f}° (standing), no knee angle information")
        
        # 4. Kiểm tra SITTING - Chỉ khi spine 45-75° VÀ chân gập rõ ràng
        # Điều kiện: Spine angle 45-75° VÀ cả 2 chân đều gập (< 130°)
        elif spine_angle >= 45 and spine_angle <= 75:
            if min_knee_angle is not None and max_knee_angle is not None:
                # Cả 2 chân đều gập rõ ràng: min < 110° VÀ max < 130°
                if min_knee_angle < 110 and max_knee_angle < 130:
                    posture = 'sitting'
                    confidence = 0.90
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (upright), both legs clearly bent (left {angles.get('knee_left', 'N/A'):.1f}°, right {angles.get('knee_right', 'N/A'):.1f}°)" if angles.get('knee_left') is not None and angles.get('knee_right') is not None else f"Spine angle {spine_angle:.1f}° (upright), both legs clearly bent (min {min_knee_angle:.1f}°, max {max_knee_angle:.1f}°)")
                # Trung bình < 120° VÀ min < 110° → sitting
                elif avg_knee_angle is not None and avg_knee_angle < 120 and min_knee_angle < 110:
                    posture = 'sitting'
                    confidence = 0.85
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (upright), bent legs (avg {avg_knee_angle:.1f}°, min {min_knee_angle:.1f}°)")
                # Trường hợp khác → có thể sitting nhưng không chắc chắn
                elif avg_knee_angle is not None and avg_knee_angle < 130:
                    posture = 'sitting'
                    confidence = 0.75
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (upright), moderately bent legs ({avg_knee_angle:.1f}°)")
                else:
                    # Chân không đủ gập → transitioning
                    posture = 'transitioning'
                    confidence = 0.65
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (intermediate), legs not bent enough for sitting (min {min_knee_angle:.1f}°, max {max_knee_angle:.1f}°)")
            elif avg_knee_angle is not None and avg_knee_angle < 120:
                # Chỉ có trung bình, nhưng < 120° → sitting
                posture = 'sitting'
                confidence = 0.80
                reasoning.append(f"Spine angle {spine_angle:.1f}° (upright), bent legs (avg {avg_knee_angle:.1f}°)")
            else:
                # Không đủ thông tin chân → transitioning
                posture = 'transitioning'
                confidence = 0.60
                reasoning.append(f"Spine angle {spine_angle:.1f}° (intermediate), insufficient knee information")
        
        # 5. Intermediate classification (spine 60-70° nhưng không nằm, không đứng, không ngồi)
        else:
            # Intermediate zone: 60-70° - cần thêm yếu tố
            if spine_angle >= 60 and spine_angle <= 70:
                if head_y is not None and thorax_y is not None and head_y < thorax_y:
                    # Có thể đang nằm nhưng camera ở góc nghiêng
                    if body_ratio is not None and body_ratio > 0.8:
                        posture = 'lying_on_back'
                        confidence = 0.75
                        reasoning.append(f"Spine angle {spine_angle:.1f}° (intermediate), but head higher + body ratio indicates lying on back")
                    else:
                        posture = 'transitioning'
                        confidence = 0.65
                        reasoning.append(f"Spine angle {spine_angle:.1f}° (intermediate), head higher than thorax")
                elif avg_knee_angle is not None and avg_knee_angle < 120 and min_knee_angle is not None and min_knee_angle < 110:
                    # Chân gập rõ → có thể sitting
                    posture = 'sitting'
                    confidence = 0.70
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (intermediate), bent legs ({avg_knee_angle:.1f}°) → sitting")
                else:
                    posture = 'transitioning'
                    confidence = 0.60
                    reasoning.append(f"Spine angle {spine_angle:.1f}° (intermediate between lying/standing)")
            else:
                # Other cases (very rare)
                posture = 'transitioning'
                confidence = 0.55
                reasoning.append(f"Spine angle {spine_angle:.1f}° (unclear)")

        # Bổ sung thông tin chi tiết vào reasoning
        if head_thorax_delta is not None:
            if head_thorax_delta > 0:
                reasoning.append(f"Head higher than torso by {head_thorax_delta:.1f} mm")
            elif head_thorax_delta < 0:
                reasoning.append(f"Head lower than torso by {abs(head_thorax_delta):.1f} mm")
        if avg_knee_angle is not None:
            knee_details = []
            if angles.get('knee_left') is not None:
                knee_details.append(f"left {angles['knee_left']:.1f}°")
            if angles.get('knee_right') is not None:
                knee_details.append(f"right {angles['knee_right']:.1f}°")
            if knee_details:
                reasoning.append("Knee angles: " + ", ".join(knee_details))
        if angles.get('neck_angle') is not None:
            reasoning.append(f"Neck angle: {angles['neck_angle']:.1f}°")

        feature_context = {
            'spine_angle': spine_angle,
            'avg_knee_angle': avg_knee_angle,
            'min_knee_angle': min_knee_angle,
            'max_knee_angle': max_knee_angle,
            'thorax_y': thorax_y,
            'head_thorax_delta': head_thorax_delta,
            'body_ratio': body_ratio,
            'neck_angle': angles.get('neck_angle'),
            'confidence': confidence,
            'pelvis_y': pelvis_y,
            'head_y': head_y,
            'force_safe_posture': force_safe_posture,
            'head_height_above_pelvis': head_height_above_pelvis
        }

        return {
            'posture': posture,
            'confidence': confidence,
            'angles': angles,
            'reasoning': ' | '.join(reasoning),
            'feature_context': feature_context
        }
    def detect_danger(self, keypoints, posture_result):
        """
        Phát hiện tư thế nguy hiểm
        
        Args:
            keypoints: numpy array shape (16, 3) - keypoints 3D
            posture_result: dict - kết quả từ detect_posture()
        
        Returns:
            dict: {
                'danger_level': str,  # 'NONE', 'LOW', 'MEDIUM', 'HIGH'
                'danger_message': str,
                'recommendation': str,
                'warnings': list
            }
        """
        warnings = []
        severity_rank = {'LOW': 1, 'MEDIUM': 2, 'HIGH': 3}
        danger_level = 'NONE'
        danger_message = "✅ Safe: posture within expected range"
        recommendation = ""
        
        posture = posture_result.get('posture', 'unknown')
        angles = posture_result.get('angles', {})
        feature_context = posture_result.get('feature_context', {})
        if feature_context.get('force_safe_posture'):
            return {
                'danger_level': 'NONE',
                'danger_message': "✅ Safe: posture within expected range",
                'recommendation': "",
                'warnings': []
            }
        head_thorax_delta = feature_context.get('head_thorax_delta')
        head_y = feature_context.get('head_y')
        neck_angle = angles.get('neck_angle')
        confidence = feature_context.get('confidence', posture_result.get('confidence', 0))
        avg_knee_angle = feature_context.get('avg_knee_angle')
        min_knee_angle = feature_context.get('min_knee_angle')
        spine_angle = feature_context.get('spine_angle')
        head_back_margin = self.POSITION_THRESHOLDS.get('head_back_margin', 80)
        head_ambiguous_margin = self.POSITION_THRESHOLDS.get('head_ambiguous_margin', 30)
        head_below_margin = self.POSITION_THRESHOLDS.get('head_below_thorax', 50)
        
        def add_warning(warning):
            warnings.append(warning)
        
        # 1. Check PRONE / SIDS risk using strict combined conditions
        knees = [angles.get('knee_left'), angles.get('knee_right')]
        knees_valid = all(k is not None for k in knees)
        knees_straight = knees_valid and all(
            k > self.ANGLE_THRESHOLDS['prone_knee_straight'] for k in knees
        )
        is_spine_flat = (
            spine_angle is not None and spine_angle < self.ANGLE_THRESHOLDS['prone_spine_angle']
        )
        head_below_thorax = (
            head_thorax_delta is not None
            and head_thorax_delta < -head_below_margin
        )
        pelvis_y = feature_context.get('pelvis_y')
        head_below_pelvis = (
            head_y is not None
            and pelvis_y is not None
            and (pelvis_y - head_y) > head_below_margin
        )

        if is_spine_flat and knees_straight and (head_below_thorax or head_below_pelvis):
            reason_parts = [
                f"spine angle {spine_angle:.1f}°",
                f"knee angles {knees[0]:.1f}° / {knees[1]:.1f}°",
                "head below torso" if head_below_thorax else "head below pelvis"
            ]
            add_warning({
                'type': 'SIDS_RISK',
                'severity': 'HIGH',
                'message': "🚨 DANGER: Prone indicators detected – " + " | ".join(reason_parts),
                'recommendation': "Roll infant onto back immediately and monitor breathing"
            })
        
        # 2. Check SUFFOCATION risk (very small neck angle)
        if neck_angle is not None and neck_angle < self.ANGLE_THRESHOLDS['neck_danger']:
            suffocation_severity = 'HIGH' if posture in ['lying_on_stomach', 'lying_on_back'] else 'MEDIUM'
            prefix = "🚨 DANGER" if suffocation_severity == 'HIGH' else "⚠️ WARNING"
            add_warning({
                'type': 'SUFFOCATION_RISK',
                'severity': suffocation_severity,
                'message': f"{prefix}: Neck angle {neck_angle:.1f}° is too small – possible airway obstruction",
                'recommendation': "Adjust infant's head/neck to maintain open airway"
            })
        
        # 3. Check ABNORMAL POSTURE
        abnormal_joints = []

        def append_abnormal(message, severity='MEDIUM'):
            abnormal_joints.append((severity, message))

        for angle_name, angle_value in angles.items():
            if angle_value is None or 'neck' in angle_name:
                continue

            lower_bound = 30
            upper_bound = 180

            if 'knee' in angle_name or 'elbow' in angle_name:
                lower_bound = 12 if posture in ['sitting', 'lying_on_back', 'lying_on_stomach'] else 20
                upper_bound = 170
            elif 'shoulder' in angle_name:
                lower_bound = self.ANGLE_THRESHOLDS['shoulder_relaxed_lower']
                comfortable_upper = self.ANGLE_THRESHOLDS['shoulder_relaxed_upper']
                alert_upper = self.ANGLE_THRESHOLDS['shoulder_alert_upper']

            if 'shoulder' in angle_name:
                if posture in ['lying_on_back', 'lying_on_stomach'] and confidence >= 0.6:
                    if angle_value <= comfortable_upper:
                        continue
                    severity = 'LOW' if angle_value <= alert_upper else 'MEDIUM'
                    append_abnormal(
                        f"{angle_name} {angle_value:.1f}° (comfort limit {comfortable_upper}°)",
                        severity
                    )
                    continue
                upper_bound = comfortable_upper

            if angle_value < lower_bound:
                append_abnormal(
                    f"{angle_name} {angle_value:.1f}° (lower limit {lower_bound}°)", 'MEDIUM'
                )
            elif angle_value > upper_bound:
                append_abnormal(
                    f"{angle_name} {angle_value:.1f}° (upper limit {upper_bound}°)", 'MEDIUM'
                )
        
        if abnormal_joints:
            highest = max(abnormal_joints, key=lambda x: severity_rank.get(x[0], 2))[0]
            messages = ", ".join(msg for _, msg in abnormal_joints)
            add_warning({
                'type': 'ABNORMAL_POSTURE',
                'severity': highest,
                'message': f"⚠️ WARNING: Abnormal joint angles – {messages}",
                'recommendation': "Check infant's posture and ensure limbs are in natural positions"
            })
        
        # 4. Check LYING ON BACK but with issues
        if posture == 'lying_on_back' and neck_angle is not None and neck_angle < 60:
            add_warning({
                'type': 'HEAD_POSITION',
                'severity': 'LOW',
                'message': f"⚠️ Monitor: Neck angle {neck_angle:.1f}° while lying on back – head slightly bent",
                'recommendation': "Support the head and keep airway unobstructed"
            })
        
        # 5. Low confidence / transition warnings
        if (posture in ['transitioning', 'unknown']) or confidence < 0.65:
            add_warning({
                'type': 'LOW_CONFIDENCE',
                'severity': 'LOW',
                'message': f"ℹ️ Posture confidence is low ({confidence*100:.1f}%). Review input image for occlusions.",
                'recommendation': ""
            })
        
        # Determine final message based on highest severity
        if warnings:
            warnings.sort(key=lambda w: severity_rank.get(w['severity'], 0), reverse=True)
            top = warnings[0]
            danger_level = top['severity']
            danger_message = top['message']
            recommendation = top.get('recommendation', "")
        else:
            danger_level = 'NONE'
            danger_message = "✅ Safe: posture within expected range"
            recommendation = ""
        
        return {
            'danger_level': danger_level,
            'danger_message': danger_message,
            'recommendation': recommendation,
            'warnings': warnings
        }
    
    def analyze_pose(self, keypoints):
        """
        Phân tích tư thế hoàn chỉnh (wrapper function)
        
        Args:
            keypoints: numpy array shape (16, 3) - keypoints 3D
        
        Returns:
            dict: {
                'posture': str,
                'confidence': float,
                'danger_level': str,
                'danger_message': str,
                'recommendation': str,
                'angles': dict,
                'reasoning': str,
                'warnings': list
            }
        """
        # Nhận diện tư thế
        posture_result = self.detect_posture(keypoints)
        
        # Phát hiện nguy hiểm
        danger_result = self.detect_danger(keypoints, posture_result)
        
        # Kết hợp kết quả
        result = {
            'posture': posture_result['posture'],
            'confidence': posture_result['confidence'],
            'angles': posture_result['angles'],
            'reasoning': posture_result['reasoning'],
            'danger_level': danger_result['danger_level'],
            'danger_message': danger_result['danger_message'],
            'recommendation': danger_result['recommendation'],
            'warnings': danger_result['warnings'],
            'feature_context': posture_result.get('feature_context', {})
        }
        
        return result



