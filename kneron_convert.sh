#!/bin/bash
# Kneron Toolchain 轉換腳本
# 用於將 ONNX 模型轉換為 Kneron 格式並編譯為 .nef 檔案

# 設定變數
ONNX_FILE="kneron_workspace/best.onnx"
OUTPUT_DIR="kneron_workspace/output"
MODEL_NAME="ppe_yolov8n"

# 檢查 ONNX 檔案是否存在
if [ ! -f "$ONNX_FILE" ]; then
    echo "錯誤：找不到 ONNX 檔案 $ONNX_FILE"
    echo "請先執行: py export_onnx_for_kneron.py"
    exit 1
fi

# 創建輸出目錄
mkdir -p $OUTPUT_DIR

echo "=========================================="
echo "Kneron Toolchain 轉換流程"
echo "=========================================="
echo ""
echo "步驟 1: 啟動 Kneron Toolchain Docker 容器"
echo "執行以下命令："
echo ""
echo "docker run --rm -it -v /mnt/docker:/docker_mount kneron/toolchain"
echo ""
echo "步驟 2: 在容器內執行轉換命令"
echo ""
echo "在 Docker 容器內，執行以下命令："
echo ""
echo "# 1. 轉換 ONNX 為 Kneron 格式"
echo "python3 -m kneron_transform onnx_to_knmodel \\"
echo "  --input $ONNX_FILE \\"
echo "  --output $OUTPUT_DIR/${MODEL_NAME}.knmodel"
echo ""
echo "# 2. 優化模型（如果需要）"
echo "python3 -m kneron_transform optimize \\"
echo "  --input $OUTPUT_DIR/${MODEL_NAME}.knmodel \\"
echo "  --output $OUTPUT_DIR/${MODEL_NAME}_optimized.knmodel"
echo ""
echo "# 3. 編譯為 .nef 檔案"
echo "python3 -m kneron_transform compile \\"
echo "  --input $OUTPUT_DIR/${MODEL_NAME}_optimized.knmodel \\"
echo "  --output $OUTPUT_DIR/${MODEL_NAME}.nef"
echo ""
echo "=========================================="
echo "注意事項："
echo "1. 確保 Docker 已安裝並運行"
echo "2. 確保已下載 Kneron toolchain 鏡像"
echo "3. 根據您的 Kneron 硬體型號調整編譯參數"
echo "4. 詳細命令請參考 Kneron 官方文件"
echo "=========================================="

