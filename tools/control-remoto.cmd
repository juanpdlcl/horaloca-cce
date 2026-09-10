@echo off
title Claude Remote Control - Hora Loca CCE
set "CLAUDE=C:\Users\EQUIPO\claude-cli\claude.cmd"
set "PATH=%APPDATA%\npm;C:\Program Files\nodejs;%PATH%"
cd /d "%~dp0..\.."
dir "%USERPROFILE%\.claude.json" >> "%TEMP%\claude-rc-pre.txt" 2>&1
findstr /c:"horaloca-cce" "%USERPROFILE%\.claude.json" >> "%TEMP%\claude-rc-pre.txt" 2>&1
set "LOGD=%TEMP%\claude-rc"
if not exist "%LOGD%" mkdir "%LOGD%"
echo [diag] %DATE% %TIME% > "%LOGD%\diag.txt"
echo CLAUDE=%CLAUDE% >> "%LOGD%\diag.txt"
echo APPDATA=%APPDATA% >> "%LOGD%\diag.txt"
echo CD=%CD% >> "%LOGD%\diag.txt"
if exist "%CLAUDE%" (echo shim existe >> "%LOGD%\diag.txt") else (echo shim NO existe >> "%LOGD%\diag.txt")
echo PATH=%PATH% >> "%LOGD%\diag.txt"
call "%CLAUDE%" --version >> "%LOGD%\diag.txt" 2>&1
echo.
echo  ============================================================
echo   CONTROL REMOTO DE CLAUDE CODE  -  Hora Loca CCE
echo   Deja esta ventana abierta. En el telefono: app Claude ^> Code
echo  ============================================================
echo.
call "%CLAUDE%" remote-control 2> "%LOGD%\stderr.txt"
echo [fin] codigo %ERRORLEVEL% >> "%LOGD%\diag.txt"
echo.
echo  (La sesion de control remoto termino.)
pause
