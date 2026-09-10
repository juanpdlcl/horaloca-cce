# Escribe tools/control-remoto.cmd con saltos CRLF y diagnóstico ampliado
import os
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'control-remoto.cmd')
lineas = [
    r'@echo off',
    r'title Claude Remote Control - Hora Loca CCE',
    r'set "CLAUDE=C:\Users\EQUIPO\claude-cli\claude.cmd"',
    r'set "PATH=%APPDATA%\npm;C:\Program Files\nodejs;%PATH%"',
    r'cd /d "%~dp0..\.."',
    r'dir "%USERPROFILE%\.claude.json" >> "%TEMP%\claude-rc-pre.txt" 2>&1',
    r'findstr /c:"horaloca-cce" "%USERPROFILE%\.claude.json" >> "%TEMP%\claude-rc-pre.txt" 2>&1',
    r'set "LOGD=%TEMP%\claude-rc"',
    r'if not exist "%LOGD%" mkdir "%LOGD%"',
    r'echo [diag] %DATE% %TIME% > "%LOGD%\diag.txt"',
    r'echo CLAUDE=%CLAUDE% >> "%LOGD%\diag.txt"',
    r'echo APPDATA=%APPDATA% >> "%LOGD%\diag.txt"',
    r'echo CD=%CD% >> "%LOGD%\diag.txt"',
    r'if exist "%CLAUDE%" (echo shim existe >> "%LOGD%\diag.txt") else (echo shim NO existe >> "%LOGD%\diag.txt")',
    r'echo PATH=%PATH% >> "%LOGD%\diag.txt"',
    r'call "%CLAUDE%" --version >> "%LOGD%\diag.txt" 2>&1',
    r'echo.',
    r'echo  ============================================================',
    r'echo   CONTROL REMOTO DE CLAUDE CODE  -  Hora Loca CCE',
    r'echo   Deja esta ventana abierta. En el telefono: app Claude ^> Code',
    r'echo  ============================================================',
    r'echo.',
    r'call "%CLAUDE%" remote-control 2> "%LOGD%\stderr.txt"',
    r'echo [fin] codigo %ERRORLEVEL% >> "%LOGD%\diag.txt"',
    r'echo.',
    r'echo  (La sesion de control remoto termino.)',
    r'pause',
]
open(p, 'w', encoding='ascii', newline='\r\n').write('\n'.join(lineas) + '\n')
print('launcher escrito (CRLF)')
