@echo off
echo ====================================
echo   Compilando WingetUpdater.exe
echo ====================================
echo.

REM Limpiar compilaciones anteriores
if exist "dist" rd /s /q dist
if exist "build" rd /s /q build
if exist "WingetUpdater.spec" del /q WingetUpdater.spec

echo Limpieza completada.
echo.
echo Compilando con PyInstaller...
echo.

REM Compilar con PyInstaller
pyinstaller --onefile --windowed --name="WingetUpdater" ^
    --uac-admin ^
    --version-file=version.txt ^
    --clean ^
    winget_updater.py

echo.
echo ====================================
if exist "dist\WingetUpdater.exe" (
    echo   EXITO: Ejecutable creado
    echo   Ubicacion: dist\WingetUpdater.exe
    for %%A in ("dist\WingetUpdater.exe") do echo   Tamano: %%~zA bytes
) else (
    echo   ERROR: No se pudo crear el ejecutable
)
echo ====================================
echo.

pause

