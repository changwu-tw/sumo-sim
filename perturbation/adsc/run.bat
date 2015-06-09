pause
for /r %%f in (*.dot) do (
sfdp -x -Goverlap=prism -Tpng %%~nxf > %%~nxf.png
)
pause