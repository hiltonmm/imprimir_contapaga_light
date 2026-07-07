import tkinter as tk
from tkinter import ttk, messagebox
import datetime

def solicitar_referencias():
    # 1. Cálculo automático do mês e ano anteriores
    hoje = datetime.date.today()
    # Pega o primeiro dia do mês atual e subtrai 1 dia para cair no último dia do mês passado
    primeiro_dia_mes_atual = hoje.replace(day=1)
    ultimo_dia_mes_passado = primeiro_dia_mes_atual - datetime.timedelta(days=1)
    
    mes_padrao_idx = ultimo_dia_mes_passado.month - 1  # -1 pois a lista começa no índice 0
    ano_padrao = str(ultimo_dia_mes_passado.year)
    
    # Formatação exata exigida pelo site da Light
    lista_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    referencias_selecionadas = []

    # --- Funções dos Botões da Interface ---
    def adicionar():
        mes = combo_mes.get()
        ano = entry_ano.get()
        
        if not mes or not ano.isdigit() or len(ano) != 4:
            messagebox.showwarning("Atenção", "Preencha um ano válido (4 dígitos numéricos).")
            return
        
        ref = f"{mes}/{ano}"
        if ref not in referencias_selecionadas:
            referencias_selecionadas.append(ref)
            listbox.insert(tk.END, ref)

    def remover():
        selecionado = listbox.curselection()
        if selecionado:
            idx = selecionado[0]
            listbox.delete(idx)
            referencias_selecionadas.pop(idx)

    def iniciar():
        if not referencias_selecionadas:
            messagebox.showwarning("Atenção", "Adicione pelo menos uma referência antes de iniciar!")
            return
        janela.destroy() # Fecha a janela e permite que o código Python continue

    # --- Construção da Janela (UI) ---
    janela = tk.Tk()
    janela.title("Automação Light - Faturas")
    janela.geometry("320x380")
    
    # Centralizar a janela na tela
    janela.eval('tk::PlaceWindow . center')

    tk.Label(janela, text="Selecione o Mês:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
    combo_mes = ttk.Combobox(janela, values=lista_meses, state="readonly", width=15)
    combo_mes.current(mes_padrao_idx)
    combo_mes.pack()

    tk.Label(janela, text="Ano (4 dígitos):", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    entry_ano = tk.Entry(janela, width=18)
    entry_ano.insert(0, ano_padrao)
    entry_ano.pack()

    # Frame para agrupar os botões de ação
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=15)
    tk.Button(frame_botoes, text="➕ Adicionar", command=adicionar).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="➖ Remover", command=remover).pack(side=tk.LEFT, padx=5)

    tk.Label(janela, text="Faturas que serão baixadas:", font=("Arial", 9)).pack(pady=(5, 0))
    
    # Lista visual das referências
    listbox = tk.Listbox(janela, height=6, width=25)
    listbox.pack()
    
    # Insere a data padrão automaticamente na lista para facilitar
    ref_padrao = f"{lista_meses[mes_padrao_idx]}/{ano_padrao}"
    referencias_selecionadas.append(ref_padrao)
    listbox.insert(tk.END, ref_padrao)

    # Botão de iniciar
    tk.Button(janela, text="🚀 INICIAR AUTOMAÇÃO", command=iniciar, bg="#28a745", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

    # Mantém a janela aberta
    janela.mainloop()
    
    # Quando a janela for fechada (pelo botão Iniciar), retorna a lista para o main.py
    return referencias_selecionadas