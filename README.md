# YOLOv8n PPE 檢測模型訓練專案

本專案用於訓練 YOLOv8n 模型來檢測個人防護裝備（PPE）。

## 資料集資訊

- **類別數量**: 10 個類別
- **類別名稱**: boots, gloves, goggles, helmet, no-boots, no-gloves, no-goggles, no-helmet, no-vest, vest
- **訓練集**: 3,597 張影像
- **驗證集**: 1,026 張影像
- **測試集**: 517 張影像

## 環境建置

### 1. 安裝 Python 套件

**Windows 系統：**
```bash
py -m pip install -r requirements.txt
```

**Linux/Mac 系統：**
```bash
pip install -r requirements.txt
```

**重要：GPU 支援**

如果您有 NVIDIA GPU 並想使用 GPU 加速訓練，需要安裝支援 CUDA 的 PyTorch 版本：

1. 首先卸載 CPU 版本的 PyTorch（如果已安裝）：
   ```bash
   py -m pip uninstall torch torchvision torchaudio -y
   ```

2. 安裝 CUDA 版本的 PyTorch（根據您的 CUDA 版本選擇）：
   ```bash
   # CUDA 12.1（適用於 CUDA 12.x 和 13.x）
   py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   
   # 或 CUDA 11.8（適用於 CUDA 11.x）
   py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. 驗證 GPU 是否可用：
   ```bash
   py -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
   ```

如果顯示 `CUDA available: True` 和您的 GPU 名稱，則表示 GPU 已正確配置。

### 2. 確認資料集結構

確保資料集結構如下：
```
PPE detection.v1i.yolov8/
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

## 訓練模型

執行訓練腳本：

```bash
python train.py
```

### 訓練參數說明

訓練腳本中的主要參數：
- `epochs`: 訓練輪數（預設 100）
- `batch`: 批次大小（預設 16，可根據 GPU 記憶體調整）
- `imgsz`: 輸入影像尺寸（預設 640）
- `device`: 使用 GPU 編號（0 為第一張 GPU，'cpu' 為使用 CPU）
- `patience`: 早停耐心值（50 個 epoch 無改善則停止）

### 調整訓練參數

如需調整訓練參數，請編輯 `train.py` 檔案中的 `model.train()` 參數。

## 訓練結果

訓練完成後，結果會儲存在 `runs/detect/ppe_yolov8n/` 資料夾中，包含：
- 最佳模型權重 (`best.pt`)
- 最後一個 epoch 的權重 (`last.pt`)
- 訓練過程圖表
- 驗證結果

## 使用訓練好的模型

訓練完成後，可以使用以下程式碼載入模型進行推論：

```python
from ultralytics import YOLO

# 載入訓練好的模型
model = YOLO('runs/detect/ppe_yolov8n/weights/best.pt')

# 進行預測
results = model('path/to/image.jpg')

# 顯示結果
results[0].show()
```

## 注意事項

1. 確保有足夠的 GPU 記憶體，如果記憶體不足，可以降低 `batch` 大小
2. 訓練時間取決於硬體配置，使用 GPU 會大幅加速訓練
3. 建議監控訓練過程，根據驗證結果調整超參數

