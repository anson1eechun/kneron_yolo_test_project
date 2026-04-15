# KL520 Windows 驅動安裝教學

本教學說明在 **Windows 10/11** 上，如何讓電腦正確辨識以 **USB** 連接的 **Kneron KL520** 開發板／模組，並確認驅動是否已生效。適用於需透過 **libusb / Python pyusb** 或官方 Host 工具與裝置通訊的情境。

> **官方文件（請一併查閱）**  
> [Kneron KL520 SDK 2.2.0 文件 - Introduction](https://doc.kneron.com/docs/#520_2.2.0/introduction/)  
> 各版 SDK 的驅動名稱、安裝包路徑可能略有差異，**若與本教學衝突，以官方文件為準**。

---

## 一、開始前請準備

- Windows 10 或 11（建議 64 位元）
- **可傳資料的 USB 線**（非僅充電線）
- 板子 **供電正常**（部分 EVB 需外接電源）
- 管理員權限（僅在安裝驅動或 Zadig 需要時使用）

---

## 二、先確認：電腦有沒有「看到」硬體

1. 用 USB 連接 KL520 與電腦。  
2. 開啟 **裝置管理員**（`Win + X` → 裝置管理員）。  
3. 觀察是否出現新裝置，常見位置：  
   - **通用序列匯流排裝置**  
   - **通用 WinUSB 裝置**  
   - **其他裝置**底下的 **未知裝置**（黃色驚嘆號）

若 **完全沒有新裝置**：請先檢查線材、USB 埠、板子電源；與驅動無關。

---

## 三、兩種常見安裝路徑（擇一或依文件併用）

### 路徑 A：官方提供的驅動或安裝程式（建議優先）

1. 開啟 [KL520 2.2.0 文件](https://doc.kneron.com/docs/#520_2.2.0/introduction/)。  
2. 在左側目錄搜尋與 **Windows、USB、driver、environment、setup** 相關的章節。  
3. 若文件要求：  
   - 執行 **`.exe` 安裝程式**，或  
   - 在裝置管理員對裝置選 **更新驅動程式** → **瀏覽電腦上的驅動程式** → 指向文件指定的 **驅動資料夾**  

請 **完整依照該版文件** 操作，不要略過版本號檢查。

### 路徑 B：使用 Zadig 安裝 **WinUSB**（常見於 Python `pyusb` / libusb 工具）

當裝置顯示為 **未知裝置**，或官方文件註明可使用 **WinUSB / libusb** 時，可使用本方式。

> **注意**：Zadig 會替 **你選中的那一個 USB 介面** 更換驅動。若為 **複合裝置**（一個硬體多個介面），選錯介面會導致工具連不到裝置，需重新對正確介面安裝。

**步驟：**

1. 下載 [Zadig](https://zadig.akeo.ie/)（僅在官方允許或文件建議時使用）。  
2. 以**系統管理員身分**執行 Zadig（建議）。  
3. 選單 **Options** → 勾選 **List All Devices**。  
4. 在下拉清單中選擇你的 **Kneron / KL520** 相關裝置（可與裝置管理員比對）。  
5. 右側驅動選 **WinUSB**（或文件指定之選項）。  
6. 按 **Install Driver** 或 **Replace Driver**。  
7. **拔除 USB 後再插上**，重新開啟裝置管理員，確認 **無黃色驚嘆號**。

**對照 VID（常見值）**  
SDK 內建工具腳本常使用 **USB Vendor ID `0x0D7D`**（十進位 3453）。實際 **PID** 可能依韌體模式不同，請以裝置管理員 **硬體識別碼** 為準。

---

## 四、如何確認「驅動已安裝且可用」

### 1. 裝置管理員（最直覺）

- 對應裝置 **無黃色驚嘆號**。  
- 右鍵 → **內容** → **驅動程式**：可看到 **驅動程式提供者**、**版本**、**日期**。  
- **詳細資料** → 屬性選 **硬體識別碼**：應包含 `USB\VID_0D7D&PID_...`（PID 依裝置而定）。

### 2. PowerShell：列出 Kneron 常見 VID

在 PowerShell 執行：

```powershell
Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match 'VID_0[Dd]7[Dd]' } |
  Format-Table Status, Class, FriendlyName, InstanceId -AutoSize
```

- 有列出且 **Status 為 `OK`**：通常表示系統已正確載入並枚舉該裝置。  
- **無任何輸出**：可能未連線、VID 不同，或裝置未以 USB 裝置形式出現。

### 3. 本專案附帶的 USB 測試腳本（選用）

若已安裝 **Python** 與套件 **`pyusb`**、**`libusb-package`**，可在專案根目錄執行：

```powershell
py -m pip install pyusb libusb-package
py test_kneron_usb.py
```

腳本會同時檢查 PnP 與 `pyusb` 是否能找到 **`VID 0x0D7D`** 的裝置。若顯示找不到，請對照本教學「常見問題」一節排查。

---

## 五、常見問題與處理方式

| 現象 | 可能原因 | 建議處理 |
|------|----------|----------|
| 裝置管理員出現 **未知裝置**（驚嘆號） | 尚未安裝驅動或 WinUSB | 依 **路徑 A** 或 **路徑 B** 安裝 |
| Zadig 裝完仍無法用 Python 連線 | **複合裝置**裝錯介面 | 在 Zadig 換選其他 **Interface**，再 Replace Driver |
| 裝置管理員完全沒有新項目 | 線材僅充電、埠故障、未上電 | 更換線材／埠／確認供電 |
| PnP 有裝置但工具仍連不上 | 後端 DLL、權限、或選錯裝置 | 確認使用 **64-bit Python**；必要時以系統管理員執行；關閉暫時佔用 USB 的程式 |
| 僅使用 **UART** 連線 | 不會出現 `VID_0D7D` 的 USB 裝置 | 在 **連接埠 (COM 和 LPT)** 查看 COM 號，依文件走序列埠流程 |

---

## 六、驅動裝好後的下一步

WinUSB／官方驅動解決的是 **「作業系統能否把 USB 交給程式使用」**。  

若要 **載入 NEF、執行推論**，還須依官方文件安裝 **Host SDK / 範例程式**，並確認：

- 板端韌體與 Host API **版本相容**  
- NEF 為 **KL520 目標**編譯（不可直接使用 KL530 的 NEF）

請繼續閱讀官方文件中 **Inference / Quick start / Host** 等章節。

---

## 七、版本與免責說明

- 本教學以 **KL520、Windows、USB** 常見情境整理，**不取代** Kneron 官方文件。  
- **Zadig** 會變更系統驅動綁定，請在了解風險且符合官方建議時使用。  
- 若貴單位有 IT 政策限制，請先取得同意再安裝第三方驅動工具。

---

## 參考檔案（本專案內）

| 檔案 | 說明 |
|------|------|
| `test_kneron_usb.py` | 本機測試 PnP 與 `pyusb` 是否偵測到常見 Kneron VID |

SDK 內與 USB VID/PID 相關的範例常數可參考：  
`KL520_SDK_2.2.0\KL520_SDK\firmware\utils\minion\setup.py`（`VENDOR_ID` / `PRODUCT_ID`）。
