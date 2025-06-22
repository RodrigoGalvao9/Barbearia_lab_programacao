import json
import os

clientes = []
agendamentos = []

ARQ_CLIENTES = "clientes.json"
ARQ_AGENDAMENTOS = "agendamentos.json"

def carregar_dados():
    global clientes, agendamentos
    if os.path.exists(ARQ_CLIENTES):
        with open(ARQ_CLIENTES, 'r') as f:
            clientes = json.load(f)
    if os.path.exists(ARQ_AGENDAMENTOS):
        with open(ARQ_AGENDAMENTOS, 'r') as f:
            agendamentos = json.load(f)

def salvar_dados():
    with open(ARQ_CLIENTES, 'w') as f:
        json.dump(clientes, f, indent=4)
    with open(ARQ_AGENDAMENTOS, 'w') as f:
        json.dump(agendamentos, f, indent=4)

def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    telefone = input("Telefone: ")
    cliente = {"id": len(clientes)+1, "nome": nome, "telefone": telefone}
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")

def listar_clientes():
    for cliente in clientes:
        print(f"ID: {cliente['id']} | Nome: {cliente['nome']} | Telefone: {cliente['telefone']}")

def remover_cliente():
    listar_clientes()
    cid = int(input("ID do cliente a remover: "))
    global clientes
    clientes = [c for c in clientes if c['id'] != cid]
    print("Cliente removido.")

def agendar_servico():
    listar_clientes()
    cid = int(input("ID do cliente: "))
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")
    servico = input("Serviço: ")
    valor = float(input("Valor (R$): "))
    agendamento = {
        "cliente_id": cid,
        "data": data,
        "hora": hora,
        "servico": servico,
        "valor": valor
    }
    agendamentos.append(agendamento)
    print("Serviço agendado!")

def listar_agendamentos():
    for ag in agendamentos:
        cliente = next((c for c in clientes if c['id'] == ag['cliente_id']), {"nome": "Desconhecido"})
        print(f"Cliente: {cliente['nome']} | Data: {ag['data']} {ag['hora']} | Serviço: {ag['servico']} | R$: {ag['valor']:.2f}")

def calcular_faturamento():
    total = sum(a['valor'] for a in agendamentos)
    print(f"Faturamento total: R$ {total:.2f}")

def menu():
    while True:
        print("""
===== BARBEARIA =====
1. Cadastrar cliente
2. Listar clientes
3. Remover cliente
4. Agendar serviço
5. Listar agendamentos
6. Calcular faturamento
0. Sair
        """)
        opc = input("Escolha: ")
        if opc == '1': cadastrar_cliente()
        elif opc == '2': listar_clientes()
        elif opc == '3': remover_cliente()
        elif opc == '4': agendar_servico()
        elif opc == '5': listar_agendamentos()
        elif opc == '6': calcular_faturamento()
        elif opc == '0':
            salvar_dados()
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

carregar_dados()
menu()
