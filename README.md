# 🪒 Sistema de Barbearia

Sistema completo de gerenciamento para barbearias desenvolvido em Python com interface gráfica Tkinter.

## 📋 Funcionalidades

- **👥 Gestão de Clientes**: Cadastro completo com dados pessoais
- **✂️ Registro de Cortes**: Controle de serviços realizados com preços
- **📅 Agendamentos**: Sistema de marcação de horários
- **📊 Relatórios**: Estatísticas e resumos do negócio
- **🔍 Busca**: Filtros em tempo real em todas as listas
- **💾 Persistência**: Dados salvos em arquivos JSON


## 📁 Estrutura do Projeto

```
Barbearia_lab_programacao/
├── models/
│   ├── __init__.py
│   └── models.py          # Classes de dados (Cliente, Corte, Agendamento)
├── utils/
│   ├── __init__.py
│   └── validations.py     # Validações e formatações
├── gui/
│   ├── __init__.py
│   └── cadastros.py       # Janelas de cadastro
├── barbearia.py           # Aplicação principal
├── usuarios.json          # Dados de usuários
├── clientes.json          # Dados de clientes
├── cortes.json           # Histórico de cortes
└── agendamentos.json     # Agendamentos
```

## 📊 Dados de Exemplo Incluídos

O sistema já vem com dados de exemplo carregados:
- **8 clientes** cadastrados
- **7 cortes** realizados
- **8 agendamentos** futuros
- **3 usuários** do sistema

## 🛠️ Tecnologias

- **Python 3.13**
- **Tkinter** (Interface gráfica)
- **JSON** (Persistência de dados)
- **Modularização** (Organização do código)

## � Requisitos do Sistema

- **Python 3.6+** instalado
- **Bibliotecas**: tkinter (já incluída no Python)

## 🎮 Como Executar

1. Clone ou baixe o projeto
2. Navegue até a pasta do projeto
3. Execute o comando:

```bash
python barbearia.py
```

4. Faça login com um dos usuários disponíveis

## 🔐 Usuários de Acesso

| Usuário | Senha | Perfil |
|---------|-------|--------|
| admin | 1234 | Administrador |
| rodrigo | senha123 | Operador |
| maria | barbearia2025 | Operador |

## 💡 Funcionalidades Principais

### 👥 Gestão de Clientes
- Cadastro com dados completos (nome, telefone, email, endereço, data nascimento)
- Busca e filtros em tempo real
- Validação de dados (telefone, email, etc.)

### ✂️ Controle de Cortes
- Registro de serviços realizados
- Controle de preços e barbeiros
- Histórico completo com observações

### 📅 Sistema de Agendamentos
- Marcação de horários futuros
- Controle de status (Agendado, Confirmado, Realizado, Cancelado)
- Vinculação com clientes e barbeiros

### 📊 Relatórios e Estatísticas
- Total de clientes cadastrados
- Quantidade de cortes realizados
- Receita total calculada automaticamente
- Agendamentos pendentes

## 🎨 Interface

- **Design moderno** com cores profissionais
- **Navegação por abas** organizada
- **Busca em tempo real** em todas as seções
- **Validações visuais** com mensagens claras
- **Formulários intuitivos** para cadastros

## 📝 Razão

Desenvolvido para laboratório de programação.

## 📄 Licença

Este projeto está licenciado sob a MIT License.
