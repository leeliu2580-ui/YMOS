$key = [System.Environment]::GetEnvironmentVariable("DASHSCOPE_API_KEY", "User")
if (-not $key) {
    $key = [System.Environment]::GetEnvironmentVariable("DASHSCOPE_API_KEY", "Machine")
}
if (-not $key) {
    $key = [System.Environment]::GetEnvironmentVariable("DASHSCOPE_API_KEY", "Process")
}

Write-Host "API Key found: $(if ($key) { 'YES' } else { 'NO' })"

$headers = @{
    "X-DashScope-Async" = "enable"
    "Authorization" = "Bearer $key"
    "Content-Type" = "application/json"
}

$body = Get-Content "D:\0_workspace\trae_2601\ymos\YMOS\temp_wan_body.json" -Raw -Encoding UTF8

Write-Host "Sending request to Wan2.6-t2v API..."

try {
    $response = Invoke-RestMethod -Uri "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" -Method Post -Headers $headers -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json" -TimeoutSec 60
    $response | ConvertTo-Json -Depth 10
} catch {
    $errMsg = $_.Exception.Message
    try {
        $errObj = $errMsg | ConvertFrom-Json
        $errObj | ConvertTo-Json -Depth 10
    } catch {
        Write-Host "Error: $errMsg"
    }
}
