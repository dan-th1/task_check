import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os
import uuid 

# Arquivo onde salva as tarefas
ARQUIVO = "data/tarefas.json"
CATEGORIAS = "data/categorias.json"

# Carrega tarefas salvas
def carregar_tarefas():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def carregar_categorias():
    if os.path.exists(CATEGORIAS):
        with open(CATEGORIAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return ["Cybersec", "Faculdade", "Pessoal", "Outro"]  # categorias padrão

def salvar_categorias(categorias):
    with open(CATEGORIAS, 'w', encoding='utf-8') as f:
        json.dump(categorias, f, ensure_ascii=False, indent=2)
        print("Categorias carregadas:", categorias)

tarefas = carregar_tarefas()
categorias = carregar_categorias()


# Salva tarefas
def salvar_tarefas(tarefas):
    """Salva a lista de tarefas no arquivo JSON especificado por ARQUIVO."""
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

# Dropdown de categoria
combo_categoria = ttk.Combobox(frame_entrada, values=categorias, width=12, state="readonly")
combo_categoria.set(categorias[0] if categorias else "Outro")
combo_categoria.pack(side=tk.LEFT, padx=5)



def adicionar():
    global tarefas
    texto = entrada.get().strip()
    if texto:
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        tarefas.append({
            "id": str(uuid.uuid4()),
            "data": data,
            "texto": texto,
            "categoria": combo_categoria.get(),
            "feito": False
        })
        salvar_tarefas(tarefas)
        entrada.delete(0, tk.END)
        atualizar_lista()
        
        print("Texto digitado:", texto)
        print("Tarefas antes:", tarefas)

btn_add = tk.Button(frame_entrada, text="Adicionar", command=adicionar)
btn_add.pack(side=tk.LEFT)
btn_categorias = tk.Button(frame_entrada, text="⚙️ Categorias", command=lambda: abrir_janela_categorias())
btn_categorias.pack(side=tk.LEFT, padx=5)

def editar():
    global tarefas
    selecionado = lista.curselection()
    
    if not selecionado:
        return
    
    index = selecionado[0]
    
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
    for i, t in enumerate(tarefas):
        # Pega a categoria (ou "Sem categoria" se não existir)
        categoria = t.get("categoria", "Sem categoria")
        
        if t["feito"]:
            texto = f"[{categoria}] {t['data']} ✓ {t['texto']} (concluído)"
        else:
            texto = f"[{categoria}] {t['data']} ○ {t['texto']}"
        lista.insert(tk.END, texto)

def alternar_status(event):  
    global tarefas
    # pega o item selecionado na lista (retorna uma tupla com índices)
    selecionado = lista.curselection()  
    
    if not selecionado:  
        return  
    index = selecionado[0]  
    # inverte o status da tarefa (False → True, True → False)
    tarefas[index]["feito"] = not tarefas[index]["feito"]  
    
    salvar_tarefas(tarefas)  
    atualizar_lista()

def remover():
    global tarefas
    # pega o item selecionado
    selecionado = lista.curselection()
    
    # se nada estiver selecionado, sai
    if not selecionado:
        return
    
    index = selecionado[0]
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
def abrir_janela_categorias():
    janela_cat = tk.Toplevel(janela)
    janela_cat.title("Gerenciar Categorias")
    janela_cat.geometry("300x400")
    
    # Lista de categorias
    lista_cat = tk.Listbox(janela_cat, width=40, height=15)
    lista_cat.pack(pady=10)
    
    def atualizar_lista_cat():
        lista_cat.delete(0, tk.END)
        for cat in categorias:
            lista_cat.insert(tk.END, cat)
    
    atualizar_lista_cat()
    
    # Campo de entrada para nova categoria
    entrada_cat = tk.Entry(janela_cat, width=30)
    entrada_cat.pack(pady=5)
    
    # Frame para botões
    frame_cat_botoes = tk.Frame(janela_cat)
    frame_cat_botoes.pack(pady=5)
    
    def adicionar_categoria():
        global categorias
        nova_cat = entrada_cat.get().strip()
        if nova_cat and nova_cat not in categorias:
            categorias.append(nova_cat)
            salvar_categorias(categorias)
            entrada_cat.delete(0, tk.END)
            atualizar_lista_cat()
    
    def remover_categoria():
        global categorias
        selecionado = lista_cat.curselection()
        if not selecionado or len(categorias) <= 1:
            return
        
        index = selecionado[0]
        categorias.pop(index)
        salvar_categorias(categorias)
        atualizar_lista_cat()
    
    btn_add_cat = tk.Button(frame_cat_botoes, text="Adicionar", command=adicionar_categoria)
    btn_add_cat.pack(side=tk.LEFT, padx=5)
    
    btn_remover_cat = tk.Button(frame_cat_botoes, text="Remover", command=remover_categoria)
    btn_remover_cat.pack(side=tk.LEFT, padx=5)

janela.mainloop()