Remove-Item -Path 'D:\0_workspace\trae_2601\ymos\YMOS\_fetch_v2.ps1' -Force -ErrorAction SilentlyContinue
Remove-Item -Path 'D:\0_workspace\trae_2601\ymos\YMOS\_check_taco.py' -Force -ErrorAction SilentlyContinue
Set-Location 'D:\0_workspace\trae_2601\ymos\YMOS'
git add -A
git commit -m "fix(Eyes): Trump TACO ceasefire - update Iran war market insight"
git push
