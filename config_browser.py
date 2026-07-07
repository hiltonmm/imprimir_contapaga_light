import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def iniciar_navegador():
    print("Iniciando o navegador em modo furtivo...")
    servico = Service(ChromeDriverManager().install())
    opcoes = webdriver.ChromeOptions()
    
    opcoes.add_argument("--start-maximized")
    
    # --- MODO FURTIVO ---
    opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])
    opcoes.add_experimental_option('useAutomationExtension', False)
    
    # --- CONFIGURAÇÃO DE DOWNLOAD AUTOMÁTICO ---
    # Cria uma pasta chamada 'Faturas_Baixadas' na mesma pasta do projeto
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_downloads = os.path.join(caminho_atual, 'Faturas_Baixadas')
    if not os.path.exists(pasta_downloads):
        os.makedirs(pasta_downloads)

    prefs = {
        "credentials_enable_service": False, 
        "profile.password_manager_enabled": False,
        "download.default_directory": pasta_downloads, # Salva tudo nesta pasta
        "download.prompt_for_download": False,         # Não pergunta onde salvar (salva direto)
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,    # PROÍBE o Chrome de abrir o PDF em abas (força o download)
        "profile.default_content_settings.popups": 0   # Libera pop-ups de download
    }
    opcoes.add_experimental_option("prefs", prefs)

    navegador = webdriver.Chrome(service=servico, options=opcoes)
    
    # Remove a bandeira de robô
    navegador.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    
    return navegador