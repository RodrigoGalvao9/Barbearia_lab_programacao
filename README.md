
# Sistema de Gerenciamento de Barbearia

Este é um sistema simples de linha de comando para gerenciamento de uma barbearia. Com ele, é possível realizar login, cadastrar clientes, registrar cortes, agendar horários e listar clientes.

## Funcionalidades

- **Login de Usuário**
  - Login básico com verificação de nome de usuário e senha.

- **Cadastro de Cliente**
  - Permite adicionar novos clientes com nome e telefone.

- **Registro de Corte**
  - Registra o tipo de corte feito em um cliente.

- **Agendamento**
  - Agenda data e hora para o atendimento de um cliente.

- **Listagem de Clientes**
  - Exibe todos os clientes cadastrados com seus telefones.

## Como Executar

1. Certifique-se de ter o Python instalado (versão 3.6 ou superior).
2. Salve o código em um arquivo chamado `barbearia.py`.
3. Execute o programa no terminal:

```bash
python barbearia.py
```

4. Faça login com o seguinte usuário:

```
Usuário: admin
Senha: 1234
```

## Estrutura de Dados

- `usuarios`: dicionário contendo usuários e senhas.
- `clientes`: lista de dicionários com nome e telefone dos clientes.
- `cortes`: lista de dicionários com informações sobre os cortes.
- `agendamentos`: lista de dicionários com data e hora agendada.

## Exemplo de Uso

```plaintext
=== Login ===
Usuário: admin
Senha: 1234
Login bem-sucedido!

=== MENU ===
1. Cadastrar cliente
2. Registrar corte
3. Agendar horário
4. Listar clientes
5. Sair
Escolha uma opção:
```
