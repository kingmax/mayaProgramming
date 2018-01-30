set render="C:\Program Files\Autodesk\Maya2016\bin\Render.exe"

set fileA="D:\alienbrainWork\AZT-17002-NKP\Production\project_Lincoln\3dmodels\motion_render.mb"

time /t
rem %render% -renderer "arnold" -proj "E:\myMaya\Lincoln\workspace.mel" %fileA%
%render% -renderer "arnold" -rd "E:\myMaya\Lincoln" %fileA%
time /t
pause
exit

set fileB="D:\alienbrainWork\AZT-17002-NKP\Production\project_Patrick\3dmodels\motion_render.mb"
%render% -renderer "arnold" -rd "E:\myMaya\Patrick" %fileB%

pause

