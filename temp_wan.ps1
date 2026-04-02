$apiKey = [System.Environment]::GetEnvironmentVariable("DASHSCOPE_API_KEY","User")
if (-not $apiKey) { $apiKey = [System.Environment]::GetEnvironmentVariable("DASHSCOPE_API_KEY","Machine") }
if (-not $apiKey) { $apiKey = [System.Environment]::GetEnvironmentVariable("DASHSCOPE_API_KEY","Process") }

$headers = @{
    "X-DashScope-Async" = "enable"
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

$body = Get-Content "D:/0_workspace/trae_2601/ymos/YMOS/temp_wan_body.json" -Raw

$response = Invoke-RestMethod -Uri "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" -Method Post -Headers $headers -Body $body -TimeoutSec 60

$response | ConvertTo-Json -Depth 10
