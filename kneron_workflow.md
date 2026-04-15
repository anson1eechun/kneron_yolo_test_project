# Kneron 工作流程指南

本指南說明如何將訓練好的 YOLOv8 模型轉換為 Kneron .nef 格式。

## 前置需求

1. **Docker Desktop** 已安裝並運行
2. **Kneron Toolchain Docker 鏡像** 已下載
3. **訓練好的模型** (best.pt)

## 步驟 1: 導出 ONNX 格式

```bash
py export_onnx_for_kneron.py
```

這會將模型導出為 ONNX 格式，並儲存在 `kneron_workspace/` 目錄中。

## 步驟 2: 下載 Kneron Toolchain Docker 鏡像

```bash
docker pull kneron/toolchain:latest
```

## 步驟 3: 啟動 Kneron Toolchain 容器

### Windows (使用 WSL2)

```bash
docker run --rm -it -v /mnt/docker:/docker_mount kneron/toolchain
```

### Linux/Mac

```bash
docker run --rm -it -v $(pwd):/workspace kneron/toolchain
```

## 步驟 4: 在容器內進行轉換

進入容器後，執行以下命令：

### 4.1 檢查 ONNX 檔案

```bash
# 確認檔案存在
ls -lh /docker_mount/kneron_workspace/best.onnx
```

### 4.2 轉換 ONNX 為 Kneron 格式

根據 Kneron 官方文件，使用適當的轉換工具：

```bash
# 範例命令（請根據實際 Kneron toolchain 版本調整）
python3 -m kneron_transform onnx_to_knmodel \
  --input /docker_mount/kneron_workspace/best.onnx \
  --output /docker_mount/kneron_workspace/output/ppe_yolov8n.knmodel
```

### 4.3 優化模型（可選）

```bash
python3 -m kneron_transform optimize \
  --input /docker_mount/kneron_workspace/output/ppe_yolov8n.knmodel \
  --output /docker_mount/kneron_workspace/output/ppe_yolov8n_optimized.knmodel
```

### 4.4 編譯為 .nef 檔案

```bash
# 根據您的 Kneron 硬體型號設定參數
python3 -m kneron_transform compile \
  --input /docker_mount/kneron_workspace/output/ppe_yolov8n_optimized.knmodel \
  --output /docker_mount/kneron_workspace/output/ppe_yolov8n.nef \
  --target <您的 Kneron 硬體型號>  # 例如: kneron_kl720
```

## 步驟 5: 驗證 .nef 檔案

轉換完成後，.nef 檔案會儲存在 `kneron_workspace/output/` 目錄中。

## 常見問題

### Q: 如何知道 ONNX 模型的輸入節點名稱？

A: 可以使用以下 Python 腳本檢查：

```python
import onnx

model = onnx.load("kneron_workspace/best.onnx")
input_name = model.graph.input[0].name
print(f"輸入節點名稱: {input_name}")
```

### Q: 轉換時出現錯誤怎麼辦？

A: 
1. 確認 ONNX 版本與 Kneron toolchain 相容
2. 檢查輸入尺寸是否正確（應為 640x640）
3. 確認 ONNX opset 版本（建議使用 11）
4. 參考 Kneron 官方文件中的錯誤處理指南

### Q: 如何選擇正確的 Kneron 硬體型號？

A: 根據您使用的 Kneron 開發板型號選擇，常見的有：
- `kneron_kl520`
- `kneron_kl720`
- `kneron_kl730`

## 參考資源

- [Kneron 官方文件](https://www.kneron.com/docs/)
- [Kneron Toolchain GitHub](https://github.com/kneron/kneron-toolchain)

## 注意事項

1. **ONNX 版本**: 確保導出的 ONNX 版本與 Kneron toolchain 相容
2. **輸入尺寸**: YOLOv8 的輸入尺寸為 640x640，請確保轉換時保持一致
3. **硬體型號**: 編譯時必須指定正確的 Kneron 硬體型號
4. **檔案路徑**: 在 Docker 容器內，確保使用正確的掛載路徑

