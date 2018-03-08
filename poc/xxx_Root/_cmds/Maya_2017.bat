@echo off
pushd %~dp0

set MAYA_UI_LANGUAGE=en_US

set MAYA_SHELF_PATH=%CD%\..\Maya\2017\prefs\shelves
set MAYA_PLUG_IN_PATH=%CD%\..\Maya\2017\plug-ins
set MAYA_MODULE_PATH=%CD%\..\Maya\2017\modules
set MAYA_SCRIPT_PATH=%CD%\..\Maya\2017\scripts
set XBMLANGPATH=%CD%\..\Maya\2017\icons

set _LIBS=%CD%\..\_libs
set PYTHONPATH=%_LIBS%;%MAYA_SCRIPT_PATH%;%PYTHONPATH%;

set MAYAEXE="C:\Program Files\Autodesk\Maya2017\bin\maya.exe"
rem set LOGFILE=%CD%\..\Maya\2017\maya2017.log

rem del /f /q %LOGFILE%
echo starting %MAYAEXE%
%MAYAEXE%
rem %MAYAEXE% -log %LOGFILE%

popd