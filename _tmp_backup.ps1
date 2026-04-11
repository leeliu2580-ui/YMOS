Set-Location 'D:\0_workspace\trae_2601\ymos\YMOS'
Write-Host "Running backup..."
$result = & '.\backup.ps1' 2>&1
Write-Host $result
Write-Host "EXIT: $LASTEXITCODE"
