"""
導出模型為不同格式
支援 ONNX, TensorRT, CoreML, TensorFlow 等格式
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
    
    print("\n可用的導出格式：")
    print("1. ONNX (推薦，通用格式)")
    print("2. TensorRT (NVIDIA GPU 加速)")
    print("3. CoreML (Apple 裝置)")
    print("4. TensorFlow (SavedModel)")
    print("5. TensorFlow Lite (行動裝置)")
    print("6. OpenVINO (Intel 硬體)")
    print("7. 全部格式")
    
    choice = input("\n請選擇要導出的格式 (1-7，直接按 Enter 預設為 ONNX): ").strip()
    
    formats = {
        '1': 'onnx',
        '2': 'engine',  # TensorRT
        '3': 'coreml',
        '4': 'saved_model',  # TensorFlow
        '5': 'tflite',
        '6': 'openvino',
        '7': 'all'
    }
    
    export_format = formats.get(choice, 'onnx')
    
    if export_format == 'all':
        formats_to_export = ['onnx', 'engine', 'coreml', 'saved_model', 'tflite', 'openvino']
    else:
        formats_to_export = [export_format]
    
    print(f"\n開始導出模型...")
    for fmt in formats_to_export:
        try:
            print(f"\n導出為 {fmt.upper()} 格式...")
            model.export(format=fmt, imgsz=640)
            print(f"✓ {fmt.upper()} 格式導出成功")
        except Exception as e:
            print(f"✗ {fmt.upper()} 格式導出失敗: {e}")
    
    print("\n導出完成！導出的檔案位於模型目錄中")

if __name__ == "__main__":
    main()

