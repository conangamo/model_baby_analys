"""
Script đơn giản để chạy inference trên ảnh/video mới
Sử dụng model đã train sẵn từ SavedModels

Cách sử dụng:
    python inference_simple.py --image path/to/image.jpg
    python inference_simple.py --image path/to/image.jpg --output output.png
"""

import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import os
import sys
import argparse
import matplotlib.pyplot as plt

# Thêm đường dẫn project vào sys.path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)

from PoseEstimation.ModelArchs import ModelGenerator
from PoseEstimation.Core import Inference
import DataSets.Utils.Config as cfg
import DataSets.Utils.Transforms as transform_utils
import DataSets.Utils.Visualisation as vis

# Image size mặc định
IMAGE_SIZE = 256


def preprocess_image(image_path, center=None, scale=None):
    """
    Pre-process ảnh để đưa vào model
    
    Args:
        image_path: Đường dẫn đến ảnh
        center: Tọa độ center (nếu None, sẽ dùng center của ảnh)
        scale: Scale factor (nếu None, sẽ tính từ ảnh)
    
    Returns:
        processed_image: Ảnh đã pre-process (tensor)
        center: Tọa độ center đã dùng
        scale: Scale factor đã dùng
        original_image: Ảnh gốc (numpy array)
    """
    # Load ảnh
    image = Image.open(image_path).convert('RGB')
    original_image = np.array(image)
    
    # Tính center và scale nếu không được cung cấp
    if center is None:
        # Center của ảnh
        h, w = original_image.shape[:2]
        center = np.array([w / 2, h / 2])
    
    if scale is None:
        # Scale dựa trên kích thước ảnh
        h, w = original_image.shape[:2]
        scale = max(h, w) / 200.0  # scale in relation to 200px
    
    # Transform ảnh
    rotation = 0
    trans = transform_utils.get_affine_transform(
        center, scale, rotation, IMAGE_SIZE
    )
    
    # Warp ảnh
    processed_image = cv2.warpAffine(
        original_image, trans, (IMAGE_SIZE, IMAGE_SIZE), flags=cv2.INTER_LINEAR
    )
    
    # Convert to tensor
    processed_image = transforms.ToTensor()(processed_image)
    
    return processed_image, center, scale, original_image


