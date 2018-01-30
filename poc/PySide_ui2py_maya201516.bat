rem echo ui2py_maya2017(PySide2) ui-file, will generate ui-file.ui.py
rem "C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2017\bin\pyside2-uic" -o %1.py %1

rem "C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2017\bin\pyside2-uic" -o snapUV2GridByTextureSize_ui.py snapUV2GridByTextureSize.ui
"C:\Program Files\Autodesk\Maya2015\bin\mayapy.exe" "C:\Program Files\Autodesk\Maya2015\bin\pyside-uic" -o %1.py %1
pause