"""
使用訓練好的模型進行預測
支援單張圖片、圖片資料夾、MP4 影片檔案
"""

from ultralytics import YOLO
import os
import sys

def is_video_file(filepath):
    """檢查是否為影片檔案"""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    return any(filepath.lower().endswith(ext) for ext in video_extensions)

def main():
    # 載入最佳模型
    model_path = "runs/detect/runs/ppe_yolov8n22/weights/best.pt"
    
    if not os.path.exists(model_path):
        print(f"錯誤：找不到模型檔案 {model_path}")
        return
    
    print(f"載入模型: {model_path}")
    model = YOLO(model_path)
    
    # 檢查是否有指定輸入
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        print("請提供輸入檔案路徑")
        print("\n用法:")
        print("  圖片: py predict.py <圖片路徑>")
        print("  影片: py predict.py <影片路徑.mp4>")
        print("  資料夾: py predict.py <資料夾路徑>")
        return
    
    if not os.path.exists(source):
        print(f"錯誤：找不到檔案或資料夾 {source}")
        return
    
    # 判斷輸入類型
    is_video = is_video_file(source) if os.path.isfile(source) else False
    
    if is_video:
        print(f"\n偵測到影片檔案: {source}")
        print("開始處理影片...")
    else:
        print(f"\n正在對 {source} 進行預測...")
    
    # 進行預測
    results = model.predict(
        source=source,
        save=True,              # 儲存預測結果
        conf=0.25,              # 信心度閾值（可調整，0.25 為預設值）
        save_txt=True,          # 儲存標籤檔案（僅圖片）
        save_conf=True,         # 儲存信心度
        show=False,             # 不顯示結果視窗
        line_width=2,           # 邊框線寬度
    )
    
    if is_video:
        print(f"\n✓ 影片處理完成！")
        print(f"結果影片儲存在: runs/detect/predict/")
        # 影片結果會儲存為帶有預測框的影片檔案
    else:
        print(f"\n✓ 預測完成！")
        print(f"結果儲存在: runs/detect/predict/")
        print(f"共處理 {len(results)} 個檔案")

if __name__ == "__main__":
    main()

