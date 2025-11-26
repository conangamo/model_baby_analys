"""
Script test đơn giản để kiểm tra inference có hoạt động không
"""

import os
import sys

# Thêm đường dẫn project vào sys.path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)

def test_imports():
    """Kiểm tra các imports cần thiết"""
    print("=" * 70)
    print("KIỂM TRA IMPORTS")
    print("=" * 70)
    
    try:
        import torch
        print(f"✅ torch: {torch.__version__}")
    except ImportError as e:
        print(f"❌ torch: {e}")
        return False
    
    try:
        import torchvision
        print(f"✅ torchvision: {torch.__version__}")
    except ImportError as e:
        print(f"❌ torchvision: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ numpy: {np.__version__}")
    except ImportError as e:
        print(f"❌ numpy: {e}")
        return False
    
    try:
        import cv2
        print(f"✅ cv2: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ cv2: {e}")
        return False
    
    try:
        import matplotlib
        print(f"✅ matplotlib: {matplotlib.__version__}")
    except ImportError as e:
        print(f"❌ matplotlib: {e}")
        return False
    
    try:
        from PIL import Image
        print(f"✅ PIL (Pillow)")
    except ImportError as e:
        print(f"❌ PIL: {e}")
        return False
    
    print()
    return True


def test_models():
    """Kiểm tra các model có tồn tại không"""
    print("=" * 70)
    print("KIỂM TRA SAVEDMODELS")
    print("=" * 70)
    
    model_dir = os.path.join(BASE_PATH, "SavedModels", "SavedModels")
    
    if not os.path.exists(model_dir):
        print(f"❌ Không tìm thấy thư mục: {model_dir}")
        print("💡 Đảm bảo đã download và giải nén SavedModels từ OneDrive")
        return False
    
    print(f"✅ Thư mục SavedModels tồn tại: {model_dir}")
    print()
    
    # Kiểm tra các model cần thiết
    models_to_check = [
        ("MINI_RGBD_2D", "model.tar"),
        ("MINI_RGBD_FineTune", "model.tar"),
    ]
    
    all_exist = True
    for model_name, model_file in models_to_check:
        model_path = os.path.join(model_dir, model_name, model_file)
        if os.path.exists(model_path):
            size = os.path.getsize(model_path) / (1024 * 1024)  # MB
            print(f"✅ {model_name}/{model_file} ({size:.2f} MB)")
        else:
            print(f"❌ {model_name}/{model_file} - KHÔNG TÌM THẤY")
            all_exist = False
    
    print()
    return all_exist


def test_model_loading():
    """Kiểm tra có thể load model không"""
    print("=" * 70)
    print("KIỂM TRA LOAD MODEL")
    print("=" * 70)
    
    try:
        import torch
        from PoseEstimation.ModelArchs import ModelGenerator
        
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"Device: {device}")
        
        # Tạo model trực tiếp mà không cần dataset loader
        # (Vì chúng ta chỉ cần model để inference, không cần dataset)
        print("Đang tạo models...")
        pose2d_model = ModelGenerator.load2DPoseEstimationModel(device)
        lifting_model = ModelGenerator.get3DLiftingNetwork(device)
        print("✅ Models đã được tạo")
        
        # Load weights
        model_dir = os.path.join(BASE_PATH, "SavedModels", "SavedModels")
        pose2d_path = os.path.join(model_dir, "MINI_RGBD_2D", "model.tar")
        lifting_path = os.path.join(model_dir, "MINI_RGBD_FineTune", "model.tar")
        
        if os.path.exists(pose2d_path):
            print("Đang load 2D pose model...")
            checkpoint = torch.load(pose2d_path, map_location=device)
            pose2d_model.load_state_dict(checkpoint["model_state_dict"])
            pose2d_model.eval()
            print("✅ 2D Pose Model đã được load")
        else:
            print(f"❌ Không tìm thấy: {pose2d_path}")
            return False
        
        if os.path.exists(lifting_path):
            print("Đang load 3D lifting model...")
            checkpoint = torch.load(lifting_path, map_location=device)
            lifting_model.load_state_dict(checkpoint["model_state_dict"])
            lifting_model.eval()
            print("✅ 3D Lifting Model đã được load")
        else:
            print(f"❌ Không tìm thấy: {lifting_path}")
            return False
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        print()
        return False


def main():
    print("\n" + "=" * 70)
    print("SCRIPT TEST INFERENCE")
    print("=" * 70)
    print()
    
    # Test 1: Imports
    if not test_imports():
        print("❌ Một số imports bị thiếu. Hãy cài đặt: pip install -r requirements.txt")
        return
    
    # Test 2: Models
    if not test_models():
        print("❌ Một số models bị thiếu. Hãy download SavedModels từ OneDrive")
        return
    
    # Test 3: Load models
    if not test_model_loading():
        print("❌ Không thể load models. Kiểm tra lại SavedModels")
        return
    
    # Tổng kết
    print("=" * 70)
    print("✅ TẤT CẢ KIỂM TRA ĐÃ PASS!")
    print("=" * 70)
    print()
    print("Bạn có thể chạy inference bằng lệnh:")
    print("  python inference_simple.py --image path/to/your/image.jpg")
    print()


if __name__ == "__main__":
    main()

