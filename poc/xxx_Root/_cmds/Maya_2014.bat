@echo off
pushd %~dp0

set _APP=Maya
set _VER=2014

set QT_PREFERRED_BINDING=PySide2;PySide

set MAYA_UI_LANGUAGE=en_US

set MAYA_SHELF_PATH=%CD%\..\%_APP%\%_VER%\prefs\shelves
set MAYA_PLUG_IN_PATH=%CD%\..\%_APP%\%_VER%\plug-ins
set MAYA_MODULE_PATH=%CD%\..\%_APP%\%_VER%\modules
set MAYA_SCRIPT_PATH=%CD%\..\%_APP%\%_VER%\scripts
set XBMLANGPATH=%CD%\..\%_APP%\%_VER%\icons

set _LIBS=%CD%\..\_libs
set PYTHONPATH=%_LIBS%;%MAYA_SCRIPT_PATH%;%PYTHONPATH%;

set MAYAEXE="C:\Program Files\Autodesk\Maya2014\bin\maya.exe"
set LOGFILE=%CD%\..\%_APP%\%_VER%\%_APP%%_VER%.log

del /f /q %LOGFILE%
echo starting %MAYAEXE%
rem %MAYAEXE%
%MAYAEXE% -log %LOGFILE%

popd