Set-Location 'D:\0_workspace\trae_2601\ymos\YMOS'
Remove-Item -Path '_cleanup.ps1' -Force -ErrorAction SilentlyContinue
git add -A
git commit -m "feat(Eyes): 投资雷达 2026-04-08 + 更新持仓/Watchlist状态机价格"
git push
