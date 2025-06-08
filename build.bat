@echo off
setlocal enabledelayedexpansion

echo.
echo === Starting Dahitter build (Nuitka + standalone) ===
echo.

:: === Clean up old dist directory ===
if exist dist (
    echo Removing old dist folder...
    rmdir /s /q dist
)

:: === Convert icon path to absolute ===
set ICON=src\dahitter\icons\icon.ico
for %%I in (%ICON%) do set ICON_ABS=%%~fI

:: === Build main Dahitter GUI ===
echo.
echo === Building Dahitter GUI (main.py) ===
python -m nuitka ^
  --follow-imports ^
  --enable-plugin=pyside6 ^
  --windows-console-mode=disable ^
  --windows-icon-from-ico="%ICON_ABS%" ^
  --standalone ^
  --output-filename=Dahitter.exe ^
  --output-dir=dist ^
  --include-data-files=src/dahitter/icons/*.ico=src/dahitter/icons/ ^
  --include-data-files=src/dahitter/icons/*.svg=src/dahitter/icons/ ^
  --remove-output ^
  main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Dahitter build failed.
    exit /b 1
)

:: === Build tile capture tool ===
echo.
echo === Building TileCaptureTool (make_tile_templates.py) ===
python -m nuitka ^
  --follow-imports ^
  --windows-icon-from-ico="%ICON_ABS%" ^
  --standalone ^
  --output-filename=TileCaptureTool.exe ^
  --output-dir=dist ^
  --remove-output ^
  tools\make_tile_templates.py

if errorlevel 1 (
    echo.
    echo [ERROR] TileCaptureTool build failed.
    exit /b 1
)

:: === Copy template images (excluding .gitkeep) ===
echo.
echo Copying templates (excluding .gitkeep)...

set SRC=templates
set DEST=dist\main.dist\templates

for /d %%D in (%SRC%\*) do (
    xcopy "%%D\*.png" "%DEST%\%%~nxD\" /E /I /Y >nul
)

:: === Rename build output directories ===
ren dist\main.dist DahitterCore
ren dist\make_tile_templates.dist TileCaptureToolCore

:: === Done ===
echo.
echo === Build completed (Nuitka + standalone) ===
echo [Main Executable]:     dist\DahitterCore\Dahitter.exe
echo [Capture Tool]:        dist\TileCaptureToolCore\TileCaptureTool.exe
echo.
pause
