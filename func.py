
from database import conectar

atividades = []
def registro_rotina():
    nome = input("Nome da atividade do dia de hoje: ")

    conn, cursor = conectar()

    
    cursor.execute('INSERT INTO tarefas (atividade, status) VALUES (?, ?)', (nome, 'Pendente'))
    
    conn.commit()
    conn.close()
    print(f"✅ {nome} salva no banco de dados")
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
    print("\n--- SUAS ATIVIDADES ---")
    conn, cursor = conectar()
    cursor.execute('SELECT * FROM tarefas')
    linhas = cursor.fetchall()
    conn.close()

    if not linhas:
        print("Lista vazia.")
    else:
        for item in linhas:
            print(f"{item[0]}. {item[1]} [{item[2]}]")
    
    
    input("\nPressione Enter para continuar...")



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
            

        

