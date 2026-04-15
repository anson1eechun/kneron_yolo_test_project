# Docker Desktop 啟動指南

## 問題診斷

您遇到的錯誤：
```
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
```

這表示 **Docker Desktop 沒有運行**。

## 解決步驟

### 步驟 1: 啟動 Docker Desktop

1. **從開始選單啟動**
   - 點擊 Windows 開始按鈕
   - 搜尋 "Docker Desktop"
   - 點擊 "Docker Desktop" 應用程式

2. **從桌面捷徑啟動**
   - 如果桌面有 Docker Desktop 捷徑，雙擊啟動

3. **從系統匣啟動**
   - 檢查系統匣（右下角）是否有 Docker 圖示
   - 如果沒有，表示 Docker Desktop 未運行

### 步驟 2: 等待 Docker Desktop 啟動完成

啟動 Docker Desktop 後，您會看到：
- Docker Desktop 視窗開啟
- 系統匣出現 Docker 圖示（鯨魚圖示）
- 圖示從「正在啟動」變為「運行中」

**重要**: 首次啟動可能需要幾分鐘時間，請耐心等待。

### 步驟 3: 確認 Docker Desktop 狀態

啟動完成後，在 PowerShell 中執行：

```powershell
docker ps
```

如果看到類似以下的輸出（即使沒有容器），表示 Docker 已正常運行：
```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### 步驟 4: 驗證 Docker 版本

```powershell
docker --version
docker-compose --version
```

應該會顯示版本資訊，例如：
```
Docker version 29.2.0, build 0b9d198
```

## 常見問題

### Q: Docker Desktop 啟動失敗怎麼辦？

**A: 檢查以下項目：**

1. **WSL 2 是否已安裝**
   ```powershell
   wsl --status
   ```
   如果沒有安裝 WSL 2，需要先安裝：
   ```powershell
   wsl --install
   ```

2. **虛擬化是否啟用**
   - 檢查 BIOS/UEFI 設定中的虛擬化選項（Intel VT-x 或 AMD-V）
   - 確保已啟用

3. **Windows 版本**
   - Docker Desktop 需要 Windows 10 64-bit: Pro, Enterprise, or Education (Build 15063+) 或 Windows 11
   - 確認您的 Windows 版本符合要求

4. **重新啟動電腦**
   - 有時需要重新啟動才能正常運行

### Q: Docker Desktop 啟動很慢怎麼辦？

**A: 可能的原因：**

1. **首次啟動**：首次啟動需要初始化，可能需要 5-10 分鐘
2. **資源不足**：確保有足夠的記憶體和 CPU 資源
3. **防毒軟體**：某些防毒軟體可能會影響 Docker Desktop 的啟動速度

### Q: 如何確認 Docker Desktop 設定正確？

**A: 檢查設定：**

1. 打開 Docker Desktop
2. 點擊右上角的「設定」（齒輪圖示）
3. 確認以下設定：
   - ✅ **General** → **Use the WSL 2 based engine**（已勾選）
   - ✅ **Resources** → **Enable integration with my default WSL distro**（已勾選）

## 啟動 Docker Desktop 後的下一步

一旦 Docker Desktop 正常運行，您可以繼續執行：

```powershell
# 1. 下載 Kneron Toolchain
docker pull kneron/toolchain:latest

# 2. 啟動容器
docker run --rm -it -v G:\workplace\kneron_yolo_test:/workspace kneron/toolchain
```

## 快速檢查腳本

創建一個 PowerShell 腳本來檢查 Docker 狀態：

```powershell
# 檢查 Docker 是否運行
Write-Host "檢查 Docker Desktop 狀態..." -ForegroundColor Yellow

try {
    $result = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker Desktop 正在運行" -ForegroundColor Green
        docker --version
    } else {
        Write-Host "✗ Docker Desktop 未運行" -ForegroundColor Red
        Write-Host "請啟動 Docker Desktop 應用程式" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ 無法連接到 Docker" -ForegroundColor Red
    Write-Host "請確認 Docker Desktop 已啟動" -ForegroundColor Yellow
}
```

## 參考資源

- [Docker Desktop for Windows 官方文件](https://docs.docker.com/desktop/windows/)
- [Docker Desktop 故障排除指南](https://docs.docker.com/desktop/troubleshoot/)

