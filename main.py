import json
import os
import glob
import time
import tkinter as tk
from tkinter import messagebox
from config_browser import iniciar_navegador
from login_light import efetuar_login
from faturas_light import acessar_contas_pagas
from interface import solicitar_referencias

def limpar_pasta_downloads():
    print("🧹 Limpando a pasta de downloads antiga...")
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    pasta = os.path.join(caminho_atual, 'Faturas_Baixadas')
    
    if os.path.exists(pasta):
        arquivos = glob.glob(os.path.join(pasta, '*'))
        for arquivo in arquivos:
            try:
                os.remove(arquivo)
            except Exception as e:
                print(f"  ⚠️ Não foi possível apagar {arquivo}: {e}")
    else:
        os.makedirs(pasta)

def imprimir_faturas():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    pasta = os.path.join(caminho_atual, 'Faturas_Baixadas')
    arquivos = glob.glob(os.path.join(pasta, '*.pdf'))
    
    if not arquivos:
        print("❌ Nenhum arquivo PDF encontrado para imprimir.")
        return
        
    print(f"\n🖨️ Enviando {len(arquivos)} faturas para a impressora padrão...")
    for arquivo in arquivos:
        try:
            os.startfile(arquivo, "print")
            time.sleep(3) 
        except Exception as e:
            print(f"  ❌ Erro ao imprimir {arquivo}: {e}")
    print("✅ Envio para a impressora concluído!")

def carregar_instalacoes():
    caminho_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_json = os.path.join(caminho_atual, 'instalacoes.json')
    try:
        with open(caminho_json, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            return dados.get("instalacoes", [])
    except Exception:
        return []

def main():
    codigos_instalacao = carregar_instalacoes()
    if not codigos_instalacao:
        return
        
    referencias = solicitar_referencias()
    if not referencias:
        return
        
    limpar_pasta_downloads()

    tarefas_pendentes = {codigo: referencias[:] for codigo in codigos_instalacao}
    
    root = tk.Tk()
    root.withdraw()
    
    navegador = iniciar_navegador()
    
    try:
        if efetuar_login(navegador):
            while tarefas_pendentes:
                print("\nOrquestrador: Iniciando lote de extração...")
                erros = acessar_contas_pagas(navegador, tarefas_pendentes)
                
                if not erros:
                    print("\n✅ 100% de sucesso! Todas as faturas foram baixadas.")
                    messagebox.showinfo("Sucesso", "Todas as faturas foram baixadas com sucesso!")
                    break 
                else:
                    msg_erro = "As seguintes faturas falharam ou o site engasgou:\n\n"
                    for cod, refs in erros.items():
                        msg_erro += f"Instalação {cod}: {', '.join(refs)}\n"
                    msg_erro += "\nDeseja tentar baixar essas faturas novamente agora?"
                    
                    tentar_novamente = messagebox.askyesno("Erros Encontrados", msg_erro)
                    
                    if tentar_novamente:
                        tarefas_pendentes = erros 
                        print("\n🔄 Reiniciando robô apenas para as faturas com falha...")
                        navegador.refresh()
                        time.sleep(5)
                    else:
                        print("\n⚠️ Usuário optou por ignorar as falhas restantes.")
                        break 
            
            imprimir_agora = messagebox.askyesno("Impressão", "Processo finalizado.\n\nDeseja enviar todas as faturas baixadas para a impressora padrão?")
            if imprimir_agora:
                imprimir_faturas()
                
            print("\n🎉 Automação finalizada! Fechando o sistema...")
            
        else:
            print("Orquestrador: Interrompendo automação pois o login falhou.")
            
    finally:
        print("Encerrando a automação e fechando o navegador.")
        navegador.quit()
        root.destroy() 

if __name__ == "__main__":
    main()