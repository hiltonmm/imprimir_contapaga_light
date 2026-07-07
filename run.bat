@echo off
echo ==========================================
echo Iniciando o Robo de Faturas Light...
echo ==========================================
echo.

:: Ativa o ambiente virtual para garantir que as bibliotecas sejam encontradas
call venv\Scripts\activate.bat

:: Roda o orquestrador principal
python main.py

echo.
pause