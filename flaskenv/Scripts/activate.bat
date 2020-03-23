@echo off

rem This file is UTF-8 encoded, so we need to update the current code page while executing it
<<<<<<< HEAD
<<<<<<< HEAD
for /f "tokens=2 delims=:" %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set "_OLD_CODEPAGE=%%a"
=======
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
>>>>>>> 91a64aee0455ce9262321357b25f9663ca67a86e
=======
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
>>>>>>> 91a64aee0455ce9262321357b25f9663ca67a86e
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)

<<<<<<< HEAD
<<<<<<< HEAD
set "VIRTUAL_ENV=D:\app\flaskenv"

if not defined PROMPT (
    set "PROMPT=$P$G"
)

if defined _OLD_VIRTUAL_PROMPT (
    set "PROMPT=%_OLD_VIRTUAL_PROMPT%"
)

if defined _OLD_VIRTUAL_PYTHONHOME (
    set "PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%"
)

set "_OLD_VIRTUAL_PROMPT=%PROMPT%"
set "PROMPT=(flaskenv) %PROMPT%"

if defined PYTHONHOME (
    set "_OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%"
    set PYTHONHOME=
)

if defined _OLD_VIRTUAL_PATH (
    set "PATH=%_OLD_VIRTUAL_PATH%"
) else (
    set "_OLD_VIRTUAL_PATH=%PATH%"
)

set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
=======
=======
>>>>>>> 91a64aee0455ce9262321357b25f9663ca67a86e
set VIRTUAL_ENV=C:\Users\JIANG WANYING\Desktop\Group11-online-system-for-the-healing-paws-veterinary-hospita\flaskenv

if not defined PROMPT set PROMPT=$P$G

if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%

set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(flaskenv) %PROMPT%

if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
<<<<<<< HEAD
>>>>>>> 91a64aee0455ce9262321357b25f9663ca67a86e
=======
>>>>>>> 91a64aee0455ce9262321357b25f9663ca67a86e

:END
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
<<<<<<< HEAD
<<<<<<< HEAD
    set "_OLD_CODEPAGE="
=======
    set _OLD_CODEPAGE=
>>>>>>> 91a64aee0455ce9262321357b25f9663ca67a86e
=======
    set _OLD_CODEPAGE=
>>>>>>> 91a64aee0455ce9262321357b25f9663ca67a86e
)
