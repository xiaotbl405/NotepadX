@echo off
setlocal enabledelayedexpansion

:: 编译依赖的子程序
pyinstaller --onefile --uac-admin --noconsole --python-option pyinstaller batoexe.py
pyinstaller --onefile --uac-admin --noconsole --python-option pyinstaller vbstoexe.py

:: 等待子程序编译完成
timeout /t 5 /nobreak >nul
pause
:: 打包主程序（包含子程序作为资源）
pyinstaller ^
--onefile ^
--uac-admin ^
--noconsole ^
--add-data "batoexe.exe;." ^
--add-data "vbstoexe.exe;." ^
main.py

pause
