@echo off
REM YMOS 执行计划心跳启动器
REM 运行此批处理文件开始每小时检查

echo 启动 YMOS 心跳监控...
echo 关闭此窗口可停止监控

:loop
    powershell -ExecutionPolicy Bypass -File "D:\7_AI\YMOS\scripts\heartbeat_check.ps1"
    echo ---
    echo 下次检查: 1小时后 (Ctrl+C 停止)
    timeout /t 3600 /nobreak >nul
goto loop