# Kneron Toolchain 容器內命令參考

## 問題診斷

如果遇到 `No module named kneron_transform` 錯誤，表示命令格式可能不同。

## 檢查可用工具

在容器內執行以下命令來查找可用的工具：

```bash
# 1. 檢查 Python 模組
python3 -c "import sys; print('\n'.join(sys.path))"

# 2. 查找 Kneron 相關的命令
which kneron
ls -la /usr/bin/ | grep kneron
ls -la /usr/local/bin/ | grep kneron

# 3. 檢查是否有其他轉換工具
find /usr -name "*kneron*" 2>/dev/null
find /opt -name "*kneron*" 2>/dev/null

# 4. 檢查環境變數
env | grep -i kneron

# 5. 查看容器內的幫助文件
ls -la /workspace/
cat /workspace/README* 2>/dev/null
```

## 常見的 Kneron Toolchain 命令格式

根據不同的 Kneron toolchain 版本，命令格式可能不同：

### 格式 1: 使用 knmodel_tool

```bash
# 轉換 ONNX 為 Kneron 格式
knmodel_tool onnx_to_knmodel \
  --input best.onnx \
  --output output/ppe_yolov8n.knmodel
```

### 格式 2: 使用 kneron_tool

```bash
# 轉換 ONNX 為 Kneron 格式
kneron_tool convert \
  --input best.onnx \
  --output output/ppe_yolov8n.knmodel \
  --format knmodel
```

### 格式 3: 使用 Python 腳本

```bash
# 查找 Python 腳本
find /usr -name "*.py" | grep -i kneron
find /opt -name "*.py" | grep -i kneron

# 如果找到腳本，例如：
python3 /usr/local/bin/kneron_convert.py \
  --input best.onnx \
  --output output/ppe_yolov8n.knmodel
```

### 格式 4: 使用命令行工具

```bash
# 檢查是否有命令行工具
onnx2knmodel --help
kneron-convert --help
```

## 檢查 Kneron Toolchain 版本和文件

```bash
# 檢查版本
cat /etc/kneron* 2>/dev/null
cat /opt/kneron*/VERSION 2>/dev/null

# 查看文件
ls -la /opt/kneron*/ 2>/dev/null
ls -la /usr/local/kneron*/ 2>/dev/null

# 查看 README 或文檔
find /opt -name "README*" 2>/dev/null
find /usr -name "README*" | grep -i kneron 2>/dev/null
```

## 建議的檢查步驟

在容器內執行以下命令序列：

```bash
# 步驟 1: 檢查當前目錄和檔案
pwd
ls -la

# 步驟 2: 檢查 ONNX 檔案
ls -lh best.onnx

# 步驟 3: 查找所有可用的命令
compgen -c | grep -i kneron
compgen -c | grep -i knmodel
compgen -c | grep -i onnx

# 步驟 4: 檢查 Python 路徑中的模組
python3 -c "import pkgutil; [print(name) for _, name, _ in pkgutil.iter_modules() if 'kneron' in name.lower()]"

# 步驟 5: 列出所有已安裝的 Python 套件
pip3 list | grep -i kneron
```

## 如果找不到工具

如果以上方法都找不到，可能需要：

1. **檢查 Kneron 官方文件**
   - 確認您使用的 toolchain 版本
   - 查看該版本的具體使用方法

2. **檢查容器內的示例**
   ```bash
   find / -name "*example*" -type f 2>/dev/null | grep -i kneron
   find / -name "*sample*" -type f 2>/dev/null | grep -i kneron
   ```

3. **聯繫 Kneron 支援**
   - 提供您的 toolchain 版本資訊
   - 詢問正確的命令格式

## 替代方案：使用 Kneron SDK

如果 toolchain 容器內沒有轉換工具，可能需要：

1. 使用 Kneron SDK（在本地環境）
2. 使用 Kneron 的線上轉換服務
3. 使用其他版本的 toolchain 鏡像

