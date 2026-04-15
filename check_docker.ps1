# Docker Desktop 狀態檢查腳本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker Desktop 狀態檢查" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 檢查 Docker 命令是否可用
Write-Host "1. 檢查 Docker 命令..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [OK] $dockerVersion" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] Docker 命令不可用" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "   [ERROR] Docker 未安裝或不在 PATH 中" -ForegroundColor Red
    exit 1
}

Write-Host ""

# 檢查 Docker Desktop 是否運行
Write-Host "2. 檢查 Docker Desktop 是否運行..." -ForegroundColor Yellow
try {
    $result = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [OK] Docker Desktop 正在運行" -ForegroundColor Green
        Write-Host ""
        Write-Host "   當前運行的容器:" -ForegroundColor Cyan
        docker ps
    } else {
        Write-Host "   [ERROR] Docker Desktop 未運行" -ForegroundColor Red
        Write-Host ""
        Write-Host "   請執行以下步驟:" -ForegroundColor Yellow
        Write-Host "   1. 從開始選單啟動 'Docker Desktop'" -ForegroundColor White
        Write-Host "   2. 等待 Docker Desktop 完全啟動（可能需要幾分鐘）" -ForegroundColor White
        Write-Host "   3. 確認系統匣（右下角）有 Docker 圖示" -ForegroundColor White
        Write-Host "   4. 重新執行此腳本確認狀態" -ForegroundColor White
        exit 1
    }
} catch {
    Write-Host "   [ERROR] 無法連接到 Docker API" -ForegroundColor Red
    Write-Host "   請確認 Docker Desktop 已啟動" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "3. 檢查 Docker Compose..." -ForegroundColor Yellow
try {
    $composeVersion = docker-compose --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   [OK] $composeVersion" -ForegroundColor Green
    } else {
        Write-Host "   [WARNING] Docker Compose 不可用（非必需）" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   [WARNING] Docker Compose 未安裝（非必需）" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Docker 狀態檢查完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "下一步: 執行以下命令下載 Kneron Toolchain" -ForegroundColor Green
Write-Host "  docker pull kneron/toolchain:latest" -ForegroundColor White
Write-Host ""

