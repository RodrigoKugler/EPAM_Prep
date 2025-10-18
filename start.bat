@echo off
chcp 65001 >nul
echo ========================================
echo   EPAM SQL Practice Environment
echo ========================================
echo.
echo Verificando ambiente...
echo.

if not exist epam_practice.db (
    echo Database nao encontrado. Criando...
    python setup_database.py
    echo.
)

echo Iniciando Quick Start...
echo.
python quick_start.py

pause


