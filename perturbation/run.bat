for /R %i in (*.dot) do sfdp -x -Goverlap=prism -Tpng %i > *.png
pause
cmd.exe