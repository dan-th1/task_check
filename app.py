import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os

# Arquivo onde salva as tarefas
ARQUIVO = "tarefas.json"

# Carrega tarefas salvas
def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Salva tarefas
def salvar_tarefas(tarefas):
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=2)

# Janela principal
janela = tk.Tk()
janela.title("Rastreador de Tarefas")
janela.geometry("500x400")

# Entrada de tarefa
frame_entrada = tk.Frame(janela)
frame_entrada.pack(pady=10)

entrada = tk.Entry(frame_entrada, width=40)
entrada.pack(side=tk.LEFT, padx=5)

def adicionar():
    texto = entrada.get().strip()
    if texto:
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        tarefas = carregar_tarefas()
        tarefas.append({"data": data, "texto": texto, "feito": False})
        salvar_tarefas(tarefas)
        entrada.delete(0, tk.END)
        atualizar_lista()
        
        print("Texto digitado:", texto)
        print("Tarefas antes:", tarefas)

btn_add = tk.Button(frame_entrada, text="Adicionar", command=adicionar)
btn_add.pack(side=tk.LEFT)

def editar():
    selecionado = lista.curselection()
    
    if not selecionado:
        return
    
    index = selecionado[0]
    tarefas = carregar_tarefas()
    
    # coloca o texto atual no campo de entrada
    entrada.delete(0, tk.END)
    entrada.insert(0, tarefas[index]["texto"])
    
    # função interna pra salvar edição
    def salvar_edicao():
        novo_texto = entrada.get().strip()
        if not novo_texto:
            return
        
        tarefas[index]["texto"] = novo_texto
        salvar_tarefas(tarefas)
        entrada.delete(0, tk.END)
        atualizar_lista()
        btn_salvar.pack_forget()
    btn_salvar.config(command=salvar_edicao)
    btn_salvar.pack()


# Lista de tarefas
lista = tk.Listbox(janela, width=60, height=15)
lista.pack(pady=10)

def atualizar_lista():
    lista.delete(0, tk.END)
    tarefas = carregar_tarefas()
    for i, t in enumerate(tarefas):
        if t["feito"]:
            texto = f"{t['data']} ✓ {t['texto']} (concluído)"
        else:
            texto = f"{t['data']} ○ {t['texto']}"
        lista.insert(tk.END, texto)

def alternar_status(event):  
    # pega o item selecionado na lista (retorna uma tupla com índices)
    selecionado = lista.curselection()  
    
    if not selecionado:  
        return  
    index = selecionado[0]  
    tarefas = carregar_tarefas()   
    # inverte o status da tarefa (False → True, True → False)
    tarefas[index]["feito"] = not tarefas[index]["feito"]  
    
    salvar_tarefas(tarefas)  
    atualizar_lista()

def remover():
    # pega o item selecionado
    selecionado = lista.curselection()
    
    # se nada estiver selecionado, sai
    if not selecionado:
        return
    
    index = selecionado[0]
    tarefas = carregar_tarefas()
    # remove a tarefa da lista
    tarefas.pop(index)
    
    salvar_tarefas(tarefas)
    atualizar_lista()


# Frame para os botões de ação
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

# botão remover
btn_remover = tk.Button(frame_botoes, text="Remover", command=remover)
btn_remover.pack(side=tk.LEFT, padx=5)

# botão editar
btn_editar = tk.Button(frame_botoes, text="Editar", command=editar)
btn_editar.pack(side=tk.LEFT, padx=5)

btn_salvar = tk.Button(frame_botoes, text="Salvar edição")
btn_salvar.pack(side=tk.LEFT, padx=5)
btn_salvar.pack_forget()  # começa escondido

# liga o duplo clique à função
lista.bind("<Double-Button-1>", alternar_status)

atualizar_lista()

janela.mainloop()