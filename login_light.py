import os
import time
import random
import traceback
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para simular digitação humana
def digitar_como_humano(elemento, texto):
    for letra in texto:
        elemento.send_keys(letra)
        # Pausa aleatória entre 0.05 e 0.25 segundos por tecla
        time.sleep(random.uniform(0.05, 0.25))

def efetuar_login(navegador):
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_env = os.path.join(caminho_atual, '.env')
    load_dotenv(caminho_env)

    EMAIL = os.getenv("LIGHT_EMAIL")
    SENHA = os.getenv("LIGHT_SENHA")

    if not EMAIL or not SENHA:
        print("❌ ERRO: O arquivo .env não foi encontrado ou está vazio!")
        return False

    url_login = "https://agenciavirtual.light.com.br/Portal/Login.aspx"
    
    try:
        print(f"Acessando a página de login: {url_login}")
        navegador.get(url_login)
        
        # Pausa humana antes de começar a digitar
        time.sleep(random.uniform(1.5, 3.0))

        print("Procurando campo de e-mail/CPF...")
        campo_email = WebDriverWait(navegador, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Informe seu CPF, CNPJ ou E-mail']"))
        )
        print("Digitando e-mail...")
        digitar_como_humano(campo_email, EMAIL)
        
        # Pausa natural entre pular do e-mail para a senha
        time.sleep(random.uniform(0.5, 1.2))

        print("Procurando campo de senha...")
        campo_senha = navegador.find_element(By.XPATH, "//input[@placeholder='Informe sua senha']")
        print("Digitando senha...")
        digitar_como_humano(campo_senha, SENHA)

        # Pausa antes de clicar no botão
        time.sleep(random.uniform(0.8, 1.5))

        print("Clicando no botão de login...")
        botao_entrar = navegador.find_element(By.XPATH, "//input[@value='ENTRAR']")
        botao_entrar.click()

        print("✅ Login enviado!")
        return True

    except Exception as e:
        print("\n❌ ERRO FATAL NO LOGIN:")
        print("-" * 50)
        traceback.print_exc()
        print("-" * 50)
        return False