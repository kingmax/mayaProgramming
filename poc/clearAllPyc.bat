@echo off

for /f %%i in ("%0") do set curpath=%%~dpi
cd /d %curpath%

::Attrib %curpath% -r

for %%a in (%curpath%*.pyc) do (
    Attrib %%a -r
    del %%a
)
@echo off

for /f "usebackq tokens=*" %%a in (`dir /b/s/a:d %curpath%`) do (

    for %%X in (%curpath%%%~nxa\*.pyc) do (
        Attrib %%X -r
        del %%X
    )
)