def run_inference(image_path, output_path=None, use_bbox_model=False):
    """
    Chạy inference trên ảnh
    
    Args:
        image_path: Đường dẫn đến ảnh
        output_path: Đường dẫn để lưu kết quả (nếu None, sẽ hiển thị)
        use_bbox_model: Có dùng bbox model để detect infant không (tùy chọn)
    """
    print("=" * 70)
    print("CHẠY INFERENCE TRÊN ẢNH")
    print("=" * 70)
    print(f"Ảnh input: {image_path}")
    
    # Kiểm tra file tồn tại
    if not os.path.exists(image_path):
        print(f"❌ Lỗi: Không tìm thấy file {image_path}")
        return
    
    # Setup device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    
    # Load models
    print("\n1. Đang load models...")
    
    try:
        # Tạo model trực tiếp mà không cần dataset loader
        # (Vì chúng ta chỉ cần model để inference, không cần dataset)
        pose2D_model = ModelGenerator.load2DPoseEstimationModel(device)
        lifting_model = ModelGenerator.get3DLiftingNetwork(device)
        print("   ✅ Models đã được tạo")
    except Exception as e:
        print(f"   ❌ Lỗi khi tạo models: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Load pretrained weights
    print("\n2. Đang load pretrained weights...")
    model_dir = os.path.join(BASE_PATH, "SavedModels", "SavedModels")
    
    # Đường dẫn đến các model
    pose2d_path = os.path.join(model_dir, "MINI_RGBD_2D", "model.tar")
    lifting_path = os.path.join(model_dir, "MINI_RGBD_FineTune", "model.tar")
    
    # Kiểm tra file model tồn tại
    if not os.path.exists(pose2d_path):
        print(f"   ❌ Không tìm thấy model: {pose2d_path}")
        print(f"   💡 Đảm bảo đã download SavedModels từ OneDrive")
        print(f"   💡 Link: https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7")
        return
    
    if not os.path.exists(lifting_path):
        print(f"   ❌ Không tìm thấy model: {lifting_path}")
        print(f"   💡 Đảm bảo đã download SavedModels từ OneDrive")
        print(f"   💡 Link: https://liveuclac-my.sharepoint.com/:u:/g/personal/rmhisje_ucl_ac_uk/EcQr9vyPlSBPmdJSazAIDP0BJ7ydxgrjSmYpeoho1v5efQ?e=4MTIH7")
        return
    
    try:
        # Load 2D pose model
        checkpoint = torch.load(pose2d_path, map_location=device)
        pose2D_model.load_state_dict(checkpoint["model_state_dict"])
        pose2D_model.eval()
        print("   ✅ 2D Pose Model đã được load")
        
        # Load 3D lifting model
        checkpoint = torch.load(lifting_path, map_location=device)
        lifting_model.load_state_dict(checkpoint["model_state_dict"])
        lifting_model.eval()
        print("   ✅ 3D Lifting Model đã được load")
    except Exception as e:
        print(f"   ❌ Lỗi khi load models: {e}")
        return
    
    # Optional: Load bbox model nếu cần
    bbox_model = None
    if use_bbox_model:
        print("\n3. Đang load bbox model...")
        try:
            from FasterRCNN.BoundingBoxModel import BoundingBoxModel
            bbox_path = os.path.join(model_dir, "MINI_RGBD_Bbox", "model.tar")
            if os.path.exists(bbox_path):
                bbox_model = BoundingBoxModel(device, bbox_path)
                print("   ✅ Bbox Model đã được load")
            else:
                print("   ⚠️  Không tìm thấy bbox model, sẽ dùng center/scale từ ảnh")
        except Exception as e:
            print(f"   ⚠️  Lỗi khi load bbox model: {e}")
            print("   ⚠️  Sẽ dùng center/scale từ ảnh")
    
    # Pre-process ảnh
    print("\n4. Đang pre-process ảnh...")
    try:
        # Nếu có bbox model, dùng nó để detect infant
        if bbox_model is not None:
            image_pil = Image.open(image_path).convert('RGB')
            scale, center = bbox_model.getCentreAndScale(image_pil)
            print(f"   ✅ Đã detect infant với bbox model")
        else:
            center = None
            scale = None
            print(f"   ✅ Đang pre-process ảnh (dùng center/scale từ ảnh)")
        
        processed_image, center, scale, original_image = preprocess_image(
            image_path, center, scale
        )
        print(f"   ✅ Ảnh đã được pre-process")
        print(f"   Center: {center}, Scale: {scale:.2f}")
    except Exception as e:
        print(f"   ❌ Lỗi khi pre-process ảnh: {e}")
        return
    
    # Chạy inference
    print("\n5. Đang chạy inference...")
    try:
        # Chuẩn bị input
        input_tensor = processed_image.unsqueeze(0).to(device)
        
        # Inference 2D pose
        with torch.no_grad():
            pose2d_output = pose2D_model(input_tensor)
            pose2d_preds = pose2d_output.detach().cpu().numpy()
        
        # Post-process 2D predictions
        center_array = np.array([[center[1], center[0]]])  # [x, y] format
        scale_array = np.array([scale])
        pred_coords_2d = Inference.postProcessPredictions(
            pose2d_preds, center_array, scale_array, 64
        )
        print("   ✅ 2D pose đã được dự đoán")
        
        # Inference 3D lifting
        num_joints = cfg.MPII["numJoints"]
        pose2d_flat = torch.tensor(pred_coords_2d).view(-1, num_joints * 2).to(device)
        
        with torch.no_grad():
            pose3d_output = lifting_model(pose2d_flat)
            pose3d_preds = pose3d_output.detach().cpu().view(-1, num_joints, 3).numpy()
        
        print("   ✅ 3D pose đã được dự đoán")
    except Exception as e:
        print(f"   ❌ Lỗi khi chạy inference: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Visualize kết quả
    print("\n6. Đang visualize kết quả...")
    try:
        fig = plt.figure(figsize=(15, 5))
        
        # Config
        connected_joints = cfg.MPII["connectedJoints"]
        joint_colours = cfg.MPII["jointColours"]
        
        # Plot 1: Input image
        ax1 = plt.subplot(1, 3, 1)
        ax1.set_title("Input Image", fontsize=12)
        vis.plotImage(ax1, original_image)
        
        # Plot 2: 2D Pose
        ax2 = plt.subplot(1, 3, 2)
        ax2.set_title("2D Pose Prediction", fontsize=12)
        vis.plotImage(ax2, original_image)
        vis.plot2DJoints(
            ax2, pred_coords_2d[0], connected_joints, joint_colours, None
        )
        
        # Plot 3: 3D Pose
        ax3 = plt.subplot(1, 3, 3, projection='3d')
        ax3.set_title("3D Pose Prediction", fontsize=12)
        vis.plot3DJoints(ax3, pose3d_preds[0], connected_joints, joint_colours)
        
        plt.tight_layout()
        
        # Lưu hoặc hiển thị
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"   ✅ Kết quả đã được lưu vào: {output_path}")
        else:
            # Tạo thư mục output nếu chưa có
            output_dir = os.path.join(BASE_PATH, "Images", "InferenceOutput")
            os.makedirs(output_dir, exist_ok=True)
            
            # Tên file output
            input_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_dir, f"{input_name}_result.png")
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"   ✅ Kết quả đã được lưu vào: {output_path}")
        
        plt.close()
        
    except Exception as e:
        print(f"   ❌ Lỗi khi visualize: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n" + "=" * 70)
    print("✅ HOÀN THÀNH!")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description='Chạy inference trên ảnh/video')
    parser.add_argument('--image', type=str, required=True,
                        help='Đường dẫn đến ảnh input')
    parser.add_argument('--output', type=str, default=None,
                        help='Đường dẫn để lưu kết quả (tùy chọn)')
    parser.add_argument('--use-bbox', action='store_true',
                        help='Sử dụng bbox model để detect infant (tùy chọn)')
    
    args = parser.parse_args()
    
    run_inference(args.image, args.output, args.use_bbox)


if __name__ == "__main__":
    main()

