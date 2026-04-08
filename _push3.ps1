Set-Location 'D:\0_workspace\trae_2601\ymos\YMOS'
Remove-Item -Path '_crypto_mon.ps1' -Force -ErrorAction SilentlyContinue
git add -A
git commit -m "feat(memory): 2026-04-08 日记 - ETH>5%异常波动 + Trump TACO事件记录"
git push
