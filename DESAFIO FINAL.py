import sqlite3  # banco de dados
import tkinter as tk  # interface básica
from tkinter import messagebox  # caixas de mensagens
from tkinter import ttk  # interface gráfica tb

# Função para conectar ao banco de dados
def conectar():
    return sqlite3.connect('teste.db')

# Função para criar a tabela no banco de dados
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL               
        )       
    ''')
    conn.commit()
    conn.close()

# CREATE - Inserir novo usuário
def inserir_usuario():
    nome = entry_nome.get()
    email = entry_email.get()
    if nome and email:
        conn = conectar()
        c = conn.cursor()
        c.execute('INSERT INTO usuarios(nome, email) VALUES(?, ?)', (nome, email))
        conn.commit()
        conn.close()
        messagebox.showinfo('AVISO', 'DADOS INSERIDOS COM SUCESSO!')
        mostrar_usuario()
    else:
        messagebox.showerror('ERRO', 'ALGO DEU ERRADO!')

# READ - Mostrar todos os usuários na tabela
def mostrar_usuario():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    for usuario in usuarios:
        tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2]))
    conn.close()

# DELETE - Deletar um usuário
def delete_usuario():
    dado_del = tree.selection()
    if dado_del:
        user_id = tree.item(dado_del)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('', 'DADO DELETADO')
        mostrar_usuario()
    else:
        messagebox.showerror('', 'OCORREU UM ERRO')

# UPDATE - Editar um usuário
def editar():
    selecao = tree.selection()
    if selecao:
        user_id = tree.item(selecao)['values'][0]
        novo_nome = entry_nome.get()
        novo_email = entry_email.get()

        if novo_nome and novo_email:
            conn = conectar()
            c = conn.cursor()
            c.execute('UPDATE usuarios SET nome = ?, email = ? WHERE id = ?', (novo_nome, novo_email, user_id))
            conn.commit()
            conn.close()
            messagebox.showinfo('', 'DADOS ATUALIZADOS')
            mostrar_usuario()
        else:
            messagebox.showwarning('', 'PREENCHA TODOS OS CAMPOS')
    else:
        messagebox.showerror('', 'ALGO DEU ERRADO!')

# Criando a interface gráfica
root = tk.Tk()
root.title("Sistema CRUD de Usuários")

# Definindo o layout
frame = tk.Frame(root)
frame.pack(pady=10)

# Campos de entrada para nome e email
label_nome = tk.Label(frame, text="Nome")
label_nome.grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

label_email = tk.Label(frame, text="E-mail")
label_email.grid(row=1, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame)
entry_email.grid(row=1, column=1, padx=5, pady=5)

# Botões para as operações CRUD
btn_inserir = tk.Button(frame, text="Inserir", command=inserir_usuario)
btn_inserir.grid(row=2, column=0, padx=5, pady=5)

btn_editar = tk.Button(frame, text="Editar", command=editar)
btn_editar.grid(row=2, column=1, padx=5, pady=5)

btn_deletar = tk.Button(frame, text="Deletar", command=delete_usuario)
btn_deletar.grid(row=2, column=2, padx=5, pady=5)

# Criando a Treeview para exibir os usuários
tree = ttk.Treeview(root, columns=("ID", "Nome", "E-mail"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nome", text="Nome")
tree.heading("E-mail", text="E-mail")
tree.pack(pady=10)

# Inicializa a tabela
criar_tabela()
mostrar_usuario()

# Executando a interface
root.mainloop()
