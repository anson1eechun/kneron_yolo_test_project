# YOLOv8 教學版：一步一步產出 ONNX 與 NEF（KL530）

這份是「照著做就能完成」的教學手冊，目標流程如下：  
`best.pt` -> `best.onnx` -> `models_530.nef`

---

## 路徑無關使用原則（重點）

本教學可套用到任何人的資料夾結構，請遵守這三個規則：

1. 先 `cd` 到「你的專案根目錄」再執行所有命令。
2. 指令一律優先使用「相對路徑」（例如 `kneron_workspace/best.onnx`）。
3. Docker 掛載一律用「目前目錄」變數（PowerShell 用 `${PWD}`）。

---

## 0. 你會學到什麼

完成本教學後，你會得到：

- `kneron_workspace/best.onnx`
- `kneron_workspace/output/kl530_flow/models_530.nef`
- 對應模型資訊（Model ID / Input / Output）

---

## 1. 開始前先確認環境（不要跳過）

### 1-1 先切到你的專案根目錄（每個人路徑可不同）

在 PowerShell 執行：

```powershell
# 範例：請改成你自己的專案路徑
cd <你的專案根目錄>

# 確認目前位置
pwd
```

預期：顯示你自己的專案根目錄（不需要和別人一樣）。

### 1-2 確認專案內有訓練好的 `best.pt`

請確認 `export_onnx_for_kneron.py` 裡的 `model_path` 指向正確模型，例如：

```python
model_path = "runs/detect/runs/ppe_yolov8n22/weights/best.pt"
```

如果路徑不對，先改對再繼續。  
重點是「指到你自己的 `best.pt`」，不是固定某個人的資料夾。

### 1-3 確認 Docker 已啟動

```powershell
docker ps
```

如果出現 Docker API 連線錯誤，先開啟 Docker Desktop，等到狀態是 Running 再重試。

### 1-4（首次才需要）下載 Kneron toolchain

```powershell
docker pull kneron/toolchain:latest
```

---

## 2. 第一步：從 `best.pt` 匯出 ONNX

### 2-1 執行匯出腳本

```powershell
py export_onnx_for_kneron.py
```

此腳本已為 Kneron 做好常用設定：

- `imgsz=640`
- `opset=11`
- `dynamic=False`
- `simplify=True`

### 2-2 看結果是否成功

成功時請確認檔案存在：

```powershell
dir kneron_workspace\best.onnx
```

若看得到 `best.onnx`，代表 ONNX 已產出成功。

---

## 3. 第二步：檢查 ONNX 是否符合轉檔需求

### 3-1 執行 ONNX 檢查

```powershell
py check_onnx.py kneron_workspace/best.onnx
```

### 3-2 請逐項核對（很重要）

檢查輸出中至少要符合：

- Input shape 是 `[1, 3, 640, 640]`
- Output 存在（通常是 `output0`）
- Opset 為 11
- 顯示模型驗證通過

只要這一步不通過，就先不要進行 NEF 編譯。

---

## 4. 第三步：進入 Kneron toolchain 容器

### 4-1 啟動容器

在專案根目錄執行：

```powershell
docker run --rm -it -v "${PWD}:/workspace" kneron/toolchain
```

你會進入 Linux shell（提示字元通常像 `root@xxxx:/workspace#`）。  
`${PWD}` 代表目前所在資料夾，所以每個人都可以直接使用。

### 4-2 在容器內確認 ONNX 存在

```bash
cd /workspace/kneron_workspace
ls -lh best.onnx
```

若顯示 `No such file`，通常是 Volume 掛載路徑打錯，請先退出容器重跑第 4-1 步。

---

## 5. 第四步：在容器內產出 KL530 的 NEF

> 注意：不同版本 toolchain 指令可能不同。  
> 先用「標準流程」，失敗再走「替代流程」。

### 5-A 標準流程（容器支援 `kneron_transform` 時）

```bash
cd /workspace/kneron_workspace
mkdir -p output/kl530_flow

# 1) ONNX -> knmodel
python3 -m kneron_transform onnx_to_knmodel \
  --input best.onnx \
  --output output/kl530_flow/ppe_yolov8n.knmodel

# 2) 優化（可選但建議）
python3 -m kneron_transform optimize \
  --input output/kl530_flow/ppe_yolov8n.knmodel \
  --output output/kl530_flow/ppe_yolov8n_optimized.knmodel

# 3) 編譯為 KL530 的 NEF
python3 -m kneron_transform compile \
  --input output/kl530_flow/ppe_yolov8n_optimized.knmodel \
  --output output/kl530_flow/models_530.nef \
  --target kl530
```

### 5-B 替代流程（遇到 `No module named kneron_transform`）

先查容器內有哪些 Kneron 工具可用：

```bash
cd /workspace/kneron_workspace
bash check_toolchain.sh
```

再依檢查結果改用該版本可用的命令。  
（你的專案已放好 `check_toolchain.sh`，就是為了這一步）

---

## 6. 第五步：確認 NEF 產出成功

離開容器後，在 PowerShell 檢查：

```powershell
dir kneron_workspace\output\kl530_flow
```

成功時至少會看到：

- `models_530.nef`
- `fw_info.txt`
- `best_modelid_32770_ioinfo.json`

---

## 7. 第六步：核對模型關鍵資訊（部署前必做）

請開啟並確認：

- `kneron_workspace/output/kl530_flow/fw_info.txt`
- `kneron_workspace/output/kl530_flow/best_modelid_32770_ioinfo.json`

核對重點：

- Model ID：`32770`
- Input：`images` / `[1,3,640,640]`
- Output：`output0` / `[1,14,8400]`

這些值在你之後跑 KL530 推論時會用到。

---

## 8. 教學常見錯誤與解法

### 問題 A：找不到 `best.pt`

原因：`export_onnx_for_kneron.py` 的 `model_path` 不正確。  
解法：先改成你實際的 `best.pt` 路徑再重跑。

### 問題 B：ONNX 輸入尺寸不是 640x640

原因：匯出參數不是 `imgsz=640`。  
解法：修正腳本後重新匯出 ONNX。

### 問題 C：Docker 無法連線

原因：Docker Desktop 尚未啟動。  
解法：先啟動 Docker Desktop，待 Running 後再執行命令。

### 問題 D：`kneron_transform` 指令不存在

原因：toolchain 版本不同。  
解法：跑 `bash check_toolchain.sh` 找實際可用工具，再改用對應命令。

### 問題 E：容器內看不到專案檔案

原因：啟動容器時不是在專案根目錄，或使用了寫死路徑。  
解法：先在主機端用 `pwd` 確認目前目錄，再用：

```powershell
docker run --rm -it -v "${PWD}:/workspace" kneron/toolchain
```

---

## 9. 快速複習（上課示範可用）

```powershell
# Step 0: 切到你的專案目錄（每個人不同）
cd <你的專案根目錄>

# Step 1: 匯出 ONNX
py export_onnx_for_kneron.py

# Step 2: 驗證 ONNX
py check_onnx.py kneron_workspace/best.onnx

# Step 3: 進容器編譯 NEF
docker run --rm -it -v "${PWD}:/workspace" kneron/toolchain
```

容器內：

```bash
cd /workspace/kneron_workspace
mkdir -p output/kl530_flow
# 依第 5 章標準流程或替代流程完成編譯
```
