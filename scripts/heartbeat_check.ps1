# YMOS 执行计划心跳检查脚本
# 由 OpenClaw 自动创建，每小时执行一次

$ErrorActionPreference = 'Continue'
$logFile = "D:\7_AI\YMOS\logs\heartbeat.log"
$planFile = "D:\7_AI\YMOS\EXECUTION_PLAN.md"
$promptsDir = "D:\7_AI\YMOS\memory\prompts"
$outputDir = "D:\7_AI\YMOS\output\reports"

# 创建日志函数
function Write-Log($msg) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "$timestamp | $msg"
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Output $line
}

Write-Log "=== Heartbeat Check Started ==="

# 检查计划文件是否存在
if (-not (Test-Path $planFile)) {
    Write-Log "WARNING: EXECUTION_PLAN.md not found"
    exit 1
}

# 读取当前进度（从文档中提取 Day 信息）
$content = Get-Content $planFile -Raw -Encoding UTF8
if ($content -match "### Day (\d+)") {
    $currentDay = $matches[1]
    Write-Log "当前进度: Day $currentDay"
} else {
    Write-Log "WARNING: Cannot determine current day"
    $currentDay = "unknown"
}

# 检查 Prompt 版本
if (Test-Path $promptsDir) {
    $promptFiles = Get-ChildItem $promptsDir -Filter "*.md" -File
    Write-Log "已有 Prompt 版本: $($promptFiles.Count) 个"
    foreach ($f in $promptFiles) {
        Write-Log "  - $($f.Name)"
    }
} else {
    Write-Log "NOTE: prompts 目录尚不存在，正在初始化"
}

# 检查 output 目录
if (Test-Path $outputDir) {
    $reports = Get-ChildItem $outputDir -Filter "*.md" -File -ErrorAction SilentlyContinue
    Write-Log "已有报告: $($reports.Count) 个"
} else {
    Write-Log "NOTE: output/reports 目录尚不存在"
}

# Git 状态检查
$gitStatus = "D:\7_AI\YMOS\.git"
if (Test-Path $gitStatus) {
    Push-Location "D:\7_AI\YMOS"
    try {
        $status = git status --porcelain 2>&1
        if ($status) {
            Write-Log "Git 有未提交的更改:"
            $status | ForEach-Object { Write-Log "  $_" }
        } else {
            Write-Log "Git 工作区干净"
        }
        
        $branch = git branch --show-current 2>&1
        Write-Log "当前分支: $branch"
    }
    catch {
        Write-Log "Git 检查失败: $_"
    }
    finally {
        Pop-Location
    }
} else {
    Write-Log "NOTE: 尚未初始化 Git 仓库"
}

Write-Log "=== Heartbeat Check Completed ==="
Write-Output ""