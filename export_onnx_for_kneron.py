"""
導出 YOLOv8 模型為 ONNX 格式（專為 Kneron 優化）
根據 Kneron toolchain 的要求進行導出
"""

from ultralytics import YOLO
import os

def main():
    # 載入最佳模型
    model_path = "runs/detect/runs/ppe_yolov8n22/weights/best.pt"
    
    if not os.path.exists(model_path):
        print(f"錯誤：找不到模型檔案 {model_path}")
        return
    
    print(f"載入模型: {model_path}")
    model = YOLO(model_path)
    
    # 創建輸出目錄
    output_dir = "kneron_workspace"
    os.makedirs(output_dir, exist_ok=True)
    
    # 導出 ONNX 格式
    print("\n開始導出 ONNX 格式...")
    print("注意：Kneron toolchain 需要 ONNX 格式的模型")
    
    try:
        # 導出 ONNX，設定適合 Kneron 的參數
        onnx_path = model.export(
            format='onnx',
            imgsz=640,          # 輸入影像尺寸（與訓練時一致）
            simplify=True,      # 簡化模型
            opset=11,           # ONNX opset 版本（Kneron 通常支援 11）
            dynamic=False,      # 固定輸入尺寸（Kneron 通常需要固定尺寸）
        )
        
        # 移動到 kneron_workspace 目錄
        import shutil
        onnx_filename = os.path.basename(onnx_path)
        target_path = os.path.join(output_dir, onnx_filename)
        shutil.move(onnx_path, target_path)
        
        print(f"\n✓ ONNX 檔案導出成功！")
        print(f"檔案位置: {target_path}")
        print(f"\n檔案資訊：")
        print(f"  - 輸入尺寸: 640x640")
        print(f"  - ONNX Opset: 11")
        print(f"  - 輸入名稱: 請檢查 ONNX 檔案的輸入節點名稱")
        
        # 提示下一步
        print(f"\n下一步：")
        print(f"1. 確保 Docker 已安裝並運行")
        print(f"2. 執行: docker pull kneron/toolchain:latest")
        print(f"3. 使用 Kneron toolchain 進行轉換和編譯")
        print(f"4. 參考 kneron_convert.sh 腳本進行轉換")
        
    except Exception as e:
        print(f"\n✗ ONNX 導出失敗: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

