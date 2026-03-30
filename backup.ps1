$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

git add .
$hasChanges = $true
try {
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { $hasChanges = $false }
} catch {
    if ($LASTEXITCODE -eq 0) { $hasChanges = $false } else { $hasChanges = $true }
}

if ($hasChanges) {
    $date = Get-Date -Format 'yyyy-MM-dd'
    git commit -m "workspace backup $date"
} else {
    Write-Host 'No changes to commit'
}

git push origin main
Write-Host 'BACKUP_OK'
