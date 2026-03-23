
from database import conectar

atividades = []
def registro_rotina():
    nome = input("Nome da atividade: ")
    pasta = input("Em qual pasta/categoria (ex: Estudos, Trabalho): ") 

    conn, cursor = conectar()
    
    cursor.execute('INSERT INTO tarefas (atividade, categoria, status) VALUES (?, ?, ?)', 
                   (nome, pasta, 'Pendente'))
    
    conn.commit()
    conn.close()
    print(f"✅ {nome} salva na pasta [{pasta}]")
    input("\nPressione Enter para continuar...")

    

def status():
    listar_rotina() 
    try:
        id_tarefa = int(input("\nDigite o ID da atividade para alterar o status: "))
        
        conn, cursor = conectar()
        
        
        cursor.execute('SELECT status FROM tarefas WHERE id = ?', (id_tarefa,))
        resultado = cursor.fetchone()
        
        if resultado:
            status_atual = resultado[0]
            
            novo_status = "Concluída" if status_atual == "Pendente" else "Pendente"
            
            
            cursor.execute('UPDATE tarefas SET status = ? WHERE id = ?', (novo_status, id_tarefa))
            conn.commit()
            print(f"✅ Status da tarefa {id_tarefa} alterado para: {novo_status}")
        else:
            print("⚠️ ID não encontrado.")
            
        conn.close()
    except ValueError:
        print("Erro: Digite um número de ID válido.")
    
    input("\nPressione Enter para continuar...")



def remover():
    listar_rotina() 
    try:
        id_tarefa = int(input("\nDigite o ID da atividade que deseja remover: "))
        
        conn, cursor = conectar()
        cursor.execute('DELETE FROM tarefas WHERE id = ?', (id_tarefa,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"🗑️ Tarefa ID {id_tarefa} removida com sucesso!")
        else:
            print("⚠️ ID não encontrado no banco de dados.")
        conn.close()
    except ValueError:
        print("Erro: Digite um número de ID válido.")
    
    input("\nPressione Enter para continuar...")
    


def listar_rotina():
    print("\n--- SUAS ATIVIDADES POR PASTA ---")
    conn, cursor = conectar()
    
    cursor.execute('SELECT id, atividade, status, categoria FROM tarefas ORDER BY categoria')
    linhas = cursor.fetchall()
    conn.close()

    if not linhas:
        print("Lista vazia.")
    else:
        pasta_atual = ""
        for item in linhas:
            id_t, nome, status_t, pasta = item
            
            if pasta != pasta_atual:
                print(f"\n📂 PASTA: {pasta.upper()}")
                pasta_atual = pasta
            
            simbolo = "✅" if status_t == "Concluída" else "⏳"
            print(f"   {id_t}. {nome} [{simbolo}]")
    
    input("\nPressione Enter para continuar...")


def atualizar_lista(tree, dados_do_banco):
    
    for i in tree.get_children():
        tree.delete(i)
        
    
    categorias_criadas = {}

    for id_task, nome, cat in dados_do_banco:
        if cat not in categorias_criadas:
            
            pai = tree.insert("", "end", text=cat, open=True) 
            categorias_criadas[cat] = pai
            
        
        tree.insert(categorias_criadas[cat], "end", text=nome, values=(id_task,))



def iniciar_sistema():
    while True:
        
        opcao = ...

        if opcao == '1':
            registro_rotina()
        elif opcao == '2':
            status()
        elif opcao == '3':
            remover()
        elif opcao == '4':
            listar_rotina()
        elif opcao == '5':
            print("Saindo do sistema Focused Mind Day...")
            break
            

        

