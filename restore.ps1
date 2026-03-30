$ErrorActionPreference = 'Stop'

param(
    [string]$RepoUrl = 'https://github.com/leeliu2580-ui/YMOS.git',
    [string]$TargetDir = 'D:\0_workspace\trae_2601\ymos\YMOS',
    [switch]$SkipClone,
    [switch]$RunBackupCheck
)

function Write-Step($msg) {
    Write-Host "[STEP] $msg" -ForegroundColor Cyan
}

function Write-Ok($msg) {
    Write-Host "[OK] $msg" -ForegroundColor Green
}

function Write-WarnEx($msg) {
    Write-Host "[WARN] $msg" -ForegroundColor Yellow
}

Write-Step 'Starting YMOS recovery bootstrap'

if (-not $SkipClone) {
    if (Test-Path $TargetDir) {
        Write-WarnEx "TargetDir already exists: $TargetDir"
        Write-WarnEx 'Skipping clone to avoid overwriting existing files.'
    } else {
        $parent = Split-Path $TargetDir -Parent
        if (-not (Test-Path $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        Write-Step "Cloning repository from $RepoUrl"
        git clone $RepoUrl $TargetDir
        Write-Ok 'Clone complete'
    }
}

if (-not (Test-Path $TargetDir)) {
    throw "TargetDir does not exist: $TargetDir"
}

Set-Location $TargetDir
Write-Step "Working directory: $TargetDir"

Write-Step 'Checking git remote and branch'
git remote -v
git branch --show-current

Write-Step 'Checking key files'
$required = @(
    'AGENTS.md',
    'SOUL.md',
    'TOOLS.md',
    'MEMORY.md',
    'HEARTBEAT.md',
    'backup.ps1',
    'backup.sh',
    'docs\README-重生指南.md',
    'docs\README-重生检查清单.md'
)

$missing = @()
foreach ($path in $required) {
    if (Test-Path $path) {
        Write-Ok "$path"
    } else {
        $missing += $path
        Write-WarnEx "Missing: $path"
    }
}

Write-Step 'Checking local-only directories that may need manual restoration'
$localOnly = @(
    '.tools',
    '.openclaw',
    '.clawhub',
    'output',
    'skills\cmc-official'
)
foreach ($path in $localOnly) {
    if (Test-Path $path) {
        Write-Ok "Present: $path"
    } else {
        Write-WarnEx "Not present (may be normal, restore manually if needed): $path"
    }
}

if ($RunBackupCheck) {
    Write-Step 'Running backup check via backup.ps1'
    if (Test-Path '.\backup.ps1') {
        & .\backup.ps1
    } else {
        Write-WarnEx 'backup.ps1 not found, skipping backup check'
    }
}

if ($missing.Count -gt 0) {
    Write-WarnEx 'Recovery bootstrap finished with missing core files:'
    $missing | ForEach-Object { Write-WarnEx $_ }
    exit 1
}

Write-Ok 'Recovery bootstrap finished'
Write-Host 'Next steps:' -ForegroundColor Cyan
Write-Host '- Restore local-only directories if your workflow needs them' -ForegroundColor White
Write-Host '- Reinstall project-specific tools and runtimes' -ForegroundColor White
Write-Host '- Run ./backup.ps1 to verify backup path' -ForegroundColor White
