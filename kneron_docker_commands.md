# Kneron Docker 命令參考

## 模型資訊

根據檢查結果，您的 ONNX 模型資訊如下：
- **輸入名稱**: `images`
- **輸入形狀**: `[1, 3, 640, 640]`
- **輸出名稱**: `output0`
- **輸出形狀**: `[1, 14, 8400]`
- **ONNX Opset**: 11

## 步驟 1: 下載 Kneron Toolchain

```bash
docker pull kneron/toolchain:latest
```

## 步驟 2: 啟動 Docker 容器

### Windows (使用 WSL2 或 PowerShell)

```powershell
# 確保 Docker Desktop 正在運行
# 然後執行：
docker run --rm -it -v ${PWD}:/workspace kneron/toolchain
```

或者使用絕對路徑：

```powershell
docker run --rm -it -v G:\workplace\kneron_yolo_test:/workspace kneron/toolchain
```

### Linux/Mac

```bash
docker run --rm -it -v $(pwd):/workspace kneron/toolchain
```

## 步驟 3: 在容器內執行轉換

進入容器後，您會看到類似這樣的提示：

```
root@<container_id>:/workspace#
```

### 3.1 檢查檔案

```bash
# 確認 ONNX 檔案存在
ls -lh /workspace/kneron_workspace/best.onnx

# 檢查檔案大小（應該約 11.7 MB）
```

### 3.2 轉換 ONNX 為 Kneron 格式

根據 Kneron 官方文件，使用以下命令：

```bash
# 進入工作目錄
cd /workspace/kneron_workspace

# 轉換 ONNX 為 Kneron 格式
# 注意：實際命令可能因 Kneron toolchain 版本而異
python3 -m kneron_transform onnx_to_knmodel \
  --input best.onnx \
  --output output/ppe_yolov8n.knmodel
```

### 3.3 優化模型（可選）

```bash
python3 -m kneron_transform optimize \
  --input output/ppe_yolov8n.knmodel \
  --output output/ppe_yolov8n_optimized.knmodel
```

### 3.4 編譯為 .nef 檔案

```bash
# 根據您的 Kneron 硬體型號選擇目標平台
# 常見選項：kl520, kl720, kl730

python3 -m kneron_transform compile \
  --input output/ppe_yolov8n_optimized.knmodel \
  --output output/ppe_yolov8n.nef \
  --target kl720  # 請根據您的硬體修改
```

## 步驟 4: 驗證輸出

轉換完成後，檢查輸出檔案：

```bash
ls -lh /workspace/kneron_workspace/output/
```

您應該會看到：
- `ppe_yolov8n.knmodel` - Kneron 模型格式
- `ppe_yolov8n_optimized.knmodel` - 優化後的模型（如果執行了優化）
- `ppe_yolov8n.nef` - 最終的 NEF 檔案（用於部署）

## 注意事項

1. **硬體型號**: 編譯時必須指定正確的 Kneron 硬體型號
   - KL520: 適用於邊緣 AI 應用
   - KL720: 更高性能的版本
   - KL730: 最新版本

2. **路徑問題**: 
   - Windows 上使用 Docker 時，確保路徑正確掛載
   - 如果遇到路徑問題，可以使用絕對路徑

3. **命令格式**: 
   - 實際的命令可能因 Kneron toolchain 版本而異
   - 請參考 Kneron 官方文件中的最新命令格式

4. **錯誤處理**: 
   - 如果轉換失敗，檢查 ONNX 檔案是否正確
   - 確認輸入/輸出節點名稱是否匹配
   - 檢查 Kneron toolchain 版本是否支援您的 ONNX opset 版本

## 快速參考

完整的命令序列（在 Docker 容器內）：

```bash
cd /workspace/kneron_workspace
mkdir -p output

# 轉換
python3 -m kneron_transform onnx_to_knmodel \
  --input best.onnx \
  --output output/ppe_yolov8n.knmodel

# 優化（可選）
python3 -m kneron_transform optimize \
  --input output/ppe_yolov8n.knmodel \
  --output output/ppe_yolov8n_optimized.knmodel

# 編譯
python3 -m kneron_transform compile \
  --input output/ppe_yolov8n_optimized.knmodel \
  --output output/ppe_yolov8n.nef \
  --target kl720
```

