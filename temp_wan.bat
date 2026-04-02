@echo off
for /f "tokens=2* delims== " %%A in ('powershell -Command "[System.Environment]::GetEnvironmentVariable('DASHSCOPE_API_KEY','User')"') do set KEY=%%A
for /f "tokens=2* delims== " %%A in ('powershell -Command "if (-not '%KEY%') { [System.Environment]::GetEnvironmentVariable('DASHSCOPE_API_KEY','Machine') }"') do if not defined KEY set KEY=%%A

curl.exe -L https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis ^
  -H "X-DashScope-Async: enable" ^
  -H "Authorization: Bearer %KEY%" ^
  -H "Content-Type: application/json" ^
  -d @temp_wan_body.json
