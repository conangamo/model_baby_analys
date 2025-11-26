"""
Script chạy inference và lưu tọa độ keypoints ra file
Output bao gồm:
- Ảnh visualization (như inference_simple.py)
- File JSON chứa tọa độ 2D và 3D của các keypoints
- File CSV chứa tọa độ (tùy chọn)

Cách sử dụng:
    python inference_with_keypoints.py --image path/to/image.jpg
    python inference_with_keypoints.py --image path/to/image.jpg --save-csv
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
import json

# Thêm đường dẫn project vào sys.path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)

from PoseEstimation.ModelArchs import ModelGenerator
from PoseEstimation.Core import Inference
from PoseEstimation.PoseAnalyzer import PoseAnalyzer
import DataSets.Utils.Config as cfg
import DataSets.Utils.Transforms as transform_utils
import DataSets.Utils.Visualisation as vis

# Image size mặc định
IMAGE_SIZE = 256


def preprocess_image(image_path, center=None, scale=None):
    """
    Pre-process ảnh để đưa vào model
    """
    # Load ảnh
    image = Image.open(image_path).convert('RGB')
    original_image = np.array(image)
    
    # Tính center và scale nếu không được cung cấp
    if center is None:
        h, w = original_image.shape[:2]
        center = np.array([w / 2, h / 2])
    
    if scale is None:
        h, w = original_image.shape[:2]
        scale = max(h, w) / 200.0
    
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


def plot_clean_2d_skeleton(ax, joints2D, connected_joints):
    """
    Plot 2D skeleton với màu sắc gọn gàng, rõ ràng hơn
    Sử dụng màu theo nhóm: tay (blue), chân (green), cột sống (red)
    """
    # Định nghĩa màu theo nhóm cơ thể
    # MPII joints: 0-5 (legs), 6-9 (spine/head), 10-15 (arms)
    # Màu sắc:
    # - Cột sống/đầu: #FF4444 (đỏ nhạt)
    # - Chân: #44FF44 (xanh lá nhạt)  
    # - Tay: #4444FF (xanh dương nhạt)
    
    # Xác định màu cho mỗi connection dựa trên joints
    spine_connections = [6, 7, 8, 9]  # pelvis, thorax, neck, head indices
    leg_connections = [0, 1, 2, 3, 4, 5]  # legs indices
    arm_connections = [10, 11, 12, 13, 14, 15]  # arms indices
    
    for i in range(len(connected_joints)):
        joint1 = connected_joints[i, 0]
        joint2 = connected_joints[i, 1]
        
        # Xác định màu dựa trên loại connection
        if joint1 in spine_connections or joint2 in spine_connections:
            color = '#FF6B6B'  # Đỏ nhạt cho cột sống/đầu
            linewidth = 2.5
        elif joint1 in leg_connections or joint2 in leg_connections:
            color = '#4ECDC4'  # Xanh ngọc cho chân
            linewidth = 2.0
        elif joint1 in arm_connections or joint2 in arm_connections:
            color = '#45B7D1'  # Xanh dương cho tay
            linewidth = 2.0
        else:
            color = '#95A5A6'  # Xám cho các connection khác
            linewidth = 1.5
        
        # Vẽ đường kết nối
        x = [joints2D[joint1, 0], joints2D[joint2, 0]]
        y = [joints2D[joint1, 1], joints2D[joint2, 1]]
        ax.plot(x, y, lw=linewidth, c=color, alpha=0.8, zorder=1)
    
    # Vẽ joints với kích thước và màu hợp lý
    # Phân loại joints theo nhóm
    for i in range(len(joints2D)):
        if i in spine_connections:
            color = '#FF4444'  # Đỏ cho cột sống/đầu
            size = 60
        elif i in leg_connections:
            color = '#2ECC71'  # Xanh lá cho chân
            size = 50
        elif i in arm_connections:
            color = '#3498DB'  # Xanh dương cho tay
            size = 50
        else:
            color = '#34495E'  # Xám đậm cho khác
            size = 40
        
        ax.scatter(joints2D[i, 0], joints2D[i, 1], 
                  c=color, s=size, zorder=2, 
                  edgecolors='white', linewidths=1.5, alpha=0.9)


def save_keypoints_json(keypoints_2d, keypoints_3d, joint_names, output_path, pose_analysis=None):
    """
    Lưu keypoints ra file JSON
    
    Args:
        keypoints_2d: numpy array shape (num_joints, 2)
        keypoints_3d: numpy array shape (num_joints, 3)
        joint_names: list of joint names
        output_path: path to save JSON file
        pose_analysis: dict containing pose analysis results (optional)
    """
    data = {
        "keypoints_2d": {
            "format": "pixel_coordinates",
            "description": "2D keypoints in image pixel coordinates (x, y)",
            "joints": {}
        },
        "keypoints_3d": {
            "format": "millimeters",
            "description": "3D keypoints in millimeters (x, y, z)",
            "joints": {}
        }
    }
    
    for i, joint_name in enumerate(joint_names):
        data["keypoints_2d"]["joints"][joint_name] = {
            "x": float(keypoints_2d[i, 0]),
            "y": float(keypoints_2d[i, 1])
        }
        data["keypoints_3d"]["joints"][joint_name] = {
            "x": float(keypoints_3d[i, 0]),
            "y": float(keypoints_3d[i, 1]),
            "z": float(keypoints_3d[i, 2])
        }
    
    # Thêm phân tích tư thế nếu có
    if pose_analysis is not None:
        data["pose_analysis"] = {
            "posture": pose_analysis.get("posture", "unknown"),
            "confidence": float(pose_analysis.get("confidence", 0.0)),
            "danger_level": pose_analysis.get("danger_level", "NONE"),
            "danger_message": pose_analysis.get("danger_message", ""),
            "recommendation": pose_analysis.get("recommendation", ""),
            "reasoning": pose_analysis.get("reasoning", ""),
            "angles": {
                k: float(v) if v is not None else None 
                for k, v in pose_analysis.get("angles", {}).items()
            },
            "warnings": pose_analysis.get("warnings", [])
        }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Keypoints saved to: {output_path}")


def save_keypoints_csv(keypoints_2d, keypoints_3d, joint_names, output_path):
    """
    Lưu keypoints ra file CSV
    """
    import csv
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Header
        writer.writerow(['Joint Name', '2D_X', '2D_Y', '3D_X', '3D_Y', '3D_Z'])
        
        # Data
        for i, joint_name in enumerate(joint_names):
            writer.writerow([
                joint_name,
                f"{keypoints_2d[i, 0]:.2f}",
                f"{keypoints_2d[i, 1]:.2f}",
                f"{keypoints_3d[i, 0]:.2f}",
                f"{keypoints_3d[i, 1]:.2f}",
                f"{keypoints_3d[i, 2]:.2f}"
            ])
    
    print(f"   ✅ Keypoints CSV saved to: {output_path}")


def run_inference(image_path, output_path=None, use_bbox_model=False, save_csv=False):
    """
    Chạy inference và lưu keypoints
    """
    print("=" * 70)
    print("RUNNING INFERENCE AND SAVING KEYPOINTS")
    print("=" * 70)
    print(f"Input image: {image_path}")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found {image_path}")
        return
    
    # Setup device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    
    # Load models
    print("\n1. Loading models...")
    
    try:
        pose2D_model = ModelGenerator.load2DPoseEstimationModel(device)
        lifting_model = ModelGenerator.get3DLiftingNetwork(device)
        print("   ✅ Models created")
    except Exception as e:
        print(f"   ❌ Error creating models: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Load pretrained weights
    print("\n2. Loading pretrained weights...")
    model_dir = os.path.join(BASE_PATH, "SavedModels", "SavedModels")
    
    pose2d_path = os.path.join(model_dir, "MINI_RGBD_2D", "model.tar")
    lifting_path = os.path.join(model_dir, "MINI_RGBD_FineTune", "model.tar")
    
    if not os.path.exists(pose2d_path) or not os.path.exists(lifting_path):
        print(f"   ❌ Model files not found")
        print(f"   💡 Make sure to download SavedModels from OneDrive")
        return
    
    try:
        checkpoint = torch.load(pose2d_path, map_location=device)
        pose2D_model.load_state_dict(checkpoint["model_state_dict"])
        pose2D_model.eval()
        
        checkpoint = torch.load(lifting_path, map_location=device)
        lifting_model.load_state_dict(checkpoint["model_state_dict"])
        lifting_model.eval()
        print("   ✅ Models loaded")
    except Exception as e:
        print(f"   ❌ Error loading models: {e}")
        return
    
    # Pre-process image
    print("\n3. Pre-processing image...")
    try:
        center = None
        scale = None
        processed_image, center, scale, original_image = preprocess_image(
            image_path, center, scale
        )
        print(f"   ✅ Image pre-processed")
    except Exception as e:
        print(f"   ❌ Error pre-processing image: {e}")
        return
    
    # Run inference
    print("\n4. Running inference...")
    try:
        input_tensor = processed_image.unsqueeze(0).to(device)
        
        # Inference 2D pose
        with torch.no_grad():
            pose2d_output = pose2D_model(input_tensor)
            pose2d_preds = pose2d_output.detach().cpu().numpy()
        
        # Post-process 2D predictions
        center_array = np.array([[center[1], center[0]]])
        scale_array = np.array([scale])
        pred_coords_2d = Inference.postProcessPredictions(
            pose2d_preds, center_array, scale_array, 64
        )
        print("   ✅ 2D pose predicted")
        
        # Inference 3D lifting
        num_joints = cfg.MPII["numJoints"]
        pose2d_flat = torch.tensor(pred_coords_2d).view(-1, num_joints * 2).to(device)
        
        with torch.no_grad():
            pose3d_output = lifting_model(pose2d_flat)
            pose3d_preds = pose3d_output.detach().cpu().view(-1, num_joints, 3).numpy()
        
        print("   ✅ 3D pose predicted")
    except Exception as e:
        print(f"   ❌ Error during inference: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Pose analysis
    print("\n5. Analyzing pose...")
    pose_analysis = None
    try:
        analyzer = PoseAnalyzer(config=cfg.MPII)
        pose_analysis = analyzer.analyze_pose(pose3d_preds[0])
        
        # Print analysis results
        print(f"   📊 POSTURE: {pose_analysis['posture']}")
        print(f"   - Confidence: {pose_analysis['confidence']*100:.1f}%")
        print(f"   - Reasoning: {pose_analysis['reasoning']}")
        
        # Print warnings if any
        if pose_analysis['danger_level'] != 'NONE':
            print(f"   {pose_analysis['danger_message']}")
            if pose_analysis.get('recommendation'):
                print(f"   💡 {pose_analysis['recommendation']}")
        else:
            print(f"   ✅ {pose_analysis['danger_message']}")
        
        # Print important angles
        angles = pose_analysis.get('angles', {})
        if angles.get('spine_angle') is not None:
            print(f"   - Spine angle: {angles['spine_angle']:.1f}°")
        if angles.get('knee_left') is not None or angles.get('knee_right') is not None:
            knee_angles = [a for a in [angles.get('knee_left'), angles.get('knee_right')] if a is not None]
            if knee_angles:
                print(f"   - Knee angle (avg): {np.mean(knee_angles):.1f}°")
        
        print("   ✅ Pose analysis completed")
    except Exception as e:
        print(f"   ⚠️  Error during pose analysis: {e}")
        import traceback
        traceback.print_exc()
        # Tiếp tục mà không có phân tích tư thế
    
    # Save keypoints
    print("\n6. Saving keypoints...")
    try:
        # Create output directory
        output_dir = os.path.join(BASE_PATH, "Images", "InferenceOutput")
        os.makedirs(output_dir, exist_ok=True)
        
        # Base filename
        input_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # Get joint names
        joint_names = cfg.MPII["jointNames"]
        
        # Save JSON
        json_path = os.path.join(output_dir, f"{input_name}_keypoints.json")
        save_keypoints_json(
            pred_coords_2d[0], 
            pose3d_preds[0], 
            joint_names, 
            json_path,
            pose_analysis=pose_analysis
        )
        
        # Save CSV if requested
        if save_csv:
            csv_path = os.path.join(output_dir, f"{input_name}_keypoints.csv")
            save_keypoints_csv(
                pred_coords_2d[0], 
                pose3d_preds[0], 
                joint_names, 
                csv_path
            )
        
        # Print summary
        print("\n   📊 KEYPOINTS SUMMARY:")
        print(f"   - Number of joints: {num_joints}")
        print(f"   - 2D coordinates: (x, y) in pixels")
        print(f"   - 3D coordinates: (x, y, z) in millimeters")
        print(f"   - JSON file: {json_path}")
        if save_csv:
            print(f"   - CSV file: {csv_path}")
        
    except Exception as e:
        print(f"   ❌ Error saving keypoints: {e}")
        import traceback
        traceback.print_exc()
    
    # Visualize results
    print("\n7. Visualizing results...")
    try:
        fig = plt.figure(figsize=(18, 6))
        
        connected_joints = cfg.MPII["connectedJoints"]
        joint_colours = cfg.MPII["jointColours"]
        
        # Plot 1: Input image
        ax1 = plt.subplot(1, 3, 1)
        ax1.set_title("Input Image", fontsize=12, fontweight='bold')
        vis.plotImage(ax1, original_image)
        
        # Plot 2: 2D Pose với thông tin tư thế
        ax2 = plt.subplot(1, 3, 2)
        ax2.set_title("2D Pose Prediction", fontsize=12, fontweight='bold')
        vis.plotImage(ax2, original_image)
        
        # Custom clean visualization với màu sắc gọn gàng hơn
        plot_clean_2d_skeleton(
            ax2, pred_coords_2d[0], connected_joints
        )
        
        # Thêm thông tin tư thế vào ảnh 2D
        if pose_analysis is not None:
            # Display posture
            posture_text = f"Posture: {pose_analysis['posture']}"
            confidence_text = f"Confidence: {pose_analysis['confidence']*100:.1f}%"
            
            # Màu sắc dựa trên mức độ nguy hiểm
            danger_level = pose_analysis.get('danger_level', 'NONE')
            if danger_level == 'HIGH':
                text_color = 'red'
                bg_color = 'yellow'
                text_weight = 'bold'
            elif danger_level == 'MEDIUM':
                text_color = 'orange'
                bg_color = 'lightyellow'
                text_weight = 'bold'
            elif danger_level == 'LOW':
                text_color = 'darkorange'
                bg_color = 'wheat'
                text_weight = 'normal'
            else:
                text_color = 'green'
                bg_color = 'lightgreen'
                text_weight = 'normal'
            
            # Sử dụng tọa độ theo tỉ lệ để tránh chồng lấn
            line_y = 0.95
            line_spacing = 0.08
            
            # Hiển thị posture
            ax2.text(0.02, line_y, posture_text,
                    transform=ax2.transAxes,
                    fontsize=11, color=text_color, weight=text_weight,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor=bg_color, alpha=0.8))
            line_y -= line_spacing
            
            # Hiển thị confidence
            ax2.text(0.02, line_y, confidence_text,
                    transform=ax2.transAxes,
                    fontsize=10, color='blue',
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7))
            line_y -= line_spacing
            
            # Hiển thị reasoning (nếu có)
            reasoning_text = pose_analysis.get('reasoning', '')
            if reasoning_text:
                # Rút ngắn reasoning nếu quá dài, chia thành nhiều dòng
                if len(reasoning_text) > 60:
                    # Chia thành 2 dòng
                    words = reasoning_text.split()
                    mid = len(words) // 2
                    line1 = ' '.join(words[:mid])
                    line2 = ' '.join(words[mid:])
                    reasoning_text = f"{line1}\n{line2}"
                    line_spacing_reasoning = 0.06
                else:
                    line_spacing_reasoning = 0.05
                
                ax2.text(0.02, line_y, f"Reasoning: {reasoning_text}",
                        transform=ax2.transAxes,
                        fontsize=9, color='darkblue',
                        verticalalignment='top',
                        bbox=dict(boxstyle='round,pad=0.4', facecolor='lightblue', alpha=0.7))
                line_y -= line_spacing_reasoning * (2 if '\n' in reasoning_text else 1)
            
            # Hiển thị cảnh báo nếu có
            bottom_y = 0.10
            if danger_level != 'NONE':
                danger_message = pose_analysis.get('danger_message', '')
                # Rút ngắn message nếu quá dài
                if len(danger_message) > 50:
                    danger_message = danger_message[:47] + "..."
                
                ax2.text(0.02, bottom_y, danger_message,
                        transform=ax2.transAxes,
                        fontsize=12, color='red', weight='bold',
                        verticalalignment='bottom',
                        bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow',
                                edgecolor='red', linewidth=2, alpha=0.9))
                bottom_y += 0.08
                
                # Thêm recommendation nếu có
                if pose_analysis.get('recommendation'):
                    rec_text = pose_analysis['recommendation']
                    # Bỏ "Recommendation: " prefix nếu có
                    if rec_text.startswith("Recommendation: "):
                        rec_text = rec_text[len("Recommendation: "):]
                    if len(rec_text) > 60:
                        # Chia thành 2 dòng
                        words = rec_text.split()
                        mid = len(words) // 2
                        line1 = ' '.join(words[:mid])
                        line2 = ' '.join(words[mid:])
                        rec_text = f"{line1}\n{line2}"
                        bottom_y += 0.05
                    ax2.text(0.02, bottom_y, f"💡 {rec_text}",
                            transform=ax2.transAxes,
                            fontsize=10, color='darkblue',
                            verticalalignment='bottom',
                            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))
                    if '\n' in rec_text:
                        bottom_y += 0.06
            else:
                # Display safe message
                ax2.text(0.02, bottom_y, "✅ Safe",
                        transform=ax2.transAxes,
                        fontsize=11, color='green', weight='bold',
                        verticalalignment='bottom',
                        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.8))
        
        # Plot 3: 3D Pose
        ax3 = plt.subplot(1, 3, 3, projection='3d')
        ax3.set_title("3D Pose Prediction", fontsize=12, fontweight='bold')
        vis.plot3DJoints(ax3, pose3d_preds[0], connected_joints, joint_colours)
        
        # Thêm thông tin góc vào 3D plot nếu có
        if pose_analysis is not None:
            angles = pose_analysis.get('angles', {})
            info_lines = []
            if angles.get('spine_angle') is not None:
                info_lines.append(f"Spine: {angles['spine_angle']:.1f}°")
            if angles.get('knee_left') is not None:
                info_lines.append(f"Knee L: {angles['knee_left']:.1f}°")
            if angles.get('knee_right') is not None:
                info_lines.append(f"Knee R: {angles['knee_right']:.1f}°")
            
            if info_lines:
                info_text = "\n".join(info_lines)
                ax3.text2D(0.02, 0.98, info_text, 
                          transform=ax3.transAxes, fontsize=9,
                          verticalalignment='top',
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        plt.tight_layout()
        
        # Save image
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f"   ✅ Result image saved to: {output_path}")
        else:
            img_output_path = os.path.join(output_dir, f"{input_name}_result.png")
            plt.savefig(img_output_path, dpi=150, bbox_inches='tight')
            print(f"   ✅ Result image saved to: {img_output_path}")
        
        plt.close()
        
    except Exception as e:
        print(f"   ❌ Error visualizing: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("✅ COMPLETED!")
    print("=" * 70)
    print("\n📁 Files saved:")
    print(f"   - Visualization image: {output_dir}/{input_name}_result.png")
    print(f"   - Keypoints JSON: {output_dir}/{input_name}_keypoints.json")
    if save_csv:
        print(f"   - Keypoints CSV: {output_dir}/{input_name}_keypoints.csv")


def main():
    parser = argparse.ArgumentParser(description='Run inference and save keypoints')
    parser.add_argument('--image', type=str, required=True,
                        help='Path to input image')
    parser.add_argument('--output', type=str, default=None,
                        help='Path to save result image (optional)')
    parser.add_argument('--use-bbox', action='store_true',
                        help='Use bbox model to detect infant (optional)')
    parser.add_argument('--save-csv', action='store_true',
                        help='Save keypoints to CSV file (in addition to JSON)')
    
    args = parser.parse_args()
    
    run_inference(args.image, args.output, args.use_bbox, args.save_csv)


if __name__ == "__main__":
    main()

