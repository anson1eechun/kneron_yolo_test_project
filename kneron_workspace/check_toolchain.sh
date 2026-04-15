#!/bin/bash
# Kneron Toolchain 檢查腳本
# 在 Docker 容器內執行此腳本來查找可用的工具

echo "=========================================="
echo "Kneron Toolchain 工具檢查"
echo "=========================================="
echo ""

echo "1. 檢查當前目錄和檔案..."
pwd
ls -la
echo ""

echo "2. 檢查 ONNX 檔案..."
if [ -f "best.onnx" ]; then
    ls -lh best.onnx
    echo "[OK] ONNX 檔案存在"
else
    echo "[ERROR] 找不到 best.onnx 檔案"
fi
echo ""

echo "3. 查找 Kneron 相關的命令..."
echo "   查找 'kneron' 命令:"
compgen -c | grep -i kneron | head -10
echo ""
echo "   查找 'knmodel' 命令:"
compgen -c | grep -i knmodel | head -10
echo ""
echo "   查找 'onnx' 相關命令:"
compgen -c | grep -i onnx | head -10
echo ""

echo "4. 檢查系統路徑中的可執行檔..."
echo "   /usr/bin 中的 Kneron 工具:"
ls -la /usr/bin/ | grep -i kneron
ls -la /usr/bin/ | grep -i knmodel
echo ""
echo "   /usr/local/bin 中的 Kneron 工具:"
ls -la /usr/local/bin/ | grep -i kneron
ls -la /usr/local/bin/ | grep -i knmodel
echo ""

echo "5. 查找 Kneron 相關的檔案..."
echo "   在 /usr 中查找:"
find /usr -name "*kneron*" -type f 2>/dev/null | head -10
echo ""
echo "   在 /opt 中查找:"
find /opt -name "*kneron*" -type f 2>/dev/null | head -10
echo ""

echo "6. 檢查 Python 模組..."
echo "   已安裝的 Kneron 相關套件:"
pip3 list 2>/dev/null | grep -i kneron || echo "   未找到相關套件"
echo ""

echo "7. 檢查環境變數..."
env | grep -i kneron || echo "   未找到 Kneron 相關環境變數"
echo ""

echo "8. 查找示例檔案和文檔..."
find /opt -name "README*" 2>/dev/null | head -5
find /usr -name "*example*" -type f 2>/dev/null | grep -i kneron | head -5
echo ""

echo "9. 檢查版本資訊..."
cat /etc/kneron* 2>/dev/null || echo "   未找到版本檔案"
cat /opt/kneron*/VERSION 2>/dev/null || echo "   未找到版本檔案"
echo ""

echo "=========================================="
echo "檢查完成"
echo "=========================================="
echo ""
echo "如果找到工具，請嘗試執行:"
echo "  <工具名稱> --help"
echo "  或"
echo "  <工具名稱> -h"
echo ""

