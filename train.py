"""
YOLOv8n 模型訓練腳本
用於訓練 PPE (個人防護裝備) 檢測模型
"""

from ultralytics import YOLO
import os
import torch

def main():
    # 設定資料集配置檔案路徑
    data_yaml = "PPE detection.v1i.yolov8/data.yaml"
    
    # 檢查檔案是否存在
    if not os.path.exists(data_yaml):
        print(f"錯誤：找不到資料集配置檔案 {data_yaml}")
        return
    
    # 自動檢測可用設備
    if torch.cuda.is_available():
        device = 0  # 使用第一張 GPU
        batch_size = 16
        workers = 8
        print(f"偵測到 CUDA GPU，將使用 GPU 進行訓練")
    else:
        device = 'cpu'  # 使用 CPU
        batch_size = 4  # CPU 訓練時使用較小的批次大小
        workers = 4     # CPU 訓練時使用較少的工作線程
        print("未偵測到 CUDA GPU，將使用 CPU 進行訓練（訓練速度會較慢）")
    
    # 檢查是否有可恢復的訓練檢查點
    checkpoint_path = "runs/detect/ppe_yolov8n2/weights/last.pt"
    resume_training = os.path.exists(checkpoint_path)
    
    if resume_training:
        print(f"找到檢查點，將從 {checkpoint_path} 恢復訓練...")
        model = YOLO(checkpoint_path)  # 從檢查點載入
    else:
        # 載入 YOLOv8n 預訓練模型（nano 版本，最小最快）
        print("載入 YOLOv8n 預訓練模型...")
        model = YOLO('yolov8n.pt')  # 自動下載預訓練權重
    
    # 開始訓練
    print("開始訓練模型...")
    results = model.train(
        data=data_yaml,           # 資料集配置檔案
        epochs=100,               # 訓練輪數（可根據需要調整）
        imgsz=640,                # 輸入影像尺寸
        batch=batch_size,         # 批次大小（根據設備自動調整）
        name='ppe_yolov8n2',      # 實驗名稱（與之前的訓練一致）
        project='runs',           # 專案資料夾
        device=device,            # 自動選擇設備（GPU 或 CPU）
        workers=workers,          # 資料載入工作線程數（根據設備自動調整）
        patience=50,              # 早停耐心值（50 個 epoch 無改善則停止）
        save=True,                # 儲存檢查點
        save_period=10,           # 每 10 個 epoch 儲存一次
        val=True,                 # 訓練過程中進行驗證
        plots=True,               # 生成訓練圖表
        verbose=True,             # 顯示詳細資訊
        resume=resume_training,    # 從檢查點恢復訓練
    )
    
    print("訓練完成！")
    print(f"最佳模型儲存在: {results.save_dir}")

if __name__ == "__main__":
    main()

