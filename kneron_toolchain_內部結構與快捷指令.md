# Kneron Toolchain 內部結構與快捷指令手冊

本文件是教學用途，目標是讓學員快速理解：

- Kneron toolchain 在做什麼
- 容器內部結構如何看
- 每個階段會產生哪些檔案
- 常用與快速排錯指令怎麼下

> 注意：不同 Kneron 版本的指令入口可能不同（例如 `kneron_transform`、其他 CLI 或 SDK 工具）。  
> 本文件提供「通用觀念 + 可移植命令模板」。

---

## 1. Toolchain 是什麼（功能總覽）

Kneron toolchain 可以視為一條編譯管線，把一般深度學習模型轉為 NPU 可執行格式。

標準流程：

1. **模型匯入（Import）**  
   讀入 ONNX，解析 graph、tensor shape、op 相容性。
2. **量化（Quantization）**  
   將 float 模型轉為 int8/int16 等硬體友善格式，產生 scale/radix。
3. **圖優化（Graph Optimization）**  
   做 operator fusion、memory layout 調整、硬體排程優化。
4. **後端編譯（Backend Compile）**  
   針對目標晶片（如 KL530）產生可部署二進位。
5. **封裝（Packaging）**  
   生成最終 `NEF` 與部署需要的 metadata（I/O、model id、fw info）。

---

## 2. 內部結構怎麼看（觀察視角）

在教學上，可把 toolchain 分成三層：

- **命令入口層**：你下的 CLI 命令（可能是 Python module 或可執行檔）
- **編譯流程層**：import -> quantize -> optimize -> compile -> package
- **輸出產物層**：NEF 與報表檔（供部署和除錯）

你不一定看得到所有「原始程式內部模組」，但可透過輸出檔反推每一階段是否正常。

---

## 3. 容器內常見目錄與角色

以下是教學時最實用的目錄觀念（非綁定固定版本）：

- `/workspace`：你從主機掛進來的專案資料夾
- `/workspace/kneron_workspace`：模型與輸出工作區（建議）
- `/usr/bin`, `/usr/local/bin`：可執行工具可能在這裡
- `/opt/...`：部分版本會把 SDK / toolchain 資料放在這裡

快速檢查：

```bash
pwd
ls -la
ls -la /usr/bin
ls -la /usr/local/bin
ls -la /opt
```

---

## 4. 典型輸出檔案與意義（以 KL530 流程為例）

在 `output/kl530_flow` 常見：

- `models_530.nef`  
  最終部署檔，燒錄/載入裝置時使用。
- `best_modelid_32770_ioinfo.json`  
  I/O 規格（input/output 名稱、shape、bitwidth、scale/radix）。
- `fw_info.txt`  
  model id、記憶體配置、bin size 等部署資訊。
- `model_fx_report.json` / `model_fx_report.html`  
  編譯與轉換報告（問題分析常用）。
- `*.bie`  
  中間或底層二進位產物（通常不直接手改）。

---

## 5. 快捷指令（Host 端）

### 5-1 三個最常用指令

```powershell
# 1) 切到你的專案根目錄
cd <你的專案根目錄>

# 2) 啟動 toolchain 容器（路徑無關）
docker run --rm -it -v "${PWD}:/workspace" kneron/toolchain

# 3) 看容器是否可啟
docker ps
```

### 5-2 一次做 ONNX 前置驗證

```powershell
py export_onnx_for_kneron.py
py check_onnx.py kneron_workspace/best.onnx
```

---

## 6. 快捷指令（Container 端）

### 6-1 開始前快檢（建議每次進容器先跑）

```bash
cd /workspace/kneron_workspace
ls -lh best.onnx
python3 --version
```

### 6-2 掃描可用命令入口（版本不一致時最重要）

```bash
# 列出可能命令
compgen -c | grep -Ei "kneron|knmodel|onnx" | head -n 50

# 列出可能可執行檔
ls -la /usr/bin | grep -Ei "kneron|knmodel|onnx"
ls -la /usr/local/bin | grep -Ei "kneron|knmodel|onnx"

# 列出 Python 套件中是否有 kneron 相關
python3 -c "import pkgutil; print('\n'.join([m.name for m in pkgutil.iter_modules() if 'kneron' in m.name.lower()]))"
```

### 6-3 標準編譯模板（若支援 `kneron_transform`）

```bash
cd /workspace/kneron_workspace
mkdir -p output/kl530_flow

python3 -m kneron_transform onnx_to_knmodel \
  --input best.onnx \
  --output output/kl530_flow/model.knmodel

python3 -m kneron_transform optimize \
  --input output/kl530_flow/model.knmodel \
  --output output/kl530_flow/model_opt.knmodel

python3 -m kneron_transform compile \
  --input output/kl530_flow/model_opt.knmodel \
  --output output/kl530_flow/models_530.nef \
  --target kl530
```

---

## 7. 功能對照表（教學講解可直接用）

- **Import 失敗**：通常是 ONNX ops / shape / 動態維度問題
- **Quantization 問題**：精度下降、scale/radix 不合理
- **Compile 失敗**：目標晶片參數錯誤或 op 不支援
- **Packaging 成功但推論異常**：多半是前後處理或 I/O 對不上

對應檢查檔案：

- I/O 問題 -> `*_ioinfo.json`
- model id / 記憶體 -> `fw_info.txt`
- 編譯行為細節 -> `model_fx_report.json/html`

---

## 8. 教學時最實用的排錯流程（5 分鐘版）

1. **看檔案在不在**  
   `best.onnx`、`models_530.nef` 是否存在。
2. **看 I/O 對不對**  
   input name、shape、output shape 是否與推論程式一致。
3. **看目標晶片對不對**  
   compile target 是否真的是 `kl530`。
4. **看指令入口有沒有**  
   `kneron_transform` 不存在就先掃描可用命令。
5. **看報告檔**  
   `model_fx_report` 裡常能找到 op 不支援或最佳化警告。

---

## 9. 快速問答（課堂常見）

### Q1：為什麼同樣教材，有人可以跑有人不行？

通常不是模型問題，而是：

- 工作目錄不同（沒有在專案根目錄）
- Docker 掛載路徑寫死
- toolchain 版本不同（命令名不同）

### Q2：NEF 有了就一定能推論嗎？

不一定。仍需確認：

- Model ID
- input/output 名稱與 shape
- 前處理（RGB/BGR、normalize、resize）一致
- 後處理（YOLO decode + NMS）一致

### Q3：教學時怎麼避免路徑問題？

永遠先做兩件事：

```powershell
cd <你的專案根目錄>
docker run --rm -it -v "${PWD}:/workspace" kneron/toolchain
```

---

## 10. 一頁速查（可貼投影片）

```powershell
# Host
cd <你的專案根目錄>
py export_onnx_for_kneron.py
py check_onnx.py kneron_workspace/best.onnx
docker run --rm -it -v "${PWD}:/workspace" kneron/toolchain
```

```bash
# Container
cd /workspace/kneron_workspace
ls -lh best.onnx
mkdir -p output/kl530_flow
# 依你版本可用命令做 onnx -> knmodel -> nef
ls -lh output/kl530_flow
```

---

如果你要做「講師版教材」，可在此文件後再加兩頁：

1. 失敗示範（故意用錯路徑 / 用錯 target）  
2. 修復示範（如何用 6-2 的命令在 1 分鐘內定位問題）
