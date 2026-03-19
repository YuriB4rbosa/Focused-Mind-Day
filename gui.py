import customtkinter as ctk
from database import conectar
from tkinter import messagebox

ctk.set_appearance_mode("grenn")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Focused Mind Day")
        self.geometry("450x600")

        
        self.label = ctk.CTkLabel(self, text="Nova Atividade:", font=("Roboto", 16))
        self.label.pack(pady=10)

        self.entry_tarefa = ctk.CTkEntry(self, placeholder_text="O que vamos fazer hoje?", width=300)
        self.entry_tarefa.pack(pady=5)

        self.btn_add = ctk.CTkButton(self, text="Adicionar", command=self.adicionar_tarefa)
        self.btn_add.pack(pady=10)

        
        self.frame_lista = ctk.CTkScrollableFrame(self, width=400, height=300, label_text="Suas Rotinas")
        self.frame_lista.pack(pady=20, padx=20)

        self.atualizar_interface()

    def adicionar_tarefa(self):
        nome = self.entry_tarefa.get()
        if nome:
            conn, cursor = conectar()
            cursor.execute('INSERT INTO tarefas (atividade, status) VALUES (?, ?)', (nome, 'Pendente'))
            conn.commit()
            conn.close()
            self.entry_tarefa.delete(0, 'end')
            self.atualizar_interface()
        else:
            messagebox.showwarning("Aviso", "Digite o nome da atividade!")

    def atualizar_interface(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        conn, cursor = conectar()
        cursor.execute('SELECT * FROM tarefas')
        for item in cursor.fetchall():
            id_banco, nome, status = item[0], item[1], item[2]
            
            f = ctk.CTkFrame(self.frame_lista, fg_color="transparent")
            f.pack(fill="x", pady=2, padx=5)
            
            
            check_var = ctk.StringVar(value=status)
            check = ctk.CTkCheckBox(f, text=nome, 
                                    command=lambda i=id_banco, v=check_var: self.alternar_status(i, v),
                                    variable=check_var, 
                                    onvalue="Concluída", 
                                    offvalue="Pendente")
            
            if status == "Concluída":
                check.select()
                check.configure(text_color="gray") 
            
            check.pack(side="left", padx=10)
            
            btn_del = ctk.CTkButton(f, text="X", width=30, fg_color="#c0392b", 
                                    hover_color="#a93226", 
                                    command=lambda i=id_banco: self.deletar(i))
            btn_del.pack(side="right", padx=5)
        conn.close()

    def alternar_status(self, id_tarefa, var):
        novo_status = var.get()
        conn, cursor = conectar()
        cursor.execute('UPDATE tarefas SET status = ? WHERE id = ?', (novo_status, id_tarefa))
        conn.commit()
        conn.close()
        self.atualizar_interface() 

    def deletar(self, id_tarefa):
        conn, cursor = conectar()
        cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
        conn.commit()
        conn.close()
        self.atualizar_interface()

