"""
測試訓練好的模型
對測試集進行評估並顯示結果
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
    
    # 對測試集進行評估
    data_yaml = "PPE detection.v1i.yolov8/data.yaml"
    
    print("\n正在評估測試集...")
    metrics = model.val(data=data_yaml, split='test')
    
    print("\n=== 測試集評估結果 ===")
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"精確度 (Precision): {metrics.box.mp:.4f}")
    print(f"召回率 (Recall): {metrics.box.mr:.4f}")
    
    print("\n=== 各類別詳細結果 ===")
    if hasattr(metrics, 'box') and hasattr(metrics.box, 'maps'):
        class_names = ['boots', 'gloves', 'goggles', 'helmet', 'no-boots', 
                      'no-gloves', 'no-goggles', 'no-helmet', 'no-vest', 'vest']
        for i, (name, map50) in enumerate(zip(class_names, metrics.box.maps)):
            print(f"{name:15s} mAP50: {map50:.4f}")

if __name__ == "__main__":
    main()

