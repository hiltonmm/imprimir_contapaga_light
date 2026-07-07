import time
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def acessar_contas_pagas(navegador, tarefas):
    url_contas = "https://agenciavirtual.light.com.br/AGV_Comprovante_Conta_Paga_VW/Comprovante_Conta_Paga.aspx"
    
    erros_da_rodada = {} 
    
    try:
        print("Acessando área de faturas...")
        if navegador.current_url != url_contas:
            navegador.get(url_contas)
            time.sleep(5)
        
        for codigo, referencias in tarefas.items():
            if not referencias:
                continue
                
            print(f"\n{'='*55}")
            print(f"🔍 PROCESSANDO A INSTALAÇÃO: {codigo}")
            print(f"{'='*55}")
            
            erros_deste_codigo = [] 
            
            for ref in referencias:
                print(f"\n  -> Buscando referência: {ref}")
                try:
                    # 1. Encontra a sanfona (accordion)
                    xpath_instalacao = f"//span[text()='{codigo}']/ancestor::div[contains(@class, 'accordion-item-header')]"
                    div_instalacao = WebDriverWait(navegador, 15).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_instalacao))
                    )
                    navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", div_instalacao)
                    time.sleep(1)
                    
                    # Verifica se a sanfona está fechada. Se estiver, clica para abrir.
                    if div_instalacao.get_attribute("aria-expanded") != "true":
                        div_instalacao.click()
                        print("  ✅ Sanfona expandida. Aguardando renderização do servidor...")
                    else:
                        print("  ✅ Sanfona já estava expandida.")
                    
                    # A pausa raiz que sabemos que funciona para o OutSystems carregar a tabela
                    time.sleep(5)
                    
                    # 2. Localiza a fatura específica
                    xpath_linha = f"//*[contains(text(), '{ref}')]/ancestor::div[contains(@class, 'row') and contains(@class, 'align-items-center')]"
                    linha_fatura = WebDriverWait(navegador, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpath_linha))
                    )
                    
                    # 3. Dispara o download nativo
                    xpath_link = ".//div[contains(@class, 'd-lg-block')]//a[contains(@href, '__doPostBack')]"
                    link_elemento = linha_fatura.find_element(By.XPATH, xpath_link)
                    evento_js = link_elemento.get_attribute("href")
                    
                    janela_principal = navegador.current_window_handle
                    navegador.execute_script(evento_js)
                    print(f"  ✅ PostBack disparado para {ref}!")
                    
                    # 4. Controle de abas
                    print("  ⏳ Aguardando 7 segundos para conclusão do download...")
                    time.sleep(7)
                    
                    abas_abertas = navegador.window_handles
                    if len(abas_abertas) > 1:
                        for aba in abas_abertas:
                            if aba != janela_principal:
                                try:
                                    navegador.switch_to.window(aba)
                                    navegador.close()
                                except:
                                    pass
                    
                    navegador.switch_to.window(janela_principal)
                    print("  ✅ Concluído com sucesso.")
                    time.sleep(3)

                except Exception as e:
                    print(f"  ⚠️ Falha ao processar {ref}.")
                    print(f"  Detalhe do erro: {type(e).__name__} - Não foi possível encontrar o elemento na tela.")
                    erros_deste_codigo.append(ref) 
                    
                    try:
                        if len(navegador.window_handles) > 0:
                            navegador.switch_to.window(navegador.window_handles[0])
                    except:
                        pass
                    continue 

            if erros_deste_codigo:
                erros_da_rodada[codigo] = erros_deste_codigo

        return erros_da_rodada

    except Exception as e:
        print("\n❌ ERRO GRAVE NO MÓDULO DE FATURAS:")
        traceback.print_exc()
        return tarefas