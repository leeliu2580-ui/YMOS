@echo off
cd /d %~dp0..
powershell -ExecutionPolicy Bypass -File scripts\git_autocommit_whitelist.ps1 %*
