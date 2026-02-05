@echo off
REM Script pour lancer la conversion des images en base64

echo ========================================
echo Conversion des images en base64
echo ========================================
echo.

REM Essayer différentes commandes Python
if exist "python.exe" (
    python.exe convertir-images-base64.py
    goto :fin
)

if exist "python3.exe" (
    python3.exe convertir-images-base64.py
    goto :fin
)

py -3 convertir-images-base64.py 2>nul
if %errorlevel% == 0 goto :fin

py convertir-images-base64.py 2>nul
if %errorlevel% == 0 goto :fin

echo.
echo ========================================
echo ERREUR : Python introuvable
echo ========================================
echo.
echo Veuillez installer Python depuis :
echo https://www.python.org/downloads/
echo.
echo Ou consultez INSTALLATION_PYTHON.md pour plus d'informations.
echo.
pause
exit /b 1

:fin
echo.
echo ========================================
echo Conversion terminee
echo ========================================
echo.
pause
