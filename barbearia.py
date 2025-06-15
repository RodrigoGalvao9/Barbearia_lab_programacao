usuarios = {"admin": "1234"}
clientes = []
cortes = []
agendamentos = []

def login():
    print("=== Login ===")
    user = input("Usuário: ")
    senha = input("Senha: ")
    if usuarios.get(user) == senha:
        print("Login bem-sucedido!\n")
        return True
    else:
        print("Usuário ou senha inválido!\n")
        return False

def menu():
    print("\n=== MENU ===")
    print("1. Cadastrar cliente")
    print("2. Registrar corte")
    print("3. Agendar horário")
    print("4. Listar clientes")
    print("5. Sair")
    return input("Escolha uma opção: ")

def cadastrar_cliente():
    nome = input("Nome do cliente: ")
    telefone = input("Telefone: ")
    clientes.append({"nome": nome, "telefone": telefone})
    print("Cliente cadastrado com sucesso!")

def registrar_corte():
    cliente = input("Nome do cliente: ")
    tipo = input("Tipo de corte: ")
    cortes.append({"cliente": cliente, "corte": tipo})
    print("Corte registrado!")

def agendar():
    cliente = input("Nome do cliente: ")
    data = input("Data (dd/mm/aaaa): ")
    hora = input("Hora (hh:mm): ")
    agendamentos.append({"cliente": cliente, "data": data, "hora": hora})
    print("Agendamento feito!")

def listar_clientes():
    print("\n=== Lista de Clientes ===")
    for c in clientes:
        print(f"- {c['nome']} ({c['telefone']})")

# Programa principal
if login():
    while True:
        opcao = menu()
        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            registrar_corte()
        elif opcao == "3":
            agendar()
        elif opcao == "4":
            listar_clientes()
        elif opcao == "5":
            print("Encerrando...")
            break
        else:
            print("Opção inválida!")
