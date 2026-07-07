@echo off
echo ==========================================
echo Instalando o Robo de Faturas Light...
echo ==========================================
echo.

echo 1. Criando ambiente virtual (venv)...
python -m venv venv

echo 2. Ativando o ambiente e instalando dependencias...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 3. Verificando arquivo de configuracao...
if not exist .env (
    copy .env.example .env
    echo [AVISO] Arquivo .env criado! Lembre-se de edita-lo e colocar seu login e senha.
) else (
    echo [OK] Arquivo .env ja existe.
)

echo.
echo ==========================================
echo Instalacao concluida com sucesso!
echo ==========================================
pause