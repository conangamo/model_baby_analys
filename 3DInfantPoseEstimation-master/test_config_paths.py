"""
Script kiểm tra đường dẫn trong Config.py
Chạy script này để kiểm tra xem các đường dẫn dataset có đúng không
"""

import os
import sys

# Thêm đường dẫn project vào sys.path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_PATH)

try:
    import DataSets.Utils.Config as cfg
    print("✅ Config.py đã được load thành công!\n")
except Exception as e:
    print(f"❌ Lỗi khi load Config.py: {e}")
    sys.exit(1)

def check_path(path, path_name):
    """Kiểm tra xem đường dẫn có tồn tại không"""
    if os.path.exists(path):
        print(f"✅ {path_name}:")
        print(f"   Đường dẫn: {path}")
        print(f"   Tồn tại: Có")
        return True
    else:
        print(f"❌ {path_name}:")
        print(f"   Đường dẫn: {path}")
        print(f"   Tồn tại: Không (cần kiểm tra lại)")
        return False

def main():
    print("=" * 70)
    print("KIỂM TRA ĐƯỜNG DẪN TRONG CONFIG.PY")
    print("=" * 70)
    print()
    
    results = []
    
    # Kiểm tra MPI_INF
    print("1. KIỂM TRA MPI-INF-3DHP DATASET:")
    print("-" * 70)
    if hasattr(cfg, 'MPI_INF') and 'basePath' in cfg.MPI_INF:
        exists = check_path(cfg.MPI_INF['basePath'], "basePath")
        results.append(("MPI_INF.basePath", exists))
    else:
        print("❌ Không tìm thấy MPI_INF.basePath trong config")
        results.append(("MPI_INF.basePath", False))
    print()
    
    # Kiểm tra MINI_RGBD
    print("2. KIỂM TRA MINI-RGBD DATASET:")
    print("-" * 70)
    if hasattr(cfg, 'MINI_RGBD') and 'basePath' in cfg.MINI_RGBD:
        exists = check_path(cfg.MINI_RGBD['basePath'], "basePath")
        results.append(("MINI_RGBD.basePath", exists))
    else:
        print("❌ Không tìm thấy MINI_RGBD.basePath trong config")
        results.append(("MINI_RGBD.basePath", False))
    print()
    
    # Kiểm tra MPII
    print("3. KIỂM TRA MPII DATASET:")
    print("-" * 70)
    if hasattr(cfg, 'MPII'):
        if 'annotationFileDirectory' in cfg.MPII:
            exists = check_path(cfg.MPII['annotationFileDirectory'], "annotationFileDirectory")
            results.append(("MPII.annotationFileDirectory", exists))
        else:
            print("❌ Không tìm thấy MPII.annotationFileDirectory trong config")
            results.append(("MPII.annotationFileDirectory", False))
        
        if 'imageDirectory' in cfg.MPII:
            exists = check_path(cfg.MPII['imageDirectory'], "imageDirectory")
            results.append(("MPII.imageDirectory", exists))
        else:
            print("❌ Không tìm thấy MPII.imageDirectory trong config")
            results.append(("MPII.imageDirectory", False))
    else:
        print("❌ Không tìm thấy MPII trong config")
    print()
    
    # Kiểm tra MAHVEA
    print("4. KIỂM TRA MAVHEA (MAHVEA) DATASET:")
    print("-" * 70)
    if hasattr(cfg, 'MAHVEA'):
        if 'labelsFname' in cfg.MAHVEA:
            exists = check_path(cfg.MAHVEA['labelsFname'], "labelsFname")
            results.append(("MAHVEA.labelsFname", exists))
        else:
            print("❌ Không tìm thấy MAHVEA.labelsFname trong config")
            results.append(("MAHVEA.labelsFname", False))
        
        if 'baseDirectory' in cfg.MAHVEA:
            exists = check_path(cfg.MAHVEA['baseDirectory'], "baseDirectory")
            results.append(("MAHVEA.baseDirectory", exists))
        else:
            print("❌ Không tìm thấy MAHVEA.baseDirectory trong config")
            results.append(("MAHVEA.baseDirectory", False))
        
        if 'videoDirectory' in cfg.MAHVEA:
            exists = check_path(cfg.MAHVEA['videoDirectory'], "videoDirectory")
            results.append(("MAHVEA.videoDirectory", exists))
        else:
            print("❌ Không tìm thấy MAHVEA.videoDirectory trong config")
            results.append(("MAHVEA.videoDirectory", False))
    else:
        print("❌ Không tìm thấy MAHVEA trong config")
    print()
    
    # Tóm tắt kết quả
    print("=" * 70)
    print("TÓM TẮT KẾT QUẢ:")
    print("=" * 70)
    total = len(results)
    passed = sum(1 for _, exists in results if exists)
    failed = total - passed
    
    for path_name, exists in results:
        status = "✅" if exists else "❌"
        print(f"{status} {path_name}")
    
    print()
    print(f"Tổng số đường dẫn kiểm tra: {total}")
    print(f"✅ Tồn tại: {passed}")
    print(f"❌ Không tồn tại: {failed}")
    print()
    
    if failed > 0:
        print("⚠️  LƯU Ý:")
        print("   - Một số đường dẫn không tồn tại.")
        print("   - Nếu bạn chưa download dataset, điều này là bình thường.")
        print("   - Nếu bạn đã download, hãy kiểm tra lại đường dẫn trong Config.py")
        print("   - Xem file HUONG_DAN_SUA_DUONG_DAN.md để biết cách sửa đường dẫn")
        print()
        return 1
    else:
        print("✅ Tất cả đường dẫn đều tồn tại!")
        print()
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

