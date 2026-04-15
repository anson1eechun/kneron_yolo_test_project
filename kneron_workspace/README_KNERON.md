# Kneron Toolchain 使用說明

## 檢查結果

根據檢查，當前的 `kneron/toolchain:latest` 容器似乎是一個基礎環境，可能不包含預裝的轉換工具。

## 可能的解決方案

### 方案 1: 檢查 Kneron 官方文件

Kneron toolchain 的命令格式可能因版本而異。請參考：
- [Kneron 官方文件](https://www.kneron.com/docs/)
- [Kneron Toolchain GitHub](https://github.com/kneron/kneron-toolchain)

### 方案 2: 使用 Kneron SDK（本地環境）

如果 Docker 容器內沒有工具，可能需要：
1. 在本地 Windows 環境安裝 Kneron SDK
2. 使用 SDK 提供的轉換工具

### 方案 3: 檢查其他 Kneron 鏡像

可能有多個 Kneron 鏡像版本：
```bash
docker search kneron
```

### 方案 4: 手動安裝工具

在容器內可能需要安裝 Kneron toolchain：
```bash
# 在容器內執行（需要網路連接）
# 根據 Kneron 官方文件安裝工具
```

## 當前狀態

- ✅ ONNX 檔案已準備：`kneron_workspace/best.onnx` (12.2 MB)
- ✅ Docker 容器運行正常
- ❌ 未找到 Kneron 轉換工具

## 建議的下一步

1. **查閱 Kneron 官方文件**：確認正確的 toolchain 使用方式
2. **聯繫 Kneron 支援**：詢問 toolchain 的正確使用方法
3. **檢查 Kneron SDK**：考慮在本地環境使用 SDK 進行轉換

## ONNX 模型資訊

- **檔案位置**: `/workspace/kneron_workspace/best.onnx`
- **檔案大小**: 12.2 MB
- **輸入**: `images` [1, 3, 640, 640]
- **輸出**: `output0` [1, 14, 8400]
- **ONNX Opset**: 11

模型已準備好，等待轉換工具。

