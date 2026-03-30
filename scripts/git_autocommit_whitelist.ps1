param(
    [string]$Message = "Auto-commit tracked YMOS updates",
    [switch]$NoCommit
)

$ErrorActionPreference = 'Stop'
Set-Location -Path (Split-Path -Parent $PSScriptRoot)

$paths = @(
    'Eyes',
    'Brain',
    '持仓与关注',
    'skills',
    'memory',
    'MEMORY.md',
    'IDENTITY.md',
    'USER.md',
    'SOUL.md',
    'TOOLS.md',
    'HEARTBEAT.md',
    'test_tickflow.py',
    'test_tickflow_markets.py',
    'test_env_apis.py',
    'test_tushare_data_skill.py',
    'test_hype_external_apis.py',
    'probe_tushare_permissions.py',
    'ymos_data_test.py'
)

$excludePatterns = @(
    'output/',
    '.tools/',
    '.openclaw/',
    '.clawhub/',
    '__pycache__/',
    'node_modules/'
)

Write-Host '== YMOS whitelist git auto-commit ==' -ForegroundColor Cyan
Write-Host 'Repo:' (Get-Location)

foreach ($path in $paths) {
    if (Test-Path $path) {
        git add -- $path
    }
}

$status = git status --short
if (-not $status) {
    Write-Host 'No changes to commit.' -ForegroundColor Yellow
    exit 0
}

$filtered = @()
foreach ($line in $status) {
    $keep = $true
    foreach ($pattern in $excludePatterns) {
        if ($line -like "*$pattern*") {
            $keep = $false
            break
        }
    }
    if ($keep) { $filtered += $line }
}

if (-not $filtered -or $filtered.Count -eq 0) {
    Write-Host 'No whitelist changes to commit after filtering.' -ForegroundColor Yellow
    exit 0
}

Write-Host "Staged/eligible changes:" -ForegroundColor Green
$filtered | ForEach-Object { Write-Host $_ }

if ($NoCommit) {
    Write-Host 'NoCommit flag set; stopping before commit.' -ForegroundColor Yellow
    exit 0
}

git commit -m $Message
Write-Host 'Commit complete. Push manually when ready: git push' -ForegroundColor Green
