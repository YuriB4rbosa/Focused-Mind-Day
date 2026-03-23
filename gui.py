import customtkinter as ctk
from database import conectar
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Focused Mind Day")
        self.geometry("500x700")
        # Opções: "dark" (padrão), "light" ou "system"
        ctk.set_appearance_mode("dark")
        

        # Inputs
        ctk.CTkLabel(self, text="Nova Atividade:", font=("Roboto", 16)).pack(pady=(20,5))
        self.entry_tarefa = ctk.CTkEntry(self, placeholder_text="O que vamos fazer?", width=350)
        self.entry_tarefa.pack(pady=5)

        ctk.CTkLabel(self, text="Categoria:", font=("Roboto", 16)).pack(pady=5)
        self.entry_pasta = ctk.CTkEntry(self, placeholder_text="Ex: Estudos, Trabalho...", width=350)
        self.entry_pasta.pack(pady=5)

        self.btn_add = ctk.CTkButton(self, text="Adicionar Rotina", command=self.adicionar_tarefa, fg_color="#24a0ed")
        self.btn_add.pack(pady=20)

        # Container da Lista
        self.frame_lista = ctk.CTkScrollableFrame(self, width=450, height=400, label_text="Minhas Tarefas")
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.atualizar_interface()

    def adicionar_tarefa(self):
        nome = self.entry_tarefa.get()
        pasta = self.entry_pasta.get()
        
        if nome and pasta:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tarefas (atividade, categoria, status) VALUES (?, ?, ?)', 
                         (nome, pasta, 'Pendente'))
            conn.commit()
            conn.close()
            
            self.entry_tarefa.delete(0, 'end')
            self.entry_pasta.delete(0, 'end')
            self.atualizar_interface()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def atualizar_interface(self):
        # Limpa a interface atual
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tarefas ORDER BY categoria')
        
        pasta_atual = ""
        for item in cursor.fetchall():
            id_banco, nome, pasta, status = item
            
            # Cabeçalho da Categoria
            if pasta != pasta_atual:
                pasta_atual = pasta
                lbl_cat = ctk.CTkLabel(self.frame_lista, text=f"📂 {pasta.upper()}", 
                                     font=("Roboto", 14, "bold"), text_color="#3b8ed0")
                lbl_cat.pack(fill="x", pady=(15, 5), padx=10)

            # Frame da Tarefa
            f = ctk.CTkFrame(self.frame_lista, fg_color="#2b2b2b")
            f.pack(fill="x", pady=2, padx=10)

            # Texto da tarefa (com check simples)
            simbolo = "✅" if status == "Concluída" else "❌"
            lbl_task = ctk.CTkLabel(f, text=f"{simbolo} {nome}", font=("Roboto", 13))
            lbl_task.pack(side="left", padx=10, pady=5)

            # Botão Deletar
            btn_del = ctk.CTkButton(f, text="🗑️", width=30, fg_color="#cc3300", 
                                   command=lambda i=id_banco: self.deletar(i))
            btn_del.pack(side="right", padx=5)

            # Botão Alternar Status
            btn_status = ctk.CTkButton(f, text="Concluída", width=60, 
                                      command=lambda i=id_banco, s=status: self.alternar_status(i, s))
            btn_status.pack(side="right", padx=5)

        conn.close()

    def alternar_status(self, id_tarefa, status_atual):
        novo_status = "Concluída" if status_atual == "Pendente" else "Pendente"
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('UPDATE tarefas SET status = ? WHERE id = ?', (novo_status, id_tarefa))
        conn.commit()
        conn.close()
        self.atualizar_interface()

    def deletar(self, id_tarefa):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
        conn.commit()
        conn.close()
        self.atualizar_interface()