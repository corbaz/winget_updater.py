@echo off
echo ====================================
echo   Compilando win-upgrade.exe
echo ====================================
echo.

REM Limpiar compilaciones anteriores
if exist "dist" rd /s /q dist
if exist "build" rd /s /q build
if exist "win-upgrade.spec" del /q win-upgrade.spec

echo Limpieza completada.
echo.
echo Compilando con PyInstaller...
echo.

REM Compilar con PyInstaller
pyinstaller --onefile --windowed --name="win-upgrade" ^
    --icon=win-upgrade.ico ^
    --uac-admin ^
    --clean ^
    --add-data="win-upgrade.ico;." ^
    winget_updater.py

echo.
echo ====================================
if exist "dist\win-upgrade.exe" (
    echo   EXITO: Ejecutable creado
    echo   Ubicacion: dist\win-upgrade.exe
    for %%A in ("dist\win-upgrade.exe") do echo   Tamano: %%~zA bytes
) else (
    echo   ERROR: No se pudo crear el ejecutable
)
echo ====================================
echo.

pause

