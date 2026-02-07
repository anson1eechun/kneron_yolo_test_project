"""
專門用於處理影片的預測腳本
提供更多影片處理選項
"""

from ultralytics import YOLO
import os
import sys

def main():
    # 載入最佳模型
    model_path = "runs/detect/runs/ppe_yolov8n22/weights/best.pt"
    
    if not os.path.exists(model_path):
        print(f"錯誤：找不到模型檔案 {model_path}")
        return
    
    print(f"載入模型: {model_path}")
    model = YOLO(model_path)
    
    # 檢查是否有指定輸入
    if len(sys.argv) < 2:
        print("請提供影片檔案路徑")
        print("\n用法: py predict_video.py <影片路徑.mp4> [選項]")
        print("\n選項:")
        print("  --conf <值>     信心度閾值 (0.0-1.0，預設: 0.25)")
        print("  --save-dir <路徑> 儲存目錄 (預設: runs/detect/predict)")
        print("\n範例:")
        print("  py predict_video.py video.mp4")
        print("  py predict_video.py video.mp4 --conf 0.5")
        return
    
    video_path = sys.argv[1]
    
    if not os.path.exists(video_path):
        print(f"錯誤：找不到影片檔案 {video_path}")
        return
    
    # 解析參數
    conf_threshold = 0.25
    save_dir = None
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--conf' and i + 1 < len(sys.argv):
            conf_threshold = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--save-dir' and i + 1 < len(sys.argv):
            save_dir = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    print(f"\n影片檔案: {video_path}")
    print(f"信心度閾值: {conf_threshold}")
    if save_dir:
        print(f"儲存目錄: {save_dir}")
    
    # 進行預測
    print("\n開始處理影片...")
    print("這可能需要一些時間，請耐心等待...")
    
    results = model.predict(
        source=video_path,
        save=True,              # 儲存預測結果
        conf=conf_threshold,    # 信心度閾值
        save_dir=save_dir,     # 自訂儲存目錄
        line_width=2,           # 邊框線寬度
        show=False,             # 不顯示結果視窗
    )
    
    print(f"\n✓ 影片處理完成！")
    if save_dir:
        print(f"結果影片儲存在: {save_dir}")
    else:
        print(f"結果影片儲存在: runs/detect/predict/")
    print("\n提示：處理後的影片檔名會加上 '_predict' 後綴")

if __name__ == "__main__":
    main()

